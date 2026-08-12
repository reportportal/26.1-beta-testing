# Search & Filters (folder 90)

**Parent folder:** 89 — Booking Flow Demo (DO NOT MODIFY)


### TC1 — [TMS-BOOK-004] Sort hotel results by lowest price

- **Priority:** LOW
- **Description:** Demo ID: TMS-BOOK-004 | Area: Search | Type: Functional. Suggested attachments: attachments/TMS-BOOK-004_sort-by-price-ui-mock.svg
- **Attributes:** `search`, `agentic_candidate`, `smoke`, `booking`
- **Type:** TEXT
- **Preconditions:** Search results are displayed for a destination with at least 10 available properties.
- **Instructions:** Results are reordered with the lowest nightly rate first; each subsequent hotel has an equal or higher displayed price than the previous one.
- **Expected result:** Results are reordered with the lowest nightly rate first; each subsequent hotel has an equal or higher displayed price than the previous one.

### TC2 — [TMS-BOOK-006] Show only properties with free cancellation

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-006 | Area: Filters | Type: Functional. Suggested attachments: attachments/TMS-BOOK-006_free-cancellation-filter-ui-mock.svg
- **Attributes:** `cancellation`, `booking`, `filters`, `agentic_candidate`
- **Type:** TEXT
- **Preconditions:** Search results include both refundable and non-refundable rate plans.
- **Instructions:** Only hotels offering at least one free-cancellation rate appear in the results; each visible listing displays a "Free cancellation" badge or equivalent label.
- **Expected result:** Only hotels offering at least one free-cancellation rate appear in the results; each visible listing displays a "Free cancellation" badge or equivalent label.

### TC3 — [TMS-BOOK-008] Search with empty destination field

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-008 | Area: Search | Type: Negative. Suggested attachments: attachments/TMS-BOOK-008_empty-destination-validation-ui-mock.svg
- **Attributes:** `booking`, `negative`, `smoke`, `automated`, `search`
- **Type:** TEXT
- **Estimation:** 5
- **Preconditions:** User is on the home page; check-in and check-out dates are valid.
- **Instructions:** Search does not proceed; the Destination field is highlighted with a required-field error and no results page opens.
- **Expected result:** Search does not proceed; the Destination field is highlighted with a required-field error and no results page opens.

### TC4 — [TMS-BOOK-001] Search hotels by destination city

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-001 | Area: Search | Type: Functional. Suggested attachments: attachments/TMS-BOOK-001_search-results-ui-mock.svg
- **Attributes:** `booking`, `automated`, `regression`, `search`, `smoke`
- **Type:** STEPS
- **Preconditions:** User is on the TravelBook home page; at least one active hotel exists for "Barcelona, Spain".

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Open the hotel search widget. | Target page or panel opens and is ready for input. |
| 2 | Enter "Barcelona" in the Destination field. | Entered value is accepted and displayed in the field. |
| 3 | Select "Barcelona, Spain" from autocomplete suggestions. | Selected option is applied to the current context. |
| 4 | Set check-in to 14 days from today and check-out to 17 days from today. | Selected value is applied. |
| 5 | Set guests to 2 adults, 1 room. | Selected value is applied. |
| 6 | Click Search. | Search results page opens showing hotels in Barcelona with name, price per night, star rating, and thumbnail for each property. |

### TC5 — [TMS-BOOK-002] Filter search results by star rating

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-002 | Area: Filters | Type: Functional. Suggested attachments: attachments/TMS-BOOK-002_star-rating-filter-ui-mock.svg
- **Attributes:** `booking`, `search`, `automated`, `filters`, `regression`
- **Type:** STEPS
- **Estimation:** 5
- **Preconditions:** Search results are displayed for a city with mixed 3-5 star properties (e.g. Barcelona).

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | On the results page, open the Star rating filter. | Step completes successfully. |
| 2 | Select 4 stars and 5 stars only. | Selected option is applied to the current context. |
| 3 | Click Apply. | Action is executed without blocking validation errors. |
| 4 | Review the filtered list. | Only hotels rated 4 or 5 stars are shown; properties with 3 stars or below are excluded from the list. |

### TC6 — [TMS-BOOK-003] Filter search results by nightly price range

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-003 | Area: Filters | Type: Functional. Suggested attachments: attachments/TMS-BOOK-003_price-filter-ui-mock.svg
- **Attributes:** `booking`, `regression`, `dates`, `automated`, `filters`
- **Type:** STEPS
- **Estimation:** 5
- **Preconditions:** Search results are displayed with prices ranging from EUR 50 to EUR 400 per night.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Open the Price filter on the results page. | Target page or panel opens and is ready for input. |
| 2 | Set minimum price to EUR 100 and maximum price to EUR 250. | Selected value is applied. |
| 3 | Apply the filter. | Action is executed without blocking validation errors. |
| 4 | Verify displayed prices for the first five results. | All visible hotels show a nightly rate between EUR 100 and EUR 250 inclusive; no result outside the range is displayed. |

### TC7 — [TMS-BOOK-005] Search with valid check-in and check-out dates

- **Priority:** HIGH
- **Description:** Demo ID: TMS-BOOK-005 | Area: Search | Type: Functional. Suggested attachments: attachments/TMS-BOOK-005_date-picker-ui-mock.svg
- **Attributes:** `search`, `agentic_candidate`, `dates`, `booking`, `smoke`
- **Type:** STEPS
- **Preconditions:** User is on the home page; system date is known.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Enter a valid destination (e.g. "Lisbon, Portugal"). | Entered value is accepted and displayed in the field. |
| 2 | Set check-in to tomorrow. | Selected value is applied. |
| 3 | Set check-out to 3 days after check-in. | Selected value is applied. |
| 4 | Click Search. | Action is executed without blocking validation errors. |
| 5 | Confirm the search summary banner or breadcrumb. | Search executes successfully; results reflect the selected stay dates and show availability for the full date range. |

### TC8 — [TMS-BOOK-007] Search with check-out date before check-in date

- **Priority:** HIGH
- **Attributes:** `booking`, `agentic_candidate`, `negative`, `dates`, `search`
- **Type:** STEPS
- **Preconditions:** User is on the home page search widget.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Enter destination "Rome, Italy". | Entered value is accepted and displayed in the field. |
| 2 | Set check-in to 10 days from today. | Selected value is applied. |
| 3 | Set check-out to 7 days from today (before check-in). | Selected value is applied. |
| 4 | Click Search. | Action is executed without blocking validation errors. |
| 5 | Observe validation feedback. | Search is blocked; an inline validation message indicates check-out must be after check-in; no results page is loaded. |

### TC9 — [TMS-BOOK-009] Open hotel details from search results

- **Priority:** MEDIUM
- **Description:** Demo ID: TMS-BOOK-009 | Area: Search | Type: Functional. Suggested attachments: attachments/TMS-BOOK-009_hotel-details-ui-mock.svg
- **Attributes:** `booking`, `regression`, `search`, `agentic_candidate`
- **Type:** STEPS
- **Preconditions:** Search results list contains at least one available hotel.

| # | Instructions | Expected result |
|---|--------------|-----------------|
| 1 | Perform a valid search for any destination. | User can review the updated state for this step. |
| 2 | Click the first hotel name or View details link. | Action is executed without blocking validation errors. |
| 3 | Review the hotel details page. | User can review the updated state for this step. |
| 4 | Scroll to amenities and room types sections. | Hotel details page opens with photos, address, amenities list, available room types, and starting price matching the search result entry. |

---
