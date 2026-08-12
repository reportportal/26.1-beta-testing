# Booking Flow (folder 92)

**Parent folder:** 89 — Booking Flow Demo (DO NOT MODIFY)


### TC19 — [TMS-BOOK-014] Booking confirmation summary displays correct details

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-014 | Area: Booking | Type: Functional. Suggested attachments: attachments/TMS-BOOK-014_booking-confirmation.pdf
- **Attributes:** `smoke`, `booking`
- **Type:** TEXT
- **Preconditions:** A successful booking was just completed (reference BK-2026-004521).
- **Instructions:** Confirmation page shows booking reference BK-2026-004521, correct hotel name, stay dates, room type, guest name, total paid amount, and cancellation policy summary.
- **Expected result:** Confirmation page shows booking reference BK-2026-004521, correct hotel name, stay dates, room type, guest name, total paid amount, and cancellation policy summary.

### TC20 — [TMS-BOOK-015] Confirmation email sent after successful booking

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-015 | Area: Booking | Type: Functional. Suggested attachments: attachments/TMS-BOOK-015_confirmation-email.eml
- **Attributes:** `booking`, `regression`, `account`
- **Type:** TEXT
- **Preconditions:** User completed a booking with email test.user@example.com; mail sandbox is accessible.
- **Instructions:** Within 2 minutes, a confirmation email arrives at test.user@example.com containing booking reference, hotel address, check-in/out dates, and a link to manage the reservation.
- **Expected result:** Within 2 minutes, a confirmation email arrives at test.user@example.com containing booking reference, hotel address, check-in/out dates, and a link to manage the reservation.

### TC21 — [TMS-BOOK-016] Pre-fill guest details from saved user profile

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-016 | Area: Account | Type: Functional. Suggested attachments: attachments/TMS-BOOK-016_prefilled-profile-ui-mock.svg
- **Attributes:** `account`, `booking`, `regression`
- **Type:** TEXT
- **Preconditions:** User is logged in as demo.traveler@example.com with a complete profile (name, phone, email).
- **Instructions:** On checkout guest-details step, first name, last name, email, and phone fields are pre-populated from the profile and can be edited before continuing.
- **Expected result:** On checkout guest-details step, first name, last name, email, and phone fields are pre-populated from the profile and can be edited before continuing.

### TC22 — [TMS-BOOK-022] Same-day check-in before property cutoff time

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-022 | Area: Booking | Type: Edge. Suggested attachments: attachments/TMS-BOOK-022_same-day-dates-test-data.csv
- **Attributes:** `dates`, `booking`, `edge`
- **Type:** TEXT
- **Preconditions:** Current time is 14:00 local; property same-day cutoff is 18:00; room available for tonight.
- **Instructions:** Search with check-in today and check-out tomorrow returns available rooms; booking can be initiated and checkout shows correct same-day stay dates.
- **Expected result:** Search with check-in today and check-out tomorrow returns available rooms; booking can be initiated and checkout shows correct same-day stay dates.

### TC23 — [TMS-BOOK-029] Resume interrupted booking session from saved cart

- **Priority:** LOW
- **Description:** Demo ID: TMS-BOOK-029 | Area: Account | Type: Edge. Suggested attachments: attachments/TMS-BOOK-029_restored-cart-ui-mock.svg
- **Attributes:** `booking`, `edge`, `account`
- **Type:** TEXT
- **Preconditions:** User added a room to cart while logged in, then closed the browser without paying; cart retention is 24 h.
- **Instructions:** After logging back in within 24 h, My cart or checkout resume prompt restores the selected hotel, dates, and room with all previously entered guest fields intact.
- **Expected result:** After logging back in within 24 h, My cart or checkout resume prompt restores the selected hotel, dates, and room with all previously entered guest fields intact.

### TC24 — [TMS-BOOK-010] Select room and proceed to checkout

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-010 | Area: Booking | Type: Functional. Suggested attachments: attachments/TMS-BOOK-010_room-selection-checkout-ui-mock.svg
- **Attributes:** `smoke`, `regression`, `booking`
- **Type:** STEPS
- **Preconditions:** User opened hotel details for an available property.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Select a standard double room for 2 adults. | Selected option is applied to the current context. |
| 2 | Choose a refundable rate plan. | Step completes successfully. |
| 3 | Click Book now or Reserve. | Action is executed without blocking validation errors. |
| 4 | Confirm navigation to checkout. | Action is executed without blocking validation errors. |
| 5 | Verify hotel name, dates, and room type on checkout header. | Checkout page loads with correct hotel, stay dates, room type, and nightly rate summary before guest details entry. |

### TC25 — [TMS-BOOK-011] Complete guest contact and stay details

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-011 | Area: Booking | Type: Functional. Suggested attachments: attachments/TMS-BOOK-011_guest-data-test-data.csv
- **Attributes:** `regression`, `booking`
- **Type:** STEPS
- **Preconditions:** User is on checkout step 1 (Guest details) with a room selected.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Enter first name, last name, and email (test.user@example.com). | Entered value is accepted and displayed in the field. |
| 2 | Enter mobile phone with valid country code. | Entered value is accepted and displayed in the field. |
| 3 | Set estimated arrival time. | Selected value is applied. |
| 4 | Click Continue to payment. | Action is executed without blocking validation errors. |
| 5 | Review the booking summary sidebar. | Guest details are accepted; user advances to the payment step with summary showing correct guest name and contact email. |

