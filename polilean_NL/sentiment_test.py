from models import analyze_sentiment

# import /input/response1.txt as text
with open('input/response1.txt') as f:
    text = f.read()

print(analyze_sentiment(text))