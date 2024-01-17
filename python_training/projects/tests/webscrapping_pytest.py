import os
import pandas as pd
import pytest
from websitescrapper.py import scrape_jobs

def test_scrape_jobs():
   scrape_jobs()
   assert os.path.exists('jobs.csv'), "CSV file was not created."
   df = pd.read_csv('jobs.csv')
   assert not df.empty, "CSV file is empty."
   assert 'Title' in df.columns, "'Title' column missing in CSV file."
   assert 'Description' in df.columns, "'Description' column missing in CSV file."
   assert 'Link' in df.columns, "'Link' column missing in CSV file."