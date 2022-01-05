# Virtual-Hand-Application

The goal of the Virtual Hand Controller is to believably move a virtual hand using a non-optical solution. This project focuses on finding a solution using a set of force sensors.

To accomplish realistic movements with such little data, these programs are making use of TensorFlow's machine learning. With a dataset (generated using the force sensors and visual-hand tracking) we can feed the data into a neural network and train a solution for the given hardware.

A client and server application and program were developed for creating, managing, and storing the datasets and models. It becomes especially vital to the progression of the project as hundreds of datasets and models will need to be managed. In addition, since it take time to train a model, the Client GUI offers the user the ability to queue model training and view its live progress.

- The previous non-GUI version of the program: https://github.com/MichaelLapshin/Virtual-Hand


# Important Features

### Accessing the Server
The client is able to check if the server is online, create user accounts, and log-in. This allows for multiple users to use the application.

### Generating Datasets
The client is able to generate a dataset by navigating to the apporpriate the tab (Datasets -> New).

Supported dataset recording devices:
- Video camera (using the Mediapipe hand-tracking library)
- Leap Motion hand controller (dedicated software/hardware for hand-tracking)

Within the dataset creation page, the user can specify the properties of...
- the recording device (i.e. width, heigh, frames per second)
- the dataset recording process (i.e. time to zero the sensors, training length, frames per second)
- the dataset entry within the database (i.e. name, time, rating, access permissions)

All appropriate used of the page are asserted. Some exmples:
- the user cannot start a dataset recording until the appropriate hardware is connected and the current property entries are inputted.
- the user cannot upload a dataset without being logged in and generating a dataset first.
- etc.


### Viewing the Datasets
The user is able to view only their generated datasets and ones from other users that are set to public. The Admin has access to all datasets.
Each dataset allows for its name and rating to be changed. They may also be smoothed.

Smoothing the dataset:
- The sensor and angular data can be seperately smoothed using the Savitzky–Golay filter (by specifying the smoothing distance and degree).
- Each smoothed dataset can be rated and renamed. All entries are asserted for the appropriate type of input.
- The smoothing process uses the angular data to generate angular velocity and angular acceleration data. Images are generated for each finger limb.

Merging datasets:
- Only datasets that have not been smoothed may be selected and merged to create a larger dataset.


### Generating the Models
The user can select any smoothed (processed) dataset, specify training parameters and initiate a training task. The entires include name, rating, access permissions, reference dataset, time created, the batch size, number of epochs, number of layers, neurons per layer, activation function, etc.

The training the multi-threaded (for each limb) to improve training speeds.

### Viewing the Models
Once a model entry has been created, the user is able to view all of its properties (is the user has sufficient permissions).

After the training of each model, a series of prediction graphs and loss-graphs are created and stored on the server. They are sent to and displayed to the user when a model is selected.


### Testing a Model
Once a model has been trained, within the "Model Processes" tab, the user may select a model and "Start Server". This creates a local UDP server which listens for incoming environement data, obtains the current sensor readings, makes a prediction using the model, and returns the result back the (Unity program) sender.


### Settings
The client GUI program includes settings for modifying GUI scale, its update rate, and its two base colours. The settings are saved on the client-side.


# Challenges

Since the program does not know the hand's intended position for certain (visually), it uses neural networks to predict how the virtual hand-limbs should move given its current state to achieve the desired state.

The hardware is limited in acccuracy and frequency which renders a solution challenging to develop. The sensor amplifiers are limited to 80Hz sampling rate with about 1% reading error. The current visual hand-trackers used in to train the models are limited to 60Hz and 120Hz.


# A previous apporach (predicting angular velocities)

Previously, the application and Tensorflow models tried to predict the angular velocity of the finger limbs. While the generated models have shown signs of correct hand movements, it is often incorrect.

High error rates of predicting angular velocities of limbs is likely due to the sensor and visual hand-tracking system noise. Even with data smoothing and filtering, the noise in the data is too significant to reliably generate working models.


# The new approach (predicting angular position)