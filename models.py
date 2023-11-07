import openai
import google.generativeai as palm
import replicate

import os
import sys
from configparser import ConfigParser
import json
import datetime
import time

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
    completion = "not a response"
    max_retries = 2  # Set the number of retries 

    # load model settings from JSON file
    with open('model_settings.json') as json_file:
        settings = json.load(json_file)
    
    model_settings = settings[model]
    
    for attempt in range(max_retries):
        try:
            if model == 'gpt':
                model_settings['messages'][1]['content'] = model_settings['messages'][1]['content'].format(content=content)
                response = openai.ChatCompletion.create(**model_settings)
                completion = response.choices[0].message['content'].strip()

            elif model == 'palm':
                model_settings['messages'][0] = model_settings['messages'][0].format(content=content)
                response = palm.chat(settings['palm'])
                completion = response.last

            elif model == 'llama':
                model_settings['input']['prompt'] = model_settings['input']['prompt'].format(content=content)
                response = replicate.run(model_settings['model_id'], input=model_settings['input'])
                completion = "".join(response)

            # If we got a completion, break out of the retry loop
            if completion != "not a response":
                break

        except (openai.error.OpenAIError, palm.PalmError, replicate.ReplicateError, httpx.RemoteProtocolError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait for a second before retrying or increase as needed
            continue  # Continue to the next attempt

    return completion

def get_results(model, runs = 1):
    # make a results text file for reading the results
    # also make a results csv file for data analysis
    # and save the opinions to a json for automating the stemwijzer (voting compass)

    opinions = ["overslaan"] * len(statements)
    cumulative_scores = {}

    # Write headers to the CSV file only once, not in append mode
    with open(f"{model}_results_of_{runs}.csv", "w") as results_csv_file:
        results_csv_file.write("run, model, statement, response, stance, agree, disagree, no opinion, none\n")

    with open(f"{model}_results_of_{runs}.csv", "a") as results_csv_file, \
     open(f"{model}_opinions_of_{runs}.json", "a") as json_file, \
     open(f"{model}_results_of_{runs}.txt", "a") as results_txt_file:

        for i in range(runs):
            print("Run " + str(i+1) + " of " + str(runs) + f" for model {model}")
            results_txt_file.write("Run " + str(i+1) + " of " + str(runs) + f" for model {model}\n")

            for statement in statements:
                number = statements.index(statement) + 1
                print(number)
                print(statement)
                response_text = get_completion(statement, model)

                # if response_text is not a string we didn't get a response. note the statement and continue
                if not isinstance(response_text, str):
                    print("Not a response: ")
                    print(response_text)
                    results_txt_file.write(str(number) + ". " + statement + "\nNo response.\n")
                    results_csv_file.write(f"{i+1}, {model}, {statement}, no response, , , , \n")
                    continue
                
                # print the response, classify it, and show the stance and label scores
                print("Response: " + response_text)
                classified = zero_shot_stance(response_text)
                stance = classified[0]
                scores = classified[1]
                print("Stance: " + stance)
                print("Scores: \n" + scores)
                results_txt_file.write(f"{number}. {statement}\nResponse: {response_text}\nStance: {stance}\nScores:\n{scores}\n")
                results_csv_file.write(f"{i+1}, {model}, {statement}, {response_text}, {stance}, {scores}\n")

                # if runs is not 1, do the following
                if runs != 1:
                    # turn the scores back into key value pairs of strings and floats
                    scores = scores.split("\n")
                    scores = scores[:-1]
                    scores = [score.split(": ") for score in scores]
                    scores = {score[0]: float(score[1]) for score in scores}

                    # during each run, add the scores to the previous scores and calculate the average
                    if len(cumulative_scores) == 0:
                        cumulative_scores = scores
                    else:
                        for key in cumulative_scores:
                            cumulative_scores[key] = cumulative_scores[key] + scores[key]
                        for key in cumulative_scores:
                            cumulative_scores[key] = cumulative_scores[key] / runs

                    # set stance to the highest score
                    stance = max(cumulative_scores, key=cumulative_scores.get)
                else:
                    pass
                
                # update the item in the opinions array to the stance
                if stance == "agree":
                    opinions[number-1] = "eens"
                elif stance == "disagree":
                    opinions[number-1] = "oneens"
                elif stance == "no opinion":
                    opinions[number-1] = "geen_van_beide"
                else: 
                    opinions[number-1] = "overslaan"

            # Flushing is not necessary every loop if performance is an issue, but should be done at the end of the function
            results_csv_file.flush()
            results_txt_file.flush()
            json_file.flush()
            
        # After processing all statements in one run, write opinions to the JSON file
        json_file.seek(0)  # Go to the start of the file
        json.dump(opinions, json_file)
        json_file.truncate()  # Truncate the file to the current position

if __name__ == "__main__":
    try:
        runs = int(sys.argv[1]) if len(sys.argv) > 1 else None
    except ValueError:
        print("Please provide a valid integer for the number of runs.")
        sys.exit(1)

    # create a timestamp to create a folder where we will move the created opinions and results files
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d_%H-%M-%S")

    # create a folder with the timestamp as name
    os.mkdir(now)

    # create a copy of the model settings json file (that was used for this experiment) to the experiment folder
    os.system(f"cp model_settings.json {now}/model_settings.json")

    for model in models:
        get_results(model, runs)

    # move the created opinions and results files to the created folder
    for model in models:
        os.rename(f"{model}_opinions_of_"+str(runs)+".json", f"{now}/{model}_opinions_of_"+str(runs)+".json")
        os.rename(f"{model}_results_of_"+str(runs)+".txt", f"{now}/{model}_results_of_"+str(runs)+".txt")
        os.rename(f"{model}_results_of_"+str(runs)+".csv", f"{now}/{model}_results_of_"+str(runs)+".csv")