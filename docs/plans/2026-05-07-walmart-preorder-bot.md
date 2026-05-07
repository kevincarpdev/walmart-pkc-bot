# Walmart Preorder Bot Implementation Plan

**Goal:** Create an automated bot that monitors Walmart product links, rotates IPs to bypass detection, and enters the checkout queue precisely at 5:59:00 for live drops.

**Architecture:**
- **Language:** Python 3.12
- **Automation:** Playwright (Chromium) with `playwright-stealth` for bot detection evasion.
- **Concurrency:** `asyncio` for managing multiple task-specific browsers.
- **Rotation:** Proxy support (SOCKS5/HTTP) per browser instance.
- **Timing:** High-precision synchronization with NTP or system clock for the 5:59:00 burst.

**Tech Stack:** `playwright`, `playwright-stealth`, `aiohttp`, `python-dotenv`, `pytz`.

---

### Task 1: Initialize Project and Requirements
**Objective:** Set up the base directory, virtual environment, and dependency list.
**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
**Step 1:** Create `requirements.txt` with `playwright`, `playwright-stealth`, `python-dotenv`, `pytz`.
**Step 2:** Configure `.env.example` for proxies and target URLs.
**Step 3:** Commit.

### Task 2: Build Proxy & Stealth Browser Factory
**Objective:** Create a utility to spawn Playwright instances with unique proxies and stealth configurations.
**Files:**
- Create: `src/browser_factory.py`
**Step 1:** Implement `get_stealth_browser(proxy_url=None)` using `playwright-stealth`.
**Step 2:** Add logic to handle different IP/Proxy configurations per instance.
**Step 3:** Commit.

### Task 3: Implement Wait-for-Live Logic (Timing Engine)
**Objective:** Create a precise scheduler that triggers refreshes leading up to 5:59:00.
**Files:**
- Create: `src/timing.py`
**Step 1:** Implement a countdown timer that calculates the exact delta to 5:58:55 (start of burst).
**Step 2:** Use `asyncio.sleep` with micro-adjustments for jitter reduction.
**Step 3:** Commit.

### Task 4: Develop Walmart Queue Entry & Scraper
**Objective:** Navigate to the product page and detect the transition from "Out of Stock" to "Add to Cart" or "Queue".
**Files:**
- Create: `src/scraper.py`
**Step 1:** Implement page navigation with custom headers/User-Agents.
**Step 2:** Create the "Refresh Loop" function that triggers at the specified time.
**Step 3:** Implement selector-based detection for the "Add to Cart" button or the Queue modal.
**Step 4:** Commit.

### Task 5: Guest Checkout Flow (Phase 1)
**Objective:** Automate the handoff from "Add to Cart" to the Guest Checkout screen.
**Files:**
- Create: `src/checkout.py`
**Step 1:** Fill out initial guest info (Email, Shipping).
**Step 2:** Handle the "Continue to Payment" transition.
**Step 3:** Commit.

### Task 6: Main Execution Script
**Objective:** Orchestrate multiple browser instances across the given product list.
**Files:**
- Create: `main.py`
**Step 1:** Load URLs and Proxies from config.
**Step 2:** Launch the async loop for all concurrent browsers.
**Step 3:** Commit.
