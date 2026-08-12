import { test, expect } from '@playwright/test';
import { ReportingApi } from '@reportportal/agent-js-playwright';
import { BookingHomePage } from '../pages/BookingHomePage';
import { SearchResultsPage } from '../pages/SearchResultsPage';

const suiteName = 'Search & Filters';

function daysFromNow(days: number): Date {
  const date = new Date();
  date.setUTCHours(0, 0, 0, 0);
  date.setUTCDate(date.getUTCDate() + days);
  return date;
}

test.describe(suiteName, () => {
  ReportingApi.setDescription(
    'Automation of TMS folder 90 ("Search & Filters") against https://www.booking.com. Built to showcase ' +
      'ReportPortal reporting capabilities (Test Case ID, attributes, description, statuses, attachments) — ' +
      'not to be a precise regression suite. A few tests intentionally fail because the real site does not ' +
      'behave exactly like the legacy TMS test case describes.',
    suiteName,
  );
  ReportingApi.addAttributes(
    [
      { key: 'tms-folder', value: '90' },
      { value: 'booking.com' },
      { value: 'demo' },
    ],
    suiteName,
  );

  test.describe('Destination Search', () => {
    ReportingApi.setDescription(
      'Building and submitting a search from the homepage: destination lookup, date selection, and both the ' +
        'happy path and negative validation around them.',
      'Destination Search',
    );
    ReportingApi.addAttributes([{ key: 'feature', value: 'destination-search' }], 'Destination Search');

    test('[TMS-BOOK-001] Search hotels by destination city', async ({ page, browserName }) => {
      ReportingApi.setTestCaseId('TMS-BOOK-001');
      ReportingApi.addAttributes([
        { key: 'priority', value: 'HIGH' },
        { key: 'area', value: 'Search' },
        { key: 'type', value: 'Functional' },
        { key: 'browser', value: browserName },
        { value: 'booking' },
        { value: 'automated' },
        { value: 'regression' },
        { value: 'search' },
        { value: 'smoke' },
      ]);
      ReportingApi.setDescription(
        '**Preconditions:** User is on the TravelBook home page; at least one active hotel exists for "Barcelona, Spain".\n\n' +
          '**Steps:**\n' +
          '1. Open the hotel search widget. — Target page or panel opens and is ready for input.\n' +
          '2. Enter "Barcelona" in the Destination field. — Entered value is accepted and displayed in the field.\n' +
          '3. Select "Barcelona, Spain" from autocomplete suggestions. — Selected option is applied.\n' +
          '4. Set check-in to 14 days from today and check-out to 17 days from today. — Selected value is applied.\n' +
          '5. Set guests to 2 adults, 1 room. — Selected value is applied.\n' +
          '6. Click Search. — Search results page opens showing hotels in Barcelona with name, price, rating and thumbnail.',
      );

      const home = new BookingHomePage(page);
      const results = new SearchResultsPage(page);

      await home.open();
      await home.fillDestination('Barcelona');
      await home.selectDates(daysFromNow(14), daysFromNow(17));
      await home.setOccupancy(2, 1);
      await home.submitSearch();

      await results.waitForResults();
      await expect(results.propertyCards.first()).toBeVisible();
      expect(await results.propertyCards.count()).toBeGreaterThan(0);
    });

    test('[TMS-BOOK-005] Search with valid check-in and check-out dates', async ({ page, browserName }) => {
      ReportingApi.setTestCaseId('TMS-BOOK-005');
      ReportingApi.addAttributes([
        { key: 'priority', value: 'HIGH' },
        { key: 'area', value: 'Search' },
        { key: 'type', value: 'Functional' },
        { key: 'browser', value: browserName },
        { value: 'search' },
        { value: 'agentic_candidate' },
        { value: 'dates' },
        { value: 'booking' },
        { value: 'smoke' },
      ]);
      ReportingApi.setDescription(
        '**Preconditions:** User is on the home page; system date is known.\n\n' +
          '**Steps:**\n' +
          '1. Enter a valid destination (e.g. "Lisbon, Portugal").\n' +
          '2. Set check-in to tomorrow.\n' +
          '3. Set check-out to 3 days after check-in.\n' +
          '4. Click Search.\n' +
          '5. Confirm the search summary banner or breadcrumb. — Results reflect the selected stay dates.',
      );

      const home = new BookingHomePage(page);
      const results = new SearchResultsPage(page);

      await home.open();
      await home.fillDestination('Lisbon');
      await home.selectDates(daysFromNow(1), daysFromNow(4));
      await home.submitSearch();

      await results.waitForResults();
      await expect(results.propertyCards.first()).toBeVisible();
    });

    test('[TMS-BOOK-008] Search with empty destination field', async ({ page, browserName }) => {
      ReportingApi.setTestCaseId('TMS-BOOK-008');
      ReportingApi.addAttributes([
        { key: 'priority', value: 'MEDIUM' },
        { key: 'area', value: 'Search' },
        { key: 'type', value: 'Negative' },
        { key: 'browser', value: browserName },
        { value: 'booking' },
        { value: 'negative' },
        { value: 'smoke' },
        { value: 'automated' },
        { value: 'search' },
      ]);
      ReportingApi.setDescription(
        '**Preconditions:** User is on the home page; check-in and check-out dates are valid.\n\n' +
          '**Expected result:** Search does not proceed; the Destination field is highlighted with a required-field ' +
          'error and no results page opens.\n\n' +
          '_Note: intentionally expected to fail — the current booking.com UI does not block an empty-destination ' +
          'search the way this legacy TMS case describes._',
      );

      const home = new BookingHomePage(page);
      await home.open();

      await page.getByRole('button', { name: /^search$/i }).click();
      await page.waitForTimeout(1000);

      await expect(page.getByText('Please enter a destination')).toBeVisible({ timeout: 3000 });
    });

    test('[TMS-BOOK-007] Search with check-out date before check-in date', async ({ page, browserName }) => {
      ReportingApi.setTestCaseId('TMS-BOOK-007');
      ReportingApi.addAttributes([
        { key: 'priority', value: 'HIGH' },
        { key: 'area', value: 'Search' },
        { key: 'type', value: 'Negative' },
        { key: 'browser', value: browserName },
        { value: 'booking' },
        { value: 'agentic_candidate' },
        { value: 'negative' },
        { value: 'dates' },
        { value: 'search' },
      ]);
      ReportingApi.setDescription(
        '**Preconditions:** User is on the home page search widget.\n\n' +
          '**Steps:**\n' +
          '1. Enter destination "Rome, Italy".\n' +
          '2. Set check-in to 10 days from today.\n' +
          '3. Set check-out to 7 days from today (before check-in).\n' +
          '4. Click Search.\n' +
          '5. Observe validation feedback. — Search is blocked with an inline validation message.\n\n' +
          "_Note: intentionally expected to fail — booking.com's calendar UI prevents selecting an earlier " +
          'check-out instead of surfacing the inline blocking error this legacy TMS case expects._',
      );

      const home = new BookingHomePage(page);
      await home.open();
      await home.fillDestination('Rome');
      await home.selectDates(daysFromNow(10), daysFromNow(7));
      await home.submitSearch();

      await expect(page.getByText('Check-out date must be after check-in date')).toBeVisible({ timeout: 3000 });
    });
  });

  test.describe('Results Filtering', () => {
    ReportingApi.setDescription(
      'Narrowing an already-loaded results page down with the star rating, price range, and free cancellation ' +
        'filters.',
      'Results Filtering',
    );
    ReportingApi.addAttributes([{ key: 'feature', value: 'results-filtering' }], 'Results Filtering');

    test('[TMS-BOOK-002] Filter search results by star rating', async ({ page, browserName }) => {
      ReportingApi.setTestCaseId('TMS-BOOK-002');
      ReportingApi.addAttributes([
        { key: 'priority', value: 'MEDIUM' },
        { key: 'area', value: 'Filters' },
        { key: 'type', value: 'Functional' },
        { key: 'browser', value: browserName },
        { value: 'booking' },
        { value: 'search' },
        { value: 'automated' },
        { value: 'filters' },
        { value: 'regression' },
      ]);
      ReportingApi.setDescription(
        '**Preconditions:** Search results are displayed for a city with mixed 3-5 star properties (e.g. Barcelona).\n\n' +
          '**Steps:**\n' +
          '1. On the results page, open the Star rating filter.\n' +
          '2. Select 4 stars and 5 stars only.\n' +
          '3. Click Apply.\n' +
          '4. Review the filtered list. — Only hotels rated 4 or 5 stars are shown.',
      );

      const home = new BookingHomePage(page);
      const results = new SearchResultsPage(page);

      await home.open();
      await home.fillDestination('Barcelona');
      await home.selectDates(daysFromNow(14), daysFromNow(17));
      await home.submitSearch();

      await results.waitForResults();
      const countBefore = await results.propertyCards.count();
      await results.filterByStarRating(4, 5);
      const countAfter = await results.propertyCards.count();

      expect(countAfter).toBeLessThanOrEqual(countBefore);
    });

    test('[TMS-BOOK-003] Filter search results by nightly price range', async ({ page, browserName }) => {
      ReportingApi.setTestCaseId('TMS-BOOK-003');
      ReportingApi.addAttributes([
        { key: 'priority', value: 'MEDIUM' },
        { key: 'area', value: 'Filters' },
        { key: 'type', value: 'Functional' },
        { key: 'browser', value: browserName },
        { value: 'booking' },
        { value: 'regression' },
        { value: 'dates' },
        { value: 'automated' },
        { value: 'filters' },
      ]);
      ReportingApi.setDescription(
        '**Preconditions:** Search results are displayed with prices ranging from EUR 50 to EUR 400 per night.\n\n' +
          '**Steps:**\n' +
          '1. Open the Price filter on the results page.\n' +
          '2. Set minimum price to EUR 100 and maximum price to EUR 250.\n' +
          '3. Apply the filter.\n' +
          '4. Verify displayed prices for the first five results are within EUR 100-250.\n\n' +
          '_Note: intentionally expected to fail — booking.com\'s own filter buckets, currency and included taxes ' +
          "don't line up exactly with the strict bound this legacy TMS case expects._",
      );

      const home = new BookingHomePage(page);
      const results = new SearchResultsPage(page);

      await home.open();
      await home.fillDestination('Barcelona');
      await home.selectDates(daysFromNow(14), daysFromNow(17));
      await home.submitSearch();

      await results.waitForResults();
      await results.filterByPriceRange(100, 250);

      const prices = await results.getVisiblePrices(5);
      for (const price of prices) {
        expect(price).toBeGreaterThanOrEqual(100);
        expect(price).toBeLessThanOrEqual(250);
      }
    });

    test('[TMS-BOOK-006] Show only properties with free cancellation', async ({ page, browserName }) => {
      ReportingApi.setTestCaseId('TMS-BOOK-006');
      ReportingApi.addAttributes([
        { key: 'priority', value: 'MEDIUM' },
        { key: 'area', value: 'Filters' },
        { key: 'type', value: 'Functional' },
        { key: 'browser', value: browserName },
        { value: 'cancellation' },
        { value: 'booking' },
        { value: 'filters' },
        { value: 'agentic_candidate' },
      ]);
      ReportingApi.setDescription(
        '**Preconditions:** Search results include both refundable and non-refundable rate plans.\n\n' +
          '**Expected result:** Only hotels offering at least one free-cancellation rate appear in the results; ' +
          'each visible listing displays a "Free cancellation" badge or equivalent label.',
      );

      const home = new BookingHomePage(page);
      const results = new SearchResultsPage(page);

      await home.open();
      await home.fillDestination('Barcelona');
      await home.selectDates(daysFromNow(14), daysFromNow(17));
      await home.submitSearch();

      await results.waitForResults();
      await results.filterByFreeCancellation();

      await expect(results.propertyCards.first()).toBeVisible();
    });
  });

  test.describe('Results Interaction', () => {
    ReportingApi.setDescription(
      'Acting on an already-loaded results page: reordering it and drilling into a single property.',
      'Results Interaction',
    );
    ReportingApi.addAttributes([{ key: 'feature', value: 'results-interaction' }], 'Results Interaction');

    test('[TMS-BOOK-004] Sort hotel results by lowest price', async ({ page, browserName }) => {
      ReportingApi.setTestCaseId('TMS-BOOK-004');
      ReportingApi.addAttributes([
        { key: 'priority', value: 'LOW' },
        { key: 'area', value: 'Search' },
        { key: 'type', value: 'Functional' },
        { key: 'browser', value: browserName },
        { value: 'search' },
        { value: 'agentic_candidate' },
        { value: 'smoke' },
        { value: 'booking' },
      ]);
      ReportingApi.setDescription(
        '**Preconditions:** Search results are displayed for a destination with at least 10 available properties.\n\n' +
          '**Expected result:** Results are reordered with the lowest nightly rate first; each subsequent hotel ' +
          'has an equal or higher displayed price than the previous one.',
      );

      const home = new BookingHomePage(page);
      const results = new SearchResultsPage(page);

      await home.open();
      await home.fillDestination('Barcelona');
      await home.selectDates(daysFromNow(14), daysFromNow(17));
      await home.setOccupancy(2, 1);
      await home.submitSearch();

      await results.waitForResults();
      await results.sortByPriceLowestFirst();

      const prices = await results.getVisiblePrices(5);
      for (let i = 1; i < prices.length; i++) {
        expect(prices[i]).toBeGreaterThanOrEqual(prices[i - 1]);
      }
    });

    test('[TMS-BOOK-009] Open hotel details from search results', async ({ page, browserName }) => {
      ReportingApi.setTestCaseId('TMS-BOOK-009');
      ReportingApi.addAttributes([
        { key: 'priority', value: 'MEDIUM' },
        { key: 'area', value: 'Search' },
        { key: 'type', value: 'Functional' },
        { key: 'browser', value: browserName },
        { value: 'booking' },
        { value: 'regression' },
        { value: 'search' },
        { value: 'agentic_candidate' },
      ]);
      ReportingApi.setDescription(
        '**Preconditions:** Search results list contains at least one available hotel.\n\n' +
          '**Steps:**\n' +
          '1. Perform a valid search for any destination.\n' +
          '2. Click the first hotel name or View details link.\n' +
          '3. Review the hotel details page.\n' +
          '4. Scroll to amenities and room types sections. — Hotel details page opens with photos, address, ' +
          'amenities, room types and price matching the search result entry.',
      );

      const home = new BookingHomePage(page);
      const results = new SearchResultsPage(page);

      await home.open();
      await home.fillDestination('Barcelona');
      await home.selectDates(daysFromNow(14), daysFromNow(17));
      await home.submitSearch();

      await results.waitForResults();
      const detailsPage = await results.openFirstProperty();

      await detailsPage.waitForLoadState('domcontentloaded');
      await expect(detailsPage.locator('h2').first()).toBeVisible({ timeout: 15000 });
    });
  });
});
