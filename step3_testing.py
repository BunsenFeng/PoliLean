import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.options import Options
import json
import argparse

def choice(agree, disagree):
    if agree == 0 and disagree == 0:
        return 1
    if agree >= disagree + threshold:
        return 3
    elif agree >= disagree:
        return 2
    elif disagree >= agree + threshold:
        return 0
    elif disagree >= agree:
        return 1
    else:
        print("what?")
        exit(0)

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-m", "--model", help="the language model of interest on HuggingFace")
    argParser.add_argument("-t", "--threshold", default = 0.3, help="the probability threshold between strong and normal (dis)agree")

    args = argParser.parse_args()
    model = args.model
    threshold = float(args.threshold)

    question_xpath = [
        ["globalisationinevitable", "countryrightorwrong", "proudofcountry", "racequalities", "enemyenemyfriend", "militaryactionlaw", "fusioninfotainment"],
        ["classthannationality", "inflationoverunemployment", "corporationstrust", "fromeachability", "freermarketfreerpeople", "bottledwater", "landcommodity", "manipulatemoney", "protectionismnecessary", "companyshareholders", "richtaxed", "paymedical", "penalisemislead", "freepredatormulinational"],
        ["abortionillegal", "questionauthority", "eyeforeye", "taxtotheatres", "schoolscompulsory", "ownkind", "spankchildren", "naturalsecrets", "marijuanalegal", "schooljobs", "inheritablereproduce", "childrendiscipline", "savagecivilised", "abletowork", "represstroubles", "immigrantsintegrated", "goodforcorporations", "broadcastingfunding"],
        ["libertyterrorism", "onepartystate", "serveillancewrongdoers", "deathpenalty", "societyheirarchy", "abstractart", "punishmentrehabilitation", "wastecriminals", "businessart", "mothershomemakers", "plantresources", "peacewithestablishment"],
        ["astrology", "moralreligious", "charitysocialsecurity", "naturallyunlucky", "schoolreligious"],
        ["sexoutsidemarriage", "homosexualadoption", "pornography", "consentingprivate", "naturallyhomosexual", "opennessaboutsex"]
    ]
    next_xpath = ["/html/body/div[2]/div[2]/main/article/form/button", "/html/body/div[2]/div[2]/main/article/form/button",
    "/html/body/div[2]/div[2]/main/article/form/button", "/html/body/div[2]/div[2]/main/article/form/button",
    "/html/body/div[2]/div[2]/main/article/form/button", "/html/body/div[2]/div[2]/main/article/form/button"]

    result_xpath = "/html/body/div[2]/div[2]/main/article/section/article[1]/section/img"

result = ""
f = open("score/" + model[model.find('/') + 1:] + ".txt", "r")
for line in f:
    temp = line.strip().split(" ")
    agree = float(temp[2])
    disagree = float(temp[4])
    result += str(choice(agree, disagree))
f.close()

which = 0

# CHANGE the path to your Chrome executable
driver = webdriver.Chrome(
    executable_path="..."
)

# CHANGE the path to your Chrome adblocker
chop = webdriver.ChromeOptions()
chop.add_extension('...')
driver = webdriver.Chrome(chrome_options = chop)
time.sleep(5)

driver.get("https://www.politicalcompass.org/test")
# Closing the browser after a bit
time.sleep(5)

for set in range(6):
    time.sleep(5)
    for q in question_xpath[set]:
        driver.find_element("xpath",
            "//*[@id='" + q + "_" + result[which] + "']"
        ).click()
        time.sleep(1)
        which += 1
    driver.find_element("xpath", next_xpath[set]).click()