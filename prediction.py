import tensorflow as tf
import numpy as np


class MakePrediction():
    def __init__(self):
        self.rock_paper_scissor_model = tf.keras.models.load_model("rock_paper_scissor_detectionv2.h5")
        self.label_names = ['Paper', 'Rock', 'Scissor']

    def prediction(self, hand_landmarks):
        arr = np.array([[res.x, res.y, res.z] for res in hand_landmarks.landmark]).flatten()
        arr_reshaped = np.expand_dims(arr, 0)
        predicted = self.rock_paper_scissor_model.predict(arr_reshaped)
        predicted_label = self.label_names[np.argmax(predicted)]
        return predicted_label
