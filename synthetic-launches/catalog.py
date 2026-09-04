"""TMS test catalog for Stream A / Stream B synthetic ReportPortal launches.

Source of truth for both generated Postman collections and the uploader.
Case ids, steps and tags match 26.1-beta-testing/test-cases/*.md.
"""

from __future__ import annotations


def _ns(num: int, instruction: str, expected: str, status: str = "passed",
        logs: list | None = None) -> dict:
    return {
        "name": f"**Step {num}:** {instruction} <br />**Expected Result:** {expected}",
        "status": status,
        "logs": logs or [],
    }


def _case(*, tc_id: str, title: str, priority: str, area: str, case_type: str,
          tags: list[str], preconditions: str, expected: str, author: str,
          suite: str, stack: str, code_ref: str, item_type: str = "TEXT",
          nested: list | None = None, item_logs: list | None = None,
          status: str = "passed", defect: str | None = None,
          quick: bool = False) -> dict:
    description = (
        f"**Preconditions:** {preconditions}\n\n"
        f"**Expected result:** {expected}"
    )
    return {
        "id": tc_id,
        "name": f"[{tc_id}] {title}",
        "priority": priority,
        "area": area,
        "case_type": case_type,
        "tags": tags,
        "preconditions": preconditions,
        "expected": expected,
        "description": description,
        "author": author,
        "suite": suite,
        "stack": stack,
        "code_ref": code_ref,
        "item_type": item_type,
        "nested": nested or [],
        "item_logs": item_logs or [],
        "status": status,
        "defect": defect,
        "quick": quick,
    }


# ---------------------------------------------------------------------------
# Stream A — Appium / WebdriverIO (mobile-qa)
# ---------------------------------------------------------------------------

_WDIO_ASSERT = (
    "    at Context.<anonymous> ({path}:{line}:18)\n"
    "    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)"
)

SUITE_CANCEL = "Cancellations & Modifications"
SUITE_MOBILE = "Mobile Booking (Demo)"
AUTHOR_MAYA = "Maya Chen"
AUTHOR_LUCA = "Luca Rossi"

