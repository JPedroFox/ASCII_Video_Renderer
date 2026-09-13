import cv2
import numpy as np

def frame_to_luminance_grid(frame_bgr, grid_cols, grid_rows):
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (grid_cols, grid_rows), interpolation=cv2.INTER_AREA)
    return small.astype(np.float32) / 255.0

def luminance_to_chars(luminance_grid, char_ramp):
    n = len(char_ramp)
    indices = np.clip((luminance_grid * n).astype(int), 0, n - 1)
    return indices  # matrix of indices, not strings — faster to index later