### TC26 — [TMS-BOOK-012] Apply valid promotional discount code

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-012 | Area: Booking | Type: Functional. Suggested attachments: attachments/TMS-BOOK-012_promo-terms.pdf
- **Attributes:** `booking`, `regression`, `payment`
- **Type:** STEPS
- **Preconditions:** User is on checkout with a room total of EUR 300; promo code SUMMER2026 (10% off) is active in test environment.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Locate the Promo code field on checkout. | User can review the updated state for this step. |
| 2 | Enter SUMMER2026. | Entered value is accepted and displayed in the field. |
| 3 | Click Apply. | Action is executed without blocking validation errors. |
| 4 | Review updated price breakdown. | User can review the updated state for this step. |
| 5 | Proceed without completing payment. | Promo code is accepted; total price decreases by 10%; discount line item is visible in the price summary. |

### TC27 — [TMS-BOOK-013] Complete payment with valid credit card

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-013 | Area: Payment | Type: Functional. Suggested attachments: attachments/TMS-BOOK-013_booking-confirmation.pdf
- **Attributes:** `payment`, `booking`, `smoke`
- **Type:** STEPS
- **Preconditions:** User is on payment step; guest details are complete; test card 4111 1111 1111 1111 is allowed in sandbox.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Select Credit card payment method. | Selected option is applied to the current context. |
| 2 | Enter card number 4111 1111 1111 1111, future expiry, and CVV 123. | Entered value is accepted and displayed in the field. |
| 3 | Enter cardholder name matching guest name. | Entered value is accepted and displayed in the field. |
| 4 | Accept terms and conditions. | Step completes successfully. |
| 5 | Click Confirm booking. | Action is executed without blocking validation errors. |
| 6 | Wait for confirmation screen. | Payment is processed successfully; booking confirmation page displays a unique booking reference and status Confirmed. |

### TC28 — [TMS-BOOK-017] Add special room requests during checkout

- **Priority:** LOW
- **Description:** Demo ID: TMS-BOOK-017 | Area: Booking | Type: Functional. Suggested attachments: attachments/TMS-BOOK-017_special-requests-ui-mock.svg
- **Attributes:** `regression`, `edge`, `booking`
- **Type:** STEPS
- **Preconditions:** User is on checkout guest-details step.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Locate the Special requests text area. | User can review the updated state for this step. |
| 2 | Enter "Late check-in after 22:00; high floor preferred." | Entered value is accepted and displayed in the field. |
| 3 | Continue to payment without completing the booking. | Action is executed without blocking validation errors. |
| 4 | Open booking summary or review step. | Target page or panel opens and is ready for input. |
| 5 | Verify the request is listed. | Special request text is saved and visible in the booking summary; no validation error is shown for allowed request length. |

### TC29 — [TMS-BOOK-018] Apply expired promotional code at checkout

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-018 | Area: Booking | Type: Negative. Suggested attachments: attachments/TMS-BOOK-018_expired-promo-ui-mock.svg
- **Attributes:** `booking`, `negative`, `payment`
- **Type:** STEPS
- **Preconditions:** User is on checkout; expired code WINTER2025 exists in the system.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Enter WINTER2025 in the promo code field. | Entered value is accepted and displayed in the field. |
| 2 | Click Apply. | Action is executed without blocking validation errors. |
| 3 | Observe system response. | User can review the updated state for this step. |
| 4 | Confirm total price unchanged. | Promo is rejected with message "This promotional code has expired"; total price remains unchanged and user can continue without discount. |

### TC30 — [TMS-BOOK-019] Submit booking without accepting terms and conditions

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-019 | Area: Booking | Type: Negative. Suggested attachments: attachments/TMS-BOOK-019_terms-validation-ui-mock.svg
- **Type:** STEPS
- **Preconditions:** User is on payment step with valid card details entered.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Fill in valid payment details. | Entered value is accepted and displayed in the field. |
| 2 | Leave the Terms and conditions checkbox unchecked. | User can review the updated state for this step. |
| 3 | Click Confirm booking. | Action is executed without blocking validation errors. |
| 4 | Observe validation behavior. | User can review the updated state for this step. |
| 5 | Confirm booking is not created. | Booking submission is blocked; terms checkbox is highlighted; inline error prompts user to accept terms; no confirmation page or reference is generated. |

### TC31 — [TMS-BOOK-020] Complete payment with declined credit card

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-020 | Area: Payment | Type: Negative. Suggested attachments: attachments/TMS-BOOK-020_payment-decline-response.json
- **Attributes:** `booking`, `payment`, `negative`
- **Type:** STEPS
- **Preconditions:** User is on payment step; test declined card 4000 0000 0000 0002 is configured in sandbox.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Enter card 4000 0000 0000 0002 with valid expiry and CVV. | Entered value is accepted and displayed in the field. |
| 2 | Accept terms and conditions. | Step completes successfully. |
| 3 | Click Confirm booking. | Action is executed without blocking validation errors. |
| 4 | Wait for payment response. | User can review the updated state for this step. |
| 5 | Verify booking state. | Payment fails with a clear error (e.g. "Card declined"); user remains on payment step; no confirmation email or booking reference is issued. |

### TC32 — [TMS-BOOK-021] Book property at maximum allowed guest capacity

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-021 | Area: Booking | Type: Edge. Suggested attachments: attachments/TMS-BOOK-021_capacity-rules.pdf
- **Attributes:** `filters`, `edge`, `booking`
- **Type:** STEPS
- **Preconditions:** Hotel "Seaside Inn" allows maximum 4 guests per standard room; 1 room selected.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Open hotel details for Seaside Inn. | Target page or panel opens and is ready for input. |
| 2 | Set guests to 4 adults in 1 room. | Selected value is applied. |
| 3 | Select an available standard room. | Selected option is applied to the current context. |
| 4 | Proceed to checkout. | Action is executed without blocking validation errors. |
| 5 | Attempt to increase guests to 5 on checkout. | Booking proceeds successfully for 4 guests; increasing to 5 triggers validation or unavailability message and prevents checkout completion at invalid capacity. |

---
