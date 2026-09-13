import pygame_gui
import pygame
from tkinter import Tk, filedialog

def pick_video_file():
    root = Tk()
    root.withdraw()  # hide main tkinter window, we only want the dialog
    root.attributes('-topmost', True)
    path = filedialog.askopenfilename(
        title="Select a video",
        filetypes=[("Videos", "*.mp4 *.avi *.mov *.mkv")]
    )
    root.destroy()
    return path if path else None


class UIPanel:

    def relayout(self, panel_width, window_height):
        self.upload_btn.set_relative_position((20, 20))
        self.grid_label.set_relative_position((20, 80))
        self.grid_slider.set_relative_position((20, 115))
        self.info_label.set_relative_position((20, 160))
        self.export_btn.set_relative_position((20, window_height - 70))

    def __init__(self, manager: pygame_gui.UIManager, panel_width: int, window_height: int):
        self.manager = manager

        self.upload_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (panel_width - 40, 40)),
            text="Upload Video",
            manager=manager
        )

        self.grid_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 80), (panel_width - 40, 30)),
            text="Grid Width: 160",
            manager=manager
        )

        self.grid_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((20, 115), (panel_width - 40, 30)),
            start_value=160,
            value_range=(1, 320),
            manager=manager
        )

        self.info_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 160), (panel_width - 40, 90)),
            text="",
            manager=manager
        )

        self.export_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, window_height - 70), (panel_width - 40, 40)),
            text="Export Video",
            manager=manager
        )

    def update_info(self, video, grid_cols, grid_rows, render_fps):
        if video is None:
            self.info_label.set_text("No video loaded")
            return
        text = (f"Res: {video.width}x{video.height}\n"
                f"Aspect: {video.aspect_ratio:.2f}\n"
                f"Video FPS: {video.fps:.1f}\n"
                f"Grid: {grid_cols}x{grid_rows}\n"
                f"Render FPS: {render_fps:.1f}")
        self.info_label.set_text(text)