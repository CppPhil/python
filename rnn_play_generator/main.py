import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from keras.preprocessing import sequence
import keras
import numpy as np

path_to_file = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org'
                                                          '/data/shakespeare.txt')

# Read, then decode for py2 compat.
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
# length of the text is the number of characters in it
print('Length of text: {} characters'.format(len(text)))

# Take a look at the first 250 characters in the text
print(text[:250])

# Encoding
vocab = sorted(set(text))
# Creating a mapping from unique characters to indices
char2idx = {u: i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)


def text_to_int(the_text):
    return np.array([char2idx[c] for c in the_text])


text_as_int = text_to_int(text)

# Let's look at how part of our text is encoded.
print("Text: ", text[:13])
print("Encoded: ", text_to_int(text[:13]))


def int_to_text(ints):
    try:
        ints = ints.numpy()
    except:
        pass
    return ''.join(idx2char[ints])


print(int_to_text(text_as_int[:13]))

seq_length = 100  # Length of sequence for a training example
examples_per_epoch = len(text) // (seq_length + 1)

# Create training examples / targets
char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

# Batch into lengths of 101, drop remainder that can't fit into another batch.
sequences = char_dataset.batch(seq_length + 1, drop_remainder=True)


def split_input_target(chunk):  # for the example: hello
    input_text = chunk[:-1]  # hell
    target_text = chunk[1:]  # ello
    return input_text, target_text  # hell, ello


dataset = sequences.map(split_input_target)  # We use map to apply the above function to every entry

for x, y in dataset.take(2):
    print("\n\nEXAMPLE\n")
    print("INPUT")
    print(int_to_text(x))
    print("\nOUTPUT")
    print(int_to_text(y))

# Make training batches
BATCH_SIZE = 64  # 64 Training examples and also have 64 outputs at once every time.
VOCAB_SIZE = len(vocab)  # vocab is the number of unique characters
EMBEDDING_DIM = 256
RNN_UNITS = 1024

BUFFER_SIZE = 10000

data = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    the_model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                  batch_input_shape=[batch_size, None]),  # None makes it so that you don't have to
        # know the length of each sequence etc.
        tf.keras.layers.LSTM(rnn_units,  # Long-Short term memory
                             return_sequences=True,  # Return intermediate step results. We need the output at every
                             # timestep.
                             stateful=True,
                             recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size)  # The output layer needs to have as many neurons as the size of the
        # vocabulary so that we can see the probability of every possible character being the next one.
    ])
    return the_model


model = build_model(VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, BATCH_SIZE)
model.summary()

# Create a Loss function
# We're passing sequences each of length 100.
# Sometimes we'll just pass one entry of variable length.
for input_example_batch, target_example_batch in data.take(1):
    # Use the model before it's been trained.
    example_batch_predictions = model(input_example_batch)  # ask our model for a prediction on our first batch of
    # training data
    print(example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")  # print out the output shape

# We can see that the prediction is an array of 64 arrays, one for each entry in the batch
print(len(example_batch_predictions))
print(example_batch_predictions)

# Let's examine one prediction
pred = example_batch_predictions[0]
print(len(pred))
print(pred)
# Notice this is a 2D array of length 100, where each interior array is the prediction for the next character at each
# time step.

# And finally we'll look at a prediction at the first timestep
time_pred = pred[0]
print(len(time_pred))
print(time_pred)
# And of course it's 65 values representing the probability of each character occurring next

# If we want to determine the predicted character we need to sample the output distribution
sampled_indices = tf.random.categorical(pred, num_samples=1)

# Now we can reshape that array and convert all the integers to numbers to see the actual characters
sampled_indices = np.reshape(sampled_indices, (1, -1))[0]
predicted_chars = int_to_text(sampled_indices)

print(predicted_chars)  # And this is what the model predicted for training sequence 1.


# So now we need to create a loss function that can compare that output to the expected output and give
# us some numeric value representing how close the two were.
# Logits are probability distributions.
def loss(labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)


# We want to reduce the loss in the neural network.
model.compile(optimizer='adam', loss=loss)

# Creating checkpoints
# Directory where the checkpoints will be saved.
checkpoint_dir = './training_checkpoints'
# Name of the checkpoint files
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefix,
    save_weights_only=True)

history = model.fit(data, epochs=2, callbacks=[checkpoint_callback])

# Loading the model
model = build_model(VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, batch_size=1)

model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))
model.build(tf.TensorShape([1, None]))


def generate_text(the_model, start_string):
    # Evaluation step (generating text using the learned model)

    # Number of characters to generate
    num_generate = 800

    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures result in more predictable text.
    # Higher temperatures result in more surprising text.
    # Experiment to find the best setting.
    temperature = 1.0

    # Here batch size is 1
    the_model.reset_states()
    for i in range(num_generate):
        predictions = the_model(input_eval)
        # Remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # Using a categorical distribution to predict the character return by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

        # We pass the predicted character as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])

    return start_string + ''.join(text_generated)


input_string = 'romeo'
print(generate_text(model, input_string))
