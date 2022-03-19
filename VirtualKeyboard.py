import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


detector = HandDetector(detectionCon=0.8,maxHands=1)
keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                         20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 12, y + 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    return img


#
# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                           20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
#                       (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#
#     out = img.copy()
#     alpha = 0.5
#     mask = imgNew.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#     return out


class Button():
    def __init__(self, pos, text, size=[40, 40]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([60 * j + 50, 60 * i + 50], key))

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    # lmList, bboxInfo = detector.findPosition(img)
    cv2.rectangle(img, (35, 35), (635, 290), (96,96,96), cv2.FILLED)
    img = drawAll(img, buttonList)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]

        if lmList1:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 0, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 12, y + 30),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
                    l, _, _ = detector.findDistance(lmList1[8], lmList1[12], img)
                    print(l)

                ## when clicked
                    if l < 30:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 12, y + 30),
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
                        finalText += button.text
                        sleep(0.2)



    cv2.rectangle(img, (35, 380), (635, 300), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, finalText, (50, 360),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)