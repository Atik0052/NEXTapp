import openai
# print(dir(openai))
from selenium import webdriver
# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import openpyxl


def chat_with_bot(conversation, chatbot, temperature, frequency_penalty, presence_penalty):
    # Copy the conversation and insert a system message with the chatbot's role
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": chatbot}]
    messages_input.insert(0, prompt[0])

    # Create a chat completion using the OpenAI API
    model_name = "ft:gpt-3.5-turbo-0613:u2opia-mobile::8FfEVapC"  # Replace with the actual model name
    completion = openai.ChatCompletion.create(
        model=model_name,
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input
    )

    # Get the response from the chatbot
    chat_response = completion['choices'][0]['message']['content']

    # Append the chatbot's response to the conversation
    # conversation.append({"role": "assistant", "content": chat_response})

    return chat_response



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
    driver.get("https://www.quora.com/")

    # Apply filters here using Selenium as needed
    # For example, you can interact with filter elements on the webpage

    time.sleep(3)
    email_element = driver.find_element(By.ID, 'email')
    password_element = driver.find_element(By.ID, 'password')

    email_element.send_keys('aishamc46@gmail.com')
    password_element.send_keys('U2opia@2023')

    wait = WebDriverWait(driver, 10)

    # Find the "recaptcha-checkbox-border" element using its CSS selector
    # checkbox = driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-border")

    # Click the element
    # checkbox.click()


    wait = WebDriverWait(driver, 500)

    # Wait until the login button becomes clickable
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login')]")))

    # Use JavaScript to click the button, even if it's disabled
    driver.execute_script("arguments[0].click();", login_button)
    # start = driver.current_url




    # Read keywords from the "key.txt" file
    with open("D:\AISHA\cpaas-tools\key.txt", "r") as file:
        keywords = file.read().splitlines()

    # Set up your web driver and navigate to Quora
    # (Assuming you've already set up your driver as shown in your previous code)

    for keyword in keywords:
        try:
            print("keyword:",keyword)
            # Specify the Excel file name (change it as needed)
            excel_file_name = f'{keyword}.xlsx'

            # driver.get(start)
            # Locate the search input element
            time.sleep(3)
            search_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search Quora"]')
            # Clear the input field using JavaScript

            search_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search Quora"]')
            # search_input.clear()
            # Clear the search input field using JavaScript
            # driver.execute_script("arguments[0].value = '';", search_input)
            search_input.send_keys(Keys.CONTROL+'a')
            search_input.send_keys(Keys.BACKSPACE)

            WebDriverWait(driver, 10)

            # Send the keyword to the cleared search input field
            search_input.send_keys(keyword)

            # Simulate pressing the Enter key to submit the search
            search_input.send_keys(Keys.ENTER)

            WebDriverWait(driver, 5)

            # Submit the form using JavaScript
            # driver.execute_script("arguments[0].form.submit();", search_input)
            # Wait for the search result element to become visible (adjust selector as needed)
            # WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.search-result')))
    

            # Wait for the search results to load (you can adjust the timeout)
            WebDriverWait(driver, 10)
            # Find the element with the text "Past week" and click it
            # past_week_element = driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[6]/div[4]")
            # question = driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[2]/div[2]")
            past_year_element = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[6]/div[6]')
            # to enable past week data extraction only, uncomment below line
            past_year_element.click()
            # question.click()
            # past_month_element.click()

            # WebDriverWait(driver, 10)

#During final hosting, uncomment this
# ......................................................................

            # search_results = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.search_results')))
            #print("n") 


            start_time = time.time()  # Record the start time

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll down to the bottom
                time.sleep(3)  # Wait for 3 seconds

                # Check if 30 seconds have elapsed
                if time.time() - start_time > 30:
                    break  # Exit the loop after 30 seconds

