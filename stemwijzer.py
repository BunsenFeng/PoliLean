from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
# from models import get_results, get_completion
import json

# import the statements.json array
# with open('input/statements.json') as json_file:
#     statements = json.load(json_file)

models = ["gpt", "palm", "llama"]

def take_stemwijzer(web_driver, model):
    
    def findclickandwait(element):
        web_driver.find_element(by=By.CSS_SELECTOR, value=element).click()
        time.sleep(1.5) # wait for the next page to load
    
    # close the privacy statement
    findclickandwait(".privacy__close")

    # ***
    # the following code piece would take the statements directly from the website, but it would be prone to errors
    # in our use case we are sure of the statements that we want to process
    # it could be a way to scrape statements for the next election
    # ***
    # # for thirty repeats / statements
    # for i in range(30):
    #     # get the statement text from the title element
    #     title = web_driver.find_element(by=By.CSS_SELECTOR, value=".statement-title").text
    #     print(title)
    #     response_text = stemwijzer(title)

    #     *** this piece of code assumed that we would ask the model directly for their probability of agreeing or disagreeing
    #     # get the json response from the response text that is enclosed between { and }
    #     response_text = response_text[response_text.find("{"):response_text.find("}")+1]
    #     # and parse it to a dictionary
    #     response_text = eval(response_text)
    #     print(response_text["Result"])
    #     ***

    #     if response_text["Result"] == "Agree":
    #         findclickandwait(".statement__buttons-main > .button--agree") 
    #     elif response_text["Result"] == "Disagree":
    #         findclickandwait(".statement__button:nth-child(2)")
    #     elif response_text["Result"] == "Neither":
    #         findclickandwait(".statement__button:nth-child(3)")
    #     else:
    #         findclickandwait(".statement__buttons > .statement__skip")

    # ***
    # creating a responses array with only 'eens' for testing
    # responses = ["eens"] * 30
    # ***

    with open(f'{model}_opinions_of_10.json') as json_file:
        responses = json.load(json_file)
    
    for response in responses:
        if response == "eens":
            findclickandwait(".statement__buttons-main > .button--agree") 
        elif response == "oneens":
            findclickandwait(".statement__button:nth-child(2)") 
        elif response == "geen_van_beide":
            findclickandwait(".statement__button:nth-child(3)")
        elif response == "overslaan":
            findclickandwait(".statement__buttons > .statement__skip")
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

    try:
        findclickandwait(".shootout__close") # sluit de eventuele vraag voor extra stellingen
        print("geen extra stellingen")
    except:
        pass

    # Get the results from the page and store them in a text file
    # Locate the buttons
    buttons = web_driver.find_elements(by=By.XPATH, value='//button[@aria-label]')
    # print("the buttons are:")
    # print(buttons)

    # Extract information
    party_info = []
    for button in buttons:
        label = button.get_attribute('aria-label')
        party_info.append(label)
    
    party_info = party_info[4:-1] # remove the first 4 and last 1 lines (they're not the main list of results)
    # print("the party_info is:")
    # print(party_info)
    
    # Export to text file
    with open(f'{model}_leans.txt', 'w') as file:
            for info in party_info:
                file.write(f"{info}\n")

    return party_info

# Main Script
if __name__ == '__main__':

    for model in models:

        try:
            print("Connecting to ChromeDriver")
            driver = webdriver.Chrome()
            driver.implicitly_wait(1.0)

            print("Connecting to dummy site")
            driver.get("https://tweedekamer2023.stemwijzer.nl/#/stelling/1/de-regering-moet-ervoor-zorgen-dat-de-hoeveelheid-vee-minstens-de-helft-kleiner-wordt")
            time.sleep(2)

            party_info = take_stemwijzer(driver, model)
            print("The LLM leans towards:", party_info)

        except Exception as e:
            # Change: Use proper exception handling!
            print(e)

        finally:
            print("Closing ChromeDriver")
            driver.close()