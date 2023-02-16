import os
import shutil
import cv2
from datetime import datetime
import numpy as np
import logging

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):

        if self.y != other.y:
            return self.y < other.y
        else:
            return self.x < other.x

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Rect:

    def __init__(self, x, y, w, h):
        self.bl = Point(x, y)
        self.tr = Point(x + w, y + h)
        self.w = w
        self.h = h

    def __str__(self):
        return f"bl: {self.bl} tr: {self.tr}  w: {self.w}  h: {self.h}"


def is_equal(a, b, e):
    return abs(a - b) < e


def updatePolygon(polygon, P_bl, P_br, P_tl):

    up_left = Point(P_bl.x, P_tl.y)
    up_right = Point(P_br.x, P_tl.y)
    insert_up_left, insert_up_right = True, True

    if up_right in polygon:
        polygon.remove(up_right)
        insert_up_right = False

    if up_left in polygon:
        polygon.remove(up_left)
        insert_up_left = False

    if P_bl in polygon:
        polygon.remove(P_bl)

    if P_br in polygon:
        polygon.remove(P_br)

    if insert_up_left:
        polygon.append(up_left)

    if insert_up_right:
        polygon.append(up_right)

    return polygon


def find_points_triangle(polygon):
    polygon_cp = polygon.copy()

    # bottom_left (bl), bottom_right (br), top_left (tl)
    P_bl, P_br, P_tl = None, None, None
    sorted_polygon = sorted(polygon, reverse=False)
    P_bl = sorted_polygon[0]

    the_rest_polygon = []
    for point in polygon_cp:
        if P_bl != point:
            if P_bl.x <= point.x:
                the_rest_polygon.append(point)

    P_br = min(sorted(the_rest_polygon, reverse=False))

    the_rest_polygon = []
    for point in polygon:
        if point != P_bl and point != P_br:
            if point.x == P_bl.x or point.y == P_bl.y:
                the_rest_polygon.append(point)

    P_tl = min(the_rest_polygon, key=lambda k: [k.x, k.y])

    return P_bl, P_br, P_tl


def poly2rec(polygon):
    rectangles = []
    while len(polygon) > 0:
        P_bl, P_br, P_tl = find_points_triangle(polygon)

        # print( "P_bl: ", P_bl, " P_br: ", P_br, "P_tl: ", P_tl)
        rect = Rect(P_bl.x, P_bl.y,
                    P_br.x - P_bl.x, P_tl.y - P_bl.y)

        rectangles.append(rect)

        updatePolygon(polygon, P_bl, P_br, P_tl)

    return rectangles

def info():
    logging.info("im here")
    
def main():

    polygon = [

        # CASE 1
        # Point(0, 1),
        # Point(0, 2),
        # Point(2, 2),
        # Point(2, 0),
        # Point(1, 0),
        # Point(1, 1)

        # CASE 2
        # Point(0, 1),
        # Point(0, 2),
        # Point(3, 2),
        # Point(3, 1),
        # Point(2, 1),
        # Point(2, 0),
        # Point(1, 0),
        # Point(1, 1)

        # CASE 3
        # Point(44352, 0),
        # Point(44352,18997),
        # Point(60034,18997),
        # Point(60034,24623),
        # Point(68048,24623),
        # Point(68048,36968),
        # Point(45240,36968),
        # Point(45240,40008),
        # Point(5614,40008),
        # Point(5614,26366),
        # Point(0,26366),
        # Point(0,1440),
        # Point(1440,1440),
        # Point(1440,0)

        # CASE 4
        # Point(0,0),
        # Point(0,12328),
        # Point(19032,12328),
        # Point(19032,2745),
        # Point(11948,2745),
        # Point(11948,0)

        # CASE 5
        # Point(22176,0),
        # Point(22176,27578),
        # Point(5614,27578),
        # Point(5614,26366),
        # Point(0,26366),
        # Point(0,1440),
        # Point(1440,1440),
        # Point(1440,0)

        # CASE 6
        Point(0,240),
        Point(0,740),
        Point(740,740),
        Point(740,0),
        Point(300,0),
        Point(300,200),
        Point(200,200),
        Point(200,240)
    ]

    # get rectangles
    polygon_cp = polygon.copy()
    rectangles = poly2rec(polygon)

    # visualize 
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 f"logs/poly2rec_{datetime.now().strftime('%Y-%m-%d')}")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    else:
        if os.path.isdir(save_path):
            shutil.rmtree(save_path)  # remove dir and all contains
            os.makedirs(save_path)
        else:
            raise ValueError("file {} is not a file or dir.".format(save_path))
        
    # logging
    logging.root.name = f"poly2rec"
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)-2s] %(message)s",
        handlers=[
            logging.FileHandler(
                os.path.join(save_path, f"poly2rec.log"),
                mode='w'
            ),
            logging.StreamHandler()
        ]
    )

    points_X = [] # store x coodinates
    points_Y = [] # store y coordinates
    

    for point in polygon_cp:
        points_X.append(point.x) # Xs 
       
        points_Y.append(point.y)  # Ys
    
    # width, height
    width = int(max(points_X))
    height = int(max(points_X))

    img = 255 * np.ones((height, width), dtype=np.uint8)
    
    pts = []
    for point in polygon_cp:
        pts.append([point.x, point.y])

    
    # draw the polygon with black colors
    cv2.fillPoly(img, pts=[np.array(pts)], color=(0, 0, 0))

    # save orignial polygon 
    image_file = os.path.join(save_path, 'polygon.png')
    cv2.imwrite(image_file, img)

    # draw rectangles
    for rec in rectangles:

        # print rectangles (bottom_left, top_right, width, height)
        logging.info(f"bottom_left ({rec.bl.x},{rec.bl.y}) top_right ({rec.tr.x}, {rec.tr.y}), width: {rec.w}, height: {rec.h}")

        cv2.rectangle(img, (rec.bl.x, rec.bl.y), (rec.bl.x + rec.w, rec.bl.y + rec.h), (255, 255, 255), 1)

    # save the polygon with rectanges
    image_file = os.path.join(save_path, 'polygon_with_rectangles.png')
    cv2.imwrite(image_file, img)



if __name__ == '__main__':
    main()