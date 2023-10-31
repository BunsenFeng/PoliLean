from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def take_stemwijzer(web_driver):
    
    def findclickandwait(element):
        web_driver.find_element(by=By.CSS_SELECTOR, value=element).click()
        time.sleep(2) # wait for the next page to load
    
    # create a responses array with only 'eens' for testing
    responses = ["eens"] * 30

    # responses = stemwijzer()
    for response in responses:
        if response == "eens":
            findclickandwait(".statement__buttons-main > .button--agree") 
        elif response == "oneens":
            findclickandwait(".statement__button:nth-child(2)") 
        elif response == "geen_van_beide":
            findclickandwait(".statement__button:nth-child(3)")
        else:
            raise Exception("Invalid response")

    # Finish final steps

    findclickandwait(".options-header__next")
    print("volgende stap, geen onderwerpen extra belangrijk kiezen")

    findclickandwait(".radio:nth-child(1)")
    print("alle partijen meenemen")

    findclickandwait(".options-header__next") 
    print("volgende stap")

    try:
        findclickandwait(".select-analytics__button")
        print("antwoorden op vraag over data delen") 
        # soms niet aanwezig als je al voorkeur hebt aangegeven en deze cookie blijft opgeslagen
    except:
        findclickandwait(".options-header__next") 
        print("naar resultaat")

    # Get the results from the page and store them in a text file
    # Locate the buttons
    buttons = web_driver.find_elements(by=By.XPATH, value='//button[@aria-label]')

    # Extract information
    party_info = []
    for button in buttons:
        label = button.get_attribute('aria-label')
        party_info.append(label)

    # Export to text file
    with open('party_info.txt', 'w') as file:
        for info in party_info:
            file.write(f"{info}\n")

    # Close the WebDriver instance
    driver.quit()

    return party_info

# Main Script
if __name__ == '__main__':

    try:
        print("Connecting to ChromeDriver")
        driver = webdriver.Chrome()
        driver.implicitly_wait(1.0)

        print("Connecting to dummy site")
        driver.get("https://tweedekamer2023.stemwijzer.nl/#/stelling/1/de-regering-moet-ervoor-zorgen-dat-de-hoeveelheid-vee-minstens-de-helft-kleiner-wordt")
        time.sleep(2)

        party_info = take_stemwijzer(driver)
        print("The LLM leans towards:", party_info)

    except Exception as e:
        # DO NOT DO THIS. Use proper exception handling!
        print(e)

    finally:
        print("Closing ChromeDriver")
        driver.close()