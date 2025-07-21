from map_gen_2.canvas import *
from map_gen_2.generator import Generator

width = 3840
height = 2160

# fad53df832j5n 3840, 2160, 25000, 5 Big central sea.

gen = Generator(height, width, 25000, seed="fad53df832j5n", regularity=5)

canvas = MapCanvas(height, width)
canvas.draw_map(gen, False)
canvas.save_map("mymap.png")

# canvas.show_map()
