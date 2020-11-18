import nltk, tflearn, tensorflow, random, json, pickle
import numpy as np
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

nltk.download('punkt')

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:     
    words=[]
    labels=[]
    docs_x=[]
    docs_y=[]

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)
                          
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for doc in enumerate(docs_x):
        bag = []
        print(doc)
        wrds = [stemmer.stem(w[0]) for w in doc if type(w) is not int]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = list(out_empty)
        output_row[labels.index(docs_y[doc[0]])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 12)
net = tflearn.fully_connected(net, 12)
net = tflearn.fully_connected(net, 12)
net = tflearn.layers.core.dropout(net, 0.9)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net, learning_rate=0.001)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=1, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w in se:
                bag[i] = 1

    return np.array(bag)

def model_response(inp):
    results = model.predict([bag_of_words(inp, words)])[0]

    results_index = np.argmax(results)
    tag = labels[results_index]

    if results[results_index] > 0.8:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        return [tag, random.choice(responses)]
    else:
        return "Sorry, I'm not sure what you mean."
