import retrying
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import csv
import os
import time

load_dotenv()
chrome_options = Options()
chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

actions.login(driver, email, password)  # if email and password aren't given, it'll prompt in the terminal

def scrape_profile(profile_url):
    # Retry mechanism for establishing connection
    @retrying.retry(wait_fixed=2000, stop_max_attempt_number=3)
    def establish_connection():
        return Person(linkedin_url=profile_url, driver=driver, scrape=True)

    try:
        person = establish_connection()

        # Extract data
        name = person.name
        about = person.about
        experiences = person.experiences
        educations = person.educations
        interests = person.interests
        company = person.company
        job_title = person.job_title
        accomplishments = person.accomplishments

        print(f'Done extraction')
        print(person)

        # Write data to CSV file
        with open('profiles.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['linkedin_url', 'name', 'about', 'experiences', 'educations', 'interests', 'company',
                             'job_title', 'accomplishment'])
            writer.writerow(
                [profile_url, name, about, experiences, educations, interests, company, job_title, accomplishments])

        print(f'Data {name} saved to profiles.csv')

    except Exception as e:
        print(f'Error occurred: {str(e)}')
        # Handle the error or log it as needed

with open('linkedin_results.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        profile_url = row['profile_url']
        print(profile_url)
        scrape_profile(profile_url)
        time.sleep(10)

driver.quit()