import { PlaywrightTestConfig } from '@playwright/test';
import { config as rpConfig } from './rpConfigCi';

const config: PlaywrightTestConfig = {
  timeout: 90 * 1000,
  expect: {
    timeout: 15000,
  },
  fullyParallel: false,
  forbidOnly: true,
  workers: 3,
  retries: 0,
  use: {
    headless: true,
    locale: 'en-US',
    viewport: { width: 1440, height: 900 },
    userAgent:
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    screenshot: {
      mode: 'only-on-failure',
      fullPage: true,
    },
    video: 'retain-on-failure',
    actionTimeout: 15000,
    navigationTimeout: 45000,
    trace: 'retain-on-failure',
  },
  reporter: [['list'], ['html', { open: 'never' }], ['@reportportal/agent-js-playwright', rpConfig]],
  testDir: './tests',
  projects: [
    {
      name: 'booking-com',
      testDir: './tests',
    },
  ],
};

export default config;
