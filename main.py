import asyncio
import os
from playwright.async_api import async_playwright
from src.scraper import monitor_product
from src.checkout import guest_checkout
from dotenv import load_dotenv

load_dotenv()

async def run_bot():
    urls = os.getenv("PRODUCT_URLS", "").split(",")
    proxies = os.getenv("PROXIES", "").split(",")
    
    async with async_playwright() as playwright:
        tasks = []
        
        for i, url in enumerate(urls):
            url = url.strip()
            if not url:
                continue
            
            # Rotate proxies if available
            proxy = proxies[i % len(proxies)].strip() if proxies else None
            
            async def bot_instance(u, p):
                page = await monitor_product(playwright, u, p)
                if page:
                    await guest_checkout(page)
                    # Keep browser open for inspection
                    await asyncio.sleep(3600)

            tasks.append(bot_instance(url, proxy))
            
        print(f"[*] Launching {len(tasks)} bot instances...")
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n[*] Bot stopped by user.")
