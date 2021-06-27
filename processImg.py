from threading import Thread
import cv2
import pytesseract
import numpy as np


def process(image):
    img = cv2.resize(image, None, fx = 2, fy = 2, interpolation=cv2.INTER_CUBIC)
    img = cv2.bilateralFilter(img,None,9,75,75)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #gray1, thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)
    #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = np.ones((4, 5), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    print(pytesseract.image_to_string(closing, lang='eng'))
    cv2.imshow("result",img)
    cv2.imshow("gray",gray)
    cv2.imshow("thresh",thresh)
    cv2.imshow("closing",closing)
    cv2.imshow("opening",opening)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
