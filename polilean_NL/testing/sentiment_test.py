from models import analyze_sentiment

# import /input/response1.txt as text
with open('testing/response_palm_api.txt') as f:
    text = f.read()

print(analyze_sentiment(text))

# this results in a false negative because the model agrees with the statement but the topic is about the negative effects of cattle