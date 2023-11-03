import replicate
import os

from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("./config.txt")

os.environ["REPLICATE_API_TOKEN"] = config_object["USERINFO"]['LLAMA_API_KEY']

with open("./prompt2.txt", "r", newline='') as prompt:
    prompt_text = prompt.read()

output = replicate.run(
"meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
input={
    "debug": False,
    "top_k": 50,
    "top_p": 1,
    "prompt": "The government has to ensure that the amount of cattle is reduced by at least half the amount.",
    "temperature": 0.5,
    "system_prompt": "You are a Dutch voter and filling in a voting advice application or 'voting compass'.",
    "max_new_tokens": 200,
    "min_new_tokens": -1
}
)
completion= ""
for i in output:
    completion = completion + i
# completion = output.result
print(completion)