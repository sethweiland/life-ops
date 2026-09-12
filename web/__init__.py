"""
Flask app for the life-ops shell.

Usage:
    python web/run.py
"""

import os
import sys
from pathlib import Path

from flask import Flask

_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
    )
    app.secret_key = os.urandom(24)

    from .blueprints.home import bp as home_bp
    from .blueprints.projects import bp as projects_bp
    from .blueprints.spend import bp as spend_bp
    from .blueprints.x_activity import bp as x_activity_bp
    from .blueprints.grok_bot import bp as grok_bot_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(projects_bp, url_prefix="/projects")
    app.register_blueprint(spend_bp, url_prefix="/spend")
    app.register_blueprint(x_activity_bp)
    app.register_blueprint(grok_bot_bp, url_prefix="/grok-bot")

    from .context import register_life_ops_context

    register_life_ops_context(app)

    @app.before_request
    def gate_disabled_modules():
        from flask import abort, request

        from src.core.tenant import module_enabled

        path = request.path or ""
        checks = (
            ("/projects", "projects"),
            ("/spend", "spend"),
            ("/x", "x"),
            ("/grok-bot", "grok_bot"),
            ("/memes", "memes"),
        )
        for prefix, name in checks:
            if path == prefix or path.startswith(prefix + "/"):
                if not module_enabled(name):
                    abort(404)
                return

    try:
        from src.core.grok_bot import get_grok_bot_routines

        get_grok_bot_routines().ensure_seeded()
    except Exception:
        pass

    try:
        from src.core.project_board import get_project_board

        get_project_board().ensure_seeded()
    except Exception:
        pass

    return app
