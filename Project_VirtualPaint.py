import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

# Color Ranges for Detection
myColors = [[5, 107, 0, 19, 255, 255],    # Orange
            [57, 76, 0, 100, 255, 255],   # Green
            [90, 48, 0, 118, 255, 255],   # Blue
            [20, 31, 100, 255, 0, 255],   # Purple
            [133, 56, 0, 159, 156,255]]   # Yellow

# BGR Color Values for Drawing
myColorValues = [[51, 153, 255],  # Orange
                 [0, 255, 0],     # Green
                 [255, 0, 0],     # Blue
                 [0, 255, 255],   # Yellow
                 [255, 0, 255]]   # Purple

myPoints = []  ## [x , y , colorId ]

painting_enabled = True  # Flag to enable/disable virtual painting

def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        cv2.imshow(str(color[0]),mask)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 15, myColorValues[count], cv2.FILLED)
        if painting_enabled and x != 0 and y != 0:  # Check if painting is enabled
            newPoints.append([x, y, count])
        count += 1
    return newPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result", imgResult)

    # Wait for key press and perform actions
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w'):
        myPoints = []  # Clear all virtual paint
        imgResult = np.zeros_like(img)  # Clear canvas
    elif key == ord('e'):
        myPoints = []  # Stop virtual painting
    elif key == ord('d'):
        painting_enabled = not painting_enabled  # Toggle virtual painting

cap.release()
cv2.destroyAllWindows()
