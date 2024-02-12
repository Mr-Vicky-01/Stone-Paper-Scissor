import cv2
import mediapipe as mp
from prediction import MakePrediction


class Screen():
    def __init__(self):
        self.my_hands = mp.solutions.hands.Hands(max_num_hands=1)
        self.drawing_utils = mp.solutions.drawing_utils
        self.make_prediction = MakePrediction()
        self.current_frame = None  # Added attribute to store the current frame
        self.user_predicted = ""

    def process_video(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()

            # flip the image
            image = cv2.flip(frame, 1)

            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            output = self.my_hands.process(rgb_image)

            hands = output.multi_hand_landmarks
            if hands:
                for hand in hands:
                    # self.drawing_utils.draw_landmarks(image, hand)
                    prediction_result = self.make_prediction.prediction(hand)
                    cv2.putText(image, prediction_result, (15, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1,
                                cv2.LINE_AA)
                    self.user_predicted = prediction_result
            else:
                self.user_predicted = ""

            # Store the current frame
            self.current_frame = image

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def get_current_frame(self):
        return self.current_frame
