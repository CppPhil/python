import keras
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from keras.datasets import imdb
from keras.preprocessing import sequence
import numpy as np

VOCAB_SIZE = 88584

MAXLEN = 250
BATCH_SIZE = 64

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=VOCAB_SIZE)

# Shorten any review of more than 250 characters to 250 characters
# and pad any review of fewer than 250 characters to 250 characters.
# This is required because input sequences all need to be of the same size.
train_data = sequence.pad_sequences(train_data, MAXLEN)
test_data = sequence.pad_sequences(test_data, MAXLEN)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(VOCAB_SIZE, 32),  # Finds a more meaningful vectors for the input (vectors are 32
    # elements long)
    tf.keras.layers.LSTM(32),  # 32 dimensional input from the previous layer
    tf.keras.layers.Dense(1, activation="sigmoid")  # Output layer
])

# binary crossentropy because the result is binary
model.compile(loss="binary_crossentropy", optimizer="rmsprop", metrics=['acc'])
history = model.fit(train_data, train_labels, epochs=10, validation_split=0.2)

results = model.evaluate(test_data, test_labels)
print(results)

word_index = imdb.get_word_index()


def encode_text(the_text):
    tokens = keras.preprocessing.text.text_to_word_sequence(the_text)  # Tokenize
    tokens = [word_index[word] if word in word_index else 0 for word in tokens]  # Put the word's integer or 0 if it
    # doesn't exist.
    return sequence.pad_sequences([tokens], MAXLEN)[0]  # It's a list of lists, just take the inner list.


text = "that movie was just amazing, so amazing"
encoded = encode_text(text)
print(encoded)

reverse_word_index = {value: key for (key, value) in word_index.items()}


def decode_integers(integers):
    pad = 0
    the_text = ""
    for num in integers:
        if num != pad:
            the_text += reverse_word_index[num] + " "

    return the_text[:-1]


print(decode_integers(encoded))


# now it's time to make a prediction

def predict(the_text):
    encoded_text = encode_text(the_text)
    pred = np.zeros((1, 250))  # A movie review is 250 characters long.
    pred[0] = encoded_text  # Put the one entry into the array.
    result = model.predict(pred)  # Predict it
    print(result[0])  # Print it, result[0] because it's an array. index 0 is for the first and only array entry.


positive_review = "That movie was so awesome! I really loved it and would watch it again because it was amazingly great"
predict(positive_review)

negative_review = "that movie sucked. I hated it and wouldn't watch it again. Was one of the worst things I've ever " \
                  "watched "
predict(negative_review)
