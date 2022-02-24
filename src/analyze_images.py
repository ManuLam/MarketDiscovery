import time

from PIL import Image
from pytesseract import image_to_string, pytesseract
from skimage.metrics import structural_similarity
import cv2
import numpy as np

pytesseract.tesseract_cmd = "C:\\Users\\Manu\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

def cv2_show_image(image):
    cv2.imshow("Compare", image)


def cv2_save_show_image(image1, image2, show=False, save=False):
    im_h = cv2.hconcat([image1, image2])

    if show:
        cv2.imshow("Compare", im_h)
    if save:
        cv2.imwrite("compare\\diff." + time.strftime("%Y%m%d-%H%M%S") + ".png", im_h)

    return im_h


def image_compare(before, after):
    before = cv2.imread(before)
    after = cv2.imread(after)

    # Convert images to grayscale
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    print("Image similarity", score)

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1]
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(before.shape, dtype='uint8')
    filled_after = after.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(before, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

    return cv2_save_show_image(before, after)

def image_compute_numbers(image, show=True):
    img = Image.open(image)
    array = image_to_string(img, config='-c tessedit_char_whitelist=01234567890 --psm 6').replace(" ", "").split("\n")
    array = filter(lambda item: item, array)



    if show:
        cv2_show_image(cv2.imread(image))

    return array