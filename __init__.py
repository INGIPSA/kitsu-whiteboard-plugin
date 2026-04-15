from . import resources

routes = [
    ("/boards", resources.BoardsResource),
    ("/boards/<board_id>", resources.BoardResource),
]


def pre_install(manifest):
    pass


def post_install(manifest):
    import shutil
    import subprocess
    from pathlib import Path

    frontend_path = Path(__file__).resolve().parent / "frontend"
    if not (frontend_path / "package.json").exists():
        return
    if (frontend_path / "dist" / "index.html").exists():
        return
    if shutil.which("npm") is None:
        print(
            "[whiteboard] npm not found — skipping frontend build. "
            "Install Node.js 18+ or ship a prebuilt frontend/dist/."
        )
        return
    subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
    subprocess.run(["npm", "run", "build"], cwd=frontend_path, check=True)


def pre_uninstall(manifest):
    pass


def post_uninstall(manifest):
    pass
