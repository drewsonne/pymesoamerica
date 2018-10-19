from tempfile import NamedTemporaryFile
from urllib.request import urlretrieve

import cv2
import numpy as np

from pymesoamerica.codices import Catalogue


class AnalyseGrids(object):
    def __init__(self, codex):
        self._codex = Catalogue().get(codex)

    def run(self):
        return list(map(self._process_image, self._codex.images()[1:]))

    def _process_image(self, image):
        with NamedTemporaryFile(suffix='.jpg') as img_file:
            urlretrieve(image['href'], img_file.name)
            img_file.seek(0)

            img = cv2.imread(img_file.name)
            _, _, gray = cv2.split(img)
            # self.show_image(gray)

            self._find_contoured_lines(gray, img)
            # self._find_straight_lines(gray, img)

            self.show_image(img)

    def _find_contoured_lines(self, gray, img):
        ret, thresh = cv2.threshold(gray, 100, 50, cv2.THRESH_TOZERO_INV)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

    def _find_straight_lines(self, gray, img):
        # gray = cv2.cvtColor(red_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        adapt_type = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        thresh_type = cv2.THRESH_BINARY_INV
        bin_img = cv2.adaptiveThreshold(blur, 255, adapt_type, thresh_type, 11, 2)

        rho, theta, thresh = 2, np.pi / 180, 1100
        lines = cv2.HoughLines(bin_img, rho, theta, thresh)
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2)

    def show_image(self, img):
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
