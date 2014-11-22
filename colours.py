import cv2
import numpy as np
import math
import random
from sets import Set
 
dr = [-1, -1, -1, 0, 0, 1, 1, 1]
dc = [-1, 0, 1, -1, 1, -1, 0, 1]
 
height = 68 #1080/16
width = 120 #1920/16
 
field = np.zeros((height * 16, width * 16, 3), dtype = "uint8")
visited = np.zeros((height * 16, width * 16), dtype = "bool")
 
total_colours = 0
colours = []
 
def distance(c1, c2):
    return math.sqrt((c1[0] - c2[0]) * (c1[0] - c2[0]) +
                     (c1[1] - c2[1]) * (c1[1] - c2[1]) +
                     (c1[2] - c2[2]) * (c1[2] - c2[2]))
 
 
def fill(queue, prev_colour):
     
    while (len(queue) > 0):
 
        current_point = queue.pop(0)
 
        rand_it =  list(range(len(dr)))
        random.shuffle(rand_it)
 
        for i in xrange(len(dr)):
            r = current_point[0] + dr[rand_it[i]]
            c = current_point[1] + dc[rand_it[i]]
 
            if (r < 0 or r >= field.shape[0]):
                continue
             
            if (c < 0 or c >= field.shape[1]):
                continue
 
            if (visited[r, c]):
                continue
 
            if ((r,c) in queue):
                continue
 
            queue.insert(0, (r, c))
 
        r = current_point[0]
        c = current_point[1]
 
        field[r, c, 0] = prev_colour[0]
        field[r, c, 1] = prev_colour[1]
        field[r, c, 2] = prev_colour[2]
 
        visited[r, c] = True
 
        print len(colours)
 
        colours.remove(prev_colour)
        if (len(colours) > 0):
            next_colour = colours[random.randint(0, len(colours) - 1)]
             
            tries = 0
 
            min_dist = 30
 
            while (distance(prev_colour, next_colour) > min_dist):
                next_colour = colours[random.randint(0, len(colours) - 1)]
                tries += 1
 
                if (tries > 0.1 * len(colours)):
                    min_dist += 0.1
 
            prev_colour = next_colour
 
        cv2.imwrite("generated/img_" + str((total_colours - len(colours))).zfill(10) + ".png", field)
 
cv2.namedWindow("field", flags = cv2.cv.CV_WINDOW_NORMAL)
 
for r in xrange(16):
    for c in xrange(16):
        for i in xrange(height):
            for j in xrange(width):
                colours.append((int((float(r * 16 + c) / 256) * 255),
                                int((float(i) / height) * 255),
                                int((float(j) / width) * 255)))
     
 
    print r, "/", 16
 
total_colours = len(colours)
 
prev_colour = colours[random.randint(0, len(colours))]
 
current_point = (random.randint(0, field.shape[0]),
                 random.randint(0, field.shape[1]))
 
queue = []
 
queue.append(current_point)
 
fill(queue, prev_colour)
 
cv2.imshow("field", field)
cv2.waitKey(0)