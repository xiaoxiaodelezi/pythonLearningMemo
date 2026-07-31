import numpy as np
import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def draw_landmarks_on_image(rgb_image, detection_result):
    # 预处理
    # handedness和hand_landmarks是一一对应的
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # 部分基本参数
    # 各个手指对应的点
    mp_hands = mp.tasks.vision.HandLandmarksConnections
    mp_drawing = mp.tasks.vision.drawing_utils
    mp_drawing_styles = mp.tasks.vision.drawing_styles

    MARGIN = 10
    FONT_SIZE = 1
    FONT_THICKNESS = 1
    HANDEDNESS_TEXT_COLOR = (80, 205, 24)

    for idx in range(len(hand_landmarks_list)):
        # 手指
        hand_landmarks = hand_landmarks_list[idx]
        # 左右手
        handedness = handedness_list[idx]

        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style(),
        )

        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

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


model_path = "../hand_landmarker.task"

# 构建探测器
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

# 使用cv2获取livestream中的内容
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # 在这里对frame进行加工
    # frame是个3通道的numpy数组
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Step B: 转换为 Detector 要求的 Image 对象
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Step C: 传递给 detect 函数
    detection_result = detector.detect(mp_image)

    annotated_frame = draw_landmarks_on_image(frame, detection_result)

    # 再将frame转换rgb

    cv2.imshow("Live Stream", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
