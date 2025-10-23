from sanic import Blueprint, response
from sanic.response import html, redirect
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from app.config import load_sites_config, load_settings, LOGS_DIR
from app.views.auth import require_auth
import os
from datetime import datetime

bp = Blueprint("dashboard", url_prefix="/")

template_dir = Path(__file__).parent.parent / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(str(template_dir)),
    autoescape=select_autoescape(['html', 'xml'])
)


@bp.route("/")
@require_auth
async def index(request):
    sites_config = load_sites_config()
    settings = load_settings()
    
    sites = []
    for site_id, site_data in sites_config.items():
        sites.append({
            "id": site_id,
            "name": site_data.get("name", site_id),
            "enabled": site_data.get("enabled", True),
            "account_count": len(site_data.get("accounts", []))
        })
    
    logs = []
    if LOGS_DIR.exists():
        for log_file in sorted(LOGS_DIR.glob("*.log"), key=os.path.getmtime, reverse=True)[:10]:
            logs.append({
                "name": log_file.name,
                "size": log_file.stat().st_size,
                "modified": datetime.fromtimestamp(log_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
    
    template = jinja_env.get_template("dashboard.html")
    return html(template.render(
        sites=sites,
        logs=logs,
        settings=settings
    ))


@bp.route("/logs/<log_name>")
@require_auth
async def view_log(request, log_name):
    log_file = LOGS_DIR / log_name
    if not log_file.exists():
        return response.text("日志文件不存在", status=404)
    
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    return response.text(content, content_type="text/plain; charset=utf-8")
