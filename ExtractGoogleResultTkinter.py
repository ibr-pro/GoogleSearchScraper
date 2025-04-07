import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import time
import os
import threading

# --- Scraping Function ---
def scrape_google(query, max_pages, status_label):
    """Scrape Google search results and save to CSV."""
    status_label.config(text="Starting scraping process...")
    
    # Setup the webdriver
    try:
        driver = webdriver.Chrome()  # Add executable_path if needed
        driver.maximize_window()
    except Exception as e:
        status_label.config(text=f"Error initializing driver: {e}")
        return

    # Open the initial URL
    url = f"https://www.google.com/search?q={query}"
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.tF2Cxc"))
        )
    except TimeoutException:
        status_label.config(text="Timed out waiting for search results.")
        driver.quit()
        return

    # List to store all results
    all_results = []
    page_count = 1

    while True:
        status_label.config(text=f"Scraping page {page_count}...")
        
        # Extract search results
        try:
            search_results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
            for result in search_results:
                try:
                    title = result.find_element(By.TAG_NAME, "h3").text
                    link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                    all_results.append({"Title": title, "URL": link})
                except NoSuchElementException:
                    continue
        except Exception as e:
            status_label.config(text=f"Error extracting results: {e}")
            break

        # Check for "Next" button
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#pnnext > span.oeN89d"))
            )
            next_button.click()
            time.sleep(2)
            page_count += 1

            if max_pages and page_count > max_pages:
                status_label.config(text=f"Reached max page limit of {max_pages}.")
                break
        except TimeoutException:
            status_label.config(text="No more pages found.")
            break
        except Exception as e:
            status_label.config(text=f"Error navigating: {e}")
            break

    # Export to CSV
    output_file = "google_search_results_all_pages.csv"
    if all_results:
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "URL"])
            writer.writeheader()
            writer.writerows(all_results)
        status_label.config(text=f"Saved {len(all_results)} results to {output_file}")
    else:
        status_label.config(text="No results found.")

    driver.quit()

# --- GUI Function ---
def start_scraping():
    """Start the scraping process in a separate thread."""
    query = query_entry.get()
    max_pages_str = max_pages_entry.get()

    if not query or not max_pages_str:
        status_label.config(text="Please enter both query and max pages.")
        return

    try:
        max_pages = int(max_pages_str)
        if max_pages <= 0:
            raise ValueError
    except ValueError:
        status_label.config(text="Max pages must be a positive integer.")
        return

    # Run scraping in a thread to keep GUI responsive
    thread = threading.Thread(target=scrape_google, args=(query, max_pages, status_label))
    thread.start()

# --- Tkinter GUI Setup ---
root = tk.Tk()
root.title("Fidar Google Search Scraper")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Style configuration
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
style.configure("TButton", font=("Helvetica", 11, "bold"), padding=5)
style.map("TButton", background=[("active", "#4CAF50")], foreground=[("active", "white")])

# Title
title_label = ttk.Label(root, text="Google Search Scraper", font=("Helvetica", 16, "bold"), foreground="#333333")
title_label.pack(pady=20)

# Query input
query_frame = ttk.Frame(root)
query_frame.pack(pady=10, padx=20, fill="x")
ttk.Label(query_frame, text="Search Query:").pack(side="left")
query_entry = ttk.Entry(query_frame, width=30, font=("Helvetica", 11))
query_entry.pack(side="left", padx=5)

# Max pages input
max_pages_frame = ttk.Frame(root)
max_pages_frame.pack(pady=10, padx=20, fill="x")
ttk.Label(max_pages_frame, text="Max Pages:").pack(side="left")
max_pages_entry = ttk.Entry(max_pages_frame, width=10, font=("Helvetica", 11))
max_pages_entry.pack(side="left", padx=5)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=start_scraping, style="TButton")
submit_button.pack(pady=20)
style.configure("TButton", background="#4CAF50", foreground="black")  # Green button

# Status label
status_label = ttk.Label(root, text="Ready", wraplength=350, justify="center", foreground="#555555")
status_label.pack(pady=10)

# Run the GUI
root.mainloop()