# Progress note: Payment recording and invoices (Issue #10)

**Date merged:** 2026-11-25
**Built by:** Belal (feature), with a follow-up fix
**Merged by:** Adam Elmasry (AdamMasry)
**Issue:** #10 Payment recording and invoices
**PR:** #31

## Commits
- `feat: add payment recording and invoices` (Belal, 2026-11-24)
- `fix: check payment member, membership and plan match` (Belal, 2026-11-25)

## What was built
- Admins record payments in Django admin. Each payment has a member, membership, plan, amount, payment method, and date.
- Each payment gets an invoice number automatically.
- Members see their payment history and open an invoice for each payment.
- A payment whose member, membership, and plan don't match is rejected.

## Next
Promo codes (Issue #11), which depends on this work.
