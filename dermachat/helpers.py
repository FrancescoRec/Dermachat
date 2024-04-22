import json
import numpy as np
import pandas as pd
import nltk
import random
import pickle
import uuid
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import random
import re



non_diagnosis_responses = ['I cannot give you a possible diagnosis','Please, try it again','Please, give me more details','I do not understand what you mean']


def bayesian_classifier(adj_mat, symptom_list, symptoms, diseases):
    
    # Use re.sub() to remove the special characters from each symptom in the symptom_list
    cleaned_symptom_list = [re.sub(r'[:;¿?¡!-]', '', s).strip().lower() for s in symptom_list]

    # Convert the cleaned symptom list to indices, assuming the symptoms are found in the cleaned list
    sym = [symptoms.index(s) for s in cleaned_symptom_list if s in symptoms]

    p_dis = adj_mat.sum(axis=0) / adj_mat.sum()
    p_sym = adj_mat.sum(axis=1) / adj_mat.sum()
    dist = []

    for i in range(len(diseases)):
        # computing the bayes probability
        prob = np.prod((adj_mat[:,i] / adj_mat[:,i].sum())[sym]) * p_dis[i] / np.prod(p_sym[sym])
        dist.append(prob)
    
    if sum(dist) == 0:
        return non_diagnosis_responses[random.randrange(4)]
    else:
        idx = dist.index(max(dist))
        return diseases[idx]


# Load data
def load_data():
    df = pd.read_excel('models/chatbot/symptoms.xlsx')
    # Replace whitespaces and '_' with spaces
    for col in df.columns:
        if 'Symptom' in col:
            df[col] = df[col].str.replace(' ', '').str.replace('_', ' ')
    symptom_freqs = df.iloc[:, 1:].stack().value_counts()
    symptom_freqs = pd.DataFrame(symptom_freqs)
    symptom_freqs.index.name = 'Symptom'
    symptom_freqs = symptom_freqs.reset_index()
    symptom_freqs = symptom_freqs.rename(columns={'count': 'frequency'})

    symptoms = list(symptom_freqs['Symptom'].unique())
    diseases = list(df['Disease'].unique())

    adj_mat = np.zeros((len(symptoms), len(diseases)))
    for i in range(len(df)):
        for j in range(1, 18):  # Assuming 17 symptoms columns max
            disease = df.iloc[i, 0]
            symptom = df.iloc[i, j]
            if pd.notnull(symptom):
                symptom = symptom.strip()  # Strip leading and trailing whitespace
                dis_index = diseases.index(disease)
                sym_index = symptoms.index(symptom)
                adj_mat[sym_index, dis_index] += 1

    return symptoms, diseases, adj_mat

# Load descriptions and precautions
def load_descriptions():
    df_desc = pd.read_excel('models/chatbot/symptoms.xlsx', sheet_name='symptom_Description')
    return df_desc

def load_precautions():
    df_prec = pd.read_excel('models/chatbot/symptoms.xlsx', sheet_name='symptom_precaution')
    return df_prec

def print_precautions(disease, df_prec):
    # Normalize the case for comparison
    disease = disease.lower()
    # Filter the dataframe for the matching disease
    matching_precautions = df_prec[df_prec['Disease'].str.lower() == disease]
    # Check if there are any matches
    if not matching_precautions.empty:
        precautions = matching_precautions.iloc[0]
        print('Recommended precautions:')
        for i in range(1, 5):
            if pd.notnull(precautions[f'Precaution_{i}']):
                print(f"- {precautions[f'Precaution_{i}']}")
    else:
        print('No precautions available for this disease.')

def print_description(disease, df_desc):
    desc = df_desc['Disease'].str.lower() == disease.lower()
    if desc.any():
        description = df_desc.loc[desc, 'Description'].iloc[0]
        print(f'{description}')
    else:
        print('No description available for this disease.')

# Initialize lemmatizer, load data, and models
with open('models/chatbot/intents.json', 'r') as file:
    intents_json = json.load(file)

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('models/chatbot/intents.json').read())
words = pickle.load(open('models/naives-bayes/words.pkl', 'rb'))
classes = pickle.load(open('models/naives-bayes/classes.pkl', 'rb'))
model = load_model('models/llm-chatbot/chatbot_model.h5')

# Clean up the sentence
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predict class
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    return category

# Get response
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])
            break
    return result

# Process symptoms
# In helpers.py

def process_symptoms(selected_symptoms):
    # Generate a string from the list of selected symptoms
    user_symptoms_input = ', '.join(selected_symptoms)

    # Ensure only valid symptoms are processed
    user_symptoms = [sym.strip() for sym in selected_symptoms if sym.strip() in symptoms]

    if not user_symptoms:
        # If no valid symptoms are provided, respond with a prompt for more information
        add_to_conversation("Bot", "Please provide your symptoms for a diagnosis.")
    else:
        # Generate diagnosis from valid symptoms
        if user_symptoms:
            diagnosis = bayesian_classifier(adj_mat, user_symptoms, symptoms, diseases)  # Call Bayesian classifier here
            if isinstance(diagnosis, str):
                description = print_description(diagnosis, df_desc)
                precautions = print_precautions(diagnosis, df_prec)
            else:
                add_to_conversation('Bot', "Could not determine the diagnosis.")

            # Add diagnosis and information to the conversation
            response = f"The most likely diagnosis is: {diagnosis}\n\n{description}\n\nRecommended precautions:\n{precautions}"
            add_to_conversation("Bot", response)

# Initialize session state
conversation = []

# Add message to conversation history
def add_to_conversation(speaker, message):
    conversation.append((speaker, message))

# Display the conversation history
def display_conversation():
    for speaker, message in conversation:
        print(f"{speaker}: {message}")

# Initialize session state variables
user_message = ''
user_symptoms_input = ''
medical_consultation = False
clear_symptoms = False
user_input = ''

# Function to handle user messages and bot responses
def handle_message():
    global user_input
    user_message = user_input
    if user_message.strip() != '':
        add_to_conversation("You", user_message)
        predicted_class = predict_class(user_message)
        if predicted_class == "medical_consultation":
            medical_consultation = True
        else:
            response = get_response(predicted_class, intents_json)
            add_to_conversation("Bot", response)
        user_input = ''

# Initialize medical_consultation session state
medical_consultation = False

# Callback function to clear the symptoms input
def clear_symptoms_input():
    global clear_symptoms
    if clear_symptoms:
        user_symptoms_input = ''
        clear_symptoms = False

# Main logic
symptoms, diseases, adj_mat = load_data()
df_desc = load_descriptions()
df_prec = load_precautions()

# Example usage:
# process_symptoms(["Fever", "Cough"])
# handle_message()
# display_conversation()
