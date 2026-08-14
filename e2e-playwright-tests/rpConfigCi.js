import 'dotenv/config';

const config = {
  endpoint: process.env.RP_ENDPOINT,
  apiKey: process.env.RP_API_KEY,
  launch: process.env.RP_LAUNCH || 'Release regression — Search & Filters (booking.com)',
  project: process.env.RP_PROJECT,
  attributes: [
    {
      key: 'agent',
      value: 'playwright',
    },
    {
      key: 'type',
      value: 'release-regression',
    },
    {
      value: 'demo',
    },
    {
      value: 'booking.com',
    },
  ],
  description:
    '**Release regression — Search & Filters**\n\n' +
    'Scope: [booking.com](https://www.booking.com) hotel search — destination lookup, date selection, ' +
    'sorting, and results filtering (free cancellation, star rating, price range).\n\n' +
    'Source: TMS folder 90 ("Search & Filters", 9 cases, linked via Test Case ID for historical tracking).\n\n' +
    'Intent: showcase ReportPortal reporting (Test Case ID linking, attributes, descriptions, statuses, ' +
    'failure attachments) alongside real functional coverage of the search flow ahead of release. ' +
    '3 of the 9 cases are expected to fail',
  launchId: process.env.RP_LAUNCH_ID,
  includeTestSteps: true,
  launchUuidPrint: true,
  skippedIssue: false,
  restClientConfig: {
    timeout: 0,
  },
};

module.exports = { config };
