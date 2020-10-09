import cv2
import numpy as np
import imutils
import pyautogui
import pytesseract
from Coordinate import Coordinate


class ImageAnalyzer(object):
    THRESHOLD = .45

    @staticmethod
    # todo refactor find_text return coordinates of found text
    # todo make separate method to scrape all text from image and return text
    def find_text(rect_coord: Coordinate, text: str):
        # uncomment out line below to run on windows, you must install pytesseract first, please see
        # install_instructions.txt for detailed instructions pytesseract.pytesseract.tesseract_cmd = "C:\Program
        # Files (x86)\Tesseract-OCR\tesseract.exe"
        text_found = False
        image = pyautogui.screenshot(
            region=(rect_coord.topLeftX, rect_coord.topLeftY, rect_coord.bottomRightX, rect_coord.bottomRightY))
        image_text = pytesseract.image_to_string(image)
        if image_text.__contains__(text):
            text_found = True

        return text_found

    # find and locate template image within source image
    # returns list of coordinates for found image
    def find_in_image(self, template_path: str, source_path: str):
        # load template image and source image and convert to grayscale
        template = cv2.imread(template_path)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        image = cv2.imread(source_path)
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

        # scale image from half its original size to 1.5 times its original size by 30 equal increments to ensure image
        # found even if size differs
        found = None
        coords = Coordinate()
        for scale in np.linspace(.5, 1.5, 30)[::-1]:
            resized = imutils.resize(gray_image, width=int(gray_image.shape[1] * scale))
            r = gray_image.shape[1] / float(resized.shape[1])
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break
            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # find best match if multiple matches are found within threshold
            if found is None or maxVal > found[0]:
                if maxVal > self.THRESHOLD:
                    coords.imageFound = 1
                found = (maxVal, maxLoc, r)

        # return None if no image found
        if found is None:
            return None

        (_, maxLoc, r) = found
        # define top left and bottom right of found image
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

        # convert to Coordinate data type
        coords.topLeftX = startX
        coords.topLeftY = startY
        coords.bottomRightX = endX
        coords.bottomRightY = endY

        return coords

    # find template image in source image and draw rectangle around found image
    def find_image_draw_rectangle(self, template_path: str, source_path: str):
        # load template image and source image and convert to grayscale
        template = cv2.imread(template_path)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        image = cv2.imread(source_path)
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

        # scale image from half its original size to 1.5 times its original size by 30 equal increments to ensure image
        # found even if size differs
        found = None
        coords = Coordinate()
        for scale in np.linspace(.5, 1.5, 30)[::-1]:
            resized = imutils.resize(gray_image, width=int(gray_image.shape[1] * scale))
            r = gray_image.shape[1] / float(resized.shape[1])
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break
            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # find best match if multiple matches are found within threshold
            if found is None or maxVal > found[0]:
                if maxVal > self.THRESHOLD:
                    coords.imageFound = 1
                found = (maxVal, maxLoc, r)

        # return none if image not found
        if found is None:
            return None
        (_, maxLoc, r) = found

        # define top left and bottom right of found image
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

        # Draw rectangle
        cv2.rectangle(gray_image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.imshow("Image", gray_image)
        cv2.waitKey(0)

        # convert to Coordinate data type
        coords.topLeftX = startX
        coords.topLeftY = startY
        coords.bottomRightX = endX
        coords.bottomRightY = endY

        return coords

    # find template image on current screen
    def find_on_screen(self, template_path: str):
        # load template image and source image and convert to grayscale
        template = cv2.imread(template_path)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        image = pyautogui.screenshot()
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

        # scale image from half its original size to 1.5 times its original size by 30 equal increments to ensure image
        # found even if size differs
        found = None
        coords = Coordinate()
        for scale in np.linspace(.5, 1.5, 30)[::-1]:
            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break
            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # find best match if multiple matches are found within threshold
            if found is None or maxVal > found[0]:
                if maxVal > self.THRESHOLD:
                    coords.imageFound = 1
                found = (maxVal, maxLoc, r)

        # return none if image not found
        if found is None:
            return None
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

        # convert to Coordinate data type
        coords.topLeftX = startX
        coords.topLeftY = startY
        coords.bottomRightX = endX
        coords.bottomRightY = endY

        return coords

    # find multiple instances of image on current screen
    def find_all_onscreen(self, image_path: str):
        # load template image and convert to grayscale
        template = cv2.imread(image_path)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        image = pyautogui.screenshot()
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

        # scale image from half its original size to 1.5 times its original size by 30 equal increments to ensure image
        # found even if size differs
        found = None
        loc = None
        for scale in np.linspace(0.1, 2, 20)[::-1]:
            resized = imutils.resize(gray_image, width=int(gray_image.shape[1] * scale))
            r = gray_image.shape[1] / float(resized.shape[1])
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break
            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)

            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            #find all images which pass the threshold of .6
            if found is None or maxVal > found[0]:
                if maxVal > self.THRESHOLD:
                    thresh = .6
                    loc = np.where(result >= thresh)
                found = (maxVal, maxLoc, r)

        #convert all image points to list of Coordinate datatype
        coord_list = list()
        if loc is not None:
            for pt in zip(*loc[::-1]):
                coord = Coordinate()
                coord.topLeftX = pt[0]
                coord.topLeftY = pt[1]
                coord.bottomRightX = pt[0] + tW
                coord.bottomRightY = pt[1] + tH
                coord.imageFound = 1
                coord_list.append(coord)

        return coord_list


# to run quick demonstration of image analyzer's find_image_draw_rectangle method uncomment below lines and run
# python file
ia = ImageAnalyzer()
ia.find_image_draw_rectangle("car.png", "caronroad.jpeg")
