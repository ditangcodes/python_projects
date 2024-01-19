import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import pprint

def scrape_jobs():
    #Request URL of CV Library website
    url = 'https://www.cv-library.co.uk/data-engineer-jobs-in-london'
    response = requests.get(url)

    #Parse HTML Content
    soup = BeautifulSoup(response.text, 'html.parser')

    #Extract job details
    job_results = []
    print(soup.find_all('div', class_='job'))
    for job in soup.find_all('div', class_='job'):
        print(job)
        title = job.find('h2').text
        description = job.find('p', class_='description').text
        job_link = job.find('a', class_='job')['href']
        if ('Data Engineer' in title or 'Junior Data Engineer' in title) and ('Python' in description or 'SQL' in description or 'Docker' in description or 'AWS' in description):
            job_results.append({'Title': title, 'Description': description, 'Link': job_link})
    
    #Convert to DataFrame
    df = pd.DataFrame(job_results)

    #Convert to CSV and populate spreadsheet
    fieldnames = ['Job Title', 'Company Name', 'Location', 'Skills', 'Link']

    #Open the file in write mode
    with open ('jobs.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in df.iterrows():
            writer.writerow(row.to_dict())
scrape_jobs()