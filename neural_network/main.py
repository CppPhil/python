
import numpy as np
import matplotlib.pyplot as plt
import choice

# grayscale images
fashion_mnist = keras.datasets.fashion_mnist  # load dataset
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()  # split into testing and training

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Data Preprocessing
# Data should be in between 0 and 1
train_images = train_images / 255.0
test_images = test_images / 255.0

# The model The neural network Sequential -> sequential neural network (not recurrent or convolutional)
# input layer: Flatten -> Take shape 28 x 28 (matrix) and flatten it into 784 pixels
# hidden layer: Dense layer (all neurons in the prev. layer are connected to the ones in this), 128 neurons,
# relu as activation function
# output layer: Dense layer, 10 output neurons, softmax as the activation function 10 output neurons because there are
# 10 classes to detect.
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),  # input layer (1)
    keras.layers.Dense(128, activation='relu'),  # hidden layer (2)
    keras.layers.Dense(10, activation='softmax')  # output layer (3)
])
# Architecture is defined

# Compile the model
# Optimizer: adam does the gradient descent etc.
# Loss function
# Metrics: we want to see the accuracy
# These are the hyper parameters
# The amount of neurons etc are also hyper parameters.
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Training the model
# Epochs is another hyper parameter
model.fit(train_images, train_labels, epochs=10)

print('')

# Test the model on the testing data
test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=1)
print('Test accuracy:', test_accuracy)

# Make predictions
predictions = model.predict(test_images)
print(class_names[np.argmax(predictions[0])])
plt.figure()
plt.imshow(test_images[0])
plt.colorbar()
plt.grid(False)
plt.show()

choice.do_it(test_images=test_images, test_labels=test_labels, model=model)
