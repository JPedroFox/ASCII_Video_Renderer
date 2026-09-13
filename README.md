# ASCII Video Renderer

Real-time video renderer that converts any video into a dynamic ASCII animation — frame by frame, preserving motion, aspect ratio, and brightness of the original video.

Black screen, white characters. No filters, no effects — just the 95 printable ASCII characters (codes 32-126), chosen by actual visual density measured directly from the font used.

---

## Demo

```
LIVE ASCII PREVIEW         GRID: 160x90          RENDER FPS: 29.4 / 30
```

Sample videos are available in the `samples/` folder:
- **input.mp4** - Original source video for demonstration
- **output.mp4** - Example ASCII-rendered output

---

## Key Features

- **Upload any video** (`.mp4`, `.avi`, `.mov`, `.mkv`)
- **Automatic detection** of resolution, aspect ratio, and FPS from the original video
- **Automatic proportional grid** — you control only the width, height is calculated preserving the actual aspect ratio of the video *and* the physical aspect ratio of the font cell (avoids stretched or squashed image)
- **95 printable ASCII characters**, ordered by visual density measured in the font (not an arbitrary sequence like `@#*+=-:.`)
- **Real-time preview** — continuous processing, frame by frame, without pre-rendering the entire video before display
- **Resizable and maximizable window**
- **Real performance measurement** — original video FPS vs. rendering FPS, side by side, no frills
- **Export with original audio** preserved, filename automatically based on source video

---

## How it Works (Pipeline)

```
Input Video
      │
      ▼
Frame-by-frame Decoding (OpenCV)
      │
      ▼
Grid Calculation (video ratio + font ratio)
      │
      ▼
Luminance Calculation per Cell (perceptual weighted average)
      │
      ▼
Luminance → Character Mapping (by actual visual density)
      │
      ▼
Rendering to Screen (Pygame)
```

Character density is not assumed — it is **measured**: each of the 95 characters is rendered in a cell of fixed size, the lit pixels are counted, and the entire set is ordered from least dense (space, thin punctuation) to most dense (large uppercase). This means the ramp adapts to the chosen font, rather than relying on a traditional sequence that may not make visual sense outside the context in which it was originally defined.

---

## Installation

**Requirements:** Windows 10/11, Python 3.12

```bash
git clone https://github.com/seu-usuario/ascii-video-renderer.git
cd ascii-video-renderer

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Place a monospaced font in `assets/fonts/mono.ttf`.
Recommended: [JetBrains Mono](https://www.jetbrains.com/lp/mono/) (free, open license).

```bash
python main.py
```

---

## Usage

| Control | Function |
|---|---|
| **Upload Video** | Opens the file picker and loads the video |
| **Grid Width** | Controls ASCII grid resolution in real-time — height is automatically recalculated |
| **Export Video** | Exports the result as `.mp4`, with original audio, to the `output/` folder |

The side panel shows in real-time:
- Detected video resolution and aspect ratio
- Original file FPS
- Calculated grid dimensions (`width × height`)
- Actual rendering FPS — the metric that matters: shows whether the hardware is actually keeping up with the video in real-time, not just declaring that it is

---

## Generating the Executable (.exe)

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --add-data "assets;assets" --name "ASCII_Video_Renderer" main.py
```

The final executable is located in `dist/ASCII_Video_Renderer.exe` — runs on any Windows without needing to install Python or dependencies.

---

## Project Architecture

```
ascii-video-renderer/
├── assets/fonts/           # monospaced font used in rendering
├── samples/                # sample input and output videos
│   ├── input.mp4          # original source video
│   └── output.mp4         # example ASCII-rendered output
├── src/
│   ├── video_reader.py     # video decoding and metadata
│   ├── grid_calculator.py  # grid calculation preserving aspect ratio
│   ├── density_map.py      # visual density measurement of 95 characters
│   ├── glyph_cache.py      # glyph pre-rendering (performance)
│   ├── frame_processor.py  # luminance and character mapping
│   ├── ui_panel.py         # control panel (Pygame GUI)
│   ├── app_state.py        # application state
│   └── exporter.py         # final rendering and export with audio
├── main.py                 # main loop and orchestration
└── requirements.txt
```

Each pipeline step (decoding, grid calculation, luminance, mapping, rendering) is isolated in its own module — makes it easy to test, debug, and extend without mixing responsibilities.

---

## Known Limitations

- Very large grids (over ~300 in width) may not sustain 30 FPS depending on hardware, since processing runs on CPU, not GPU
- The font of the exported video (`cv2.putText`) is visually distinct from the TTF font used in live preview
- No color support — the project is deliberately monochromatic (white on black) in this version

## Possible Future Extensions

Colored ASCII, brightness/contrast control, multiple fonts with automatic density recalculation, GPU-accelerated rendering for large grids, export to image sequence, extended Unicode mode.

---

## License

*(define here: MIT, GPL, or your preference)*# ASCII_Video_Renderer
# ASCII_Video_Renderer
