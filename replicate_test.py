import replicate

with open("./prompt2.txt", "r", newline='') as prompt:
    prompt_text = prompt.read()

output = replicate.run(
    "meta/llama-2-70b:a52e56fee2269a78c9279800ec88898cecb6c8f1df22a6483132bea266648f00",
    input={"prompt":prompt_text}
)
# The meta/llama-2-70b model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/meta/llama-2-70b/versions/a52e56fee2269a78c9279800ec88898cecb6c8f1df22a6483132bea266648f00/api#output-schema
    print(item, end="")