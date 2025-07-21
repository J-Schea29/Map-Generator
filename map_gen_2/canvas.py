from tkinter import *
from PIL import Image, ImageTk
import math
from random import Random
import map_gen_2.util.vector_util as vect
from matplotlib.path import Path
import numpy as np
import aggdraw
import os


class MapCanvas:
    rand = None

    height = None
    width = None

    # Assets
    parchment = None
    mountain = []
    tree = []
    hill = []

    image = None
    draw = None

    def __init__(self, height=720, width=1280):
        self.height = height
        self.width = width
        self.rand = Random()
        self.rand.seed(0)

        self.load_assets()

        self.image = self.parchment
        self.draw = aggdraw.Draw(self.image)

    def load_assets(self):
        self.parchment = Image.open("map_gen_2/assets/parchment.jpg").convert("RGBA").resize((self.width, self.height),
                                                                                   Image.Resampling.LANCZOS)
        
        for im in os.listdir("map_gen_2/assets/mountains/"):
            self.mountain.append(
                Image.open("map_gen_2/assets/mountains/" + im).resize((40, 25), Image.Resampling.LANCZOS))
            
        for im in os.listdir("map_gen_2/assets/trees/"):
            self.tree.append(Image.open("map_gen_2/assets/trees/" + im).resize((5, 8), Image.Resampling.LANCZOS))

        for im in os.listdir("map_gen_2/assets/hills/"):
            self.hill.append(Image.open("map_gen_2/assets/hills/" + im).resize((20, 13), Image.Resampling.LANCZOS))

        print(f"Number of mountain assets loaded: {len(self.mountain)}")
        print(f"Number of tree assets loaded: {len(self.tree)}")
        print(f"Number of hill assets loaded: {len(self.hill)}")

    def show_map(self):
        self.image.show()

    def draw_line(self, p1, p2, color='black', width=1.0):
        pen = aggdraw.Pen(color, width)
        self.draw.line((p1[0], p1[1], p2[0], p2[1]), pen)

    def draw_irregular_line(self, p1, p2, splits=3, mag_fact=0.25, color='black', width=1.0):
        points = [p1, p2]
        for i in range(splits):
            new_points = []
            for p_idx in range(len(points)):
                new_points.append(points[p_idx])
                if p_idx + 1 < len(points):
                    new_points.append(vect.split_line(points[p_idx], points[p_idx + 1], self.rand, mag_fact))
            points = new_points

        for i in range(len(points) - 1):
            self.draw_line(points[i], points[i + 1], color=color, width=width)

    def draw_multi_line(self, points, color='black', width=1):
        for i in range(len(points) - 1):
            self.draw_line(points[i], points[i + 1], color=color, width=width)

    def draw_irregular_multi_line(self, points, splits=3, mag_fact=0.25, color='black', width=1):
        for i in range(len(points) - 1):
            self.draw_irregular_line(points[i], points[i + 1], splits=splits, mag_fact=mag_fact, color=color,
                                     width=width)

    def draw_point(self, p, color='black', radius=3):
        brush = aggdraw.Brush(color)
        self.draw.ellipse((p[0] - radius, p[1] - radius, p[0] + radius, p[1] + radius), None, brush)

    def fill_region(self, points, color='blue', opacity=128):
        brush = aggdraw.Brush(color, opacity)
        pen = aggdraw.Pen(color, width=0, opacity=0)
        corrected_points = []
        for p in points:
            corrected_points.extend([p[0], p[1]])
        self.draw.polygon(corrected_points, pen, brush)

    def draw_image_at(self, p, image_input):
        image = image_input.copy()
        x = int(round(p[0]))
        y = int(round(p[1]))

        self.image.paste(image, (x - math.floor(image.width / 2),
                                 y - math.floor(image.height / 2),
                                 x + math.ceil(image.width / 2),
                                 y + math.ceil(image.height / 2)),
                         mask=image)
        # Image.Image.paste(self.image, image, (x - math.floor(image.width / 2),
        #                          y - math.floor(image.height / 2),
        #                          x + math.ceil(image.width / 2),
        #                          y + math.ceil(image.height / 2)),
        #                          image
        #                          )
        

    def fill_region_with_image(self, points, image, step=5, offset_fact=0.5):
        min_p = [self.width, self.height]
        max_p = [0, 0]

        for point in points:
            min_p[0] = min(min_p[0], point[0])
            min_p[1] = min(min_p[1], point[1])
            max_p[0] = max(max_p[0], point[0])
            max_p[1] = max(max_p[1], point[1])

        path = Path(points)

        fill_points = []
        for x in np.arange(min_p[0], max_p[0], step):
            for y in np.arange(min_p[1], max_p[1], step):
                if path.contains_point([x, y]):
                    fill_points.append([x, y])

        fill_points = sorted(fill_points, key=lambda p: p[1])

        for fill_point in fill_points:
            offset = [(self.rand.random() - 0.5) * step * offset_fact, (self.rand.random() - 0.5) * step * offset_fact]
            self.draw_image_at(vect.add(fill_point, offset), image)

    def fill_region_with_image_set(self, points, image_set, step=5, offset_fact=0.5):
        min_p = [self.width, self.height]
        max_p = [0, 0]

        for point in points:
            min_p[0] = min(min_p[0], point[0])
            min_p[1] = min(min_p[1], point[1])
            max_p[0] = max(max_p[0], point[0])
            max_p[1] = max(max_p[1], point[1])

        path = Path(points)

        fill_points = []
        for x in np.arange(min_p[0], max_p[0], step):
            for y in np.arange(min_p[1], max_p[1], step):
                if path.contains_point([x, y]):
                    fill_points.append([x, y])

        fill_points = sorted(fill_points, key=lambda p: p[1])

        for fill_point in fill_points:
            offset = [(self.rand.random() - 0.5) * step * offset_fact, (self.rand.random() - 0.5) * step * offset_fact]
            self.draw_image_at(vect.add(fill_point, offset), self.rand.choice(image_set))

    def draw_all_mountains(self, gen, points_per_mountain=1):
        dps = []
        for m in gen.sorted_mountain_dps:
            dps.extend(m)

        points = []
        for d_p in dps:
            points.append(gen.delaunay.points[d_p])

        sorted_points = sorted(points, key=lambda point: point[1])
        for i in range(len(sorted_points)):
            if i % points_per_mountain != 0:
                continue
            p = sorted_points[i]

            self.draw_image_at(p, self.rand.choice(self.mountain))

    def draw_map(self, gen, debug=False):
        # Water
        for water_poly in gen.water_polys:
            self.fill_region(water_poly, '#dcdcdc')

        # Double‑line shore: dark ink at the edge + same ink offset into the water
        for edge in gen.water_edges:
            for i in range(len(edge) - 1):
                self.draw_line(edge[i], edge[i + 1], "#483320", 2)

        self.draw.flush()

        # for edge in gen.deep_water_etched_lines:
        #     for i in range(len(edge) - 1):
        #         self.draw_line(edge[i], edge[i + 1], "#483320", 1)

        # self.draw.flush()

        river_lengths = [len(riv) for riv in gen.river_points]
        min_len = min(river_lengths)
        max_len = max(river_lengths)

        # Rivers
        for riv in gen.river_points:
            river_len = len(riv)

            # Step 2: normalize
            if max_len != min_len:
                scale = (river_len - min_len) / (max_len - min_len)
            else:
                scale = 0  # all rivers same length

            max_thickness = 2 + scale * 2  # goes from 2 to 3

            for i in range(len(riv) - 1):
                thickness = max_thickness * (len(riv) + 1 - i) / len(riv)
                self.draw_irregular_line(riv[i], riv[i + 1], color="#483320", width=thickness, splits=2)

        self.draw.flush()
        if debug:
            self.draw_debug_geometry(gen)
            self.draw.flush()

        # Mountains
        self.draw_all_mountains(gen, 1)
        # Hills
        for d_p in gen.hill_dps:
            region = gen.voronoi.regions[gen.voronoi.point_region[d_p]]
            points = []
            for vert_idx in region:
                points.append(gen.voronoi.vertices[vert_idx])
            self.fill_region_with_image_set(points, self.hill, 12, offset_fact=0.2)
        # Forests
        for d_p in gen.forest_dps:
            region = gen.voronoi.regions[gen.voronoi.point_region[d_p]]
            points = []
            for vert_idx in region:
                points.append(gen.voronoi.vertices[vert_idx])
            self.fill_region_with_image_set(points, self.tree)
        # self.draw.flush()
        self.draw = aggdraw.Draw(self.image)
        self.draw.flush()
    def draw_debug_geometry(self, gen):
        for ridge in gen.voronoi.ridge_vertices:
            v1_idx = ridge[0]
            v2_idx = ridge[1]
            if v1_idx != -1 and v2_idx != -1:
                self.draw_line(gen.voronoi.vertices[v1_idx], gen.voronoi.vertices[v2_idx])

        for vert in gen.voronoi.vertices:
            self.draw_point(vert, "blue", 1)
        for point in gen.init_points:
            self.draw_point(point, "red", 1)
        for p in gen.all_water_dps:
            self.draw_point(gen.delaunay.points[p], "blue")

        for line in gen.sorted_mountain_dps:
            points = []
            for d_p in line:
                points.append(gen.delaunay.points[d_p])
            self.draw_multi_line(points, color="red")
        for point in gen.all_mountain_dps:
            self.draw_point(gen.delaunay.points[point], color="purple")

        for p in gen.debug_points:
            self.draw_point(p, "yellow")

        self.draw_multi_line(gen.debug_points, color="yellow")


    def save_map(self, filename: str = "map_output.png"):
        """
        Saves the current canvas image to a file.

        Args:
            filename (str): Path where the map image will be saved.
        """
        # Ensure all drawing operations are flushed
        self.draw.flush()
        # Save the image with transparency support
        self.image.save(filename)
        print(f"Map saved to {filename}")