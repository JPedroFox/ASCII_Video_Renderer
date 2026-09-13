from src.config import CHAR_ASPECT_RATIO, GRID_MIN_WIDTH, GRID_MAX_WIDTH

def calculate_grid(video_width, video_height, target_grid_width):
    target_grid_width = max(GRID_MIN_WIDTH, min(GRID_MAX_WIDTH, target_grid_width))
    video_aspect = video_width / video_height
    grid_height = max(1, round(target_grid_width / video_aspect * CHAR_ASPECT_RATIO))
    return target_grid_width, grid_height