from numpy.core.shape_base import block
import vsketch
from shapely import geometry, affinity
import numpy as np
import random
import os

# future ideas:
# windows, doors, chimneys
# perspective positioning/composition
# curved parts

np.set_printoptions(suppress=True)

class Tower():
    
    def __init__(self, vsk, other) -> None:
        
        self.o = other
        
        self.vsk = vsk
        
        self.pos = np.array([[0,0]])

        
        self.block_types = np.array([
            ["straight", self.o.block_straight],
            ["diagonal_in", self.o.block_diagonal_in],
            ["diagonal_out", self.o.block_diagonal_out],
            ["random_angle", self.o.block_random_angle]
        ], dtype=object)
        


    def add_block(self):
        vsk = self.vsk
        
        block_type = random.choices(self.block_types[:,0], weights=self.block_types[:,1])[0]
        
        if block_type == "straight":
            self.pos = np.append(self.pos, 
                [[self.pos[-1,0],
                self.pos[-1,1] -(vsk.random(self.o.block_height_rand) +self.o.block_height_min)]],
                axis=0)
            
        if block_type == "diagonal_in":
            displace = vsk.random(self.o.block_height_rand) + self.o.block_height_min
            self.pos = np.append(self.pos, 
                [[self.pos[-1,0] + displace,
                self.pos[-1,1] - displace]],
                axis=0)
            
        if block_type == "diagonal_out":
            displace = vsk.random(self.o.block_height_rand) + self.o.block_height_min
            self.pos = np.append(self.pos, 
                [[self.pos[-1,0] - displace,
                self.pos[-1,1] - displace]],
                axis=0)
        
        if block_type == "random_angle":
            self.pos = np.append(self.pos, 
                [[self.pos[-1,0] +vsk.random(self.o.block_angle_x_rand) +self.o.block_angle_x_min,
                self.pos[-1,1] -(vsk.random(self.o.block_height_rand) +self.o.block_height_min)]],
                axis=0)
        
    def add_top(self):
        vsk = self.vsk
        
        self.pos = np.append(
            self.pos, [[max(self.pos[:,0]) + vsk.random(self.o.top_w_rand) + self.o.top_w_min,
            self.pos[-1,1] - (vsk.random(self.o.top_h_rand) + self.o.top_h_min)]], axis=0)
        

    def draw_tower(self):
        vsk = self.vsk
        
        # vsk.geometry(geometry.LineString(self.pos))
        
        for i in range(self.o.line_count):
        
            scale = np.cos((np.pi/(self.o.line_count-1)) * i)
            
            scaled = affinity.scale(geometry.LineString(self.pos), scale)
            translated = affinity.translate(scaled, (max(self.pos[:,0]) - min(self.pos[:,0])) /2  * (1 - scale))
            centered = affinity.translate(translated, -(max(self.pos[:,0]) - min(self.pos[:,0])))
        
            vsk.geometry(centered)


class Day09ArchitectureSketch(vsketch.SketchClass):
    
    line_count = vsketch.Param(20)
    
    block_straight = vsketch.Param(5)
    block_diagonal_in = vsketch.Param(4)
    block_diagonal_out = vsketch.Param(4)
    block_random_angle = vsketch.Param(2)
    
    block_height_min = vsketch.Param(5)
    block_height_rand = vsketch.Param(2)
    
    block_angle_x_min = vsketch.Param(-3.5)
    block_angle_x_rand = vsketch.Param(7)
    
    block_count_min = vsketch.Param(10)
    block_count_max = vsketch.Param(15)
    
    top_h_min = vsketch.Param(5)
    top_h_rand = vsketch.Param(5)
    
    top_w_min = vsketch.Param(5)
    top_w_rand = vsketch.Param(5)


    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")
        
        vsk.line(-19,0,178,0)
        
        for x in range(5):
            
            t = Tower(vsk, self)
            for i in range(int(vsk.random(self.block_count_min, self.block_count_max))):
                t.add_block()
            t.add_top()
            t.draw_tower()
            vsk.translate(39,0)

        # implement your sketch here
        # vsk.circle(0, 0, self.radius, mode="radius")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        filename = os.path.basename(__file__)[7:-3]
        vsk.vpype(f"rotate 180 linemerge linesimplify reloop linesort gwrite {filename}.gcode")


if __name__ == "__main__":
    Day09ArchitectureSketch.display()
