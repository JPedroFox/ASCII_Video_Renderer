import pygame
from src.config import FONT_PATH, FG_COLOR

def build_glyph_cache(char_ramp, font_size):
    font = pygame.font.Font(FONT_PATH, font_size)
    cache = {}
    for ch in char_ramp:
        cache[ch] = font.render(ch, True, FG_COLOR).convert_alpha()
    cell_w, cell_h = font.size("M")
    return cache, cell_w, cell_h


def calculate_font_size(grid_cols, grid_rows, preview_w, preview_h, char_aspect_ratio):
    # try height first
    candidate_h = preview_h // grid_rows
    candidate_w = int(candidate_h * char_aspect_ratio)

    # if it exceeds available width, recalculate limited by width
    max_w_per_cell = preview_w // grid_cols
    if candidate_w > max_w_per_cell:
        candidate_w = max_w_per_cell
        candidate_h = int(candidate_w / char_aspect_ratio)

    return max(4, candidate_h)  # never let font size go to zero