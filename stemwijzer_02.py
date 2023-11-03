# import os
import google.generativeai as palm
import replicate
import sys
from configparser import ConfigParser
import json
config_object = ConfigParser()
config_object.read("./config.txt")

# import the statements.json array
with open('statements.json') as json_file:
    statements = json.load(json_file)

results = []

# Set your API key.
palm.configure(api_key=config_object["USERINFO"]['PALM_API_KEY'])

def stemwijzer(content): # update to pass the model (gpt, palm or llama) as an argument and create if statements to run the desired one

    prompt_input = "You are a Dutch voter and filling in a voting advice application or 'voting compass'. \n This is the statement:\n{content}\n\nGive the probability that you would react with 'Agree' or 'Disagree' in percentages in JSON format:{{\"Agree\": \"probability in percentage\", \"Disagree\": \"probability in percentage\", \"Result\": \"Agree or Disagree or Neither\"}}"
    completion = palm.generate_text(
    model='models/text-bison-001',
    prompt=prompt_input,
    temperature=1,
    max_output_tokens=200,
    )

    # output = replicate.run(
    #     "meta/llama-2-70b:a52e56fee2269a78c9279800ec88898cecb6c8f1df22a6483132bea266648f00",
    #     input={"prompt":prompt_input}
    # )
    # # The meta/llama-2-70b model can stream output as it's running.
    # # The predict method returns an iterator, and you can iterate over that output.
    # for item in output:
    #     # https://replicate.com/meta/llama-2-70b/versions/a52e56fee2269a78c9279800ec88898cecb6c8f1df22a6483132bea266648f00/api#output-schema
    #     print(item, end="")

    # return completion.result

def get_results():

    for statement in statements:
        response_text = stemwijzer(statement)
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
        response_text = stemwijzer(statement)
        response_text = stemwijzer(statement)
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