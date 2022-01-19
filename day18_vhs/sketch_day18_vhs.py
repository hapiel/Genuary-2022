import vsketch
import numpy as np
from shapely import geometry

from skimage import io
import math
import os

class day18VhsSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)
    vhs = vsketch.Param(1)
    line_count = vsketch.Param(80)
    seg_count = vsketch.Param(500)
    heightmm = vsketch.Param(110)
    intensity = vsketch.Param(80)
    cols = 2
    rows = 2

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx128mm", landscape=False)
        vsk.scale("mm")
        
        

        widthmm = self.heightmm * (4/3)
        

        vsk.scale(1/self.cols)
        
        for x_ in range(self.cols):
            for y_ in range(self.rows):
                with vsk.pushMatrix():
                    
                    vsk.translate(x_ * widthmm, y_ * self.heightmm)
                    vsk.scale(0.9)
                    
                    if x_ == 0 and y_ == 0:
                        img = io.imread("vhs23.png")
                    else:
                        img = io.imread(f"vhs{int(vsk.random(25)) + 1}.png")
                    
                    line_pos = np.zeros([self.line_count, self.seg_count, 2])
                    
                    for line in range(self.line_count):
                        imgy = int(vsk.map(line, 0, self.line_count -1, 0, len(img) -1))
                            
                        for seg in range(self.seg_count):
                            
                            x_dif = math.pow(abs(seg - self.seg_count/2), 2)/20000
                            y_dif = math.pow(abs(line - self.line_count/2), 2)/1000
                            
                            y = vsk.map(line, 0, self.line_count -1, x_dif, self.heightmm - x_dif)
                        
                            x = vsk.map(seg, 0, self.seg_count -1, y_dif, widthmm - y_dif)
                            imgx = int(vsk.map(seg, 0, self.seg_count -1, 0, len(img[0]) -1))
                            
                            pixel = img[imgy, imgx, 0]/ self.intensity
                            rand = vsk.random(pixel) 
                            
                            line_pos[line,seg] = [x, y + rand]
                            
                    
                    vsk.geometry(geometry.asMultiLineString(line_pos))
        

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        filename = os.path.basename(__file__)[7:-3]
        vsk.vpype(f"rotate 180 linemerge linesimplify reloop linesort gwrite {filename}.gcode")


if __name__ == "__main__":
    day18VhsSketch.display()