#..........................................................................
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            spans = soup.find_all('span', class_='q-text qu-dynamicFontSize--regular qu-color--blue_dark qu-bold')

            time.sleep(5)
            links = []
            for span in spans:
                a_tag = span.find('a', class_='q-box Link___StyledBox-t2xg9c-0 dFkjrQ puppeteer_test_link qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline')
                if a_tag:
                    href = a_tag.get('href')
                    links.append(href)

            for link in links:
                driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                span_element = soup.find('span', class_='q-box qu-userSelect--text')

                if span_element:
                    text = span_element.get_text(strip=True)
                    texts.append(text)
                    # data['text'].append(text)

                parent_element = driver.find_element(By.CLASS_NAME, "q-box.qu-zIndex--action_bar")

                # Step 2: Find the button element within the parent element
                button_element = parent_element.find_element(By.CSS_SELECTOR, 'button.q-click-wrapper')

                # Step 3: Check the button's text
                button_text_element = button_element.find_element(By.CSS_SELECTOR, 'div.q-text.qu-display--inline-flex.qu-alignItems--center.qu-overflow--hidden.puppeteer_test_button_text.qu-medium.qu-color--gray.qu-ml--tiny')
                button_text = button_text_element.text

                print(f"Question: {text}")

                if button_text == "Answer":
                    button_element.click()
                    print("answer button clicked")
                elif button_text == "Edit draft":
                    button_element.click()
                    print("Edit draft button clicked")
                else:
                    print("Already answered!")
                    continue




                time.sleep(2)

                # Initialize conversation with ChatGPT
                conversation = [
                    {"role": "system", "content": "You are AISHA, sales assistant for Message Central."},
                    ({"role": "user", "content": text })
                ]

                # Send user question to ChatGPT and get the bot's response
                chatbot = "ft:gpt-3.5-turbo-0613:u2opia-mobile::82igfK9W"  # Example chatbot name #fine tuned model name
                temperature = 0.7
                frequency_penalty = 0.0
                presence_penalty = 0.0

                bot_response = chat_with_bot(conversation, chatbot, temperature, frequency_penalty, presence_penalty)
                print("bot response")

                # print(f"Answer: {bot_response}")

                # Wait for the <div class="doc empty"> element to become visible

                wait = WebDriverWait(driver, 20)
                
                try:
                    # Attempt to locate the doc_element using the first CSS selector
                    doc_element = driver.find_element(By.CSS_SELECTOR, 'div[data-placeholder="Write your answer"][data-kind="doc"]')
                except:
                    print("doc1 not found")
                    try:
                        # If the first selector fails, attempt to locate the doc_element using the second CSS selector
                        doc_element = driver.find_element(By.CSS_SELECTOR, 'div[data-kind="doc"]')
                    except:
                        # Handle the case where neither selector works
                        print("Unable to locate the 'doc_element' element.")

                wait = WebDriverWait(driver, 10)

                print("..........................................")
                if doc_element:
                    
                    # print("doc_element")
                    # Locate the <div class="content"> element within the <div class="doc empty"> element
                    content_editable_div = driver.find_element(By.CSS_SELECTOR, 'div[data-placeholder="Write your answer"][contenteditable="true"]')
                

                    if content_editable_div:
                        # print("content entered")

                        content_editable_div.click()
                
                        # content_element.click()
                        # print("content clicked")


                        # Send "Ctrl + A" key combination to select all text within the element
                        # content_editable_div.send_keys(Keys.COMMAND + 'a')

                        #For window 
                        content_editable_div.send_keys(Keys.CONTROL + 'a')

                        # Send the "Delete" key to delete the selected text
                        content_editable_div.send_keys(Keys.BACKSPACE)
                        # print("content deleted")

                        # Set the text content of the <div class="content"> element to the bot's response
                        driver.execute_script("arguments[0].textContent = arguments[1];", content_editable_div, bot_response)
                        # print("response added")


                    # You can adjust the sleep duration if needed
                    time.sleep(2)  # Wait for a moment to ensure the content is updated
                    edited_content = ''
                    edit = input("Do you want to edit this answer? (Y/N): ")
                    data["Question"].append(text)
                    if edit.lower() =='y':
                        input("Press enter when you've done editing!...")

                        edited_content = content_editable_div.text
                        # Update the conversation history
                        # conversation.append({"role": "assistant", "content": edited_content})
                        print(f"Answer:{edited_content}")
                        
                    else:
                        print("you don't want to edit")
                        # conversation.append({"role": "assistant", "content": bot_response})
                        print(f"Answer: {bot_response}")
                       
                    # Ask the user for input
                    user_input = input("Do you want to post this? (Y/N): ")
                    # data["Answer"].append(edited_content)

                    # existing_workbook = openpyxl.load_workbook(excel_file_name)
                    # existing_worksheet = existing_workbook.active

                    # Check if the user input is 'Y' (case-insensitive)
                    if user_input.lower() == 'y':
                        # Locate the "Post" button and click it
                        post_button = driver.find_element(By.CSS_SELECTOR, 'button.puppeteer_test_modal_submit')
                        if post_button:
                            post_button.click()
                            print("Posted successfully!")
                            # existing_workbook.append(['Question',text])
                            # data["Question"].append(text)
                            if edited_content:
                                # Update the conversation history
                                conversation.append({"role": "assistant", "content": edited_content})
                                print("appended the edited content")
                                # existing_worksheet.append(['Answer', edited_content])\
                                continue
                            else:
                                # Update the conversation history
                                conversation.append({"role": "assistant", "content": bot_response})
                                print("appended the bot response")

                                continue
                                # existing_worksheet.append(['Answer', bot_response])
                                # existing_workbook.save(excel_file_name)
                            
                        else:
                            print("Post button not found.")
                            continue
                    else:
                        print("Posting canceled.")
                        content_editable_div.send_keys(Keys.CONTROL + 'a')
                        content_editable_div.send_keys(Keys.BACKSPACE)
                        continue
                    print(".....................................................")
                    # save_to_excel = input("Do you want this answer to save to be saved in excel sheet")

        except Exception as e:
            print(e)
            print("........................................exception.....................................................")
