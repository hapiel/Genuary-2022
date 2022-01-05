import vsketch
from shapely import geometry
import math

class Day05DestroyASquareSketch(vsketch.SketchClass):
    
    grid_w = vsketch.Param(11)
    grid_h = vsketch.Param(7)
    square_size = vsketch.Param(8.5)
    buffer_size = vsketch.Param(8.5)

    mask_max = vsketch.Param(1.2)
    mask_min = vsketch.Param(0.1)

    fade_x = vsketch.Param(True)
    fade_y = vsketch.Param(True)

    layers = vsketch.Param(2)

    middle_square = vsketch.Param(True)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")

        grid_size = self.square_size + self.buffer_size

        for x in range (self.grid_w):
            for y in range (self.grid_h):



                square = geometry.Polygon([[0,0], [0,1], [1,1], [1,0]])

                # position of the masking square
                mask_pos = vsk.random(4)
                if mask_pos < 1:
                    mx = 0 
                    my = mask_pos 
                elif mask_pos < 2:
                    mx = 1
                    my = mask_pos - 1
                elif mask_pos < 3:
                    mx = mask_pos - 2
                    my = 0
                elif mask_pos:
                    mx = mask_pos - 3
                    my = 1

                # center positions

                # mx, my = mx - 0.5, my - 0.5

                # size of the masking circle
                dist_x_center = abs(self.grid_w / 2 - (x + 0.5))
                dist_y_center = abs(self.grid_h / 2 - (y + 0.5))

                max_dist = ((0, self.grid_w)[self.fade_x] + (0, self.grid_h)[self.fade_y]) / 2
                dist_from_center = (0, dist_x_center)[self.fade_x] + (0, dist_y_center)[self.fade_y]
                
                c_rad = vsk.map( dist_from_center, 0, max_dist + 0.001, self.mask_min, self.mask_max) 

                
                coords = [(mx - c_rad, my - c_rad),(mx + c_rad, my - c_rad), (mx + c_rad, my + c_rad), (mx - c_rad, my + c_rad)]

                mask_square = geometry.Polygon(coords)
                mask_circle = geometry.Point(mx,my).buffer(c_rad)

                # mixing up the masking styles
                if vsk.random(1) > 0.5:
                    # mask the square with circle
                    mx = vsk.map(mx, 0, 1, -0.5, 1.5)
                    my = vsk.map(my, 0, 1, -0.5, 1.5)
                    mask_shape = mask_circle
                else: 
                    mask_shape = mask_square
                    
                broken_square = square.boundary.difference(mask_shape)

                # random layer
                vsk.stroke(int(vsk.random(self.layers)) +1)

                with vsk.pushMatrix():
                    vsk.translate( grid_size * x, grid_size * y)
                    vsk.scale( self.square_size)

                    if x == int(self.grid_w / 2) and y == int(self.grid_h / 2) and self.middle_square:
                        vsk.stroke(self.layers + 1)
                        for i in range(100):
                            vsk.geometry(square)
                    else:
                        vsk.geometry( broken_square)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day05DestroyASquareSketch.display()
