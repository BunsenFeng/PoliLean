from models import zero_shot_stance, get_completion
import json

# set completion to a pre-selected response
with open('testing/response_chatgpt_website.txt') as f:
    completion = f.read()

# *** OR ***

# set text to the first item in /input/statements.json
# with open('input/statements.json') as json_file:
#     statements = json.load(json_file)
#     text = statements[0]

# model = 'gpt'
# print(model + "says: ")
# completion = get_completion(text, model)
# print(completion)

print(zero_shot_stance(completion))