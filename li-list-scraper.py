from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import csv
import os

load_dotenv()
driver = webdriver.Chrome()
driver.implicitly_wait(10) # seconds

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal

results = []
for page in range(1, 45):
  driver.get(f'https://www.linkedin.com/search/results/people/?keywords=coingecko&origin=SWITCH_SEARCH_VERTICAL&page={page}')

  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.entity-result__content')))

  profiles = driver.find_elements(By.CSS_SELECTOR, '.entity-result__content')

  for profile in profiles:
    name = profile.find_element(By.CSS_SELECTOR, '.entity-result__title').text
    url = profile.find_element(By.CSS_SELECTOR, '.entity-result__title').get_attribute('href')
    results.append({'name': name, 'url': url})

  print(f'Scraped {len(profiles)} profiles from page {page}')

with open('linkedin_results.csv', 'w', newline='', encoding='utf-8') as f:
  writer = csv.writer(f)
  writer.writerow(['name', 'url'])
  writer.writerows(results) 

print('Scraping complete!')
driver.quit()