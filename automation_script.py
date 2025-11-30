from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Navigating to https://ajitg25-book-recommender-app-1pqxpk.streamlit.app/ ...")
        page.goto("https://ajitg25-book-recommender-app-1pqxpk.streamlit.app/")

        # Wait for network to be idle to ensure page is loaded
        page.wait_for_load_state("networkidle")

        # Use a robust locator to find the button by its text
        try:
            print("Looking for 'Yes, get this app back up!' button...")
            # get_by_role is the recommended way to locate buttons by text in Playwright
            button = page.get_by_role("button", name="Yes, get this app back up!")
            
            if button.is_visible(timeout=10000):
                print("Button found! Highlighting it...")
                button.highlight() # Visually highlight the element

                #now click on the button
                button.click()
                print("Button clicked successfully.")
            else:
                print("Button not found (is_visible returned False).")
                
        except Exception as e:
            print(f"Error looking for button: {e}")

        # Keep browser open for a few seconds to observe
        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    run()
