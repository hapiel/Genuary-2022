import enum
import sys, os

from numpy.lib.function_base import angle

# location of utils file:
sys.path.append(os.path.join(os.path.abspath(__file__), "../../"))
import utils 

import vsketch
import numpy as np
import math
import copy

points = np.array([[0.,0.,0.]])

def find_angle(a, b, c):
    ba = a-b
    bc = c-b

    cos_a = utils.clamp(np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc)), -1, 1)
    return np.arccos(cos_a)

class Snake:

    def __init__(self, vsk, other, pos):

        self.o = other

        self.pos = np.array(pos, dtype=float)
        self.vel = np.array([0., 0.])
        self.vel_prev = np.array([0., 0.])
        self.pos_prev = np.array([0., 0.])

        self.step_size = vsk.random(self.o.snake_growth_r) + self.o.snake_growth_min

        self.step_pos = np.pi + 0.4
        self.scale = vsk.random(self.o.snake_scale) + self.o.snake_min_scale
        self.rad = 0

        self.positions = np.array([[0.,0.,0.]])

    def place(self, vsk):
        while self.step_pos < np.pi * 3 :
            # prev self
            self.vel_prev = copy.copy(self.vel)
            self.pos_prev = copy.copy(self.pos)

            # select velocity from noise array
            x_scaled = utils.clamp(int( self.pos[0] /self.o.n_size), 0, len(self.o.n_vec   ) - 1)
            y_scaled = utils.clamp(int( self.pos[1] /self.o.n_size), 0, len(self.o.n_vec[0]) - 1)

            self.vel += self.o.n_vec[x_scaled][y_scaled] *3

            # adjust velocity to current step
            self.vel = self.vel / np.linalg.norm(self.vel) * (math.cos(self.step_pos)+1) * self.scale
            self.step_pos += self.step_size

            # update position
            self.pos += self.vel

            if self.pos[0] < 0 or self.pos[1] < 0 or self.pos[0] > self.o.widthmm or self.pos[1] > self.o.heightmm:
                break

            if self.add_positions(vsk): break


        # no break
        else:
            global points
            points = np.append(points, self.positions, axis=0)

            # for pos in self.positions:
            #     self.draw_circles(vsk, *pos)
            
            self.draw_arcs(vsk, self.positions)

    def draw_circles(self, vsk, x, y, rad):
        vsk.circle(x, y, rad * 2)
    
    def draw_arcs(self, vsk, positions):

        # skip first & last 2
        for i, pos in enumerate(positions[2:-3]):
            i += 2
            angle_prev = 0.1
            angle_next = np.pi
            
            # skip first and last
            if i > 0 and i < len(positions) -1:
                angle_prev = find_angle(positions[i][:2] + [1, 0], positions[i][:2], positions[i -1][:2])
                if positions[i][1] < positions[i -1][1]:
                    angle_prev = -angle_prev

                angle_next = find_angle(positions[i][:2] + [1, 0], positions[i][:2], positions[i +1][:2])
                if positions[i][1] < positions[i +1][1]:
                    angle_next = -angle_next

                if i % 2 == 0: angle_next, angle_prev = angle_prev, angle_next
                vsk.arc(*pos, pos[2], angle_prev, angle_next, mode="radius")

            # debug lines
            # with vsk.pushMatrix():
            #     vsk.translate(*pos[:2])
            #     with vsk.pushMatrix():
            #         vsk.rotate(angle_next )
            #         vsk.line(0,0,2,0)
            #     vsk.rotate(angle_prev )
            #     vsk.line(0,0,2,0)


    def add_positions(self, vsk):
        
        rad_prev = self.rad 
        # distance between previous and current spot
        dist = math.dist(self.pos, self.pos_prev)

        self.rad = abs(dist - rad_prev)

        global points


        range = self.o.snake_scale + self.o.snake_min_scale
        near_x = points[points[:,0] > self.pos[0] - range]
        near_x = near_x[near_x[:,0] < self.pos[0] + range]
        near_xy = near_x[near_x[:,1] > self.pos[1] - range]
        near_xy = near_xy[near_xy[:,1] < self.pos[1] + range]


        for point in near_xy:
            if math.dist(point[:2], self.pos) - self.rad < point[2] + self.o.snake_buffer:
                # break the sequence
                return True
                
        
        self.positions = np.append(self.positions, [[*self.pos, self.rad]], axis=0)
        


class Day04FidenzaSketch(vsketch.SketchClass):

    n_size = vsketch.Param(5.0)
    n_wildness = vsketch.Param(20.0)
    n_show = vsketch.Param(False)

    snake_count = vsketch.Param(50)
    snake_scale = vsketch.Param(3.0)
    snake_min_scale = vsketch.Param(0.8)

    snake_buffer = vsketch.Param(0.5)
    snake_growth_r = vsketch.Param(0.5)
    snake_growth_min = vsketch.Param(0.1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        # reset global var
        global points
        points = np.array([[0.,0.,0.]])

        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")

        self.widthmm = utils.css_to_mm(vsk.width*0.9)
        self.heightmm = utils.css_to_mm(vsk.height*0.9)

        perlin = vsk.noise(
            np.linspace(0., 1., int(self.widthmm / self.n_size)), 
            np.linspace(0., 1., int(self.heightmm / self.n_size)))
        
        rot = perlin * np.pi * self.n_wildness + vsk.random(np.pi * 2)
        vx = np.cos(rot)
        vy = np.sin(rot)
        self.n_vec = np.stack((vx, vy), axis= -1)
        
        def line_grid():
            vsk.stroke(2)
            for x, col in enumerate(self.n_vec):
                for y, num in enumerate(col):
                    with vsk.pushMatrix():
                        vsk.translate(x * self.n_size, y * self.n_size)
                        vsk.line(0,0,num[0] * self.n_size,num[1] * self.n_size)
            vsk.stroke(1)
        
        if self.n_show: line_grid()
        
        


        for i in range(self.snake_count):
            snake = Snake(vsk, self, (vsk.random(self.widthmm),vsk.random(self.heightmm)))
            snake.place(vsk)
        # for i in range(50):
        #     snake.update(1)
        #     snake.draw_circles(vsk)
        


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("rotate 180 linemerge linesimplify reloop linesort gwrite last.gcode")


if __name__ == "__main__":
    Day04FidenzaSketch.display()
