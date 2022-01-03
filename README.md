# Virtual-Hand-Application

The goal of the Virtual Hand Controller is to believably move a virtual hand using a non-optical solution. This project focuses on finding a solution using a set of force sensors.

To accomplish realistic movements with such little data, these programs are making use of TensorFlow's machine learning. With a dataset (generated using the force sensors and visual-hand tracking) we can feed the data into a neural network and train a solution for the given hardware.

A client and server application and program were developed for creating, managing, and storing the datasets and models. It becomes especially vital to the progression of the project as hundreds of datasets and models will need to be managed. In addition, since it take time to train a model, the Client GUI offers the user the ability to queue model training and view its live progress.

- The previous non-GUI version of the program: https://github.com/MichaelLapshin/Virtual-Hand


# Challenges

Since the program does not know the hand's intended position for certain (visually), it uses neural networks to predict how the virtual hand-limbs should move given its current state to achieve the desired state.

The hardware is limited in acccuracy and frequency which renders a solution challenging to develop. The sensor amplifiers are limited to 80Hz sampling rate with about 1% reading error. The current visual hand-trackers used in to train the models are limited to 60Hz and 120Hz.


# A previous apporach (predicting angular velocities)

Previously, the application and Tensorflow models tried to predict the angular velocity of the finger limbs. While the generated models have shown signs of correct hand movements, it is often incorrect.

High error rates of predicting angular velocities of limbs is likely due to the sensor and visual hand-tracking system noise. Even with data smoothing and filtering, the noise in the data is too significant to reliably generate working models.


# The new approach (predicting angular position)