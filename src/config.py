ASCII_CHARS = [chr(i) for i in range(32, 127)]  # 95 printable, 32-126

GRID_MIN_WIDTH = 1
GRID_MAX_WIDTH = 320   # adjustable based on performance testing

CHAR_ASPECT_RATIO = 0.55  # width/height of monospaced font cell
                           # ideal: measure programmatically via font.size(), not guess

TARGET_FPS = 30

FONT_PATH = "assets/fonts/mono.ttf"
FONT_SIZE = 14  # size in px used to render each glyph/cell

BG_COLOR = (0, 0, 0)
FG_COLOR = (255, 255, 255)