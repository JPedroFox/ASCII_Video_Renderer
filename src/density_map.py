import pygame
import numpy as np
from src.config import ASCII_CHARS, FONT_PATH, FONT_SIZE

def build_density_ramp():
    pygame.font.init()
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    # fixed reference cell — uses the widest typical character to define cell size
    cell_w, cell_h = font.size("M")

    densities = []
    for ch in ASCII_CHARS:
        # creates a surface of FIXED size (not natural glyph size)
        cell_surface = pygame.Surface((cell_w, cell_h))
        cell_surface.fill((0, 0, 0))  # black background

        glyph = font.render(ch, True, (255, 255, 255))
        # centers the glyph within the fixed cell
        gx = (cell_w - glyph.get_width()) // 2
        gy = (cell_h - glyph.get_height()) // 2
        cell_surface.blit(glyph, (gx, gy))

        arr = pygame.surfarray.array3d(cell_surface)
        density = np.mean(arr) / 255.0  # now measures over CONSTANT area for all chars
        densities.append((density, ch))

    densities.sort(key=lambda x: x[0])
    return [ch for _, ch in densities]