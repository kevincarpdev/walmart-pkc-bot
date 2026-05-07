import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth

async def get_stealth_browser(playwright, proxy=None):
    """
    Spawns a playwright browser instance with stealth evasion and optional proxy.
    """
    browser_args = [
        "--disable-blink-features=AutomationControlled",
        "--disable-infobars",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    
    launch_kwargs = {
        "headless": True,  # User may want False for debugging
        "args": browser_args
    }
    
    if proxy:
        # proxy example: "http://user:pass@host:port"
        launch_kwargs["proxy"] = {"server": proxy}
        
    browser = await playwright.chromium.launch(**launch_kwargs)
    
    # Create context with a real-looking User-Agent
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080}
    )
    
    # Apply stealth to all new pages in this context
    page = await context.new_page()
    await stealth(page)
    
    return browser, context, page
