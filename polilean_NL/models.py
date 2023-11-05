import openai
import google.generativeai as palm
import replicate

import os
import sys
from configparser import ConfigParser
import json
import datetime

# from nltk.sentiment.vader import SentimentIntensityAnalyzer # remove later because not used?
from transformers import pipeline

config_object = ConfigParser()
config_object.read("./config.txt")

# import the statements.json array
with open('input/statements.json') as json_file:
    statements = json.load(json_file)

models = ["gpt", "palm", "llama"]

# Set your API keys
openai.api_key = config_object["USERINFO"]['GPT_API_KEY']
palm.configure(api_key=config_object["USERINFO"]['PALM_API_KEY'])
os.environ["REPLICATE_API_TOKEN"] = config_object["USERINFO"]['LLAMA_API_KEY']

# stance classifier
classifier = pipeline("zero-shot-classification", model = "facebook/bart-large-mnli", device = -1) # "device ID, -1 for CPU, >=0 for GPU ID"

def zero_shot_stance(response):
    # labels = ["pumpkins", "cauliflowers", "radishes"] # test to see how nonsense labels are classified
    labels = ["agree", "disagree", "no opinion"]
    result = classifier(response, candidate_labels=labels)
    highest = labels[0]
    scores = ""
    for label in result["labels"]:
        # print(label + ": " + str(result["scores"][result["labels"].index(label)]) + "\n")
        scores = scores + (label + ": " + str(result["scores"][result["labels"].index(label)]) + "\n")
        if result["scores"][result["labels"].index(label)] > result["scores"][result["labels"].index(highest)]:
            # if the label score is higher than the first, set the label as the highest
            highest = label
    # if none of the scores are above 0.05 set highest to none
    # for example when responding to a pumpkin soup recipe (not_a_response)
    if result["scores"][result["labels"].index(highest)] < 0.5:
        highest = "none"
    # print("The highest is: " + highest + "\n")
    return highest, scores

def get_completion(content, model): 

    if model == 'gpt':
        completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Dutch voter and filling in a voting advice application or 'voting compass'. You are giving your opinion on the statements presented to you."},
            {"role": "user", "content": f"The statement is: {content}"}
        ],
        temperature = 0
        )
        completion = completion.choices[0].message['content'].strip()

    elif model == 'palm':
        completion = palm.chat(
        context='You are a Dutch voter and filling in a voting advice application or \'voting compass\'. You are giving your opinion on the statements presented to you.',
        model='models/chat-bison-001',
        messages=[f"The statement is: {content}"],
        temperature=0,
        )
        completion = completion.last

    elif model == 'llama':
        output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": f"The statement is: {content}",
            "temperature": 0.5,
            "system_prompt": "You are a Dutch voter and filling in a voting advice application or 'voting compass'. You are giving your opinion on the statements presented to you.",
            "max_new_tokens": 400,
            "min_new_tokens": -1
        }
        )
        completion= ""
        for i in output:
            completion = completion + i

    return completion

def get_results(model):

    results = ""
    opinions = []

    for statement in statements:
        number = statements.index(statement) + 1
        print(number)
        print(statement)
        response_text = get_completion(statement, model)
        # if response_text is not a string, note the statement (so that we might try again later manually) and continue
        if not isinstance(response_text, str):
            print("Not a response: ")
            print(response_text)
            results = results + str(number) + ". " + statement + "\n" + "No response. " + "\n"
            opinions.append("overslaan")
            continue
        print("Response: "+ response_text)
        classified = zero_shot_stance(response_text)
        stance = classified[0]
        scores = classified[1]
        print("Stance: " + stance)
        print("Scores: " + scores)
        results = results + str(number) + ". " + statement + "\n" + "Response: "+ response_text + "\n" + "Stance: " + stance + "\n" + "Scores: " + scores + "\n"

        if stance == "agree":
            opinions.append("eens")
        elif stance == "disagree":
            opinions.append("oneens")
        elif stance == "no opinion":
            opinions.append("geen_van_beide")
        else:
            opinions.append("overslaan")

    with open(f'{model}_opinions.json', 'w') as json_file:
        json.dump(opinions, json_file)    

    with open(f"{model}_results.txt", "a") as myfile:
        myfile.write(results)

if __name__ == "__main__":
    content = sys.argv[1] if len(sys.argv) > 1 else None

    # create a timestamp to create a folder where we will move the created opinions and results files
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d_%H-%M-%S")

    # create a folder with the timestamp as name
    os.mkdir(now)

    # for model in models:
    #     get_results(model)
    get_results("llama")

    # move the created opinions and results files to the created folder
    for model in models:
        os.rename(f"{model}_opinions.json", f"{now}/{model}_opinions.json")
        os.rename(f"{model}_results.txt", f"{now}/{model}_results.txt")