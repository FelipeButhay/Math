import main
import pygame
import main

def get_value_table(f, center, size) -> list:
    value_table = [[]]
    n_points = int(main.SX)
    for x in range(n_points):
        x = center[0] - size/2 + x*size/n_points
        try:
            value_table[-1].append(main.xycoord_pixels(center, size, (x, f(x))))
        except:
            value_table.append([])
            continue
    
    return value_table