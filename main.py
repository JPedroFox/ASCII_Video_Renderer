import pygame
import pygame_gui
import time
import cv2

from src.video_reader import VideoReader
from src.grid_calculator import calculate_grid
from src.density_map import build_density_ramp
from src.glyph_cache import build_glyph_cache, calculate_font_size
from src.frame_processor import frame_to_luminance_grid, luminance_to_chars
from src.app_state import AppState
from src.ui_panel import UIPanel, pick_video_file
from src.config import TARGET_FPS, BG_COLOR, CHAR_ASPECT_RATIO

PANEL_WIDTH = 280
PREVIEW_W, PREVIEW_H = 960, 720  # fixed preview area, video adjusts within it
WINDOW_W = PANEL_WIDTH + PREVIEW_W
WINDOW_H = PREVIEW_H


def load_video(state: AppState, path: str):
    if state.video:
        state.video.release()
    state.video = VideoReader(path)
    state.video_path = path
    state.needs_grid_recalc = True
    state.playing = True


def recalc_grid(state: AppState, preview_w: int, preview_h: int):
    if state.video is None:
        return
    state.grid_cols, state.grid_rows = calculate_grid(
        state.video.width, state.video.height, state.grid_width
    )
    font_size = calculate_font_size(
        state.grid_cols, state.grid_rows, preview_w, preview_h, CHAR_ASPECT_RATIO
    )
    state.glyphs, state.cell_w, state.cell_h = build_glyph_cache(state.char_ramp, font_size)
    state.needs_grid_recalc = False


def render_ascii_frame(state: AppState, target_surface: pygame.Surface, preview_w: int, preview_h: int):
    frame = state.video.read_frame()
    if frame is None:
        state.video.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame = state.video.read_frame()
        if frame is None:
            return

    lum_grid = frame_to_luminance_grid(frame, state.grid_cols, state.grid_rows)
    char_indices = luminance_to_chars(lum_grid, state.char_ramp)

    cell_w, cell_h = state.cell_w, state.cell_h
    content_w = state.grid_cols * cell_w
    content_h = state.grid_rows * cell_h

    content_surface = pygame.Surface((content_w, content_h))
    content_surface.fill(BG_COLOR)
    for row in range(state.grid_rows):
        for col in range(state.grid_cols):
            ch = state.char_ramp[char_indices[row, col]]
            content_surface.blit(state.glyphs[ch], (col * cell_w, row * cell_h))

    scale = min(preview_w / content_w, preview_h / content_h)
    scaled_w, scaled_h = int(content_w * scale), int(content_h * scale)
    scaled_surface = pygame.transform.smoothscale(content_surface, (scaled_w, scaled_h))

    offset_x = (preview_w - scaled_w) // 2
    offset_y = (preview_h - scaled_h) // 2

    target_surface.fill(BG_COLOR)
    target_surface.blit(scaled_surface, (offset_x, offset_y))


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))

    state = AppState()
    state.char_ramp = build_density_ramp()
    state.glyphs, state.cell_w, state.cell_h = build_glyph_cache(state.char_ramp, font_size=14)

    window_w, window_h = WINDOW_W, WINDOW_H
    screen = pygame.display.set_mode((window_w, window_h), pygame.RESIZABLE)
    pygame.display.set_caption("ASCII Video Renderer")
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((window_w, window_h))
    ui = UIPanel(manager, PANEL_WIDTH, window_h)

    preview_w, preview_h = window_w - PANEL_WIDTH, window_h
    preview_surface = pygame.Surface((preview_w, preview_h))

    running = True

    while running:
        frame_start = time.time()
        time_delta = clock.tick(TARGET_FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                window_w, window_h = event.w, event.h
                window_w = max(window_w, PANEL_WIDTH + 200)   # don't let window get smaller than minimum usable
                window_h = max(window_h, 300)
                screen = pygame.display.set_mode((window_w, window_h), pygame.RESIZABLE)
                manager.set_window_resolution((window_w, window_h))
                preview_w, preview_h = window_w - PANEL_WIDTH, window_h
                preview_surface = pygame.Surface((preview_w, preview_h))
                ui.relayout(PANEL_WIDTH, window_h)  # reposition widgets

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == ui.upload_btn:
                    path = pick_video_file()
                    if path:
                        load_video(state, path)
                elif event.ui_element == ui.export_btn:
                    if state.video_path:
                        from src.exporter import export_video
                        export_video(
                            state.video_path, state.char_ramp, state.glyphs,
                            state.cell_w, state.cell_h, state.grid_cols, state.grid_rows
                        )
                    else:
                        print("No video loaded to export")

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == ui.grid_slider:
                    state.grid_width = int(event.value)
                    ui.grid_label.set_text(f"Grid Width: {state.grid_width}")
                    state.needs_grid_recalc = True

            manager.process_events(event)

        if state.needs_grid_recalc:
            recalc_grid(state, preview_w, preview_h)

        if state.video and state.playing and state.grid_cols > 0:
            render_ascii_frame(state, preview_surface, preview_w, preview_h)

        manager.update(time_delta)

        screen.fill((30, 30, 30))
        screen.blit(preview_surface, (PANEL_WIDTH, 0))
        manager.draw_ui(screen)

        render_fps = 1.0 / (time.time() - frame_start + 1e-6)
        ui.update_info(state.video, state.grid_cols, state.grid_rows, render_fps)

        pygame.display.flip()

    if state.video:
        state.video.release()
    pygame.quit()


if __name__ == "__main__":
    main()