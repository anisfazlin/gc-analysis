from linkedin_scraper import Person, actions
from selenium import webdriver
from dotenv import load_dotenv
import os

load_dotenv()
driver = webdriver.Chrome()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

url = "https://www.linkedin.com/in/cedriczhchan"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
# Person(linkedin_url=None, name=[], about=[], experiences=[], educations=[], interests=[], accomplishments=[], company=[], job_title=[], driver=driver, scrape=True)
person = Person(linkedin_url=url, name=[], about=[], job_title=[], company=[], driver=driver, scrape=True)

person.scrape()
# print(f'{person}')
print(f'Name : {person.name}')
print(f'About : {person.about}')
person.scrape(close_on_complete=False)