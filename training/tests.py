from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import TrainerAssignment, TrainerProfile

PASSWORD = "Test-pass1"


def make_user(email, role):
    return User.objects.create_user(email, PASSWORD, role=role, first_name=email.split("@")[0])


class TrainingTestCase(TestCase):
    def setUp(self):
        self.admin = make_user("admin@gym.test", User.Role.ADMIN)
        self.trainer = make_user("coach@gym.test", User.Role.TRAINER)
        self.other_trainer = make_user("coach2@gym.test", User.Role.TRAINER)
        self.member = make_user("member@gym.test", User.Role.MEMBER)
        self.other_member = make_user("member2@gym.test", User.Role.MEMBER)

    def login(self, user):
        self.client.force_login(user)


class AccessTests(TrainingTestCase):
    def test_anonymous_is_sent_to_login(self):
        for name in ["trainer_list", "edit_my_profile", "my_members", "assign_trainer"]:
            response = self.client.get(reverse(name))
            self.assertRedirects(response, f"{reverse('login')}?next={reverse(name)}")

    def test_only_admin_opens_assign_page(self):
        for user in [self.member, self.trainer]:
            self.login(user)
            self.assertEqual(self.client.get(reverse("assign_trainer")).status_code, 403)
        self.login(self.admin)
        self.assertEqual(self.client.get(reverse("assign_trainer")).status_code, 200)

    def test_only_trainer_opens_trainer_pages(self):
        for user in [self.member, self.admin]:
            self.login(user)
            self.assertEqual(self.client.get(reverse("my_members")).status_code, 403)
            self.assertEqual(self.client.get(reverse("edit_my_profile")).status_code, 403)

    def test_member_cannot_remove_assignment(self):
        assignment = TrainerAssignment.objects.create(member=self.member, trainer=self.trainer)
        self.login(self.member)
        response = self.client.post(reverse("unassign_trainer", args=[assignment.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(TrainerAssignment.objects.filter(pk=assignment.pk).exists())


class ProfileTests(TrainingTestCase):
    def test_trainer_creates_then_edits_profile(self):
        self.login(self.trainer)
        self.client.post(reverse("edit_my_profile"), {"specialty": "Yoga", "bio": "Ten years."})
        self.client.post(reverse("edit_my_profile"), {"specialty": "Strength", "bio": ""})
        profile = TrainerProfile.objects.get(user=self.trainer)
        self.assertEqual(profile.specialty, "Strength")
        self.assertEqual(TrainerProfile.objects.count(), 1)

    def test_members_see_trainer_profiles(self):
        profile = TrainerProfile.objects.create(user=self.trainer, specialty="Yoga")
        self.login(self.member)
        self.assertContains(self.client.get(reverse("trainer_list")), "Yoga")
        self.assertEqual(self.client.get(reverse("trainer_detail", args=[profile.pk])).status_code, 200)

    def test_deactivated_trainer_is_hidden(self):
        profile = TrainerProfile.objects.create(user=self.trainer, specialty="Yoga")
        self.trainer.is_active = False
        self.trainer.save()
        self.login(self.member)
        self.assertNotContains(self.client.get(reverse("trainer_list")), "Yoga")
        self.assertEqual(self.client.get(reverse("trainer_detail", args=[profile.pk])).status_code, 404)


class AssignmentTests(TrainingTestCase):
    def assign(self, member, trainer):
        return self.client.post(reverse("assign_trainer"), {"member": member.pk, "trainer": trainer.pk})

    def test_admin_assigns_and_reassigns(self):
        self.login(self.admin)
        self.assign(self.member, self.trainer)
        self.assign(self.member, self.other_trainer)
        assignment = TrainerAssignment.objects.get(member=self.member)
        self.assertEqual(assignment.trainer, self.other_trainer)
        self.assertEqual(TrainerAssignment.objects.count(), 1)

    def test_roles_are_checked_in_form(self):
        self.login(self.admin)
        response = self.assign(self.trainer, self.member)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TrainerAssignment.objects.exists())

    def test_admin_removes_assignment(self):
        assignment = TrainerAssignment.objects.create(member=self.member, trainer=self.trainer)
        self.login(self.admin)
        self.client.post(reverse("unassign_trainer", args=[assignment.pk]))
        self.assertFalse(TrainerAssignment.objects.exists())

    def test_trainer_sees_only_own_members(self):
        TrainerAssignment.objects.create(member=self.member, trainer=self.trainer)
        TrainerAssignment.objects.create(member=self.other_member, trainer=self.other_trainer)
        self.login(self.trainer)
        response = self.client.get(reverse("my_members"))
        self.assertContains(response, self.member.email)
        self.assertNotContains(response, self.other_member.email)
