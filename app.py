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
import requests
from bs4 import BeautifulSoup


URL = "https://www.indeed.com/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL)
    
    page.get_by_placeholder("Job title, keywords, or company").fill("data analyst")
    # page.get_by_placeholder('City, state, zip code, or "remote"').fill("remote")
    page.get_by_text("Find jobs", exact = True).click()
    
    page.wait_for_selector('ul.css-zu9cdh.eu4oa1w0', timeout=10000)
    time.sleep(5)
    
    # html_content = page.content()  # Get the HTML content of the page
    # with open("job_listings_page.html", "w", encoding="utf-8") as file:
    #     file.write(html_content)  # Save it to an HTML file
    #     print("Page saved successfully")
    
        
    up = True
    
    jobs_hrefs = []
    
    while up:
        # Wait for job listings to load
        page.wait_for_selector('ul.css-zu9cdh.eu4oa1w0', timeout=10000)
        time.sleep(5)
        # Locate the job listings container
        page_job_container = page.locator('ul.css-zu9cdh.eu4oa1w0')
        # Find all job listings within the container
        job_items = page_job_container.locator('li.css-5lfssm.eu4oa1w0').all()
        print(f"Found {len(job_items)} job items.")
        jobs = [item.locator("a.jcs-JobTitle.css-jspxzf.eu4oa1w0") for item in job_items if item.locator("a.jcs-JobTitle.css-jspxzf.eu4oa1w0").count() > 0]
        
        if jobs:
            for item in jobs:
                href = item.get_attribute("href")
                href = URL + href
                # print(href)
                jobs_hrefs.append(href)

        
        try:
            # Check if the "Next Page" button exists before attempting to click
            if page.get_by_label("Next Page").count() > 0:
                page.get_by_label("Next Page").click()  # Click the "Next Page" button if it exists
            else:
                up = False
                print("No more pages available.")
        except Exception as e:
            up = False
            print(f"An error occurred: {e}")
            
            
    if len(jobs_hrefs)>0:
        
        for job_link in jobs_hrefs:
            page.goto(job_link)
            time.sleep(3)
            # print("Redirected successfully")
            #Job URL
            
            job_url = page.url
            print(job_url)
            if page.locator("h1.jobsearch-JobInfoHeader-title.css-1b4cr5z.e1tiznh50").count() > 0:
                Job_Title = page.locator("h1.jobsearch-JobInfoHeader-title.css-1b4cr5z.e1tiznh50").inner_text()
                print(Job_Title)
                
                
            if page.locator("a.css-1ioi40n.e19afand0").count() > 0:
                Company_Name = page.locator("a.css-1ioi40n.e19afand0").inner_text()
                Company_Website = page.locator("a.css-1ioi40n.e19afand0").get_attribute("href")
                print(Company_Name, Company_Website)
                
            if page.locator("div.css-45str8.eu4oa1w0").count() > 0:
                Location = page.locator("div.css-45str8.eu4oa1w0").inner_text()
                print(Location)
                
            
            if page.locator('#jobDescriptionText').count() > 0:
                # Get the text from the div
                full_job_info = page.locator('#jobDescriptionText').inner_text()
                print(full_job_info)
                
                
            
            # Salary
            # Job_Description
            # Job_Type # Full-Time, Part-Time
            # Posting_Date
            # Job_URL

            
        
    
    
    # generate pdf
    # page.emulate_media(media="screen")
    # page.pdf(path="page.pdf")
    
    time.sleep(20)
    
    page.close()
    browser.close()