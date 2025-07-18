# This is a Web based Speech to text function and this is the realtime stt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os 
from dotenv import load_dotenv

load_dotenv()

Output_File_Path = os.getenv("Output_File_Path")

# Setting up Chrome options with specific arguments
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")  # Remove this if you want to see the browser UI
# Manually set the path to the ChromeDriver executable

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# chrome_driver_path = "Speechtotext\\chromedriver.exe"
# service = Service(executable_path=chrome_driver_path)
# Setting up the Chrome driver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)
# Creating the URL for the website using the current working directory
website = "https://allorizenproject1.netlify.app/"
# Opening the website in the Chrome browser
driver.get(website)

def listen():
    try:
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("Listening...")
        output_text = ""
        is_second_click = False
        while True:
            output_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()
            if "Start Listening" in start_button.text and is_second_click:
                if output_text:
                    is_second_click = False
            elif "Listening..." in start_button.text:
                is_second_click = True
            if current_text != output_text:
                output_text = current_text
                with open(Output_File_Path, "w") as file:
                    file.write(output_text.lower())
                    print("User:", output_text)
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    listen()