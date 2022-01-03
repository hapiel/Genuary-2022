import sys, os
from numpy import half
from shapely.geometry import geo
from shapely.geometry.multilinestring import MultiLineString
sys.path.append(os.path.abspath("D:\9mediatech\python\genuary"))

import vsketch
import utils 
import math
from shapely import geometry, affinity

class Day03SpaceSketch(vsketch.SketchClass):

    range = vsketch.Param(50)
    force = vsketch.Param(0.8)
    dia = vsketch.Param(80)
    line_count = vsketch.Param(100)
    noise_x_scale = vsketch.Param(50)
    noise_y_scale = vsketch.Param(10)
    noise_strength = vsketch.Param(10)
    rotation = vsketch.Param(-5)

    bg_step = vsketch.Param(0.4)

    ring_squish = vsketch.Param(0.3)
    ring_min = vsketch.Param(70)
    ring_max = vsketch.Param(90)
    outer_displace = vsketch.Param(2.5)
    ring_count = vsketch.Param(12 )

    planet_x = vsketch.Param(70)
    planet_y = vsketch.Param(10)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("200mmx125mm", landscape=False)
        vsk.scale("mm")

        widthmm = utils.css_to_mm(vsk.width)
        heightmm = utils.css_to_mm(vsk.height)


        attractor = (self.dia/2 + 20, self.dia*1.2)
        repulsor = (self.dia/2 + 20, self.dia*0.4)
        # vsk.circle(*attractor, 10)
        # vsk.circle(*repulsor, 10)

        lines = []
        for y in range(self.line_count):
            points = []
            for x in range(self.dia*3):

                x_map = vsk.map(x, 0, self.dia*3, 0, self.dia + 40)
                y_map = vsk.map(y, 0, self.line_count, 0, self.dia + 40)

                y_noise = vsk.noise(x/self.noise_x_scale, y/self.noise_y_scale)*self.noise_strength + y_map

                dist = min(math.dist(attractor, (x_map,y_noise)), self.range)
                y_grav = vsk.map(self.range - dist, 0, self.range, 0, self.force)
                y_interpolated = vsk.lerp(y_noise, attractor[1], y_grav)

                dist2 = min(math.dist(repulsor, (x_map,y_interpolated)), self.range)

                y_grav2 = vsk.map(self.range - dist2, 0, self.range, 0, self.force)
                y_2 = y_interpolated + y_grav2 * 20
                # y_interpolated2 = vsk.lerp(y_interpolated, repulsor[1], y_grav2 )

                points.append((x_map, y_2 ))
            lines.append(points)
        
        linestrings = []
        for point in lines:
            linestrings.append(geometry.LineString(point))

        

        p_trans = (self.planet_x, self.planet_y)

        multiline = geometry.MultiLineString(linestrings)
        # vsk.geometry(multiline)
        circle = geometry.Point(self.dia/2 + 20, self.dia/2 + 20).buffer(self.dia/2)

        planet = multiline.intersection(circle)

        circle = affinity.translate(circle, *p_trans)
        planet = affinity.translate(planet, *p_trans)
        planet = affinity.rotate(planet, self.rotation)

        bg_lines_coords = []

        bg_line_count = utils.css_to_mm(vsk.height) / self.bg_step

        for y in range(int(bg_line_count)):
            y = vsk.map(y, 0, bg_line_count , 0, utils.css_to_mm(vsk.height))
            bg_lines_coords.append(((-10,y),(210,y)))
            
        bg_lines = geometry.MultiLineString(bg_lines_coords)
        canvas = geometry.Polygon([(0,0), (200,0), (200,125), (0,125)])
        bg_lines = bg_lines.intersection(canvas).difference(circle)



        ring_count = self.ring_count
        rings = []
        for r in range(ring_count):
            if r == 0: continue
            pos = vsk.map(r, 0, ring_count, 0, self.outer_displace)
            size = vsk.map(r, 0, ring_count, self.ring_min, self.ring_max)
            rings.append(affinity.scale(geometry.Point(0, pos).buffer(size, resolution = 48), 1, self.ring_squish).boundary)

        inner_ring = affinity.scale(geometry.Point(0, 0).buffer(self.ring_min, resolution = 32), 1, self.ring_squish)
        outer_ring = affinity.scale(geometry.Point(0, self.outer_displace).buffer(self.ring_max, resolution = 32), 1, self.ring_squish)

        ring_polygon = affinity.translate(outer_ring.difference(inner_ring) , self.dia/2 + 20 + p_trans[0], self.dia/2 + 20 + p_trans[1]).buffer(0.2)

        ring_polygon = affinity.rotate(ring_polygon, self.rotation)

        bg_lines = bg_lines.difference(ring_polygon)

        multi_rings = geometry.MultiLineString(rings)
        multi_rings = affinity.translate( multi_rings, self.dia/2 + 20 + p_trans[0], self.dia/2 + 20 + p_trans[1])
        multi_rings = affinity.rotate( multi_rings, self.rotation)
        
        # vsk.geometry(multi_rings)
        
        multi_rings = multi_rings.intersection(canvas)
        
        
        half_rect = geometry.Polygon([(0, 0), (widthmm, 0), (widthmm, heightmm/2), (0, heightmm/2)])

        top_half = multi_rings.intersection(half_rect)
        top_half = top_half.difference(circle)

        bottom_half = multi_rings.difference(half_rect)

        planet = planet.difference(ring_polygon.difference(half_rect))

        vsk.geometry(top_half)
        vsk.geometry(bottom_half)

        vsk.geometry(planet)

        #split behind planet
        # vsk.geometry(half_rect)

        stars = []

        for x in range(int(widthmm/10)):
            for y in range(int(heightmm/10)):
                if vsk.random(vsk.noise(x/50, y/40) + 0.3) < 0.3:
                    stars.append(geometry.Point(x * 10 + vsk.random(10), y * 10 + vsk.random(10)).buffer(vsk.random(1.2)))

        # vsk.geometry(geometry.MultiPolygon(stars))
        bg_lines = bg_lines.difference(geometry.MultiPolygon(stars))

        vsk.geometry(bg_lines)




    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("rotate 180 linemerge linesimplify reloop linesort gwrite last.gcode")


if __name__ == "__main__":
    Day03SpaceSketch.display()
