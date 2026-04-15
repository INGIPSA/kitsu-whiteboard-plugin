from pathlib import Path

from flask import Blueprint, abort, send_from_directory

from . import resources

routes = [
    ("/boards", resources.BoardsResource),
    ("/boards/<board_id>", resources.BoardResource),
]


def init_plugin(app, manifest):
    """Register the plugin's REST API and its static frontend.

    Called by Zou (>= 0.20.60) after the plugin module has been imported.
    Newer Zou versions auto-register routes from the ``routes`` list, but
    older ones require this explicit hook.
    """
    from zou.app.utils.api import configure_api_from_blueprint

    plugin_id = manifest["id"]
    blueprint = Blueprint(plugin_id, plugin_id)

    configure_api_from_blueprint(blueprint, routes)

    dist_dir = Path(__file__).resolve().parent / "frontend" / "dist"

    @blueprint.route("/", defaults={"filename": "index.html"})
    @blueprint.route("/<path:filename>")
    def _static(filename):
        file_path = dist_dir / filename
        if not file_path.is_file():
            if (dist_dir / "index.html").is_file():
                return send_from_directory(
                    str(dist_dir), "index.html", max_age=0
                )
            abort(404)
        return send_from_directory(str(dist_dir), filename, max_age=0)

    app.register_blueprint(blueprint, url_prefix=f"/{plugin_id}")


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
