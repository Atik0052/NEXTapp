import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import openpyxl

workbook = openpyxl.Workbook()

# Create a new worksheet (change the sheet name as needed)
worksheet = workbook.active
worksheet.title = 'Question_Answers'

# Set up OpenAI GPT-3.5 API
openai.api_key = "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"  # Replace with your API key


data = {
    'Question': [],
    'Answer': []
}
texts = []

PATH = "D:\AISHA\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--headless")


with webdriver.Chrome(service=Service(PATH)) as driver:
    driver.get("https://www.linkedin.com/home")

    
    time.sleep(3)
    email_element = driver.find_element(By.ID, 'session_key')
    password_element = driver.find_element(By.ID, 'session_password')

    email_element.send_keys('aishamc46@gmail.com')
    password_element.send_keys('U2opia@2023')

    # Find and click the "Sign in" button
    sign_in_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    sign_in_button.click()

    WebDriverWait(driver, 100)    

    with open("D:\AISHA\cpaas-tools\key.txt", "r") as file:
        keywords = file.read().splitlines()
        links = []

        for keyword in keywords:
            try:
                print("keyword:",keyword)
                # Specify the Excel file name (change it as needed)
                # excel_file_name = f'{keyword}.xlsx'

                # Save the workbook to the Excel file
                # workbook.save(excel_file_name)
                # driver.get(start)
                # Locate the search input element
                time.sleep(50)

                search_input =  driver.find_element(By.CSS_SELECTOR,'input[placeholder="Search"]')
                search_input.clear()

                # Clear the search input field using JavaScript
                driver.execute_script("arguments[0].value = '';", search_input)
                
                search_input.send_keys(keyword)

                # Simulate pressing the Enter key to submit the search
                search_input.send_keys(Keys.ENTER)
                print("entered")

                WebDriverWait(driver,20)

                time.sleep(20)

                 # Find the parent div by ID
                filters_bar = driver.find_element(By.CLASS_NAME, "search-reusables__filters-bar-grouping")
                print("filter_bar")

                if filters_bar:
                    # Find the ul element within the div
                    filter_list = filters_bar.find_element(By.CLASS_NAME, "search-reusables__filter-list")

                    if filter_list:
                        # Find all li elements within the ul
                        filters = filter_list.find_elements(By.CLASS_NAME, "search-reusables__primary-filter")

                        # Iterate through the li elements
                        for filter_item in filters:
                            # Find the button within the li
                            button = filter_item.find_element(By.TAG_NAME, "button")

                            if button and button.text.strip() == "Posts":
                                # Check if the button text is "Posts" and click it
                                button.click()

                                time.sleep(20)
                                # print("going to ul")

                                main_element = driver.find_element(By.CLASS_NAME,"scaffold-layout__main")
                                print(main_element)
                                if main_element:
                            
                                    div2_element = main_element.find_element(By.CLASS_NAME,"scaffold-finite-scroll__content")
                                    print(div2_element)
                                    if div2_element:
                
                                        time.sleep(10)
                                        ul_element = div2_element.find_element(By.XPATH,'/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div/div[1]/div[1]/div/ul')
                                        print(ul_element)
                                        if ul_element:
            
                                            # Find the <li> elements within the <ul> element
                                            li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
                                            print(len(li_elements))
                                            # print("xxxxxxxxxxxxx")

                                            for li_element in li_elements:
                                                # print(li_element)
                                                anchor_tags = li_element.find_elements(By.TAG_NAME,'a')
                                                print(len(anchor_tags))

                                                for anchor_tag in anchor_tags:
                                                    href = anchor_tag.get_attribute('href')
                                                    if href:
                                                        print(f"'{href}'")
                                                        links.append(href)
                                                        if "https://www.linkedin.com/in/" in href:
                                                            div_element = li_element.find_element(By.CLASS_NAME, 'feed-shared-social-actions')
                                                            print("div element found")
                                                            if div2_element:

                                                                # Step 2: Find the span with the class 'reactions-react-button feed-shared-social-action-bar__action-button' within the div
                                                                span_element = div_element.find_element(By.CSS_SELECTOR, 'span.reactions-react-button.feed-shared-social-action-bar__action-button')
                                                                if span_element:                                            
                                                                    print("span element found")

                                                                    # Step 3: Find the button within the span
                                                                    button_element = span_element.find_element(By.TAG_NAME, 'button')
                                                                    if button_element:

                                                                        print("button element found")

                                                                        # Step 4: Click the button
                                                                        # button_element.click()
                                                                        driver.execute_script("arguments[0].click();", button_element)
                                                                        print("button element clicked successfully")
                                                        break           
                                                        
                                                    print(len(links))
                                            if (len(links)>0):
                                                for link in links:
                                                    driver.get(link)
                                                    print(link)

                                                    if "https://www.linkedin.com/in/" in link:
                                                        print(" This is a personal LinkedIn profile")

                                            time.sleep(5)

                                            div1_element = driver.find_element(By.CLASS_NAME, 'pvs-profile-actions')
                                            if div1_element:
                                                print("div1_element------------", div1_element)
                                                # Assuming div1_element is your WebElement
                                                # class_attribute = div1_element.get_attribute("class")

                                                # # Split the class attribute into individual classes
                                                # classes_list = class_attribute.split()

                                                # # Print the list of classes
                                                # print(classes_list)
                                                

                                                div2_element = div1_element.find_element(By.CLASS_NAME, 'artdeco-dropdown artdeco-dropdown--placement-bottom artdeco-dropdown--justification-left ember-view')

                                                if div2_element:
                                                    print("div2 found")

                                                    button = div2_element.find_element(By.CLASS_NAME, 'artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view pvs-profile-actions__action artdeco-button artdeco-button--secondary artdeco-button--muted')

                                                    if button:
                                                        print("button found")


                                            # Find the button with a specific id
                                            # Find the "More" button by its aria-label attribute and class attribute
                                            # try:
                                            #     # Wait for the "More" button to be clickable
                                            #     wait = WebDriverWait(driver, 10)
                                            #     more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="More actions"]')))

                                            #     # Scroll to the element if needed
                                            #     driver.execute_script("arguments[0].scrollIntoView();", more_button)

                                            #     # Click the "More" button
                                            #     more_button.click()
                                            #     print("Button clicked successfully.")
                                            # except Exception as e:
                                            #     print(f"An error occurred: {e}")






                                        #     # Find the ul element inside div with class "artdeco-dropdown__content-inner"
                                        #     div_element = driver.find_element(By.CSS_SELECTOR, 'div.artdeco-dropdown__content-inner')

                                        #     # Now, find the ul element inside the previously found div
                                        #     ul_element = div_element.find_element(By.TAG_NAME, 'ul')

                                        #     # Extract all the li elements from the ul
                                        #     li_items= ul_element.find_elements(By.TAG_NAME,'li')

                                        #     print(len(li_items))

                                        #     # Loop through each <li> element and check its text content
                                        #     for li in li_items:
                                        #         print(li)
                                        #         # Find the <span> element within the <li> element
                                        #         span_element = li.find_element(By.TAG_NAME, 'span')
                                        #         print("span element found")



                                        #         if span_element:
                                        #             print("............")

                                        #             # Extract and print the text content of the <span> element
                                        #             button_text = span_element.text.strip()
                                        #             try:

                                        #                 print(button_text)                 
                                        #                 if button_text == "Connect":
                                        #                     button_element =li.find_element(By.TAG_NAME,'div')
                                        #                     button_element.click()
                                        #                     # Click the button in the <li> elementsoup = BeautifulSoup(html_content, 'html.parser')
                                        #                     # soup = BeautifulSoup(driver.page_source, 'html.parser')
                                        #                     # # Find the element by its attributes
                                        #                     # try:
                                                                
                                        #                     #     div_element = soup.find('div', class_='artdeco-dropdown__item artdeco-dropdown__item--is-dropdown ember-view full-width display-flex align-items-center')
                                        #                     #     print("/.,mnbvcxsdfrgtyhuiop;//////////////////////////")
                                                                
                                        #                         # # Click the <div> element (assuming it's clickable)
                                        #                         # div_element.click()
                                        #                         # print("Clicked the 'Connect' button.")
                                        #                         # time.sleep(5)

                                        #                         # soup = BeautifulSoup(driver.page_source, 'html.parser')

                                        #                         # send_button = soup.find_element(By.CLASS_NAME, 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1')
        
                                        #                         # # Click the button
                                        #                     #     # send_button.click()
                                        #                     # except Exception as e:
                                        #                     #     print(f"Error: {e}")
                                                                                            
                                        #                 else:
                                        #                     print(".......................")
                                        #                     continue
                                        #             except Exception as e:
                                        #                 print(e)


                                        else:
                                            print("not personal")
                                            continue



                    print("try")                                                
            


            except Exception as e:
                print(e)
       