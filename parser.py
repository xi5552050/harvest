import asyncio
from playwright.async_api import async_playwright

SEARCH_URL = "https://www.olx.ua/uk/nedvizhimost/kvartiry/prodazha-kvartir/irpen/?currency=USD"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()
        await page.goto(
            SEARCH_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        await page.wait_for_timeout(5000)

        print("HARVEST: страница открыта")
        print("URL:", page.url)
        print("TITLE:", await page.title())

        links = await page.locator("a").all()

        found = 0

        for link in links:
            href = await link.get_attribute("href")

            if href and "/d/uk/obyavlenie/" in href:
                print("ОБЪЯВЛЕНИЕ:", href)
                found += 1

                if found >= 5:
                    break

        print("НАЙДЕНО:", found)

        await browser.close()


asyncio.run(main())
