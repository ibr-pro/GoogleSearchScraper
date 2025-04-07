# GoogleSearchScraper
A Python-based tool with a Tkinter GUI to scrape Google search results and save them to a CSV file. Supports multi-page scraping using Selenium.
# Google Search Scraper

A Python tool with a Tkinter GUI that scrapes Google search results across multiple pages using Selenium and saves them to a CSV file. Ideal for researchers, data analysts, or anyone needing to extract Google search data efficiently.

## Features
- **User-Friendly GUI**: Input search query and max pages via a Tkinter interface.
- **Multi-Page Scraping**: Extracts titles and URLs from multiple Google result pages.
- **CSV Export**: Saves results in a structured `google_search_results_all_pages.csv` file.
- **Responsive Design**: Runs scraping in a background thread to keep the GUI active.

## Prerequisites
- **Python 3.6+**: Ensure Python is installed.
- **Dependencies**: Install required libraries with:
  ```bash
  pip install selenium tkinter
