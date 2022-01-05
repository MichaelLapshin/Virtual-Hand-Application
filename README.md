# Virtual-Hand-Application

The goal of the Virtual Hand Controller is to believably move a virtual hand using a non-optical solution. This project focuses on finding a solution using a set of force sensors.

To accomplish realistic movements with such little data, these programs are making use of TensorFlow's machine learning. With a dataset (generated using the force sensors and visual-hand tracking) we can feed the data into a neural network and train a solution for the given hardware.

A client and server application and program were developed for creating, managing, and storing the datasets and models. It becomes especially vital to the progression of the project as hundreds of datasets and models will need to be managed. In addition, since it take time to train a model, the Client GUI offers the user the ability to queue model training and view its live progress.

- The previous non-GUI version of the program: https://github.com/MichaelLapshin/Virtual-Hand



# Important Features

## Accessing the Server
The client is able to check if the server is online, create user accounts, and log-in. This allows for multiple users to use the application.

![Account](https://user-images.githubusercontent.com/55516685/148303279-a017cb6f-1d1e-4ebf-8010-7daddbc51bd4.PNG)

## Generating Datasets
The client is able to generate a dataset by navigating to the appropriate the tab (Datasets -> New).

Supported dataset recording devices:
- Video camera (using the MediaPipe hand-tracking library)
- Leap Motion hand controller (dedicated software/hardware for hand-tracking)

Within the dataset creation page, the user can specify the properties of...
- the recording device (i.e. width, heigh, frames per second)
- the dataset recording process (i.e. time to zero the sensors, training length, frames per second)
- the dataset entry within the database (i.e. name, time, rating, access permissions)

All appropriate used of the page are asserted. Some examples:
- the user cannot start a dataset recording until the appropriate hardware is connected and the current property entries are inputted.
- the user cannot upload a dataset without being logged in and generating a dataset first.
- etc.

![Datasets New](https://user-images.githubusercontent.com/55516685/148303338-c8baa351-3426-402b-bc25-f9647d24293b.PNG)


## Viewing the Datasets
The user can view only their generated datasets and ones from other users that are set to public. The Admin has access to all datasets.
Each dataset allows for its name and rating to be changed. They may also be smoothed.

Smoothing the dataset:
- The sensor and angular data can be separately smoothed using the Savitzky–Golay filter (by specifying the smoothing distance and degree).
- Each smoothed dataset can be rated and renamed. All entries are asserted for the appropriate type of input.
- The smoothing process uses the angular data to generate angular velocity and angular acceleration data. Images are generated for each finger limb.

Merging datasets:
- Only datasets that have not been smoothed may be selected and merged to create a larger dataset.

![Datasets](https://user-images.githubusercontent.com/55516685/148303347-4159b2f2-bed6-4dac-b88d-17ac0f6ec8dc.PNG)


## Generating the Models
The user can select any smoothed (processed) dataset, specify training parameters and initiate a training task. The entries include name, rating, access permissions, reference dataset, time created, the batch size, number of epochs, number of layers, neurons per layer, activation function, etc.

The training the multi-threaded (for each limb) to improve training speeds.

![Models New](https://user-images.githubusercontent.com/55516685/148303376-d78abc41-0e2e-4c44-be04-b2040227865a.PNG)




## Viewing the Models
Once a model entry has been created, the user is able to view all of its properties (is the user has sufficient permissions).

After the training of each model, a series of prediction graphs and loss-graphs are created and stored on the server. They are sent to and displayed to the user when a model is selected.

![Models](https://user-images.githubusercontent.com/55516685/148303418-1efe731e-86aa-44f4-b388-d8330682ccca.PNG)
![Training Processes #2](https://user-images.githubusercontent.com/55516685/148303472-53316057-13f0-4942-ae85-249ad65e8038.PNG)


## Testing a Model
Once a model has been trained, within the "Model Processes" tab, the user may select a model and "Start Server". This creates a local UDP server which listens for incoming environment data, obtains the current sensor readings, makes a prediction using the model, and returns the result back the (Unity program) sender.

![Testing Model](https://user-images.githubusercontent.com/55516685/148305517-201d03ba-fbb7-4c1a-8088-4856ededa9ba.PNG)


## Settings
The client GUI program includes settings for modifying GUI scale, its update rate, and its two base colours. The settings are saved on the client-side.

![Settings](https://user-images.githubusercontent.com/55516685/148303480-8f6361fe-a2b9-478c-b676-f3cbdc897f3c.PNG)


# Challenges

Since the program does not know the hand's intended position for certain (visually), it uses neural networks to predict how the virtual hand-limbs should move given its current state to achieve the desired state.

The hardware is limited in accuracy and frequency which renders a solution challenging to develop. The sensor amplifiers are limited to 80Hz sampling rate with about 1% reading error. The current visual hand-trackers used in to train the models are limited to 60Hz and 120Hz.

![Hardware](https://user-images.githubusercontent.com/55516685/148305527-be56c0e9-b237-4057-af19-cc2439f173f1.jpg)


# A previous approach (predicting angular velocities)

Previously, the application and Tensorflow models tried to predict the angular velocity of the finger limbs. While the generated models have shown signs of correct hand movements, it is often incorrect.

High error rates of predicting angular velocities of limbs is likely due to the sensor and visual hand-tracking system noise. Even with data smoothing and filtering, the noise in the data is too significant to reliably generate working models.



# The new approach (predicting angular position)

Given the inaccuracies presented by predicting angular velocities, the system has shifted to using angular position. Since the angular position is much more consistent at a given sensor reading, then it would return much better results.

The tests using the angular position approach have shown much more consistent and smoother hand-motion. On many occasions, the fingers have actually moved correctly. 



# Conclusion (Jan 5, 2022)

To achieve the goal of moving a virtual-hand using only a few simplistic force-sensors, the client application, server, hardware and the neural networks have proved to be vital components. In the current state of the project, the client and server combination deliver an organized and interactive way to create and view datasets, generate and view models, and judge the model performance by easily hosting a local server and connecting to a Unity environment. It has been my pleasure to both develop and use the program.

While many of the tests have shown some the virtual-hand fingers to move as expected, most of the models have not shown satisfactory results. It is likely due to the 
inaccuracies of the underlying hardware and software. Although the hardware can be further upgraded and many more weeks (or months) can be spent to research and update the Tensorflow code to yield better results, I have chosen to move on to my next project which I was been anticipating and planning for months.
