from transformers import pipeline, AutoTokenizer
import argparse


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-m", "--model", help="the language model of interest on HuggingFace")
    argParser.add_argument("-d", "--device", default = -1, help="device ID, -1 for CPU, >=0 for GPU ID")

    args = argParser.parse_args()
    model = args.model
    device = int(args.device)

    generator = pipeline("text-generation", model = model, device = device, max_new_tokens = 100)
    result = generator("Do you want to build a snowman?")
    print(result[0]["generated_text"])
    print("success!")