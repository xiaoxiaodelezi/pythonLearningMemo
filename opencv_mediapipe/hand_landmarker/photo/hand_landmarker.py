import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 各个手指对应的点
mp_hands = mp.tasks.vision.HandLandmarksConnections
# https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/drawing_utils
mp_drawing = mp.tasks.vision.drawing_utils
# https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/drawing_styles
mp_drawing_styles = mp.tasks.vision.drawing_styles

MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (80, 205, 24)


def draw_landmarks_on_image(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        """
        mp.tasks.vision.drawing_utils.draw_landmarks(
            image: np.ndarray,
            landmark_list: list[landmark_module.NormalizedLandmark],
            connections: Optional[list[_CONNECTION]] = None,
            landmark_drawing_spec: Optional[Union[DrawingSpec, Mapping[int, DrawingSpec]]] = DrawingSpec(color=RED_COLOR),
            connection_drawing_spec: Union[DrawingSpec, Mapping[tuple[int, int], DrawingSpec]] = DrawingSpec(),
            is_drawing_landmarks: bool = True
        )
        """

        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            # A mapping from each hand landmark to its default drawing spec.
            # mp.tasks.vision.drawing_styles.get_default_hand_landmarks_style() -> Mapping[int, mp.tasks.vision.drawing_utils.DrawingSpec]
            mp_drawing_styles.get_default_hand_landmarks_style(),
            # A mapping from each hand connection to its default drawing spec.
            # mp.tasks.vision.drawing_styles.get_default_hand_connections_style() -> Mapping[tuple[int, int], _DrawingSpec]
            mp_drawing_styles.get_default_hand_connections_style(),
        )

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        # cv2.putText(img, text, org, fontFace, fontScale, color, thickness=1, lineType=cv2.LINE_AA, bottomLeftOrigin=False)
        cv2.putText(
            annotated_image,
            f"{handedness[0].category_name}",
            (text_x, text_y),
            cv2.FONT_HERSHEY_DUPLEX,
            FONT_SIZE,
            HANDEDNESS_TEXT_COLOR,
            FONT_THICKNESS,
            cv2.LINE_AA,
        )

    return annotated_image


base_options = python.BaseOptions(model_asset_path="../hand_landmarker.task")
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)


image = mp.Image.create_from_file("woman_hands.jpg")

detection_result = detector.detect(image)

# numpy_view是4通道的
annotated_image = draw_landmarks_on_image(
    image.numpy_view()[:, :, :3], detection_result
)
cv2.imshow("women_hands", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

cv2.waitKey(0)
cv2.destroyAllWindows()
