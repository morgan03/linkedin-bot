from getpass import getpass
import pyautogui
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LinkedInBot():
    def __init__(self, driver, username, password):
        self.driver = driver
        self.username = username
        self.password = password

    def login_to_linkedin(self):
        """ Logs into LinkedIn """
        self.driver.get('https://gb.linkedin.com/')
        login_bar = self.driver.find_element_by_class_name('nav__button-secondary')
        login_bar.click()
        username_textbox = self.driver.find_element_by_id('username')
        password_textbox = self.driver.find_element_by_id('password')
        username_textbox.clear()
        password_textbox.clear()
        username_textbox.send_keys(self.username)
        password_textbox.send_keys(self.password)
        signin_button = self.driver.find_element_by_class_name("login__form_action_container")
        signin_button.click()

    def job_filter(self, job_name, job_location):
        """Searches linkedin for a given job within a given location"""

        self.job_name = job_name
        self.job_location = job_location
        self.driver.implicitly_wait(5)
        job_icon = driver.find_element_by_link_text('Jobs')
        job_icon.click()

        self.driver.implicitly_wait(5)
        search_keywords = self.driver.find_element_by_xpath("//input[starts-with(@id, 'jobs-search-box-keyword')]")
        search_location = self.driver.find_element_by_xpath("//input[starts-with(@id, 'jobs-search-box-location')]")
        search_location.clear()
        search_keywords.clear()
        search_keywords.send_keys(job_name)
        search_location.send_keys(job_location)
        search_location.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(5)
        #pyautogui.click(x=910, y=203, clicks=3)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Easy Apply filter."]'))).click()

    def get_job_listings(self):
        """Get all the jobs present and calls apply function on each of them"""

        for attempt in range(5):
            try:
                job_listings = WebDriverWait(self.driver, 8).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//li[@class="jobs-search-results__list-item occludable-update p0 relative ember-view"]')))
            except Exception as e:
                print('An error occurred: ', e)
                driver.refresh()
            else:
                job_results = self.driver.find_element_by_xpath('//small[@class="display-flex t-12 t-black--light t-normal"]')
                job_results_num = str(job_results.text).split()[0].replace(',', '')
                first_page_url = self.driver.current_url

                for job in job_listings:
                    self.driver.implicitly_wait(5)
                    mouse = ActionChains(self.driver).move_to_element(job)
                    mouse.perform()
                    self.apply_to_job(job)

                if int(job_results_num) > 24:
                    time.sleep(2)
                    all_pages = self.driver.find_element_by_xpath('//li[@class="artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view"]')
                    last_page = all_pages[len(all_pages)-1].text

                    last_page_int = int(re.sub(r'[^/d]', '', last_page))            # Replace any character except the blank space with ""
                    get_last_page = self.driver.find_element_by_xpath("//button[@aria-label='Page "+str(total_pages_int)+"']")
                    get_last_page.send_keys(Keys.RETURN)
                    last_page_url = self.driver.current_url
                    total_jobs = int(last_page.split('start=', 1)[1])

                    # Go through all pages and apply
                    for page in range(25, last_page_int):
                        self.driver.get(first_page_url + '&start=' + str(page))
                        time.sleep(3)
                        for attempt in range(5):
                            try:
                                new_job_listings = WebDriverWait(self.driver, 8).until(
                                        EC.presence_of_all_elements_located((By.XPATH, '//li[@class="jobs-search-results__list-item occludable-update p0 relative ember-view"]')))
                            except Exception as e:
                                print('An error occurred: ', e)
                                driver.refresh()
                            else:
                                for new_job in new_job_listings:
                                    self.driver.implicitly_wait(5)
                                    mouse_new = ActionChains(self.driver).move_to_element(new_job)
                                    mouse_new.perform()
                                    self.apply_to_job(new_job)
                else:
                    print('You have applied to all jobs available. Closing program...')
                    time.sleep(3)
                    self.driver.quit()

    def apply_to_job(self, job_listing):

        """Applies to all the jobs that are found with the easy apply filter"""

        print('\n')
        self.job_listing = job_listing
        print('You are applying to: ', self.job_listing.text)
        #apply_or_discard = input('Do you want to apply for this job? Please enter Yes or No: ')

        #if 'yes' in apply_or_discard.lower():
        try:
            self.driver.implicitly_wait(3)
            apply_button = self.driver.find_element_by_xpath("//div[@class='jobs-apply-button--top-card']")
            apply_button.click()
        except NoSuchElementException:
            print('You have already applied to this position.')
            pass
            time.sleep(2)

        try:
            self.driver.implicitly_wait(3)
            submit_application = self.driver.find_element_by_xpath('//button[@aria-label="Submit application"]')
            submit_application.click()
        except NoSuchElementException:
            print('This is not an Easy Apply position. Moving on to next role...')
            discard_application = self.driver.find_element_by_xpath('//button[@aria-label="Dismiss"]')
            discard_application.click()
            self.driver.implicitly_wait(2)
            confirm_discard = self.driver.find_element_by_xpath('//button[@data-test-dialog-primary-btn]')
            confirm_discard.click()
            pass
        #else:
            #pass

    def execute(self):
        """Executes the entire application process"""

        if username and password:
            job_name = input('Please enter the name of the job that you would like to apply for: ')
            job_location = input('Please enter where you would like to work: ')
            self.login_to_linkedin()
            self.driver.maximize_window()
            time.sleep(5)
            self.job_filter(job_name, job_location)
            time.sleep(5)
            self.get_job_listings()
        else:
            print('Please provide a username and password')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

if __name__ == '__main__':
    username = input('Please enter your email or phone number: ')
    password = getpass('Please enter your password: ')
    bot = LinkedInBot(driver, username, password)
    bot.execute()
