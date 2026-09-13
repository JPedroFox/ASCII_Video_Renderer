import cv2
import os
import shutil
import subprocess
import imageio_ffmpeg

from src.frame_processor import frame_to_luminance_grid, luminance_to_chars
from src.config import BG_COLOR

TEMP_DIR = "temp_export"
OUTPUT_DIR = "output"
def resolve_output_path(video_path, output_dir=OUTPUT_DIR):
        base_name = os.path.splitext(os.path.basename(video_path))[0]  # "input" from "input.mp4"
        candidate = os.path.join(output_dir, f"{base_name}.mp4")

        if not os.path.exists(candidate):
            return candidate

        counter = 1
        while True:
            candidate = os.path.join(output_dir, f"{base_name}({counter}).mp4")
            if not os.path.exists(candidate):
                return candidate
            counter += 1

def export_video(video_path, char_ramp, glyphs, cell_w, cell_h, grid_cols, grid_rows):
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = resolve_output_path(video_path)  # decide name BEFORE processing

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    content_w = grid_cols * cell_w
    content_h = grid_rows * cell_h

    # libx264 requires even dimensions — round down to nearest even
    content_w = content_w - (content_w % 2)
    content_h = content_h - (content_h % 2)

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        lum_grid = frame_to_luminance_grid(frame, grid_cols, grid_rows)
        char_indices = luminance_to_chars(lum_grid, char_ramp)

        # render ASCII frame using pure cv2 (no pygame) to run outside the graphics loop
        img = render_frame_cv2(char_indices, char_ramp, content_w, content_h, cell_w, cell_h)

        frame_path = os.path.join(TEMP_DIR, f"frame_{frame_idx:06d}.png")
        cv2.imwrite(frame_path, img)

        frame_idx += 1
        if frame_idx % 30 == 0:
            print(f"Processing frame {frame_idx}/{frame_count}")

    cap.release()

    merge_frames_with_audio(video_path, fps, output_path)
    shutil.rmtree(TEMP_DIR)
    print(f"Export completed: {output_path}")
    return output_path


def render_frame_cv2(char_indices, char_ramp, content_w, content_h, cell_w, cell_h):
    import numpy as np
    img = np.zeros((content_h, content_w, 3), dtype=np.uint8)  # black
    grid_rows, grid_cols = char_indices.shape

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = cell_h / 30.0
    thickness = 1

    for row in range(grid_rows):
        for col in range(grid_cols):
            ch = char_ramp[char_indices[row, col]]
            if ch == ' ':
                continue
            x = col * cell_w
            y = row * cell_h + cell_h - 2
            cv2.putText(img, ch, (x, y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

    return img


def merge_frames_with_audio(original_video_path, fps, output_path):
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    frame_pattern = os.path.join(TEMP_DIR, "frame_%06d.png")

    cmd = [
        ffmpeg_path,
        "-y",
        "-framerate", str(fps),
        "-i", frame_pattern,
        "-i", original_video_path,
        "-map", "0:v:0",
        "-map", "1:a:0?",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg error:", result.stderr)
        raise RuntimeError("Failed to export video")

    