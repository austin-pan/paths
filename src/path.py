# import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import math

# File to handle "path" objects
class path:
    def __init__(self, file_path, color):
        self.raw_img = cv.imread(file_path)
        self.img = self.raw_img
        image_paths = self.extract_paths(color)
        image_vertices = self.place_vertices(image_paths)
        # adj_mat = self.to_adj_mat(image_paths)

    def extract_paths(self, color):
        print("extracting ", color)
        [r1, g1, b1] = color # Original value
        r2, g2, b2 = 255, 255, 255 # Value that we want to replace it with

        red, green, blue = self.raw_img[:, :, 0], self.raw_img[:, :, 1], self.raw_img[:, :, 2]
        mask = (red <= 70) & (green >= 200) & (blue <= 70)
        self.img[:, :, :3][~mask] = [b2, g2, r2]

        self.gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        ret, self.gray = cv.threshold(self.gray, 200, 255, cv.THRESH_BINARY_INV)
        element = cv.getStructuringElement(cv.MORPH_CROSS,(3,3))
        self.gray = cv.dilate(self.gray, element)

        self.skel = self.skeletonize(self.gray) 
        # print("white pixels left: ", np.sum(self.img[:, :, :3] == [255, 255, 255]))

        # self.skel = cv.ximgproc.thinning(self.gray)

        lines = cv.HoughLinesP(self.skel, 1, np.pi / 180, threshold = 10, minLineLength = 3, maxLineGap = 10)
        print(len(lines))
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # if x1 == x2:
            #     x1, y1, x2, y2 = self.extend_line(x1, y1, x2, y2)
            cv.line(self.img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # self.img = self.skel
        return lines


    def extend_line(self, x1, y1, x2, y2):
        slope = self.slope(x1, y1, x2, y2)

        return [x1, y1, x2, y2]


    def skeletonize(self, img):
        size = np.size(img)
        skel = np.zeros(img.shape,np.uint8)

        element = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
        done = False

        while not done:
            eroded = cv.erode(img, element)
            temp = cv.dilate(eroded, element)
            temp = cv.subtract(img, temp)
            skel = cv.bitwise_or(skel, temp)
            img = eroded.copy()

            zeros = size - cv.countNonZero(img)
            if zeros == size:
                done = True

        return skel


    def place_vertices(self, image_paths):
        vertices = []
        for i in range(len(image_paths)):
            for j in range(i):
                intersection = self.segment_intersection(image_paths[i][0], image_paths[j][0])
                vertices.append(intersection)

                cv.circle(self.img, intersection, radius = 0, color = (255, 0, 0), thickness = 5)
        return vertices


    def save_image(self):
        cv.imwrite('../bin/paths_edited.png', self.img)


    def segment_intersection(self, line0, line1):
        p0x, p0y, p1x, p1y = line0 
        p2x, p2y, p3x, p3y = line1
        s1x = p1x - p0x
        s1y = p1y - p0y
        s2x = p3x - p2x
        s2y = p3y - p2y

        denom = -s2x * s1y + s1x * s2y
        if denom == 0:
            return (0, 0)
        s = (-s1y * (p0x - p2x) + s1x * (p0y - p2y)) / denom
        t = (s2x * (p0y - p2y) - s2y * (p0x - p2x)) / denom

        if s >= 0 and s <= 1 and t >= 0 and t <= 1:
            ix = p0x + (t * s1x)
            iy = p0y + (t * s1y)
            return (int(ix), int(iy))

        return (0, 0)


    def show_image(self):
        window_name = "paths"
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)
        cv.resizeWindow(window_name, 880, 660)
        cv.imshow(window_name, self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()


    def slope(self, x1, y1, x2, y2):
        denom = x1 - x2
        if denom == 0:
            return 0
        slope = (y1 - y2) / denom
        return slope

    
    def to_adj_mat(self, image_paths):
        pass
