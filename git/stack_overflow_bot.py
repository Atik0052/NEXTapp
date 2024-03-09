import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd


PATH = "D:\AISHA\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--headless")

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



with webdriver.Chrome(service=Service(PATH)) as driver:
    driver.get("https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f")

    time.sleep(3)
    email_element = driver.find_element(By.ID, 'email')
    password_element = driver.find_element(By.ID, 'password')

    email_element.send_keys('aishamc46@gmail.com')
    password_element.send_keys('U2opia@2023')

    WebDriverWait(driver, 10)

    time.sleep(10)


    # button_id = 'submit-button'
    login_button = driver.find_element(By.ID,'submit-button')
    login_button.click()

    time.sleep(10)

    with open("D:\AISHA\cpaas-tools\key.txt", "r") as file:
        keywords = file.read().splitlines()
        # data_to_save = []

        for keyword in keywords:
            try:
                
                print("keyword:", keyword)
                time.sleep(3)

                search_input = driver.find_element(By.CLASS_NAME, 's-input')
                search_input.clear()
                search_input.send_keys(Keys.CONTROL+'a')
                search_input.send_keys(Keys.BACKSPACE)
                search_input.click()


                search_input.send_keys(keyword)
                search_input.send_keys(Keys.ENTER)

                page_number = 1

                post_summaries = []  # Create an empty list to store post summaries

                while True:
                    WebDriverWait(driver, 10)                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    posts = soup.find_all('div', class_='s-post-summary js-post-summary')
                    post_summaries.extend(posts)  # Extend the list with new post summaries
                    break  # comment it  when the code bw=elow is uncommented
#..................To click next Button............................#
                    # try:
                    #     # Find the "Next" button for pagination
                    #     next_button = driver.find_element(By.LINK_TEXT, 'Next')
                    #     next_button.click()
                    # except NoSuchElementException:
                    #     # "Next" button is not available; exit the loop
                    #     break
#..................Uncomment for final ............................

                print(len(post_summaries))
                data_to_save = []
                for post_summary in post_summaries:
                    title_element = post_summary.find('a', class_='s-link')
                    title = None  # Initialize title with a default value

                    if title_element:
                        title = title_element.text
                        data_to_save.append({'Title': title})

                        link = title_element.get('href')
                        # data_to_save[-1]['Link'] = link

                        # Print the title and link
                        print('Title:', title)
                        print('Link:', link)


                        # Click the link
                        driver.get('https://stackoverflow.com' + link)
                        WebDriverWait(driver, 10)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        # Find the <p> element
                        p_element = soup.find('div', class_='s-prose js-post-body').find('p')

                        # Extract the text within the <p> element
                        p_text = p_element.get_text()
                        # print('Question:', p_text)
                        data_to_save[-1]['Question'] = p_text

                        

                        # print("...................................................")
                                            

                        if p_text:
                            print('Question:', p_text)

                            # Initialize conversation with ChatGPT
                            conversation = [
                                {"role": "system", "content": "You are AISHA, sales assistant for Message Central."},
                                ({"role": "user", "content": title + p_text  + "Answer in aspect of Message Central in 150 words, also use related hashtags of Message Central at the end"})
                            ]

                            # Send user question to ChatGPT and get the bot's response
                            chatbot = "gpt-3.5-turbo"  # Example chatbot name #fine tuned model name
                            temperature = 0.7
                            frequency_penalty = 0.0
                            presence_penalty = 0.0

                            bot_response = chat_with_bot(conversation, chatbot, temperature, frequency_penalty, presence_penalty)
                            
                            try:
                                # Find the question text element
                                textarea = driver.find_element(By.ID,"wmd-input")
                            

                                # print("..............")

                                # Clear any existing text in the textarea
                                textarea.clear()


                                # Paste your bot's response into the textarea
                                textarea.send_keys(bot_response)
                                print(bot_response)

                                # print("...........................")

                                try:
                                    alert = driver.switch_to.alert
                                    alert_text = alert.text
                                    if alert_text:
                                        alert.accept()
                                        print("Alert Text:", alert_text)
                                except Exception:
                                    print("No alert found:")
        
                                # # Send "Ctrl + A" key combination to select all text within the element
                                # textarea.send_keys(Keys.COMMAND + 'a')

                                # #For window 
                                # # content_element.send_keys(Keys.CONTROL + 'a')

                                # # Send the "Delete" key to delete the selected text
                                # textarea.send_keys(Keys.DELETE)
                                # print("content deleted")

                                # Set the text content of the wmd-preview element to the bot response
                                driver.execute_script("try { arguments[0].innerText = arguments[1]; } catch(e) { console.error('JS Error:', e); }", textarea, bot_response)


                                edited_content = ''
                                edit = input("Do you want to edit this answer? (Y/N): ")
                                if edit.lower() =='y':
                                    input("Press enter when you've done editing!...")
                                    edited_content = textarea.text

                                    print(f"Answer:{edited_content}")
                                    
                                else:
                                    print("you don't want to edit")
                                    conversation.append({"role": "assistant", "content": bot_response})
                                    print(f"Answer: {bot_response}")

                                # Ask the user for input
                                user_input = input("Do you want to post this? (Y/N): ")

                                # Check if the user input is 'Y' (case-insensitive)
                                if user_input.lower() == 'y':
                                    # Locate the "Post" button and click it
                                    post_button = driver.find_element(By.ID, 'submit-button')

                                    if post_button:
                                        post_button.click()
                                        print("Question posted successfully!")
                                        if edited_content:
                                            # Update the conversation history
                                            conversation.append({"role": "assistant", "content": edited_content})
                                            print("appended the edited content")
                                            data_to_save[1]['Answer'] = edited_content
                                        else:
                                            # Update the conversation history
                                            conversation.append({"role": "assistant", "content": bot_response})
                                            print("appended the bot response")
                                            data_to_save[1]['Answer'] = bot_response
                                    else:
                                        print("Post button not found.")
                                else:
                                    print("Posting canceled.")
                                    textarea.send_keys(Keys.CONTROL + 'a')
                                    # textarea.send_keys(Keys.CONTROL + 'a')
                                    textarea.send_keys(Keys.BACKSPACE)
                                    try:
                                        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
                                        # Once the alert is present, get its text
                                        alert_text = alert.text

                                        if alert_text:
                                            # Accept the alert if there is text and print it
                                            alert.accept()
                                            print("Alert Text:", alert_text)
                                    except Exception:
                                        print("No alert found:")
                                continue

                                # print(".....................................................")
                            except Exception as e:
                                print("answer section not available")
                                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

            except Exception as e:

                



                # Create a DataFrame from the collected data
                df = pd.DataFrame(data_to_save)

                # Save the DataFrame to an Excel file
                df.to_excel(f"{keyword}.xlsx", index=False)
                print(f"excel file saved successfully as {keyword}.xlsx")
                        

            except Exception as e:                                                                                                                                                                                                                                                                                                                              
                print(e)