from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import time
import os

# Setup the webdriver
driver = webdriver.Chrome()  # Add executable_path="C:/chromedriver/chromedriver.exe" if needed
driver.maximize_window()

# Define your search query
query = "cactus"
url = f"https://www.google.com/search?q={query}"

# Open the initial URL
try:
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.tF2Cxc"))
    )
except TimeoutException:
    print("Timed out waiting for search results to load.")
    driver.quit()
    exit()

# List to store all results
all_results = []

# Maximum pages to scrape (optional limit, e.g., 5 pages)
max_pages = 26
page_count = 1

while True:
    print(f"Scraping page {page_count}...")

    # Extract search results from the current page
    try:
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
        for result in search_results:
            try:
                title = result.find_element(By.TAG_NAME, "h3").text
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                all_results.append({"Title": title, "URL": link})
            except NoSuchElementException:
                print("Could not extract title or URL from a result.")
                continue
    except Exception as e:
        print(f"Error extracting results: {e}")

    # Check for the "Next" button using the provided CSS selector
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#pnnext > span.oeN89d"))
        )
        print("Found 'Next' button, navigating to next page...")
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
        page_count += 1

        # Stop if we've reached the max pages (optional)
        if max_pages and page_count > max_pages:
            print(f"Reached max page limit of {max_pages}.")
            break
    except TimeoutException:
        print("No more pages found or 'Next' button not clickable.")
        break
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        break

# Export all results to CSV
output_file = "google_search_results_all_pages.csv"
if all_results:
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "URL"])
        writer.writeheader()
        writer.writerows(all_results)
    print(f"Total {len(all_results)} results exported to {os.path.abspath(output_file)}")
else:
    print("No results found.")

# Close the browser
driver.quit()