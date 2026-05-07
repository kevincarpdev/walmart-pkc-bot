import asyncio
import os
from dotenv import load_dotenv
from .browser_factory import get_stealth_browser
from .timing import wait_until, get_target_time

load_dotenv()

async def monitor_product(playwright, url, proxy=None):
    """
    Monitors a Walmart product and refreshes aggressively at the drop time.
    """
    browser, context, page = await get_stealth_browser(playwright, proxy)
    
    try:
        print(f"[*] Task started for {url} (Proxy: {proxy})")
        
        # Initial load to get cookies/session ready
        await page.goto(url, wait_until="networkidle")
        
        drop_time = os.getenv("DROP_TIME", "18:00:00")
        target_dt = get_target_time(drop_time)
        
        print(f"[*] Waiting for drop at {drop_time}...")
        # Start refresh cycle a few seconds early to catch the window
        await wait_until(target_dt)
        
        # High-frequency refresh loop
        while True:
            try:
                # Check for Add to Cart or Queue
                atc_button = await page.query_selector('button[data-automation-id="add-to-cart-button"]')
                queue_check = await page.query_selector('text="You’re in the queue"')
                
                if atc_button and await atc_button.is_enabled():
                    print(f"[!] SUCCESS: Add to Cart found for {url}!")
                    await atc_button.click()
                    return page # Hand off to checkout
                
                if queue_check:
                    print(f"[*] Entered queue for {url}!")
                    # Wait in queue...
                    await asyncio.sleep(5)
                    continue
                
                print(f"[-] Item still OOS for {url}, refreshing...")
                await page.reload(wait_until="domcontentloaded")
                await asyncio.sleep(0.5) # Jitter/Rate limit protection
                
            except Exception as e:
                print(f"[!] Refresh error: {e}")
                await asyncio.sleep(1)
                
    finally:
        # We don't close if we succeeded to keep the session alive
        pass
