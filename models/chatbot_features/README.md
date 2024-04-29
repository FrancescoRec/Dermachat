# Chatbot Training Folder

This folder contains files necessary for training and updating the chatbot's intents. When making changes to the intents.json file, it's essential to run the training.py script to update the chatbot models. This process creates or updates the following files in the same folder:

* classes.pkl: Pickled file containing the list of unique classes (intents) used in the training data.
* words.pkl: Pickled file containing the list of unique words extracted from the training data.
* chatbot_model.h5: Trained neural network model for the chatbot.


Updated Models: After running the script, the classes.pkl, words.pkl, and chatbot_model.h5 files will be updated or created in the folder.

### Files

* intents.json: JSON file containing intents and their associated patterns and responses.
* training.py: Python script to train the chatbot using the intents specified in intents.json.
* classes.pkl: Pickled file containing the list of unique classes (intents) used in the training data.
* words.pkl: Pickled file containing the list of unique words extracted from the training data.
* chatbot_model.h5: Trained neural network model for the chatbot.

### Dependencies

* Python 3.x
* Libraries: numpy, tensorflow, nltk

### Notes

    Ensure that all necessary dependencies are installed before running the training script.
    It's recommended to back up the existing model files (classes.pkl, words.pkl, chatbot_model.h5) before retraining the chatbot.