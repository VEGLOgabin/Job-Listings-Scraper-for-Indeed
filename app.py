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
import pandas as pd
from io import BytesIO
import plotly.express as px
from datetime import datetime

import random


URL = "https://www.indeed.com/"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

def indeed_job_lead_generation(job_title):
    data_scraped = []
    with sync_playwright() as p:
        
        user_agent = random.choice(USER_AGENTS)

        browser = p.chromium.launch(headless=False)
        # context = browser.new_context()
        # Open a new page in incognito mode
        # page = context.new_page()
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        page.goto(URL)
        
        time.sleep(10)
            
        
        
        page.get_by_placeholder("Job title, keywords, or company").fill(job_title)
        page.get_by_text("Find jobs", exact = True).click()
        
        page.wait_for_selector('ul.css-zu9cdh.eu4oa1w0', timeout=10000)
        time.sleep(5)
        up = True
        jobs_hrefs = []
        
        while up:
            time.sleep(5)
            if page.get_by_role("checkbox").count()>0:
                page.get_by_role("checkbox").click()
            page.wait_for_selector('ul.css-zu9cdh.eu4oa1w0', timeout=10000)
            time.sleep(5)
            page_job_container = page.locator('ul.css-zu9cdh.eu4oa1w0')
            job_items = page_job_container.locator('li.css-5lfssm.eu4oa1w0').all()
            print(f"Found {len(job_items)} job items.")
            jobs = [item.locator("a.jcs-JobTitle.css-jspxzf.eu4oa1w0") for item in job_items if item.locator("a.jcs-JobTitle.css-jspxzf.eu4oa1w0").count() > 0]
            if jobs:
                for item in jobs:
                    href = item.get_attribute("href")
                    href = URL + href
                    jobs_hrefs.append(href)
            try:
                if page.get_by_label("Next Page").count() > 0:
                    page.get_by_label("Next Page").click() 
                    time.sleep(3)
                    if page.locator("button.css-yi9ndv.e8ju0x51").count() > 0:
                        page.locator("button.css-yi9ndv.e8ju0x51").click() 
                else:
                    up = False
                    print("No more pages available.")
            except Exception as e:
                up = False
                # print(f"An error occurred: {e}")
                
                
        if len(jobs_hrefs)>0:
            for job_link in jobs_hrefs:
                page.goto(job_link)
                time.sleep(3)      
                job_url = page.url
                if page.locator("h1.jobsearch-JobInfoHeader-title.css-1b4cr5z.e1tiznh50").count() > 0:
                    Job_Title = page.locator("h1.jobsearch-JobInfoHeader-title.css-1b4cr5z.e1tiznh50").inner_text()
                if page.locator("a.css-1ioi40n.e19afand0").count() > 0:
                    Company_Name = page.locator("a.css-1ioi40n.e19afand0").inner_text()
                    Company_Website = page.locator("a.css-1ioi40n.e19afand0").get_attribute("href")
                if page.locator("div.css-45str8.eu4oa1w0").count() > 0:
                    Location = page.locator("div.css-45str8.eu4oa1w0").inner_text()
                if page.locator('#jobDescriptionText').count() > 0:
                    Full_Job_Info = page.locator('#jobDescriptionText').inner_text()

                row = [Job_Title, Company_Name, job_url,Company_Website, Location, Full_Job_Info]
                
                data_scraped.append(row)      
        time.sleep(5)
        page.close()
        browser.close()
        
    return data_scraped
    
if __name__ == "__main__":
    
    HEADERS = ["JOB TITLE", "COMPANY NAME",  "JOB URL","COMPANY WEBSITE", "LOCATION", "FULL JOB INFORMATION"]
    
    st.title("Welcome to Indeed Jobs Scraper web app")
    
    job_title = st.text_input("# JOB TITLE", "e.g: Data analyst")
    
    
    if job_title  == "e.g: Data analyst":
        job_title = "Data analyst"
    
    data_scraped = []
    
    df = pd.DataFrame(data=data_scraped, columns=HEADERS)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button(f'Scrape all {job_title} jobs from indeed.com '):
            with st.spinner("Loading..."):
                try:
                    data_scraped = indeed_job_lead_generation(job_title)
                except Exception as e:
                    st.error(f"An error occurred during scraping: {e}")
                st.session_state.refresh = True  
            st.info(f'{len(data_scraped)} jobs found')
            st.success("Data scraped successfully")
            
    with col2:
        if len(data_scraped) == 0:
            st.warning("No data collected so fill in the job title field and click scrape button before this action otherwise you will download empty dataset")
            df = pd.DataFrame(data=data_scraped, columns=HEADERS)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download the dataset as CSV",
                data=csv,
                file_name=f'{job_title}-{datetime.now()}.csv',
                mime='text/csv'
            )
        if len(data_scraped) > 0:
            df = pd.DataFrame(data=data_scraped, columns=HEADERS)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download the dataset as CSV",
                data=csv,
                file_name=f'{job_title}-{datetime.now()}.csv',
                mime='text/csv'
            )
            
    with col3:
        if len(data_scraped) == 0:
            st.warning("No data collected so fill in the job title field and click scrape button before this action otherwise you will download empty dataset")
            df = pd.DataFrame(data=data_scraped, columns=HEADERS)
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False)
            writer.close()
            xlsx_data = output.getvalue()
            
            st.download_button(
                label="Download the dataset as XLSX",
                data=xlsx_data,
                file_name=f'{job_title}-{datetime.now()}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        if len(data_scraped) > 0:
            df = pd.DataFrame(data=data_scraped, columns=HEADERS)
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False)
            writer.close()
            xlsx_data = output.getvalue()
            
            st.download_button(
                label="Download the dataset as XLSX",
                data=xlsx_data,
                file_name=f'{job_title}-{datetime.now()}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
    if df.empty:
        st.warning("Please try to scrape data before this action otherwise no data will be displayed.")
        view_df_as_table = st.checkbox("View the dataset as a table", key="one")
        
        if view_df_as_table:
            st.table(df)
            
    if not df.empty:
        view_df_as_table = st.checkbox("View the dataset as a table", key="one")
        
        if view_df_as_table:
            st.table(df)
