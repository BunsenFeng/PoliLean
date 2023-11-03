import openai
import google.generativeai as palm
import replicate

import os
import sys
from configparser import ConfigParser
import json

from nltk.sentiment.vader import SentimentIntensityAnalyzer

config_object = ConfigParser()
config_object.read("./config.txt")

# import the statements.json array
with open('statements.json') as json_file:
    statements = json.load(json_file)

results = []

# Set your API keys
openai.api_key = config_object["USERINFO"]['GPT_API_KEY']
palm.configure(api_key=config_object["USERINFO"]['PALM_API_KEY'])
os.environ["REPLICATE_API_TOKEN"] = config_object["USERINFO"]['LLAMA_API_KEY']

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return 'eens'
    elif scores['compound'] <= -0.05:
        return 'oneens'
    else:
        return 'geen_van_beide'

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
        completion.choices[0].message['content'].strip()

    elif model == 'palm':
        completion = palm.chat(
        context='You are a Dutch voter and filling in a voting advice application or \'voting compass\'. You are giving your opinion on the statements presented to you.',
        model='models/chat-bison-001',
        messages=[f"The statement is: {content}"],
        temperature=0,
        )
        print(completion.last)

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
            "max_new_tokens": 200,
            "min_new_tokens": -1
        }
        )
        completion= ""
        for i in output:
            completion = completion + i

    return completion

def get_results():

    for statement in statements:
        response_text = get_completion(statement)
        # get the json response from the response text that is enclosed between { and }
        response_text = response_text[response_text.find("{"):response_text.find("}")+1]
        # and parse it to a dictionary
        response_text = eval(response_text)
        # if the results is Agree, add "eens" to the array, if Disagree then "oneens", if Neither then "geen_van_beide", if there is no such result then "overslaan"
        if response_text["Result"] == "Agree":
            results.append("eens")
        elif response_text["Result"] == "Disagree":
            results.append("oneens")
        elif response_text["Result"] == "Neither":
            results.append("geen_van_beide")
        else:
            results.append("overslaan")
        print(results)
    
    return results

if __name__ == "__main__":
    content = sys.argv[1] if len(sys.argv) > 1 else None

    i = 0
    for statement in statements:
        i = i + 1
        print(i)
        print(statement)
        response_text = get_completion(statement)
        # get the json response from the response text that is enclosed between { and }
        response_text = response_text[response_text.find("{"):response_text.find("}")+1]
        # and parse it to a dictionary
        response_text = eval(response_text)
        print(response_text)
        # save the number, statement and response to a text file
        with open("stemwijzer_results.txt", "a") as myfile:
            myfile.write(str(i) + "\n")
            myfile.write(statement + "\n")
            myfile.write(str(response_text) + "\n")
            myfile.write("\n")