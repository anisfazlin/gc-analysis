from linkedin_scraper import Person, actions
from selenium import webdriver
from dotenv import load_dotenv
import csv
import os

load_dotenv()
driver = webdriver.Chrome()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

url = "https://www.linkedin.com/in/cedriczhchan"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
# person = Person(driver=driver, scrape=True)
person = Person(linkedin_url=url, name=[], about=[], experiences=[], educations=[], interests=[], job_title=[], company=[], driver=driver, scrape=True)

# Extract data
name = person.name
about = person.about
experiences = person.experiences
educations = person.educations
interests = person.interests
accomplishments = person.accomplishments
company = person.company
job_title = person.job_title
person.scrape()
print(f'{name}, {company}, {job_title}, {experiences}')

# Write data to CSV file
with open('profiles.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['linkedin_url', 'name', 'about', 'experiences', 'educations', 'interests', 'company', 'job_title', 'accomplishment'])
    writer.writerow([url, name, about, experiences, educations, interests, company, job_title, accomplishments])

print(f'Data {name} saved to profiles.csv')
# person.scrape(close_on_complete=False)