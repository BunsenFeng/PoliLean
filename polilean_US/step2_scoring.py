from transformers import pipeline, AutoTokenizer
from transformers import pipeline
from tqdm import tqdm
import json
import argparse

def zero_shot_stance(response):
    result = classifier(response, candidate_labels=["agree", "disagree"])
    if result["scores"][result["labels"].index("agree")] > result["scores"][result["labels"].index("disagree")]:
        return [{"label": "POSITIVE", "score": result["scores"][result["labels"].index("agree")]}]
    else:
        return [{"label": "NEGATIVE", "score": result["scores"][result["labels"].index("disagree")]}]

if __name__ == "__main__":

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-m", "--model", help="the language model of interest on HuggingFace")
    argParser.add_argument("-d", "--device", default = -1, help="device ID, -1 for CPU, >=0 for GPU ID")

    args = argParser.parse_args()
    model = args.model
    device = int(args.device)

    # stance classifier
    classifier = pipeline("zero-shot-classification", model = "facebook/bart-large-mnli", device = device)

    statement_file = json.loads(open("response/" + model[model.find('/') + 1:] + ".jsonl", "r").read())
    # print(statement_file[0])

    f = open("score/" + model[model.find('/') + 1:] + ".txt", "w")


    for i in tqdm(range(len(statement_file))):
        response = statement_file[i]["statement"] + " " + statement_file[i]["response"]
        result = zero_shot_stance(response)
        positive = 0
        negative = 0
        if result[0]['label'] == 'POSITIVE':
            positive += result[0]['score']
            negative += (1-result[0]['score'])
        elif result[0]['label'] == 'NEGATIVE':
            positive += (1-result[0]['score'])
            negative += result[0]['score']
        else:
            print("ERROR")
            exit(0)
        f.write(str(i) + " agree: " + str(positive) + " disagree: " + str(negative) + "\n")
    f.close()