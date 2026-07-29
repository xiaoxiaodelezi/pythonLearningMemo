import cv2
import numpy as np
# import mediapipe

cap = cv2.VideoCapture(0)

# 读取文件就直接输入文件名

fourCC = cv2.VideoWriter.fourcc("X", "2", "6", "4")
fps = 20
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter("./MyDemo.mp4", fourCC, fps, (width, height))
while True:
    rec, frame = cap.read()

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    writer.write(frame)

    cv2.imshow("demo", gray)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

writer.release()
cap.release()
cv2.destroyAllWindows()
