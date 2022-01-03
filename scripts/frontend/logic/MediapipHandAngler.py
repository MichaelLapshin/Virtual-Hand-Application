"""
[main.py]
@description: Script for obtaining finger limb angles and displaying video feed.
@author: Michael Lapshin
    - Some code was taken from https://google.github.io/mediapipe/solutions/hands for capturing and processing the video feed with mediapipe.
"""
import ctypes
import math
import os
import time

from PIL import Image

from scripts import Warnings, InputConstraints

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # To remove the redundant warnings
import numpy
import threading
import cv2
import mediapipe as mp
import scripts.leap_motion.Leap as Leap

print("Imported the MediapipeHandAngler.py class successfully.")


def normalized_3d_vector(v):
    return numpy.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def dot_product_3d_vector(a, b):
    return (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2])


# r1, r2, s are the coordinates of the 3 points.
# r2 is the point in between the reference point r1 and the point for which we are trying to interpret the angle s
# @return, angle in radians: angle is bound by [0, pi]
def coord2radians(base_point, common_point, subject_point):
    reference_vector = [common_point[0] - base_point[0], common_point[1] - base_point[1],
                        common_point[2] - base_point[2]]
    direction_vector = [subject_point[0] - common_point[0], subject_point[1] - common_point[1],
                        subject_point[2] - common_point[2]]

    # Math calculations
    reference_norm = normalized_3d_vector(reference_vector)
    direction_norm = normalized_3d_vector(direction_vector)
    reference_dot_direction = dot_product_3d_vector(reference_vector, direction_vector)

    # Compute final calculations
    angle = numpy.arccos(reference_dot_direction / (reference_norm * direction_norm))
    return angle


def coord2degrees(base_point, common_point, subject_point):
    return math.degrees(coord2radians(base_point=base_point, common_point=common_point, subject_point=subject_point))


def extract_coord(joint):
    return [joint.x, joint.y, joint.z]


class HandAngleReader(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)  # calls constructor of the Thread class
        self._daemon = True
        self._running = False

        # Image capturing-related variables
        self._cap = cv2.VideoCapture()
        self._mp_drawing = mp.solutions.drawing_utils
        self._mp_hands = mp.solutions.hands
        self._raw_image = None
        self._image = None

        # of the form: limb_angles[finger, limb] ; finger(thumb -> pinky), limb(proximal -> distal)
        self._limb_angles = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def set_configurations(self, width, height, zoom, frames_per_second, video_source=0):
        # Stores the inputs locally
        self._video_source = video_source
        self._width = width
        self._height = height
        self._zoom = zoom
        self._frames_per_second = frames_per_second

    # Continuously reads from the camera feed
    def run(self):
        Warnings.not_overridden()
        assert self._running is True

    # Obtains the limb angles from the image processing results
    def process_limb_angles(self, results):
        # Processes the hand data into angles
        if results.multi_hand_landmarks:
            lm_list = results.multi_hand_landmarks[0].landmark

            for fingerIndex in range(0, 5):  # For each finger
                # palm to proximal phalange angle
                self._limb_angles[fingerIndex][0] = coord2degrees(extract_coord(lm_list[0]),
                                                                  extract_coord(lm_list[fingerIndex * 4 + 1]),
                                                                  extract_coord(lm_list[fingerIndex * 4 + 2]))
                # proximal phalange to middle phalange angle
                self._limb_angles[fingerIndex][1] = coord2degrees(extract_coord(lm_list[fingerIndex * 4 + 1]),
                                                                  extract_coord(lm_list[fingerIndex * 4 + 2]),
                                                                  extract_coord(lm_list[fingerIndex * 4 + 3]))
                # middle phalange to distal phalange angle
                self._limb_angles[fingerIndex][2] = coord2degrees(extract_coord(lm_list[fingerIndex * 4 + 2]),
                                                                  extract_coord(lm_list[fingerIndex * 4 + 3]),
                                                                  extract_coord(lm_list[fingerIndex * 4 + 4]))
        else:
            # nulls the data if the hand cannot be detected
            self._limb_angles = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def get_raw_image(self):
        return self._raw_image

    def get_processed_image(self):  # Must return a PIL.Image object
        return self._image

    # Start/Stop methods
    def start_watching(self):
        Warnings.not_overridden(False)

    def stop_watching(self):
        Warnings.not_overridden(False)

    def is_watching(self):
        Warnings.not_overridden(False)

    def start(self):
        self._running = True
        super().start()

    def stop(self):
        self._running = False

    def is_running(self):
        return self._running

    # Getters for limb angles
    def get_all_limb_angles(self):
        return self._limb_angles

    def get_thumb_angles(self):
        return self._limb_angles[0]

    def get_index_angles(self):
        return self._limb_angles[1]

    def get_middle_angles(self):
        return self._limb_angles[2]

    def get_ring_angles(self):
        return self._limb_angles[3]

    def get_pinky_angles(self):
        return self._limb_angles[4]


