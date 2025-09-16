import asyncio
from playwright.async_api import async_playwright, Page
import random
import re

async def displayed_follower_count(page: Page) -> int:
    follower_list = page.locator('ul[role="list"]')
    follower_list_childs = follower_list.locator('li')
    return await follower_list_childs.count()

async def unfollow(page: Page):
    buttons = await page.query_selector_all("button:has-text('Suivi')")
    followeb_buttons = buttons[1:]
    for followeb_button in followeb_buttons:
        await followeb_button.click()
        await page.wait_for_timeout(random.randint(a=2000, b=3000))
        unfollow_buttons = await page.query_selector_all("button:has-text('Ne plus suivre')")
        for unfollow_button in unfollow_buttons:
            await unfollow_button.click()
            await page.wait_for_timeout(random.randint(a=2000, b=3000))

async def main():
    async with async_playwright() as ap:
        browser_type = ap.chromium
        browser = await browser_type.launch(headless=False)
        page = await browser.new_page()
        await page.wait_for_timeout(random.randint(a=4000, b=6000))
        await page.goto("https://www.linkedin.com/login")
        await page.wait_for_url("https://www.linkedin.com/feed/")
        await page.wait_for_timeout(random.randint(a=4000, b=6000))
        await page.goto("https://www.linkedin.com/mynetwork/network-manager/people-follow/followers/")
        await page.wait_for_timeout(random.randint(a=4000, b=6000))
        network_manager_subtitle = page.locator('.mn-network-manager__subtitle')
        network_manager_subtitle_text = await network_manager_subtitle.inner_text()
        follower_count = int(re.sub(r"\D", "", network_manager_subtitle_text))

        current_displayed_follower = await displayed_follower_count(page=page)
        await unfollow(page=page)

        while current_displayed_follower != follower_count:
            await page.mouse.wheel(0, 500)
            await unfollow(page=page)
            current_displayed_follower = await displayed_follower_count(page=page)
        
        


if __name__ == "__main__":
    asyncio.run(main())    