# Kitsu Whiteboard Plugin

A visual review board plugin for [Kitsu](https://www.cg-wire.com/kitsu) — the open-source production management platform for animation, VFX, and game studios.

Think Miro/FigJam but integrated directly into your Kitsu production pipeline with access to your shots, assets, and concepts.

## Features

### Canvas Tools
- **Shapes**: Rectangle, Circle, Triangle, Diamond, Star
- **Lines & Arrows** with Shift snap to 45°
- **Text blocks** with Bold, Italic, Underline, alignment
- **Sticky notes** with 12 pastel color options
- **Emoji stickers** (36 picker)
- **Images**: Upload via file picker or drag & drop
- **YouTube embed** with thumbnail preview
- **Free draw** (pencil) with color/width control

### Canvas Features
- Infinite canvas — Pan (Space hold) + Zoom (scroll wheel)
- Snap to grid with dotted background
- Undo / Redo (50-step history)
- Right-click context menu: Group, Lock, Duplicate, Layer order, Delete
- Object locking with visual feedback
- Stroke/Fill colors with live update + swap (X key)
- Background color per board
- Shift constrain: perfect square, circle, 45° lines
- Double-click shapes to add centered text
- Auto-save (2s debounce)
- Export board as PNG

### Kitsu Integration
- Entity sidebar: browse and drag shots/assets onto canvas
- Thumbnails from Kitsu preview API
- Board per project — visible in project menu
- Board visibility: Private / Team / Public
- Dark theme support

### Keyboard Shortcuts
`V` Select · `Space` Pan · `D` Draw · `L` Line · `A` Arrow · `R` Rect · `C` Circle · `T` Text · `N` Sticky · `S` Sticker · `X` Swap colors · `Del` Delete · `Ctrl+Z/Y` Undo/Redo · `Ctrl+G` Group · `Ctrl+L` Lock · `Ctrl+0` Fit

## Installation

```bash
# Build frontend
cd frontend && npm install && npm run build && cd ..

# Install plugin into Zou
python zou/cli.py install-plugin --path ./kitsu-whiteboard-plugin
```

## Development

```bash
# Backend — start Zou normally
python zou/cli.py start

# Frontend — hot reload
cd frontend && npm run dev
```

## Requirements

- Kitsu / Zou >= 1.0.23
- Python 3.10+
- Node.js 18+

## License

AGPL-3.0 — see [LICENSE](LICENSE).

## Credits

- [Kitsu](https://www.cg-wire.com/kitsu) by CGWire
- [fabric.js](https://fabricjs.com/) (CGWire fork)
- Built by **Piotr Buczkowski (Bucz)** — [INGIPSA](https://github.com/INGIPSA)