class MediaPipeHandAnglerReader(HandAngleReader):

    def __init__(self):
        HandAngleReader.__init__(self)

    def set_configurations(self, width, height, zoom, frames_per_second, video_source=0):
        super().set_configurations(width, height, zoom, frames_per_second, video_source)

        # For webcam input:
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)  # Sets Width of the video feed
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)  # Sets Height of the video feed
        self._cap.set(cv2.CAP_PROP_ZOOM, self._zoom)  # Sets Zoom of the video feed
        self._cap.set(cv2.CAP_PROP_FPS, self._frames_per_second)  # Sets FPS of the video feed

    # Continuously reads from the camera feed
    def run(self):
        assert self._running is True

        # Processes and displays video feed
        with self._mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.85,
                                  min_tracking_confidence=0.1, static_image_mode=False) as hands:
            while self._running:
                time.sleep(1)

                while self._cap.isOpened() and self._running:
                    success, image = self._cap.read()

                    # TODO, implement un-distorting code for the image (to improve accuracy of the captured images)
                    #      - https://docs.opencv.org/4.5.2/dc/dbb/tutorial_py_calibration.html
                    #      - https://docs.opencv.org/3.4/d4/d94/tutorial_camera_calibration.html

                    if not success:
                        # print("Ignoring empty camera frame.")
                        continue

                    # Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
                    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

                    # To improve performance, optionally mark the image as not writeable to pass by reference.
                    image.flags.writeable = False
                    results = hands.process(image)

                    self.process_limb_angles(results=results)

                    self._raw_image = image  # Deep copy?
                    self.process_image(results=results, image=image)

                    if cv2.waitKey(5) & 0xFF == 27:
                        break

        self._cap.release()

    def process_image(self, results, image):
        # Draw the hand annotations on the image.
        image.flags.writeable = True

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self._mp_drawing.draw_landmarks(image, hand_landmarks, self._mp_hands.HAND_CONNECTIONS)

        self._image = Image.fromarray(image)

    # Start/Stop methods
    def start_watching(self):
        assert self._cap.isOpened() is False
        self._cap.open(self._video_source, cv2.CAP_DSHOW)

    def stop_watching(self):
        if self._cap.isOpened():
            self._cap.release()

    def is_watching(self):
        return self._cap.isOpened()


class LeapMotionHandAnglerReader(HandAngleReader, Leap.Listener):
    def __init__(self):
        Leap.Listener.__init__(self)
        HandAngleReader.__init__(self)

        # Sets up the leap motion controller
        self.controller = Leap.Controller(self)
        self.controller.add_listener(self)

        self.controller.set_policy(Leap.Controller.POLICY_IMAGES)
        self.controller.set_policy(Leap.Controller.POLICY_RAW_IMAGES)

        # if not self.controller.is_connected:
        #     InputConstraints.warn("The Leap Motion controller was not detected.\nIs it connected?")

        self.watching = False

    def set_configurations(self, width, height, zoom, frames_per_second, video_source=0):
        super().set_configurations(width, height, zoom, frames_per_second, video_source)

    def run(self):
        assert self._running is True

        while self._running:
            time.sleep(1)

            while self.is_watching() and self._running \
                    and self.controller.is_connected and self.controller.frame().is_valid \
                    and self.controller.frame().images[0].is_valid:

                # Obtains the frame
                frame = self.controller.frame()
                numpy_image = self.get_image_as_numpy_array(
                    frame.images[0])  # Records the image from the left camera (index 0)
                self._image = Image.fromarray(numpy_image)

                # Calculates the angle of each finger bone relative to the previous bone
                for hand in frame.hands:
                    for finger in hand.fingers:
                        for joint_id in range(0, 3):  # 1:proximal ... 3:distal

                            # Obtains the base joint
                            base_joint: Leap.Vector
                            if finger.type == Leap.Finger.TYPE_THUMB and joint_id == Leap.Bone.TYPE_METACARPAL:
                                # Since the thumb does not have a metacarpal bone, then it will use the wrist as reference
                                base_joint = hand.wrist_position
                            else:
                                base_joint = finger.bone(joint_id).prev_joint

                            # Adds the limb data
                            self._limb_angles[finger.type][joint_id] = \
                                coord2degrees(
                                    base_point=base_joint.to_float_array(),
                                    common_point=finger.bone(joint_id + 1).prev_joint.to_float_array(),
                                    subject_point=finger.bone(joint_id + 1).next_joint.to_float_array()
                                )

    def get_image_as_numpy_array(self, image):
        """
        Get the numpy array related to the leap motion infrared image data
        It is useful to show the image (e.g., using the cv2.imshow method)
        """
        image_buffer_ptr = image.data_pointer  # pointer to the image data buffer to directly access the memory in the data buffer using ctypes or numpy
        ctype_array_def = ctypes.c_ubyte * image.width * image.height

        # as ctypes array
        as_ctype_array = ctype_array_def.from_address(int(image_buffer_ptr))
        # as numpy array
        as_numpy_array = numpy.ctypeslib.as_array(as_ctype_array)
        return as_numpy_array

    # Watching methods
    def start_watching(self):
        self.watching = True

    def stop_watching(self):
        self.watching = False

    def is_watching(self):
        return self.watching
