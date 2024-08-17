# Job_Title
# Company_Name
# Location
# Salary
# Job_Description
# Job_Type # Full-Time, Part-Time
# Posting_Date
# Job_URL


from playwright.sync_api import sync_playwright
import streamlit as st
import time
import os
import pandas as pd
import plotly.express as px
from datetime import datetime
import logging


URL = "https://www.indeed.com"


# Job_Title
# Company_Name
# Location
# Salary
# Job_Description
# Job_Type # Full-Time, Part-Time
# Posting_Date
# Job_URL


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL)
    
    page.get_by_placeholder("Job title, keywords, or company").fill("data analyst")
    # page.get_by_placeholder('City, state, zip code, or "remote"').fill("remote")
    page.get_by_text("Find jobs", exact = True).click()
    
    # page_job_container = page.locator("ul.css-zu9cdh.eu4oa1w0")
    # print(page_job_container)
    # li = page_job_container.locator("li.css-5lfssm.eu4oa1w0").all()
    # print(len(li))
    
    # Wait for job listings to load
    page.wait_for_selector('ul.css-zu9cdh.eu4oa1w0', timeout=10000)
    
    # Locate the job listings container
    page_job_container = page.locator('ul.css-zu9cdh.eu4oa1w0')
    
    # Find all job listings within the container
    job_items = page_job_container.locator('li.css-5lfssm.eu4oa1w0').all()
    print(f"Found {len(job_items)} job items.")
    
    
    jobs = [item.locator("a.jcs-JobTitle.css-jspxzf.eu4oa1w0")  for item in job_items]
    
    if jobs:
        for job in jobs:
            # href = job.get_attribute('href')
            # print(href)
            print(job)
    
        

       
    
    
    
    
    
    # page_jobs = page.locator("a.jcs-JobTitle").all()
    # print(page_jobs)
    
    # if page_jobs:
    #     for item in page_jobs:
    #         href = item.get_attribute("href")
    #         print(href)
    
    # generate pdf
    # page.emulate_media(media="screen")
    # page.pdf(path="page.pdf")
    
    time.sleep(5)
    
    page.close()
    browser.close()
        




# def scrape_page(page, page_number):
#     # Locate all real estate articles
#     realestates = page.locator("article").all()
#     links = []
#     estates = []
    
#     for item in realestates:
#         estate = item.locator("a.klMkvj")
#         estates.append(estate)
#         link = estate.get_attribute("href")
#         links.append(link)
   
    
#     time.sleep(2)
#     data = [page_number, links]
#     return data



# def scrape_all_pages():
#     data = []
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.goto(URL)
        
        
#         page_number = 1
        
#         while True:
            
#             print(page_number)
#             current_data = scrape_page(page, page_number)
#             data.append(current_data)
            
#             # Check if there is a next page
#             next_page_button = page.locator("li.WDDJJ")
#             if next_page_button.count() == 0:
#                 break
            
#             next_page_button1 = page.locator("li.WDDJJ:last-child a")
#             aria_disabled = next_page_button1.get_attribute("aria-disabled")
#             if aria_disabled == "true":
#                 break
            
#             page.locator("li.WDDJJ:last-child a").click()
#             page_number +=1
#             time.sleep(10)  # Wait for the page to load
        
#         browser.close()
#     return data
        

# # Run the scraping process
# if __name__ == "__main__":
#     try:
#         data = scrape_all_pages()
#         print(data)
#     except KeyboardInterrupt:
#         print("Process interrupted")