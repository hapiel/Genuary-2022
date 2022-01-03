
import sys, os
sys.path.append(os.path.abspath("D:\9mediatech\python\genuary"))

import vsketch
import utils 
from skimage import io
import math
import random
import csv


img = io.imread("Henri-edmond-cross-a-pine-tree-bw.jpg")


class Day02DitheringSketch(vsketch.SketchClass):

    detail = vsketch.Param(10)
    len1 = vsketch.Param(3)
    len2 = vsketch.Param(7)
    len3 = vsketch.Param(30)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("200mmx125mm", landscape=True)
        vsk.scale("mm")

        points = []
        points_abs = []
        
        for y, row in enumerate(img[::self.detail]):
            for x, color in enumerate(row[::self.detail]):
                if color[0] < 160:
                    if vsk.random(color[0]) < 8:
                        xc = vsk.map(x, 0, len(row) / self.detail, 0, utils.css_to_mm(vsk.width) - 10)
                        yc = vsk.map(y,  0, len(row) / self.detail, 0, utils.css_to_mm(vsk.width) - 10) 
                        # vsk.circle(xc, yc, 0.2)
                        points.append((xc, yc))
                        points_abs.append((x, y))
                        
        with open('tree.csv', mode='w') as file:
            write = csv.writer(file, lineterminator = '\n')
            write.writerows(points_abs)
        
        print(len(points))
        point1 = random.choice(points)

        while len(points) > 1:
            points.remove(point1)
            point2 = random.choice(points)
            for _ in range(2000):
                if math.dist(point1,point2) < self.len1:
                    break
                point2 = random.choice(points)
            else: 
                for _ in range(2000):
                    if math.dist(point1,point2) < self.len2:
                        break
                    point2 = random.choice(points)
                else: 
                    for _ in range(2000):
                        if math.dist(point1,point2) < self.len3:
                            break
                        point2 = random.choice(points)
                    else: 
                        points.remove(point2)
                        points.append(point1)
                        continue


            vsk.line(point1[0], point1[1], point2[0], point2[1])
            point1 = point2
        
        



    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("rotate 270 pagesize --landscape 200mmx125mm linemerge linesimplify reloop linesort gwrite last.gcode")


if __name__ == "__main__":
    Day02DitheringSketch.display()
