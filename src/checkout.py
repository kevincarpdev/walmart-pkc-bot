import asyncio
import os
from playwright.async_api import Page

async def guest_checkout(page: Page):
    """
    Handles the Guest Checkout flow once an item is in the cart.
    """
    print("[*] Starting Guest Checkout flow...")
    
    # 1. Go to Cart
    await page.goto("https://www.walmart.com/cart", wait_until="networkidle")
    
    # 2. Click Checkout
    checkout_btn = await page.wait_for_selector('button:has-text("Checkout")', timeout=10000)
    await checkout_btn.click()
    
    # 3. Select Guest Checkout if prompted
    try:
        guest_btn = await page.wait_for_selector('button:has-text("Continue as guest")', timeout=5000)
        await guest_btn.click()
    except:
        print("[*] Already at guest info or modal didn't appear.")

    # 4. Fill Address Info (Using ENV vars)
    print("[*] Filling shipping info...")
    await page.fill('input[name="firstName"]', os.getenv("FIRST_NAME", "John"))
    await page.fill('input[name="lastName"]', os.getenv("LAST_NAME", "Doe"))
    await page.fill('input[name="addressLineOne"]', os.getenv("STREET_ADDRESS", ""))
    await page.fill('input[name="city"]', os.getenv("CITY", ""))
    await page.select_option('select[name="state"]', os.getenv("STATE", "CA"))
    await page.fill('input[name="postalCode"]', os.getenv("ZIP_CODE", ""))
    await page.fill('input[name="phone"]', os.getenv("PHONE_NUMBER", ""))
    await page.fill('input[name="email"]', os.getenv("GUEST_EMAIL", ""))

    # 5. Continue to Delivery/Payment
    # Note: Walmart UI varies, this is a skeleton for the transition.
    save_btn = await page.wait_for_selector('button:has-text("Save")', timeout=5000)
    await save_btn.click()
    
    print("[!] Information filled. Manual intervention or Payment implementation needed.")
