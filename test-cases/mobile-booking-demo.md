# Mobile Booking (Demo) (folder 95)

**Parent folder:** 89 — Booking Flow Demo (DO NOT MODIFY)


### TC70 — [TMS-MOB-001] Open booking app on iOS

- **Priority:** HIGH
- **Description:** Mobile booking demo scenario for client presentations.
- **Attributes:** `mobile`, `demo`
- **Type:** TEXT
- **Preconditions:** User has TravelBook iOS app installed.
- **Instructions:** User has TravelBook iOS app installed.
- **Expected result:** App opens on home screen with search widget visible.

### TC71 — [TMS-MOB-002] Search hotels on mobile web

- **Priority:** HIGH
- **Description:** Mobile booking demo scenario for client presentations.
- **Attributes:** `mobile`, `demo`
- **Type:** STEPS
- **Preconditions:** Mobile browser on staging.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Open staging URL on mobile viewport. | Responsive layout loads. |
| 2 | Enter Paris and valid dates. | Results list appears. |
| 3 | Apply 4★ filter. | Only 4★+ hotels shown. |

### TC72 — [TMS-MOB-003] Complete booking on Android

- **Priority:** CRITICAL
- **Description:** Mobile booking demo scenario for client presentations.
- **Attributes:** `mobile`, `demo`
- **Type:** STEPS
- **Preconditions:** Android device with Google Pay configured.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Select first available hotel. | Hotel details open. |
| 2 | Choose room and proceed to checkout. | Checkout loads. |
| 3 | Pay with test card. | Confirmation screen with reference. |

### TC73 — [TMS-MOB-004] Push notification for booking confirmation

- **Priority:** MEDIUM
- **Description:** Mobile booking demo scenario for client presentations.
- **Attributes:** `mobile`, `demo`
- **Type:** TEXT
- **Preconditions:** Booking completed on mobile.
- **Instructions:** Booking completed on mobile.
- **Expected result:** Push notification received within 60 seconds.

### TC74 — [TMS-MOB-005] Offline mode — view saved itinerary

- **Priority:** LOW
- **Description:** Mobile booking demo scenario for client presentations.
- **Attributes:** `demo`, `mobile`
- **Type:** TEXT
- **Preconditions:** User has confirmed booking cached locally.
- **Instructions:** User has confirmed booking cached locally.
- **Expected result:** Itinerary details visible without network.

### TC75 — [TMS-MOB-006] Mobile payment with Apple Pay

- **Priority:** HIGH
- **Description:** Mobile booking demo scenario for client presentations.
- **Attributes:** `demo`, `mobile`
- **Type:** STEPS
- **Preconditions:** iOS device with wallet card enrolled.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Reach payment step on iOS. | Apple Pay button visible. |
| 2 | Authorize with test wallet. | Payment succeeds. |

---
