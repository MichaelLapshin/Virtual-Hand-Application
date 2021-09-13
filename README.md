# Virtual-Hand-Application
The goal of the Virtual Hand Controller is to believably move a virtual hand using a non-optical solution. This project focuses on finding a solution using a set of force sensors.

To accomplish realistic movements with such little data, these programs are making use of TensorFlow's machine learning. With a dataset (generated using the force sensors and common optic-hand tracking) we can feed the data into a neural network and train a solution for the given hardware. 

A client and server application and program were developed for creating, managing, and storing the datasets and models. It becomes especially vital to the progression of the project and hundreds of datasets and models will need to be managed. In addition, since it take time to train a model, the Client GUI offers the user the ability to queue model training.
 - This is a refactored version of the non-GUI program: https://github.com/MichaelLapshin/Virtual-Hand

# Challenges
Since the program is unable to know the hand's intended position for certain (optically), it uses neural networks to predict how the virtual hand-limbs should move given its current state to achieve the desired state.

The hardware is limited in acccuracy and frequency which renders a solution challenging to develop. The sensor amplifiers are limited to 80Hz sampling rate with about 1% reading error. The current hand-tracker is limited to 60Hz and a 5% reading error.
