import { Page } from '@playwright/test';

export class BookingHomePage {
  constructor(private readonly page: Page) {}

  async open() {
    await this.page.goto('https://www.booking.com/', { waitUntil: 'domcontentloaded' });
    await this.dismissOverlays();
  }

  async dismissOverlays() {
    const cookieBtn = this.page.locator('#onetrust-accept-btn-handler');
    try {
      await cookieBtn.waitFor({ state: 'visible', timeout: 5000 });
      await cookieBtn.click();
    } catch {}

    const signInDismiss = this.page.getByRole('button', { name: 'Dismiss sign-in info.' });
    try {
      await signInDismiss.waitFor({ state: 'visible', timeout: 2000 });
      await signInDismiss.click();
    } catch {}
  }

  async fillDestination(destination: string) {
    const input = this.page.locator('input[name="ss"]');
    await input.click();
    await input.fill(destination);
    await this.page.waitForTimeout(1200);
    await this.page.getByTestId('autocomplete-result').first().click();
    await this.dismissOverlays();
  }

  async selectDates(checkIn: Date, checkOut: Date) {
    await this.page.getByTestId('searchbox-datepicker-calendar').waitFor({ state: 'visible', timeout: 5000 });
    await this.selectCalendarDay(checkIn);
    await this.selectCalendarDay(checkOut);
  }

  private async selectCalendarDay(date: Date) {
    const iso = date.toISOString().slice(0, 10);
    const cell = this.page.locator(`[data-date="${iso}"]`);
    for (let i = 0; i < 6 && (await cell.count()) === 0; i++) {
      await this.page.getByRole('button', { name: 'Next month' }).click();
      await this.page.waitForTimeout(300);
    }
    await cell.first().click();
  }

  async setOccupancy(adults: number, rooms: number) {
    await this.page.getByTestId('occupancy-config').click();
    await this.page.waitForTimeout(400);

    const setStepper = async (label: string, target: number, current: number) => {
      const increase = this.page.getByRole('button', { name: new RegExp(`Increase.*${label}`, 'i') });
      const decrease = this.page.getByRole('button', { name: new RegExp(`Decrease.*${label}`, 'i') });
      const diff = target - current;
      const button = diff > 0 ? increase : decrease;
      for (let i = 0; i < Math.abs(diff); i++) {
        await button.click().catch(() => {});
        await this.page.waitForTimeout(150);
      }
    };

    await setStepper('Adults', adults, 2);
    await setStepper('Rooms', rooms, 1);

    await this.page.keyboard.press('Escape').catch(() => {});
  }

  async submitSearch() {
    await this.page.keyboard.press('Escape').catch(() => {});
    await Promise.all([
      this.page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 20000 }).catch(() => {}),
      this.page.getByRole('button', { name: /^search$/i }).click(),
    ]);
    await this.page.waitForTimeout(1500);
    await this.dismissOverlays();
  }
}
