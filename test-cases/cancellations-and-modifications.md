# Cancellations & Modifications (folder 93)

**Parent folder:** 89 — Booking Flow Demo (DO NOT MODIFY)


### TC61 — [TMS-BOOK-023] Cancel refundable booking within policy window

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-023 | Area: Cancellation | Type: Functional. Suggested attachments: attachments/TMS-BOOK-023_cancellation-confirmation.pdf
- **Attributes:** `cancellation`, `smoke`, `booking`
- **Type:** TEXT
- **Preconditions:** Confirmed refundable booking BK-REF-1001 exists; free cancellation allowed until 24 h before check-in.
- **Instructions:** User can cancel the booking from My trips; status changes to Cancelled; full refund message is displayed and confirmation email is sent.
- **Expected result:** User can cancel the booking from My trips; status changes to Cancelled; full refund message is displayed and confirmation email is sent.

### TC62 — [TMS-BOOK-025] Display cancellation policy before payment

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-025 | Area: Cancellation | Type: Functional. Suggested attachments: attachments/TMS-BOOK-025_cancellation-policy.pdf
- **Attributes:** `smoke`, `cancellation`, `booking`
- **Type:** TEXT
- **Preconditions:** User is on checkout review step before payment.
- **Instructions:** Cancellation policy (deadline, refund type, and penalty if any) is visible on checkout and must be acknowledged before payment can be submitted.
- **Expected result:** Cancellation policy (deadline, refund type, and penalty if any) is visible on checkout and must be acknowledged before payment can be submitted.

### TC63 — [TMS-BOOK-028] Partial refund amount shown after date modification

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-028 | Area: Cancellation | Type: Functional. Suggested attachments: attachments/TMS-BOOK-028_refund-calculation.csv
- **Attributes:** `payment`, `booking`, `cancellation`
- **Type:** TEXT
- **Preconditions:** Refundable booking BK-REF-1004 allows partial refund when shortening stay; user shortens by one night.
- **Instructions:** After shortening the stay, the modification summary shows nights removed, updated total, and partial refund amount to be returned to the original payment method.
- **Expected result:** After shortening the stay, the modification summary shows nights removed, updated total, and partial refund amount to be returned to the original payment method.

### TC64 — [TMS-BOOK-024] Modify stay dates for an existing reservation

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-024 | Area: Cancellation | Type: Functional. Suggested attachments: attachments/TMS-BOOK-024_date-modification-ui-mock.svg
- **Attributes:** `booking`, `regression`, `dates`, `cancellation`
- **Type:** STEPS
- **Preconditions:** Active booking BK-REF-1002 with free date-change policy; alternative dates have availability.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Log in and open My trips. | User can review the updated state for this step. |
| 2 | Select booking BK-REF-1002. | Selected option is applied to the current context. |
| 3 | Click Change dates. | Action is executed without blocking validation errors. |
| 4 | Shift check-out one day later using the date picker. | User can review the updated state for this step. |
| 5 | Confirm modification and review updated total. | Action is executed without blocking validation errors. |
| 6 | Save changes. | Dates update successfully; booking summary reflects new check-out date and recalculated total; confirmation of modification is shown. |

### TC65 — [TMS-BOOK-026] Attempt cancellation of non-refundable reservation

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-026 | Area: Cancellation | Type: Negative. Suggested attachments: attachments/TMS-BOOK-026_non-refundable-policy.pdf
- **Attributes:** `cancellation`, `booking`, `negative`
- **Type:** STEPS
- **Preconditions:** Confirmed non-refundable booking BK-NRF-2001 exists; check-in is more than 7 days away.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Log in and navigate to My trips. | User can review the updated state for this step. |
| 2 | Open booking BK-NRF-2001. | Target page or panel opens and is ready for input. |
| 3 | Click Cancel booking. | Action is executed without blocking validation errors. |
| 4 | Read the policy warning dialog. | User can review the updated state for this step. |
| 5 | Confirm cancellation attempt. | System warns that no refund will be issued; after confirmation, booking status becomes Cancelled with EUR 0 refund; user receives cancellation email stating non-refundable terms. |

### TC66 — [TMS-BOOK-027] Modify booking after free-change cutoff has passed

- **Priority:** LOW
- **Description:** Demo ID: TMS-BOOK-027 | Area: Cancellation | Type: Edge. Suggested attachments: attachments/TMS-BOOK-027_policy-cutoff-test-data.csv
- **Attributes:** `cancellation`, `dates`, `edge`
- **Type:** STEPS
- **Preconditions:** Booking BK-REF-1003 has free-change deadline yesterday; check-in is in 3 days.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Log in and open booking BK-REF-1003. | User can review the updated state for this step. |
| 2 | Click Change dates. | Action is executed without blocking validation errors. |
| 3 | Attempt to move check-in one day later. | User can review the updated state for this step. |
| 4 | Review fee or restriction messaging. | User can review the updated state for this step. |
| 5 | Cancel the modification attempt. | Date change is blocked or requires a change fee clearly displayed; booking dates remain unchanged if modification is not confirmed with fee payment. |

---
