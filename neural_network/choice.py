import matplotlib.pyplot as plt
import numpy as np


def do_it(test_images, test_labels, model):
    color = 'white'
    plt.rcParams['text.color'] = color
    plt.rcParams['axes.labelcolor'] = color
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    def predict(the_model, the_image, correct_label):
        prediction = the_model.predict(np.array([the_image]))
        predicted_class = class_names[np.argmax(prediction)]
        print("Predicted class: {}".format(predicted_class))

        show_image(the_image, class_names[correct_label], predicted_class)

    def show_image(img, the_label, guess):
        plt.figure()
        plt.imshow(img, cmap=plt.cm.binary)
        plt.title("Expected: " + the_label)
        plt.xlabel("Guess: " + guess)
        plt.colorbar()
        plt.grid(False)
        plt.show()

    def get_number():
        while True:
            number = input("Pick a number: ")
            if number.isdigit():
                number = int(number)
                if 0 <= number <= 1000:
                    return int(number)
            else:
                print("Try again...")

    num = get_number()
    image = test_images[num]
    label = test_labels[num]
    print("Label: {}".format(class_names[label]))
    predict(model, image, label)
