
from typing import BinaryIO
import tflearn
import nltk
import numpy
import tensorflow
import random
import json
import pickle
import nltk.data
from nltk.stem.lancaster import LancasterStemmer




stemmer = LancasterStemmer()

with open("chatbot_intents.json") as file:
    data = json.load(file)

# print(data["intents"])

try:
    with open("data.pk", "rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []  # list of all words
    labels = []  # List of all labels
    docs_x = []  # list of different patterns
    docs_y = []  # list of corresponding words as per patterns in docs_x

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]  # reduces all words to lowercase
    words = sorted(list(set(words)))  # remove duplicated words

    labels = sorted(labels)  # This will sort our labels

    # Training and testing output
    # creating bags of words - turning our data from str to numbers

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]
    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.compat.v1.reset_default_graph()


net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 6)
net = tflearn.fully_connected(net, 6)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)  # Take on the neuro network defined above

model.fit(training, output, n_epoch=350, batch_size=6, show_metric=True)
model.save("model.tflearn")


def bag_of_word(s, wordings):
    bags = [0 for _ in range(len(wordings))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for sen in s_words:
        for i, w in enumerate(wordings):
            if w == sen:
                bags[i] = 1

    return numpy.array(bags)


# dialogue function
def chat():
    print("Hi you're through to ChatAI, how may I help you today? To end this chat please type 'quit'.")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        results = model.predict([bag_of_word(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        if results[results_index] <= 0.7:
            print("I'm sorry I didn't understand that, please try again or type agent to be transferred to a live member of the team.")
        else:
            for tg in data["intents"]:
                if tg["tag"] == tag:
                    if tg["tag"] == "no help":
                        # Set the tag to "goodbye" and start a new loop to find the "goodbye" tag
                        tag = "goodbye"
                        while True:
                            for tg in data["intents"]:
                                if tg["tag"] == "goodbye":
                                    # Send the response and exit the loop
                                    print(random.choice(tg["responses"]))
                                    break
                            # If the loop completes without finding the "goodbye" tag, exit the chat
                            break
                    else:
                        # Send the response
                        print(random.choice(tg["responses"]))
                        break


chat()

#%%
