# views.py

import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from django.http import JsonResponse

# Load necessary files
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('models/chatbot_features/intents.json').read())
words = pickle.load(open('models/chatbot_features/words.pkl', 'rb'))
classes = pickle.load(open('models/chatbot_features/classes.pkl', 'rb'))
model = load_model('models/chatbot_features/chatbot_model.h5')

# Function to clean up sentence
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Function to convert sentence to bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Function to predict class/category
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    return category

# Function to get response
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for intent in list_of_intents:
        if intent['tag'] == tag:
            result = random.choice(intent['responses'])
            break
    return result

# while True:
#     message=input("")
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     print(res)

# Django view function for chatbot
def chatbot(request):
    if request.method == 'POST':
        # Get input text from request
        message = request.POST.get('message', '')

        # Predict class
        intent = predict_class(message)

        # Get response
        response_text = get_response(intent, intents)

        # Return JSON response
        return JsonResponse({'response': response_text})
    else:
        # Handle GET requests
        message = 'This is the chatbot endpoint. Send a POST request with your message to get a response.'
        return JsonResponse({'message': message})