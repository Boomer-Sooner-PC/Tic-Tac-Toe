import time
import math
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import imutils
import numpy as np
from imutils.perspective import four_point_transform


def takePicture(index, cam):
    cam = cv2.VideoCapture(cam)
    ret, frame = cam.read()
    cv2.imwrite(f"image{index}.png", frame)
    cam.release()
    crop(f"image{index}.png", index)


def crop(path, index):
    print("Sharpening Image")

    img = Image.open(path)
    enhance = ImageEnhance.Sharpness(img)
    img = enhance.enhance(2)
    img.save(path)

    print("Reading image")
    image = cv2.imread(path)
    # convert to greyscale and find edges
    print("processing image")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 10, 50)

    # find the right contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if has 4 corners then wer have the contour

        screenCnt = np.array([[960, 45], [1640, 330], [1150, 1000], [350, 420]])

    image = cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    warped = four_point_transform(image, screenCnt.reshape(4, 2))
    warped = cv2.resize(warped, (900, 900))
    edged = cv2.Canny(warped, 0, 85)
    cv2.imwrite("noEdge.jpg", warped)
    cv2.imwrite("processed.jpg", edged)



def devide(path, index):
    print("Splitting image")
    image = Image.open(path)
    crops = [
        (0, 0, 300, 300),
        (300, 0, 600, 300),
        (600, 0, 900, 300),
        (0, 300, 300, 600),
        (300, 300, 600, 600),
        (600, 300, 900, 600),
        (0, 600, 300, 900),
        (300, 600, 600, 900),
        (600, 600, 900, 900)
    ]
    i = 1
    for crop in crops:
        img = image.crop(crop)
        img.save(f'images/{index}image{i}.jpg')
        img = Image.open(f'images/{index}image{i}.jpg')
        img.save(f'images/{index}image{i}.jpg')
        i += 1


def calculate():
    i = 1
    diffs = {}
    for suf in range(1, 10):
        obj = {}
        for pre in range(1, 3):
            path = f'images/{pre}image{suf}.jpg'
            img = cv2.imread(path, 0)
            obj[pre] = img
        dif = (np.average(obj[2]) - np.average(obj[1]))
        dif = abs(math.floor(dif))
        diffs[suf] = dif

    print(diffs)
    result = max(diffs, key=diffs.get)
    return result


if __name__ == "__main__":
    takePicture("1", cam=0)
    devide("processed.jpg", 1)
