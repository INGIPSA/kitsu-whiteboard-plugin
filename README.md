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

### Quick install (recommended — ZIP)

1. Download `kitsu-whiteboard-plugin.zip` from the [latest release](https://github.com/INGIPSA/kitsu-whiteboard-plugin/releases/latest).
2. Install on your Zou server (activate your Zou venv first if applicable):

```bash
zou install-plugin --path ~/kitsu-whiteboard-plugin.zip
```

3. Restart Zou:

```bash
sudo systemctl restart zou zou-events
```

## Accessing the plugin

After install + restart, the plugin appears automatically in the **project sidebar menu** alongside Shots, Sequences, Assets, Stats, etc. Kitsu fetches the list of installed plugins with `frontend_project_enabled = true` and renders one entry per plugin.

Direct URL (for sharing or deep-linking): `https://<your-kitsu>/api/plugins/whiteboard/?project_id=<PROJECT_ID>`

### Verifying the install

Without a JWT (fast check — just confirms routes are mounted):

```bash
# Static frontend — expect 200
curl -o /dev/null -w "%{http_code}\n" https://<your-kitsu>/api/plugins/whiteboard/

# API route — expect 401 (auth gate; this proves the route is registered)
curl -o /dev/null -w "%{http_code}\n" https://<your-kitsu>/api/plugins/whiteboard/boards
```

With a JWT (confirms Kitsu sees the plugin in its registry):

```bash
# Log in once to get a JWT:
JWT=$(curl -s -c /tmp/c.txt -X POST https://<your-kitsu>/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"..."}' | jq -r .access_token)

# List installed plugins — whiteboard should appear:
curl -H "Authorization: Bearer $JWT" https://<your-kitsu>/api/data/plugins
```

### Install from source

Prebuilt frontend assets are committed to the repo, so Node.js is **not** required on the server.

```bash
git clone https://github.com/INGIPSA/kitsu-whiteboard-plugin.git ~/kitsu-whiteboard-plugin
cd ~                                           # ⚠️ run install from OUTSIDE the plugin dir
zou install-plugin --path ./kitsu-whiteboard-plugin
```

> **Do not run `zou install-plugin --path .` from inside the plugin folder.** Zou's default `PLUGIN_FOLDER` resolves to `./plugins/`, which would nest inside your source and make `shutil.copytree` recurse into itself. Always run from the parent directory or use the ZIP.

## Troubleshooting

### Plugin doesn't appear in the project sidebar menu

1. Confirm Kitsu is **≥ 1.0.23** — earlier versions have no plugin system. `curl https://<your-kitsu>/api/` returns the version.
2. Confirm you're on whiteboard **≥ 0.1.4**. Earlier releases shipped a custom `init_plugin()` that registered routes under the wrong prefix and prevented Kitsu from picking the plugin up. Reinstall the latest release.
3. Confirm the plugin is registered (see *Verifying the install* above). If `GET /api/data/plugins` doesn't list `whiteboard`, the install didn't take — check `zou list-plugins` on the server.
4. Hard-reload Kitsu in the browser (Ctrl+Shift+R). The sidebar menu is hydrated from `/api/data/plugins` on app init, not live.

### `shutil.Error: [... /plugins/whiteboard/plugins/whiteboard/plugins/ ...]`

You ran `zou install-plugin --path .` from inside the plugin directory. Fix:

```bash
rm -rf ~/kitsu-whiteboard-plugin/plugins     # clean the recursive copy
cd ~ && zou install-plugin --path ./kitsu-whiteboard-plugin
```

### External PostgreSQL server

`zou install-plugin` runs the plugin's database migration, so Zou needs to reach your Postgres before the command will succeed. Export the same variables Zou itself uses (usually set in `/opt/zou/zou_env` or your systemd unit):

```bash
export DB_HOST=db.example.com
export DB_PORT=5432
export DB_DATABASE=zoudb
export DB_USERNAME=zou
export DB_PASSWORD=******
# OR a single DATABASE_URL:
# export DATABASE_URL=postgresql://zou:******@db.example.com:5432/zoudb

zou install-plugin --path ./kitsu-whiteboard-plugin
```

If you manage Zou with systemd, the easiest path is `source /opt/zou/zouenv/bin/activate && source /opt/zou/zou_env` (adjust paths to your install) before running the install command.

### ZIP extracted with broken paths on Linux

Releases from v0.1.1 onward are packed with a cross-platform tool (not PowerShell's `Compress-Archive`) and extract cleanly on Linux. If you hit this with an older release, please upgrade to the latest.

### Frontend 404 after `git clone`

Fixed in v0.1.0 (frontend `dist/` is committed). If you still see it, pull the latest `master`.

## Development

```bash
# Backend — start Zou normally
zou start

# Frontend — hot reload
cd frontend && npm run dev
```

## Requirements

- Kitsu / Zou with plugin support (≥ 1.0.23 — earlier versions do not ship a plugin system)
- PostgreSQL
- Python 3.10+
- Node.js 18+ (only if you build the frontend from source; not needed for ZIP install or git clone)

## License

AGPL-3.0 — see [LICENSE](LICENSE).

## Credits

- [Kitsu](https://www.cg-wire.com/kitsu) by CGWire
- [fabric.js](https://fabricjs.com/) (CGWire fork)
- Built by **Piotr Buczkowski (Bucz)** — [INGIPSA](https://github.com/INGIPSA)
