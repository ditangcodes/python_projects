import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import pprint
import re

#Request URL of CV Library website
url = 'https://www.cv-library.co.uk/data-engineer-jobs-in-london'
response = requests.get(url)

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]', ' ', text)


def scrape_jobs():
    #Parse HTML Content
    soup = BeautifulSoup(response.text, 'html.parser')

    #Extract job details
    job_results = []
#    print(soup.find_all('div', class_='title="Data Engineer"'))
    print(soup.findAll('h2', 'job__title'))
    for job in soup.find_all('div', class_="job__main"):
        #looking for job title
        title = job.find('h2', class_='job__title').text
        clean_title = title.strip()
        description = job.find('p', class_="job__description").text
        clean_desc = description.replace("(", "").replace('\n','')
        final_desc = clean_desc.strip()
        salary = job.find('dd', class_="job__details-value salary")
        job_link = job.find('a')['href']
        print(job.find('a')['href'])
        if ('Data Engineer' in clean_title or 'Junior Data Engineer' in clean_title) and ('Python' in final_desc or 'SQL' in final_desc or 'Docker' in final_desc or 'AWS' in final_desc):
            job_results.append({'Title': clean_title, 'Salary':salary, 'Description': remove_non_ascii(final_desc[0:-10]), 'Link': job_link})
    
    #Convert to DataFrame
    df = pd.DataFrame(job_results)

    #Convert to CSV and populate spreadsheet
    fieldnames = ['Title', 'Salary', 'Description', 'Link']

    #Open the file in write mode
    with open ('jobs.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in df.iterrows():
            writer.writerow(row.to_dict())

scrape_jobs()