STREAM_A_CASES = [
    _case(
        tc_id="TMS-BOOK-023",
        title="Cancel refundable booking within policy window",
        priority="HIGH", area="Cancellation", case_type="Functional",
        tags=["cancellation", "smoke", "booking"],
        preconditions="Confirmed refundable booking BK-REF-1001 exists; "
                      "free cancellation allowed until 24 h before check-in.",
        expected="User can cancel the booking from My trips; status changes to Cancelled; "
                 "full refund message is displayed and confirmation email is sent.",
        author=AUTHOR_MAYA, suite=SUITE_CANCEL, stack="wdio",
        code_ref="wdio/specs/cancellation/cancel-refundable.spec.js:14",
        quick=True,
        item_logs=[
            ("info", "[STEP] Open My trips and select booking BK-REF-1001"),
            ("debug", "GET /v1/trips/BK-REF-1001 -> 200 in 142 ms  status=CONFIRMED  "
                      "ratePlan=FREE_CANCELLATION"),
            ("info", "[STEP] Tap Cancel booking and confirm full-refund dialog"),
            ("debug", "POST /v1/bookings/BK-REF-1001/cancel -> 200 in 318 ms  "
                      "refundAmount=EUR 356.00  refundMethod=original"),
            ("info", "Booking status=CANCELLED; confirmation email queued for "
                     "maya.chen+demo@travelbook.example"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-025",
        title="Display cancellation policy before payment",
        priority="MEDIUM", area="Cancellation", case_type="Functional",
        tags=["smoke", "cancellation", "booking"],
        preconditions="User is on checkout review step before payment.",
        expected="Cancellation policy (deadline, refund type, and penalty if any) is visible "
                 "on checkout and must be acknowledged before payment can be submitted.",
        author=AUTHOR_MAYA, suite=SUITE_CANCEL, stack="wdio",
        code_ref="wdio/specs/cancellation/policy-on-checkout.spec.js:21",
        quick=True,
        item_logs=[
            ("info", "[STEP] Open checkout review for Hotel Marais, 2 nights, refundable rate"),
            ("debug", "Attempt to find element by selector: ~cancellationPolicyCard"),
            ("info", "Policy card visible: free cancellation until 24 h before check-in; "
                     "after that 100% penalty"),
            ("debug", "Pay now button enabled=false until policy checkbox is ticked"),
            ("info", "[STEP] Acknowledge cancellation policy; Pay now becomes enabled"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-028",
        title="Partial refund amount shown after date modification",
        priority="MEDIUM", area="Cancellation", case_type="Functional",
        tags=["payment", "booking", "cancellation"],
        preconditions="Refundable booking BK-REF-1004 allows partial refund when shortening "
                      "stay; user shortens by one night.",
        expected="After shortening the stay, the modification summary shows nights removed, "
                 "updated total, and partial refund amount to be returned to the original "
                 "payment method.",
        author=AUTHOR_MAYA, suite=SUITE_CANCEL, stack="wdio",
        code_ref="wdio/specs/cancellation/partial-refund.spec.js:91",
        status="failed", defect="pb",
        item_logs=[
            ("info", "[STEP] Open booking BK-REF-1004 (3 nights, EUR 534.00) and shorten by 1 night"),
            ("debug", "PUT /v1/bookings/BK-REF-1004/dates -> 200 in 267 ms  nights=2  "
                      "updatedTotal=EUR 356.00"),
            ("info", "[STEP] Read modification summary: nights removed, updated total, refund"),
            ("error",
             "AssertionError [ERR_ASSERTION]: Partial refund amount on modification summary\n"
             "Expected: EUR 178.00 (1 night × EUR 178.00)\n"
             "Received: EUR 89.00\n"
             + _WDIO_ASSERT.format(path="wdio/specs/cancellation/partial-refund.spec.js",
                                   line=91),
             "refund-calculation.csv"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-024",
        title="Modify stay dates for an existing reservation",
        priority="HIGH", area="Cancellation", case_type="Functional",
        tags=["booking", "regression", "dates", "cancellation"],
        preconditions="Active booking BK-REF-1002 with free date-change policy; "
                      "alternative dates have availability.",
        expected="Dates update successfully; booking summary reflects new check-out date "
                 "and recalculated total; confirmation of modification is shown.",
        author=AUTHOR_MAYA, suite=SUITE_CANCEL, stack="wdio",
        code_ref="wdio/specs/cancellation/change-dates.spec.js:18",
        item_type="STEPS",
        nested=[
            _ns(1, "Log in and open My trips.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Login as demo.traveler@example.com and open My trips"),
                    ("debug", "Attempt to find element by accessibility id: my-trips-tab"),
                ]),
            _ns(2, "Select booking BK-REF-1002.",
                "Selected option is applied to the current context.",
                logs=[
                    ("info", "[STEP] Open booking BK-REF-1002"),
                    ("debug", "GET /v1/trips/BK-REF-1002 -> 200 in 118 ms  "
                              "checkIn=2026-08-20  checkOut=2026-08-22"),
                ]),
            _ns(3, "Click Change dates.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Tap Change dates"),
                    ("debug", "Date-change policy: FREE until 2026-08-19 12:00"),
                ]),
            _ns(4, "Shift check-out one day later using the date picker.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Shift check-out from 2026-08-22 to 2026-08-23"),
                    ("debug", "GET /v1/availability?property=HTL-4412&checkOut=2026-08-23 -> "
                              "200  rooms=3"),
                ]),
            _ns(5, "Confirm modification and review updated total.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Review price delta: +EUR 178.00 for extra night"),
                    ("debug", "Attempt to find element by selector: ~modificationSummary"),
                ]),
            _ns(6, "Save changes.",
                "Dates update successfully; booking summary reflects new check-out date "
                "and recalculated total; confirmation of modification is shown.",
                logs=[
                    ("info", "[STEP] Save date modification"),
                    ("debug", "PUT /v1/bookings/BK-REF-1002/dates -> 200 in 241 ms  "
                              "checkOut=2026-08-23  total=EUR 534.00"),
                    ("info", "Confirmation toast: Stay updated. New check-out 23 Aug 2026."),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Change check-out of BK-REF-1002 by +1 night"),
            ("info", "Booking summary updated: 20–23 Aug 2026, EUR 534.00"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-026",
        title="Attempt cancellation of non-refundable reservation",
        priority="HIGH", area="Cancellation", case_type="Negative",
        tags=["cancellation", "booking", "negative"],
        preconditions="Confirmed non-refundable booking BK-NRF-2001 exists; "
                      "check-in is more than 7 days away.",
        expected="System warns that no refund will be issued; after confirmation, booking "
                 "status becomes Cancelled with EUR 0 refund; user receives cancellation "
                 "email stating non-refundable terms.",
        author=AUTHOR_MAYA, suite=SUITE_CANCEL, stack="wdio",
        code_ref="wdio/specs/cancellation/non-refundable.spec.js:112",
        item_type="STEPS",
        status="failed", defect="ti",
        nested=[
            _ns(1, "Log in and navigate to My trips.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Login and open My trips"),
                    ("debug", "Attempt to find element by accessibility id: my-trips-tab"),
                ]),
            _ns(2, "Open booking BK-NRF-2001.",
                "Target page or panel opens and is ready for input.",
                logs=[
                    ("info", "[STEP] Open booking BK-NRF-2001"),
                    ("debug", "GET /v1/trips/BK-NRF-2001 -> 200  ratePlan=NON_REFUNDABLE  "
                              "status=CONFIRMED"),
                ]),
            _ns(3, "Click Cancel booking.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Tap Cancel booking"),
                    ("debug", "Attempt to find element by selector: ~cancelBookingButton"),
                ]),
            _ns(4, "Read the policy warning dialog.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Read non-refundable warning dialog"),
                    ("debug", "Dialog copy: This rate is non-refundable. Refund: EUR 0.00"),
                ]),
            _ns(5, "Confirm cancellation attempt.",
                "System warns that no refund will be issued; after confirmation, booking "
                "status becomes Cancelled with EUR 0 refund; user receives cancellation "
                "email stating non-refundable terms.",
                status="failed",
                logs=[
                    ("info", "[STEP] Confirm cancellation of BK-NRF-2001"),
                    ("debug", "POST /v1/bookings/BK-NRF-2001/cancel -> 200 in 198 ms  "
                              "refundAmount=EUR 0.00"),
                    ("error",
                     "AssertionError [ERR_ASSERTION]: Booking status after non-refundable "
                     "cancellation\n"
                     "Expected: CANCELLED\n"
                     "Received: CONFIRMED\n"
                     "Cancellation email body states EUR 0 refund, but My trips still shows "
                     "status Confirmed.\n"
                     + _WDIO_ASSERT.format(
                         path="wdio/specs/cancellation/non-refundable.spec.js", line=112)),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Cancel non-refundable booking BK-NRF-2001"),
            ("warn", "Cancel API returned 200 with refundAmount=0 but trip list still "
                     "renders status=CONFIRMED"),
            ("error",
             "AssertionError [ERR_ASSERTION]: Booking status after non-refundable "
             "cancellation\nExpected: CANCELLED\nReceived: CONFIRMED\n"
             + _WDIO_ASSERT.format(
                 path="wdio/specs/cancellation/non-refundable.spec.js", line=112)),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-027",
        title="Modify booking after free-change cutoff has passed",
        priority="LOW", area="Cancellation", case_type="Edge",
        tags=["cancellation", "dates", "edge"],
        preconditions="Booking BK-REF-1003 has free-change deadline yesterday; "
                      "check-in is in 3 days.",
        expected="Date change is blocked or requires a change fee clearly displayed; "
                 "booking dates remain unchanged if modification is not confirmed with "
                 "fee payment.",
        author=AUTHOR_MAYA, suite=SUITE_CANCEL, stack="wdio",
        code_ref="wdio/specs/cancellation/cutoff-fee.spec.js:33",
        item_type="STEPS",
        nested=[
            _ns(1, "Log in and open booking BK-REF-1003.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Open booking BK-REF-1003"),
                    ("debug", "GET /v1/trips/BK-REF-1003 -> 200  freeChangeUntil=yesterday  "
                              "checkIn=in 3 days"),
                ]),
            _ns(2, "Click Change dates.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Tap Change dates"),
                    ("debug", "Attempt to find element by selector: ~changeDatesButton"),
                ]),
            _ns(3, "Attempt to move check-in one day later.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Shift check-in +1 day in the date picker"),
                    ("debug", "GET /v1/bookings/BK-REF-1003/change-quote -> 200  "
                              "fee=EUR 45.00  reason=CUTOFF_PASSED"),
                ]),
            _ns(4, "Review fee or restriction messaging.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Read change-fee banner"),
                    ("debug", "Banner: Free-change window closed. Change fee EUR 45.00."),
                ]),
            _ns(5, "Cancel the modification attempt.",
                "Date change is blocked or requires a change fee clearly displayed; "
                "booking dates remain unchanged if modification is not confirmed with "
                "fee payment.",
                logs=[
                    ("info", "[STEP] Dismiss modification without paying the fee"),
                    ("debug", "GET /v1/trips/BK-REF-1003 -> 200  dates unchanged"),
                    ("info", "Original stay dates preserved; no charge issued"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Attempt date change on BK-REF-1003 after free-change cutoff"),
            ("info", "Change fee EUR 45.00 displayed; user cancelled; dates unchanged"),
        ],
    ),
    _case(
        tc_id="TMS-MOB-001",
        title="Open booking app on iOS",
        priority="HIGH", area="Mobile", case_type="Functional",
        tags=["mobile", "demo"],
        preconditions="User has TravelBook iOS app installed.",
        expected="App opens on home screen with search widget visible.",
        author=AUTHOR_LUCA, suite=SUITE_MOBILE, stack="wdio",
        code_ref="wdio/specs/mobile/ios-launch.spec.js:9",
        quick=True,
        item_logs=[
            ("info", "[STEP] Launch TravelBook on iPhone 15 (iOS 17.5) via Appium"),
            ("debug", "session created: platformName=iOS  bundleId=com.travelbook.app  "
                      "udid=00008120-001A4D1E0A7A401E"),
            ("debug", "Attempt to find element by accessibility id: search-widget"),
            ("info", "Home screen loaded; search widget visible; deep-link ready"),
        ],
    ),
    _case(
        tc_id="TMS-MOB-002",
        title="Search hotels on mobile web",
        priority="HIGH", area="Mobile", case_type="Functional",
        tags=["mobile", "demo"],
        preconditions="Mobile browser on staging.",
        expected="Only 4★+ hotels shown.",
        author=AUTHOR_LUCA, suite=SUITE_MOBILE, stack="wdio",
        code_ref="wdio/specs/mobile/search-hotels.spec.js:58",
        item_type="STEPS",
        status="failed", defect="ab",
        nested=[
            _ns(1, "Open staging URL on mobile viewport.",
                "Responsive layout loads.",
                logs=[
                    ("info", "[STEP] Open https://staging.travelbook.example on Pixel 7 "
                             "viewport (412×915)"),
                    ("debug", "document.readyState=complete in 1.84 s; layout=mobile"),
                ]),
            _ns(2, "Enter Paris and valid dates.",
                "Results list appears.",
                logs=[
                    ("info", "[STEP] Search Paris, 18–20 Aug 2026, 2 adults"),
                    ("debug", "GET /v1/search?dest=Paris&checkIn=2026-08-18 -> 200 in 612 ms  "
                              "hotels=47"),
                ]),
            _ns(3, "Apply 4★ filter.",
                "Only 4★+ hotels shown.",
                status="failed",
                logs=[
                    ("info", "[STEP] Apply star-rating filter: 4★ and 5★"),
                    ("warn", "Results grid re-rendered after filter chip tap, retrying click (1/1)"),
                    ("error",
                     "stale element reference: element is not attached to the page document\n"
                     "  (Session info: chrome=126.0.6478.126; mobile viewport 412x915)\n"
                     "    at MobileSearchPage.applyStarFilter "
                     "(wdio/pages/MobileSearchPage.js:142:22)\n"
                     "    at Context.<anonymous> "
                     "(wdio/specs/mobile/search-hotels.spec.js:58:16)",
                     "screenshot-failure.png"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Search Paris on mobile web and apply 4★ filter"),
            ("warn", "Responsive results grid re-rendered mid-tap"),
            ("error",
             "stale element reference: element is not attached to the page document\n"
             "  (Session info: chrome=126.0.6478.126; mobile viewport 412x915)\n"
             "    at MobileSearchPage.applyStarFilter (wdio/pages/MobileSearchPage.js:142:22)\n"
             "    at Context.<anonymous> (wdio/specs/mobile/search-hotels.spec.js:58:16)",
             "screenshot-failure.png"),
        ],
    ),
    _case(
        tc_id="TMS-MOB-003",
        title="Complete booking on Android",
        priority="CRITICAL", area="Mobile", case_type="Functional",
        tags=["mobile", "demo"],
        preconditions="Android device with Google Pay configured.",
        expected="Confirmation screen with reference.",
        author=AUTHOR_LUCA, suite=SUITE_MOBILE, stack="wdio",
        code_ref="wdio/specs/mobile/android-booking.spec.js:24",
        item_type="STEPS",
        nested=[
            _ns(1, "Select first available hotel.",
                "Hotel details open.",
                logs=[
                    ("info", "[STEP] Tap first result: Hotel du Louvre"),
                    ("debug", "GET /v1/properties/HTL-8821 -> 200 in 203 ms"),
                ]),
            _ns(2, "Choose room and proceed to checkout.",
                "Checkout loads.",
                logs=[
                    ("info", "[STEP] Select Standard Double, refundable, tap Book now"),
                    ("debug", "POST /v1/cart -> 201 in 156 ms  cartId=crt-9f21"),
                ]),
            _ns(3, "Pay with test card.",
                "Confirmation screen with reference.",
                logs=[
                    ("info", "[STEP] Pay with sandbox card 4111 1111 1111 1111 via Google Pay test wallet"),
                    ("debug", "POST /v1/payments/confirm -> 200 in 891 ms  "
                              "reference=BK-2026-004610  status=CONFIRMED"),
                    ("info", "Confirmation screen: BK-2026-004610, Hotel du Louvre, 18–20 Aug"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Complete Android booking for Hotel du Louvre"),
            ("info", "Confirmed BK-2026-004610 via Google Pay sandbox"),
        ],
    ),
    _case(
        tc_id="TMS-MOB-004",
        title="Push notification for booking confirmation",
        priority="MEDIUM", area="Mobile", case_type="Functional",
        tags=["mobile", "demo"],
        preconditions="Booking completed on mobile.",
        expected="Push notification received within 60 seconds.",
        author=AUTHOR_LUCA, suite=SUITE_MOBILE, stack="wdio",
        code_ref="wdio/specs/mobile/push-confirmation.spec.js:44",
        status="failed", defect="si",
        item_logs=[
            ("info", "[STEP] Wait for booking-confirmation push after BK-2026-004610"),
            ("warn", "POST https://fcm.googleapis.com/v1/projects/travelbook/messages:send "
                     "-> retry 1/3: 504 Gateway Timeout"),
            ("warn", "POST https://fcm.googleapis.com/v1/projects/travelbook/messages:send "
                     "-> retry 2/3: 504 Gateway Timeout"),
            ("warn", "POST https://fcm.googleapis.com/v1/projects/travelbook/messages:send "
                     "-> retry 3/3: 504 Gateway Timeout"),
            ("error",
             "Error: Timeout: push notification not received within 60000ms\n"
             "Upstream notifications-service:8080 connection refused "
             "(notifications-service/10.68.21.9)\n"
             "    at PushClient.waitForNotification (wdio/helpers/PushClient.js:44:11)\n"
             "    at Context.<anonymous> (wdio/specs/mobile/push-confirmation.spec.js:44:16)\n"
             "    at process.processTicksAndRejections "
             "(node:internal/process/task_queues:95:5)"),
        ],
    ),
    _case(
        tc_id="TMS-MOB-005",
        title="Offline mode — view saved itinerary",
        priority="LOW", area="Mobile", case_type="Functional",
        tags=["demo", "mobile"],
        preconditions="User has confirmed booking cached locally.",
        expected="Itinerary details visible without network.",
        author=AUTHOR_LUCA, suite=SUITE_MOBILE, stack="wdio",
        code_ref="wdio/specs/mobile/offline-itinerary.spec.js:17",
        quick=True,
        item_logs=[
            ("info", "[STEP] Enable airplane mode; open cached itinerary BK-2026-004610"),
            ("debug", "AsyncStorage hit: itinerary:BK-2026-004610  size=18.4 KB  age=42 s"),
            ("info", "Itinerary rendered offline: Hotel du Louvre, 18–20 Aug, confirmation code visible"),
        ],
    ),
    _case(
        tc_id="TMS-MOB-006",
        title="Mobile payment with Apple Pay",
        priority="HIGH", area="Mobile", case_type="Functional",
        tags=["demo", "mobile"],
        preconditions="iOS device with wallet card enrolled.",
        expected="Payment succeeds.",
        author=AUTHOR_LUCA, suite=SUITE_MOBILE, stack="wdio",
        code_ref="wdio/specs/mobile/apple-pay.spec.js:28",
        item_type="STEPS",
        nested=[
            _ns(1, "Reach payment step on iOS.",
                "Apple Pay button visible.",
                logs=[
                    ("info", "[STEP] Navigate to payment step on iPhone 15"),
                    ("debug", "Attempt to find element by accessibility id: apple-pay-button"),
                    ("info", "Apple Pay button visible; merchantId=merchant.com.travelbook"),
                ]),
            _ns(2, "Authorize with test wallet.",
                "Payment succeeds.",
                logs=[
                    ("info", "[STEP] Authorize Apple Pay with sandbox PassKit token"),
                    ("debug", "POST /v1/payments/apple-pay -> 200 in 640 ms  "
                              "reference=BK-2026-004612  status=CONFIRMED"),
                    ("info", "Payment succeeded; confirmation BK-2026-004612"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Complete iOS checkout with Apple Pay sandbox wallet"),
            ("info", "Confirmed BK-2026-004612"),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Stream B — Playwright (web-qa)
# ---------------------------------------------------------------------------

_PW_TRACE = (
    "    at /tests/{path}:{line}:{col}\n"
    "    at /node_modules/@playwright/test/lib/worker/testInfo.js:284:11\n"
    "    at WorkerRunner._runTest (/node_modules/@playwright/test/lib/worker/workerRunner.js:512:5)"
)

SUITE_BOOKING = "Booking Flow"
SUITE_NFR = "Non-functional"
AUTHOR_PRIYA = "Priya Shah"
AUTHOR_OWEN = "Owen Blake"

STREAM_B_CASES = [
    _case(
        tc_id="TMS-BOOK-014",
        title="Booking confirmation summary displays correct details",
        priority="HIGH", area="Booking", case_type="Functional",
        tags=["smoke", "booking"],
        preconditions="A successful booking was just completed (reference BK-2026-004521).",
        expected="Confirmation page shows booking reference BK-2026-004521, correct hotel name, "
                 "stay dates, room type, guest name, total paid amount, and cancellation "
                 "policy summary.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/confirmation-summary.spec.ts:19",
        quick=True,
        item_logs=[
            ("info", "[STEP] Open confirmation page for BK-2026-004521"),
            ("debug", "locator.getByTestId('booking-reference') >> waiting for element to be visible"),
            ("info", "Summary: Hotel Le Petit Palais · 14–16 Aug 2026 · Deluxe King · "
                     "Anna Kovacs · EUR 412.00 · free cancellation until 13 Aug 18:00"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-015",
        title="Confirmation email sent after successful booking",
        priority="MEDIUM", area="Booking", case_type="Functional",
        tags=["booking", "regression", "account"],
        preconditions="User completed a booking with email test.user@example.com; "
                      "mail sandbox is accessible.",
        expected="Within 2 minutes, a confirmation email arrives at test.user@example.com "
                 "containing booking reference, hotel address, check-in/out dates, and a "
                 "link to manage the reservation.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/confirmation-email.spec.ts:38",
        status="failed", defect="si",
        item_logs=[
            ("info", "[STEP] Poll mail sandbox for confirmation of BK-2026-004521 "
                     "(test.user@example.com)"),
            ("warn", "GET http://mailhog.staging.svc:8025/api/v2/search?kind=to&query="
                     "test.user@example.com -> retry 1/3: connection reset by peer"),
            ("warn", "GET http://mailhog.staging.svc:8025/api/v2/search -> retry 2/3: "
                     "ECONNREFUSED 10.32.8.14:2525"),
            ("error",
             "Error: connect ECONNREFUSED 10.32.8.14:2525\n"
             "Mail sandbox (mailhog) is not reachable; confirmation email was not observed "
             "within 120000ms.\n"
             "    at TCPConnectWrap.afterConnect [as oncomplete] (node:net:1555:16)\n"
             "    at MailSandboxClient.waitForMessage (tests/helpers/mail.ts:38:5)\n"
             + _PW_TRACE.format(path="booking/confirmation-email.spec.ts", line=38, col=16),
             "confirmation-email.eml"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-016",
        title="Pre-fill guest details from saved user profile",
        priority="MEDIUM", area="Account", case_type="Functional",
        tags=["account", "booking", "regression"],
        preconditions="User is logged in as demo.traveler@example.com with a complete "
                      "profile (name, phone, email).",
        expected="On checkout guest-details step, first name, last name, email, and phone "
                 "fields are pre-populated from the profile and can be edited before continuing.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/prefill-profile.spec.ts:22",
        quick=True,
        item_logs=[
            ("info", "[STEP] Login as demo.traveler@example.com and open checkout guest-details"),
            ("debug", "GET /v1/users/me -> 200  firstName=Anna  lastName=Kovacs  "
                      "email=demo.traveler@example.com  phone=+36 20 555 0198"),
            ("info", "Guest fields pre-filled from profile; all four inputs editable"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-022",
        title="Same-day check-in before property cutoff time",
        priority="MEDIUM", area="Booking", case_type="Edge",
        tags=["dates", "booking", "edge"],
        preconditions="Current time is 14:00 local; property same-day cutoff is 18:00; "
                      "room available for tonight.",
        expected="Search with check-in today and check-out tomorrow returns available rooms; "
                 "booking can be initiated and checkout shows correct same-day stay dates.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/same-day.spec.ts:31",
        item_logs=[
            ("info", "[STEP] Search Barcelona check-in=today check-out=tomorrow at 14:00 local"),
            ("debug", "GET /v1/search?checkIn=2026-08-13&sameDay=true -> 200 in 488 ms  hotels=22"),
            ("info", "Checkout header dates: 13 Aug – 14 Aug 2026; cutoff 18:00 not exceeded"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-029",
        title="Resume interrupted booking session from saved cart",
        priority="LOW", area="Account", case_type="Edge",
        tags=["booking", "edge", "account"],
        preconditions="User added a room to cart while logged in, then closed the browser "
                      "without paying; cart retention is 24 h.",
        expected="After logging back in within 24 h, My cart or checkout resume prompt restores "
                 "the selected hotel, dates, and room with all previously entered guest fields intact.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/resume-cart.spec.ts:74",
        status="failed", defect="ab",
        item_logs=[
            ("info", "[STEP] Re-login within 24 h and open resume-checkout prompt"),
            ("debug", "GET /v1/cart/crt-7c90 -> 200  hotel=Seaside Inn  dates=20–22 Aug  "
                      "room=Standard Double"),
            ("warn", "sessionStorage key tb.guestDraft missing after login redirect"),
            ("error",
             "Error: expect(locator).toHaveValue(expected)\n\n"
             "Locator: getByLabel('First name')\n"
             "Expected string: \"Anna\"\n"
             "Received string: \"\"\n"
             "Hotel, dates and room restored from cart, but guest fields were empty.\n"
             + _PW_TRACE.format(path="booking/resume-cart.spec.ts", line=74, col=45),
             "screenshot-failure.png"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-010",
        title="Select room and proceed to checkout",
        priority="HIGH", area="Booking", case_type="Functional",
        tags=["smoke", "regression", "booking"],
        preconditions="User opened hotel details for an available property.",
        expected="Checkout page loads with correct hotel, stay dates, room type, and nightly "
                 "rate summary before guest details entry.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/select-room.spec.ts:16",
        item_type="STEPS",
        nested=[
            _ns(1, "Select a standard double room for 2 adults.",
                "Selected option is applied to the current context.",
                logs=[
                    ("info", "[STEP] Select Standard Double for 2 adults"),
                    ("debug", "locator.getByRole('radio', { name: 'Standard Double' }) >> click"),
                ]),
            _ns(2, "Choose a refundable rate plan.",
                "Step completes successfully.",
                logs=[
                    ("info", "[STEP] Choose refundable rate EUR 178.00 / night"),
                    ("debug", "ratePlanId=RP-FREE-24H"),
                ]),
            _ns(3, "Click Book now or Reserve.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Click Book now"),
                    ("debug", "POST /v1/cart -> 201 in 134 ms"),
                ]),
            _ns(4, "Confirm navigation to checkout.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Wait for checkout URL"),
                    ("debug", "page.url() = https://staging.travelbook.example/checkout/crt-aa12"),
                ]),
            _ns(5, "Verify hotel name, dates, and room type on checkout header.",
                "Checkout page loads with correct hotel, stay dates, room type, and nightly "
                "rate summary before guest details entry.",
                logs=[
                    ("info", "[STEP] Assert checkout header"),
                    ("debug", "Hotel Le Petit Palais · 14–16 Aug · Standard Double · EUR 178.00/night"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Select refundable Standard Double and open checkout"),
            ("info", "Checkout header matches hotel, dates, room and nightly rate"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-011",
        title="Complete guest contact and stay details",
        priority="HIGH", area="Booking", case_type="Functional",
        tags=["regression", "booking"],
        preconditions="User is on checkout step 1 (Guest details) with a room selected.",
        expected="Guest details are accepted; user advances to the payment step with summary "
                 "showing correct guest name and contact email.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/guest-details.spec.ts:20",
        item_type="STEPS",
        nested=[
            _ns(1, "Enter first name, last name, and email (test.user@example.com).",
                "Entered value is accepted and displayed in the field.",
                logs=[
                    ("info", "[STEP] Fill Anna / Kovacs / test.user@example.com"),
                    ("debug", "locator.getByLabel('Email') >> fill"),
                ]),
            _ns(2, "Enter mobile phone with valid country code.",
                "Entered value is accepted and displayed in the field.",
                logs=[
                    ("info", "[STEP] Fill phone +36 20 555 0198"),
                    ("debug", "phone validation passed (E.164)"),
                ]),
            _ns(3, "Set estimated arrival time.",
                "Selected value is applied.",
                logs=[
                    ("info", "[STEP] Set estimated arrival 16:00–17:00"),
                    ("debug", "locator.getByLabel('Estimated arrival') >> selectOption('16:00')"),
                ]),
            _ns(4, "Click Continue to payment.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Click Continue to payment"),
                    ("debug", "PATCH /v1/checkout/crt-aa12/guest -> 200 in 97 ms"),
                ]),
            _ns(5, "Review the booking summary sidebar.",
                "Guest details are accepted; user advances to the payment step with summary "
                "showing correct guest name and contact email.",
                logs=[
                    ("info", "[STEP] Assert payment step + sidebar guest block"),
                    ("debug", "sidebar.guest = Anna Kovacs <test.user@example.com>"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Submit guest details and advance to payment"),
            ("info", "Sidebar shows Anna Kovacs / test.user@example.com"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-012",
        title="Apply valid promotional discount code",
        priority="MEDIUM", area="Booking", case_type="Functional",
        tags=["booking", "regression", "payment"],
        preconditions="User is on checkout with a room total of EUR 300; promo code "
                      "SUMMER2026 (10% off) is active in test environment.",
        expected="Promo code is accepted; total price decreases by 10%; discount line item "
                 "is visible in the price summary.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/promo-valid.spec.ts:27",
        item_type="STEPS",
        nested=[
            _ns(1, "Locate the Promo code field on checkout.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Locate promo code field"),
                    ("debug", "locator.getByLabel('Promo code') >> visible"),
                ]),
            _ns(2, "Enter SUMMER2026.",
                "Entered value is accepted and displayed in the field.",
                logs=[
                    ("info", "[STEP] Type SUMMER2026"),
                ]),
            _ns(3, "Click Apply.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Click Apply"),
                    ("debug", "POST /v1/checkout/crt-aa12/promo -> 200 in 121 ms  "
                              "discount=EUR 30.00"),
                ]),
            _ns(4, "Review updated price breakdown.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Read price breakdown"),
                    ("debug", "subtotal=EUR 300.00  discount=EUR 30.00  total=EUR 270.00"),
                ]),
            _ns(5, "Proceed without completing payment.",
                "Promo code is accepted; total price decreases by 10%; discount line item "
                "is visible in the price summary.",
                logs=[
                    ("info", "[STEP] Assert discount line item 'SUMMER2026 −10%'"),
                    ("debug", "total decreased 300.00 -> 270.00"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Apply SUMMER2026 on EUR 300 checkout"),
            ("info", "Promo accepted; total EUR 270.00 (−10%)"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-013",
        title="Complete payment with valid credit card",
        priority="HIGH", area="Payment", case_type="Functional",
        tags=["payment", "booking", "smoke"],
        preconditions="User is on payment step; guest details are complete; test card "
                      "4111 1111 1111 1111 is allowed in sandbox.",
        expected="Payment is processed successfully; booking confirmation page displays a "
                 "unique booking reference and status Confirmed.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/pay-card.spec.ts:18",
        item_type="STEPS",
        nested=[
            _ns(1, "Select Credit card payment method.",
                "Selected option is applied to the current context.",
                logs=[
                    ("info", "[STEP] Select Credit card"),
                    ("debug", "locator.getByRole('radio', { name: 'Credit card' }) >> click"),
                ]),
            _ns(2, "Enter card number 4111 1111 1111 1111, future expiry, and CVV 123.",
                "Entered value is accepted and displayed in the field.",
                logs=[
                    ("info", "[STEP] Fill sandbox card 4111…1111 / 12/28 / 123"),
                    ("debug", "Stripe test token tok_visa created"),
                ]),
            _ns(3, "Enter cardholder name matching guest name.",
                "Entered value is accepted and displayed in the field.",
                logs=[
                    ("info", "[STEP] Cardholder name Anna Kovacs"),
                ]),
            _ns(4, "Accept terms and conditions.",
                "Step completes successfully.",
                logs=[
                    ("info", "[STEP] Tick Terms and conditions"),
                ]),
            _ns(5, "Click Confirm booking.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Click Confirm booking"),
                    ("debug", "POST /v1/payments/confirm -> 200 in 764 ms"),
                ]),
            _ns(6, "Wait for confirmation screen.",
                "Payment is processed successfully; booking confirmation page displays a "
                "unique booking reference and status Confirmed.",
                logs=[
                    ("info", "[STEP] Wait for confirmation"),
                    ("debug", "reference=BK-2026-004521  status=CONFIRMED"),
                    ("info", "Confirmation page displayed for BK-2026-004521"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Pay with sandbox Visa 4111…1111"),
            ("info", "Booking BK-2026-004521 Confirmed"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-017",
        title="Add special room requests during checkout",
        priority="LOW", area="Booking", case_type="Functional",
        tags=["regression", "edge", "booking"],
        preconditions="User is on checkout guest-details step.",
        expected="Special request text is saved and visible in the booking summary; no "
                 "validation error is shown for allowed request length.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/special-requests.spec.ts:19",
        item_type="STEPS",
        nested=[
            _ns(1, "Locate the Special requests text area.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Locate Special requests textarea"),
                    ("debug", "locator.getByLabel('Special requests') >> visible"),
                ]),
            _ns(2, 'Enter "Late check-in after 22:00; high floor preferred."',
                "Entered value is accepted and displayed in the field.",
                logs=[
                    ("info", "[STEP] Type special request (62 chars)"),
                ]),
            _ns(3, "Continue to payment without completing the booking.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Continue to payment"),
                    ("debug", "PATCH /v1/checkout/crt-aa12/requests -> 200"),
                ]),
            _ns(4, "Open booking summary or review step.",
                "Target page or panel opens and is ready for input.",
                logs=[
                    ("info", "[STEP] Open booking summary sidebar"),
                ]),
            _ns(5, "Verify the request is listed.",
                "Special request text is saved and visible in the booking summary; no "
                "validation error is shown for allowed request length.",
                logs=[
                    ("info", "[STEP] Assert special request text in summary"),
                    ("debug", "summary.specialRequests = Late check-in after 22:00; high floor preferred."),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Save special request on guest-details step"),
            ("info", "Request persisted in booking summary; no length validation error"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-018",
        title="Apply expired promotional code at checkout",
        priority="MEDIUM", area="Booking", case_type="Negative",
        tags=["booking", "negative", "payment"],
        preconditions="User is on checkout; expired code WINTER2025 exists in the system.",
        expected='Promo is rejected with message "This promotional code has expired"; '
                 "total price remains unchanged and user can continue without discount.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/promo-expired.spec.ts:24",
        item_type="STEPS",
        quick=True,
        nested=[
            _ns(1, "Enter WINTER2025 in the promo code field.",
                "Entered value is accepted and displayed in the field.",
                logs=[
                    ("info", "[STEP] Type WINTER2025"),
                ]),
            _ns(2, "Click Apply.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Click Apply"),
                    ("debug", "POST /v1/checkout/crt-aa12/promo -> 422  code=PROMO_EXPIRED"),
                ]),
            _ns(3, "Observe system response.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Read inline error"),
                    ("debug", "message = This promotional code has expired"),
                ]),
            _ns(4, "Confirm total price unchanged.",
                'Promo is rejected with message "This promotional code has expired"; '
                "total price remains unchanged and user can continue without discount.",
                logs=[
                    ("info", "[STEP] Assert total still EUR 300.00"),
                    ("debug", "discount line absent; Continue enabled"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Apply expired promo WINTER2025"),
            ("info", "Rejected; total unchanged at EUR 300.00"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-019",
        title="Submit booking without accepting terms and conditions",
        priority="HIGH", area="Booking", case_type="Negative",
        tags=["booking", "negative"],
        preconditions="User is on payment step with valid card details entered.",
        expected="Booking submission is blocked; terms checkbox is highlighted; inline error "
                 "prompts user to accept terms; no confirmation page or reference is generated.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/terms.spec.ts:88",
        item_type="STEPS",
        status="failed", defect="pb",
        nested=[
            _ns(1, "Fill in valid payment details.",
                "Entered value is accepted and displayed in the field.",
                logs=[
                    ("info", "[STEP] Fill sandbox Visa 4111…1111 / 12/28 / 123"),
                ]),
            _ns(2, "Leave the Terms and conditions checkbox unchecked.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Leave terms checkbox unchecked"),
                    ("debug", "locator.getByLabel('I accept the terms') >> not checked"),
                ]),
            _ns(3, "Click Confirm booking.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Click Confirm booking with terms unchecked"),
                ]),
            _ns(4, "Observe validation behavior.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Observe validation"),
                    ("warn", "No inline error on terms checkbox; request left the browser"),
                    ("debug", "POST /v1/payments/confirm -> 201 in 702 ms"),
                ]),
            _ns(5, "Confirm booking is not created.",
                "Booking submission is blocked; terms checkbox is highlighted; inline error "
                "prompts user to accept terms; no confirmation page or reference is generated.",
                status="failed",
                logs=[
                    ("info", "[STEP] Assert no confirmation page / no booking reference"),
                    ("error",
                     "Error: expect(page).not.toHaveURL(/confirmation/)\n\n"
                     "Expected: not to have URL matching /confirmation/\n"
                     "Received: \"https://staging.travelbook.example/booking/confirmation"
                     "?ref=BK-2026-004890\"\n"
                     "Terms checkbox was unchecked; booking was created anyway.\n"
                     + _PW_TRACE.format(path="booking/terms.spec.ts", line=88, col=16),
                     "screenshot-failure.png"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Submit payment with terms unchecked"),
            ("error",
             "Error: expect(page).not.toHaveURL(/confirmation/)\n"
             "Received: https://staging.travelbook.example/booking/confirmation?ref=BK-2026-004890\n"
             + _PW_TRACE.format(path="booking/terms.spec.ts", line=88, col=16),
             "screenshot-failure.png"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-020",
        title="Complete payment with declined credit card",
        priority="HIGH", area="Payment", case_type="Negative",
        tags=["booking", "payment", "negative"],
        preconditions="User is on payment step; test declined card 4000 0000 0000 0002 "
                      "is configured in sandbox.",
        expected='Payment fails with a clear error (e.g. "Card declined"); user remains on '
                 "payment step; no confirmation email or booking reference is issued.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/declined-card.spec.ts:102",
        item_type="STEPS",
        status="failed", defect="pb",
        nested=[
            _ns(1, "Enter card 4000 0000 0000 0002 with valid expiry and CVV.",
                "Entered value is accepted and displayed in the field.",
                logs=[
                    ("info", "[STEP] Fill declined test card 4000…0002 / 12/28 / 123"),
                ]),
            _ns(2, "Accept terms and conditions.",
                "Step completes successfully.",
                logs=[
                    ("info", "[STEP] Tick Terms and conditions"),
                ]),
            _ns(3, "Click Confirm booking.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Click Confirm booking"),
                    ("debug", "POST /v1/payments/confirm -> 200 in 541 ms"),
                ]),
            _ns(4, "Wait for payment response.",
                "User can review the updated state for this step.",
                logs=[
                    ("info", "[STEP] Read payment response"),
                    ("debug", "gateway.error.code=card_declined  decline_code=generic_decline"),
                    ("warn", "UI navigated to confirmation despite card_declined"),
                ]),
            _ns(5, "Verify booking state.",
                'Payment fails with a clear error (e.g. "Card declined"); user remains on '
                "payment step; no confirmation email or booking reference is issued.",
                status="failed",
                logs=[
                    ("info", "[STEP] Assert no booking reference and user stays on payment step"),
                    ("error",
                     "Error: expect(received).toBeNull()\n\n"
                     "Expected: null\n"
                     "Received: \"BK-2026-004891\"\n"
                     "Payment gateway declined the card, but a booking reference was issued "
                     "and confirmation email queued.\n"
                     + _PW_TRACE.format(path="booking/declined-card.spec.ts", line=102, col=18),
                     "payment-decline-response.json"),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Pay with declined sandbox card 4000…0002"),
            ("warn", "Gateway returned card_declined but checkout issued BK-2026-004891"),
            ("error",
             "Error: expect(received).toBeNull()\nExpected: null\nReceived: \"BK-2026-004891\"\n"
             + _PW_TRACE.format(path="booking/declined-card.spec.ts", line=102, col=18),
             "payment-decline-response.json"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-021",
        title="Book property at maximum allowed guest capacity",
        priority="MEDIUM", area="Booking", case_type="Edge",
        tags=["filters", "edge", "booking"],
        preconditions='Hotel "Seaside Inn" allows maximum 4 guests per standard room; '
                      "1 room selected.",
        expected="Booking proceeds successfully for 4 guests; increasing to 5 triggers "
                 "validation or unavailability message and prevents checkout completion "
                 "at invalid capacity.",
        author=AUTHOR_PRIYA, suite=SUITE_BOOKING, stack="playwright",
        code_ref="tests/booking/capacity.spec.ts:36",
        item_type="STEPS",
        nested=[
            _ns(1, "Open hotel details for Seaside Inn.",
                "Target page or panel opens and is ready for input.",
                logs=[
                    ("info", "[STEP] Open Seaside Inn property page"),
                    ("debug", "GET /v1/properties/HTL-2204 -> 200  maxGuestsPerRoom=4"),
                ]),
            _ns(2, "Set guests to 4 adults in 1 room.",
                "Selected value is applied.",
                logs=[
                    ("info", "[STEP] Occupancy 4 adults / 1 room"),
                ]),
            _ns(3, "Select an available standard room.",
                "Selected option is applied to the current context.",
                logs=[
                    ("info", "[STEP] Select Standard room (max 4)"),
                ]),
            _ns(4, "Proceed to checkout.",
                "Action is executed without blocking validation errors.",
                logs=[
                    ("info", "[STEP] Proceed to checkout with 4 guests"),
                    ("debug", "POST /v1/cart -> 201"),
                ]),
            _ns(5, "Attempt to increase guests to 5 on checkout.",
                "Booking proceeds successfully for 4 guests; increasing to 5 triggers "
                "validation or unavailability message and prevents checkout completion "
                "at invalid capacity.",
                logs=[
                    ("info", "[STEP] Increase occupancy to 5 adults on checkout"),
                    ("debug", "PATCH /v1/checkout/crt-bb08/occupancy -> 422  "
                              "code=CAPACITY_EXCEEDED"),
                    ("info", "Inline error: This room sleeps a maximum of 4 guests. "
                             "Confirm booking stays disabled."),
                ]),
        ],
        item_logs=[
            ("info", "[STEP] Book Seaside Inn at max capacity, then try 5 guests"),
            ("info", "4 guests allowed; 5 guests blocked with CAPACITY_EXCEEDED"),
        ],
    ),
    _case(
        tc_id="TMS-BOOK-030",
        title="Search results page loads within acceptable time",
        priority="MEDIUM", area="Non-functional", case_type="Non-functional",
        tags=["search", "non-functional", "smoke"],
        preconditions="Stable test environment; network latency normal; search query "
                      "returns >=20 hotels.",
        expected="Search results page becomes interactive within 3 seconds (First Contentful "
                 "Paint under 2 s, full results list rendered under 3 s on standard demo hardware).",
        author=AUTHOR_OWEN, suite=SUITE_NFR, stack="playwright",
        code_ref="tests/nfr/search-perf.spec.ts:41",
        status="failed", defect="ti",
        item_logs=[
            ("info", "[STEP] Cold-load search results for Paris, 20+ hotels, cable profile"),
            ("debug", "Lighthouse 11.4.0  formFactor=desktop  throttling=simulated"),
            ("info", "metrics: FCP=2847 ms  LCP=3612 ms  TTI=3188 ms  resultsRendered=3188 ms"),
            ("error",
             "Error: expect(fcp).toBeLessThan(2000)\n\n"
             "Expected: < 2000\n"
             "Received: 2847\n"
             "Full results list rendered in 3188 ms (budget 3000 ms).\n"
             + _PW_TRACE.format(path="nfr/search-perf.spec.ts", line=41, col=14),
             "lighthouse-report.json"),
        ],
    ),
]


STREAMS = {
    "A": {
        "key": "A",
        "project_slug": "stream-a",
        "collection_file": "stream-a-cancellations-mobile.postman_collection.json",
        "collection_name": "Stream A - Cancellations & Mobile",
        "launch_name": "Nightly regression - Cancellations & Mobile",
        "launch_description": (
            "**Nightly regression - Cancellations & Mobile** — "
            "triggered by merge to `release/26.1.0`\n\n"
            "[CI job#1842](https://ci.travelbook.example/job/stream-a-mobile/1842/) — "
            "[diff 7c2a91e -> 4e8b0c3](https://git.travelbook.example/qa/mobile-tests/compare/"
            "7c2a91e...4e8b0c3) — "
            "[Test plan TMS folder 93+95](https://tms.beta.reportportal.io) — "
            "[Staging](https://staging.travelbook.example)\n\n"
            "Scope: Cancellations & Modifications (6), Mobile Booking (6). "
            "Runner: WebdriverIO 8 / Appium 2. Stack: Android + iOS + mobile web."
        ),
        "attributes": [
            {"key": "stream", "value": "A"},
            {"key": "team", "value": "mobile-qa"},
            {"key": "component", "value": "cancellations"},
            {"key": "platform", "value": "android"},
            {"key": "env", "value": "staging"},
            {"key": "version", "value": "26.1.0"},
            {"key": "build", "value": "26.1.0-b1842"},
            {"key": "type", "value": "regression"},
            {"key": "retentionPolicy", "value": "regular", "system": True},
        ],
        "suites": [
            {"name": SUITE_CANCEL, "folder_id": 93,
             "description": "TMS folder 93 — cancel, refund and date-change flows."},
            {"name": SUITE_MOBILE, "folder_id": 95,
             "description": "TMS folder 95 — iOS / Android / mobile-web booking demo."},
        ],
        "cases": STREAM_A_CASES,
    },
    "B": {
        "key": "B",
        "project_slug": "stream-b",
        "collection_file": "stream-b-booking-nfr.postman_collection.json",
        "collection_name": "Stream B - Booking Flow & NFR",
        "launch_name": "Nightly regression - Booking Flow & NFR",
        "launch_description": (
            "**Nightly regression - Booking Flow & NFR** — "
            "triggered by merge to `release/26.1.0`\n\n"
            "[CI job#991](https://ci.travelbook.example/job/stream-b-web/991/) — "
            "[diff 1a9f4c2 -> 8d31e70](https://git.travelbook.example/qa/web-tests/compare/"
            "1a9f4c2...8d31e70) — "
            "[Test plan TMS folder 92+94](https://tms.beta.reportportal.io) — "
            "[Staging](https://staging.travelbook.example)\n\n"
            "Scope: Booking Flow (14), Non-functional (1). "
            "Runner: Playwright 1.47 / Chromium 126."
        ),
        "attributes": [
            {"key": "stream", "value": "B"},
            {"key": "team", "value": "web-qa"},
            {"key": "component", "value": "checkout"},
            {"key": "browser", "value": "chrome-126"},
            {"key": "env", "value": "staging"},
            {"key": "version", "value": "26.1.0"},
            {"key": "build", "value": "26.1.0-b991"},
            {"key": "type", "value": "regression"},
            {"key": "retentionPolicy", "value": "regular", "system": True},
        ],
        "suites": [
            {"name": SUITE_BOOKING, "folder_id": 92,
             "description": "TMS folder 92 — checkout, payment, confirmation and edge cases."},
            {"name": SUITE_NFR, "folder_id": 94,
             "description": "TMS folder 94 — search-results performance budget."},
        ],
        "cases": STREAM_B_CASES,
    },
}


CASES_BY_ID = {case["id"]: case for stream in STREAMS.values() for case in stream["cases"]}


def cases_for_suite(stream: dict, suite_name: str) -> list[dict]:
    return [c for c in stream["cases"] if c["suite"] == suite_name]


def issue_for(case: dict) -> dict | None:
    """Post-finish triage payload. None = leave as fresh To Investigate."""
    defect = case.get("defect")
    tc_id = case["id"]
    if defect == "pb":
        comments = {
            "TMS-BOOK-028": "Confirmed product defect: refund engine halves the nightly rate "
                            "when shortening a stay. Reproduced on staging with BK-REF-1004. "
                            "Fix targeted for 26.1.1.",
            "TMS-BOOK-019": "Confirmed product defect: Confirm booking is submitted even when "
                            "Terms and conditions is unchecked. Booking BK-2026-004890 created. "
                            "Fix targeted for 26.1.1.",
            "TMS-BOOK-020": "Confirmed product defect: declined sandbox card 4000…0002 still "
                            "issues a booking reference (BK-2026-004891). Payment and booking "
                            "state are out of sync.",
        }
        return {
            "issueType": "pb001",
            "autoAnalyzed": False,
            "ignoreAnalyzer": False,
            "comment": comments.get(tc_id, f"Confirmed product defect. TMS: {tc_id}."),
        }
    if defect == "ab":
        comments = {
            "TMS-MOB-002": "Known flaky locator: star-filter chip goes stale after the "
                           "responsive results grid re-renders. Tracked as AUTO-441.",
            "TMS-BOOK-029": "Broken guest-draft restore: sessionStorage key tb.guestDraft is "
                            "cleared on the login redirect. Tracked as AUTO-458.",
        }
        return {
            "issueType": "ab001",
            "autoAnalyzed": False,
            "ignoreAnalyzer": False,
            "comment": comments.get(tc_id, f"Automation defect. TMS: {tc_id}."),
        }
    if defect == "si":
        comments = {
            "TMS-MOB-004": "Staging notifications-service unreachable; FCM 504 after 3 retries. "
                           "Infra ticket INFRA-902.",
            "TMS-BOOK-015": "Mailhog sandbox ECONNREFUSED 10.32.8.14:2525. Confirmation email "
                            "could not be observed. Infra ticket INFRA-887.",
        }
        return {
            "issueType": "si001",
            "autoAnalyzed": False,
            "ignoreAnalyzer": False,
            "comment": comments.get(tc_id, f"System / infra issue. TMS: {tc_id}."),
        }
    return None
