import { Page } from '@playwright/test';

export class SearchResultsPage {
  constructor(private readonly page: Page) {}

  get propertyCards() {
    return this.page.getByTestId('property-card');
  }

  async waitForResults() {
    await this.propertyCards.first().waitFor({ state: 'visible', timeout: 30000 });
  }

  async sortByPriceLowestFirst() {
    await this.page.getByTestId('sorters-dropdown-trigger').click();
    await this.page.waitForTimeout(500);
    await this.page.getByText('Price (lowest first)').click();
    await this.page.waitForTimeout(500);
    await this.waitForResults();
    await this.page.waitForTimeout(1500);
  }

  async filterByFreeCancellation() {
    await this.page.getByText('Free cancellation', { exact: false }).first().click();
    await this.page.waitForTimeout(1000);
  }

  async filterByStarRating(...stars: number[]) {
    for (const star of stars) {
      await this.page
        .getByRole('checkbox', { name: new RegExp(`${star}\\s*stars?`, 'i') })
        .click()
        .catch(async () => {
          await this.page.getByText(`${star} stars`, { exact: false }).first().click();
        });
      await this.page.waitForTimeout(500);
    }
  }

  async filterByPriceRange(min: number, max: number) {
    const minInput = this.page.getByPlaceholder('Min').first();
    const maxInput = this.page.getByPlaceholder('Max').first();
    await minInput.fill(String(min)).catch(() => {});
    await maxInput.fill(String(max)).catch(() => {});
    await maxInput.press('Tab').catch(() => {});
    await this.page.waitForTimeout(1000);
  }

  async getVisiblePrices(limit = 5): Promise<number[]> {
    const priceLocator = this.page.getByTestId('price-and-discounted-price');
    const count = Math.min(await priceLocator.count(), limit);
    const prices: number[] = [];
    for (let i = 0; i < count; i++) {
      const text = (await priceLocator.nth(i).innerText()).replace(/[^\d]/g, '');
      if (text) prices.push(Number(text));
    }
    return prices;
  }

  async openFirstProperty() {
    const [detailsPage] = await Promise.all([
      this.page.waitForEvent('popup').catch(() => this.page),
      this.propertyCards.first().click(),
    ]);
    await detailsPage.waitForLoadState('domcontentloaded');
    return detailsPage;
  }
}
