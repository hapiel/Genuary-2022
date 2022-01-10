import vsketch
from shapely import geometry, affinity
import math
import os

def lb(shape):
    # align left bottom
    return affinity.translate(shape, -shape.bounds[0], shape.bounds[1])
    

class Day10MachineLearningSketch(vsketch.SketchClass):

    
    book_width_min = vsketch.Param(0.3)
    book_width_max = vsketch.Param(2)
    

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")


        square = geometry.Polygon([(0,0), (1,0),(1,1), (0,1)])

        shelve = affinity.scale(square, 30, 10)

        shelve_w = 30
        shelve_h = 10
        
        for x in range(5):
            vsk.resetMatrix()
            vsk.scale("mm")
            vsk.translate(32*x, 0)
            for y in range(8):
                
                vsk.translate(0,12)
                vsk.geometry(lb(shelve))
            
                space_remain = shelve_w
                pos = 0
                prev_book = 0
                rotated = False
                rotation = 20
                while space_remain > 1:
                    
                    next_rotated = rotated
                    if vsk.random(1) < 0.03:
                        rotated = True
                    
                    book_h = vsk.random(5, min(5 + space_remain/4, shelve_h))
                    
                    book_w = min(vsk.random(self.book_width_min, self.book_width_max), space_remain )
                    if book_w < self.book_width_min: break
                    
                    book = affinity.scale(square, book_w, book_h)
                    book = affinity.rotate(book, -rotation *rotated) 

                    
                    book = lb(book)
                    
                    book_coords = book.exterior.coords
                    
                    book_trans = affinity.translate(
                        book, 
                        pos - (book_coords[3][0] - book_coords[0][0] )*next_rotated + math.tan(math.radians(rotation)) * prev_book )

                    pos =  book_trans.bounds[2] 
                    
                    prev_book = book_coords[3][1] - book_coords[2][1]

                    vsk.geometry(book_trans)
                    
                    space_remain -=  (book.bounds[2] - book.bounds[0]) 
                    
                    # stop early
                    if shelve_w * 0.5 > space_remain and vsk.random(1) < 0.05:
                        break
                    
                    if rotated and vsk.random(1) < 0.5:
                        break
                    
                
        
        
        


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        filename = os.path.basename(__file__)[7:-3]
        vsk.vpype(f"rotate 180 linemerge linesimplify reloop linesort gwrite {filename}.gcode")


if __name__ == "__main__":
    Day10MachineLearningSketch.display()
