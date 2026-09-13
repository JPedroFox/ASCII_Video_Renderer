class AppState:
    def __init__(self):
        self.video = None              # VideoReader or None
        self.video_path = None
        self.grid_width = 160          # controlled by slider
        self.grid_cols = 0
        self.grid_rows = 0
        self.playing = False
        self.char_ramp = None
        self.glyphs = None
        self.cell_w = 0
        self.cell_h = 0
        self.needs_grid_recalc = True  # flag: slider changed, needs recalculation