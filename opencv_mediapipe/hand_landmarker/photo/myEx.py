import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 设定基本model
# 模型预先下载好，也可以使用url来下载
# 载入模型
base_options = python.BaseOptions(model_asset_path="../hand_landmarker.task")
# 构建option
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
# 创建handlandmarker探测器
detector = vision.HandLandmarker.create_from_options(options)

# mp.Image有create_from_file这个api来获取照片的numpy数组
# 注意数组的通道数
# jpg进过检验，并非是网上说的3通道，是4通道的
# 并且要注意，是rgb还是bgr
# 这个api获得的是rgb的
image = mp.Image.create_from_file("woman_hands.jpg")
# 模型计算，获取结果
detector_result = detector.detect(image)


# 在图像上标记
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


annotated_image = draw_landmarks_on_image(image.numpy_view()[:, :, :3], detector_result)

cv2.imshow("woman_hands", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
cv2.waitKey(0)
cv2.destroyAllWindows()
