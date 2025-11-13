#!/usr/bin/env python3
"""
Tee Time Booking Automation

This script automates the booking of tee times on foreupsoftware.com.
It will login, select the resident adult rate, choose a date 14 days from now,
and book the first available tee time before 10:30am with minimum 2 players.
"""

import asyncio
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TeeTimeBooker:
    def __init__(self):
        self.username = "mukhtar91@gmail.com"
        self.password = "jamesharden"
        self.base_url = "https://foreupsoftware.com/index.php/booking/20954#/login"
        self.browser = None
        self.page = None

    async def start_browser(self):
        """Initialize browser and page"""
        self.playwright = await async_playwright().start()
        # Use chromium for better compatibility
        self.browser = await self.playwright.chromium.launch(headless=False)  # Set to True for headless
        self.page = await self.browser.new_page()

        # Set a realistic user agent
        await self.page.set_user_agent(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )

    async def close_browser(self):
        """Clean up browser resources"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def login(self):
        """Login to the tee time booking system"""
        logger.info("Navigating to login page...")
        await self.page.goto(self.base_url)

        # Wait for page to load
        await self.page.wait_for_load_state('networkidle')

        logger.info("Filling in login credentials...")

        # Fill username field
        await self.page.fill('input[name="username"], input[type="email"], #username', self.username)

        # Fill password field
        await self.page.fill('input[name="password"], input[type="password"], #password', self.password)

        logger.info("Clicking Sign In button...")

        # Click sign in button - try multiple possible selectors
        sign_in_selectors = [
            'button:has-text("Sign In")',
            'input[type="submit"][value*="Sign"]',
            '.btn:has-text("Sign In")',
            'button[type="submit"]'
        ]

        for selector in sign_in_selectors:
            try:
                await self.page.click(selector)
                break
            except:
                continue

        # Wait for navigation after login
        await self.page.wait_for_load_state('networkidle')
        logger.info("Login completed")

    async def select_resident_adult_rate(self):
        """Click on 'Resident Adult (4-14 Days) Advance' button"""
        logger.info("Selecting Resident Adult rate...")

        # Wait for the rate selection page to load
        await self.page.wait_for_timeout(2000)

        # Look for the resident adult button
        resident_adult_selector = 'button:has-text("Resident Adult (4-14 Days) Advance"), a:has-text("Resident Adult (4-14 Days) Advance")'

        try:
            await self.page.wait_for_selector(resident_adult_selector, timeout=10000)
            await self.page.click(resident_adult_selector)
            logger.info("Resident Adult rate selected")
        except Exception as e:
            logger.error(f"Failed to select resident adult rate: {e}")
            # Take a screenshot for debugging
            await self.page.screenshot(path="debug_rate_selection.png")
            raise

        await self.page.wait_for_load_state('networkidle')

    def get_target_date(self):
        """Calculate the date 5 days from now"""
        target_date = datetime.now() + timedelta(days=5)
        return target_date

    async def select_date(self, target_date):
        """Select the date 5 days from now"""
        logger.info(f"Selecting date: {target_date.strftime('%Y-%m-%d')}")

        # Wait for calendar to be available
        await self.page.wait_for_timeout(2000)

        # Format date for different possible formats
        date_text = target_date.strftime('%d')  # Day only
        date_full = target_date.strftime('%Y-%m-%d')  # Full date
        date_month_day = target_date.strftime('%m/%d')  # MM/DD format

        # Try different date selection methods
        date_selectors = [
            f'[data-date="{date_full}"]',
            f'td:has-text("{date_text}"):not(.other-month)',
            f'.calendar-day:has-text("{date_text}")',
            f'button:has-text("{date_text}")'
        ]

        for selector in date_selectors:
            try:
                await self.page.wait_for_selector(selector, timeout=5000)
                await self.page.click(selector)
                logger.info(f"Date selected using selector: {selector}")
                break
            except:
                continue
        else:
            logger.error("Could not find date selector")
            await self.page.screenshot(path="debug_date_selection.png")
            raise Exception("Failed to select date")

        await self.page.wait_for_load_state('networkidle')

    def time_to_minutes(self, time_str):
        """Convert time string (e.g., '9:30 AM') to minutes since midnight"""
        try:
            time_obj = datetime.strptime(time_str, '%I:%M %p')
            return time_obj.hour * 60 + time_obj.minute
        except:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M')
                return time_obj.hour * 60 + time_obj.minute
            except:
                return 999  # Return a large number if parsing fails

    async def find_and_book_tee_time(self):
        """Find the first available tee time before 10:30am with minimum 2 players"""
        logger.info("Looking for available tee times...")

        # Wait for tee time slots to load
        await self.page.wait_for_timeout(3000)

        # Take a screenshot for debugging
        await self.page.screenshot(path="debug_tee_times.png")

        # Find all tee time slots
        tee_time_slots = await self.page.query_selector_all('.booking-slot, .tee-time-slot, .time-slot')

        if not tee_time_slots:
            logger.error("No tee time slots found")
            raise Exception("No tee time slots found on the page")

        logger.info(f"Found {len(tee_time_slots)} tee time slots")

        cutoff_minutes = 10 * 60 + 30  # 10:30 AM in minutes

        for slot in tee_time_slots:
            try:
                # Get the time text
                time_element = await slot.query_selector('.time, .booking-slot-time')
                if not time_element:
                    continue

                time_text = await time_element.text_content()
                time_minutes = self.time_to_minutes(time_text.strip())

                # Check if time is before 10:30 AM
                if time_minutes >= cutoff_minutes:
                    continue

                # Check number of players available
                players_element = await slot.query_selector('.js-booking-slot-players span:last-child')
                if players_element:
                    players_text = await players_element.text_content()
                    try:
                        available_players = int(players_text.strip())
                        if available_players < 2:
                            continue
                    except:
                        continue

                logger.info(f"Found suitable tee time: {time_text} with {players_text} players")

                # Click on this tee time slot
                await slot.click()
                await self.page.wait_for_timeout(2000)

                # Now configure the booking
                await self.configure_booking()
                return True

            except Exception as e:
                logger.warning(f"Error processing tee time slot: {e}")
                continue

        logger.error("No suitable tee times found")
        return False

    async def configure_booking(self):
        """Configure booking details: max players, no carts, then book"""
        logger.info("Configuring booking details...")

        # Wait for booking popup/form to appear
        await self.page.wait_for_timeout(2000)

        # Select maximum available players
        try:
            players_buttons = await self.page.query_selector_all('.js-booking-field-buttons[data-field="players"] a')
            if players_buttons:
                # Click the last (highest number) player option
                max_players_button = players_buttons[-1]
                await max_players_button.click()
                logger.info("Selected maximum players")
        except Exception as e:
            logger.warning(f"Could not select players: {e}")

        # Select "No" for carts
        try:
            no_carts_button = await self.page.query_selector('.js-booking-field-buttons[data-field="carts"] a[data-value="no"]')
            if no_carts_button:
                await no_carts_button.click()
                logger.info("Selected no carts")
        except Exception as e:
            logger.warning(f"Could not select cart option: {e}")

        # Wait a moment for selections to register
        await self.page.wait_for_timeout(1000)

        # Click the "Book Time" button
        try:
            book_button = await self.page.query_selector('.js-book-button, button:has-text("Book Time")')
            if book_button:
                await book_button.click()
                logger.info("Clicked Book Time button")

                # Wait for booking confirmation
                await self.page.wait_for_timeout(5000)
                logger.info("Tee time booking initiated!")
            else:
                logger.error("Could not find Book Time button")
                await self.page.screenshot(path="debug_book_button.png")
        except Exception as e:
            logger.error(f"Error clicking book button: {e}")
            await self.page.screenshot(path="debug_booking_error.png")

    async def run(self):
        """Main execution method"""
        try:
            await self.start_browser()

            # Step 1: Login
            await self.login()

            # Step 2: Select date (5 days from now)
            target_date = self.get_target_date()
            await self.select_date(target_date)

            # Step 3: Find and book tee time
            success = await self.find_and_book_tee_time()

            if success:
                logger.info("Tee time booking completed successfully!")
            else:
                logger.error("Failed to find suitable tee time")

            # Keep browser open for a moment to see results
            await self.page.wait_for_timeout(10000)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            if self.page:
                await self.page.screenshot(path="debug_error.png")
        finally:
            await self.close_browser()

async def main():
    """Entry point"""
    booker = TeeTimeBooker()
    await booker.run()

if __name__ == "__main__":
    asyncio.run(main())
