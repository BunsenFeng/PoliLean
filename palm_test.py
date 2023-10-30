# python script.py
import os
# import openai
import pprint
import google.generativeai as palm

from configparser import ConfigParser
config_object = ConfigParser()
config_object.read("./config.txt")
palm.configure(api_key=config_object["USERINFO"]['PALM_API_KEY'])

with open("./prompt2.txt", "r", newline='') as prompt:
    prompt_text = prompt.read()
completion = palm.generate_text(
    model='models/text-bison-001',
    prompt=prompt_text,
    temperature=0,
    # The maximum length of the response
    max_output_tokens=800,
)
print(completion.result)
# print(prompt_text)

# completion = palm.generate_text(
#     model='models/text-bison-001',
#     prompt="Tell me a joke.",
#     temperature=0,
#     # The maximum length of the response
#     max_output_tokens=800,
# )
# print(completion.result)

# models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
# model = models[0].name
# print(model)