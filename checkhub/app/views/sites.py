from sanic import Blueprint, response
from sanic.response import html, json, redirect
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from app.config import load_sites_config, save_sites_config
from app.models import Site
from app.utils.scheduler import CheckScheduler
from app.views.auth import require_auth

bp = Blueprint("sites", url_prefix="/sites")

template_dir = Path(__file__).parent.parent / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(str(template_dir)),
    autoescape=select_autoescape(['html', 'xml'])
)


@bp.route("/")
@require_auth
async def sites_page(request):
    sites_config = load_sites_config()
    
    sites = []
    for site_id, site_data in sites_config.items():
        sites.append({
            "id": site_id,
            "name": site_data.get("name", site_id),
            "enabled": site_data.get("enabled", True),
            "checker_class": site_data.get("checker_class", "BaseChecker"),
            "accounts": site_data.get("accounts", [])
        })
    
    template = jinja_env.get_template("sites.html")
    return html(template.render(sites=sites))


@bp.route("/api/list", methods=["GET"])
@require_auth
async def list_sites(request):
    sites_config = load_sites_config()
    
    sites = []
    for site_id, site_data in sites_config.items():
        sites.append({
            "id": site_id,
            "name": site_data.get("name", site_id),
            "enabled": site_data.get("enabled", True),
            "checker_class": site_data.get("checker_class", "BaseChecker"),
            "account_count": len(site_data.get("accounts", []))
        })
    
    return json({"success": True, "sites": sites})


@bp.route("/api/add", methods=["POST"])
@require_auth
async def add_site(request):
    data = request.json
    
    site_id = data.get("id")
    site_name = data.get("name")
    checker_class = data.get("checker_class", "BaseChecker")
    
    if not site_id or not site_name:
        return json({"success": False, "error": "站点ID和名称不能为空"}, status=400)
    
    sites_config = load_sites_config()
    
    if site_id in sites_config:
        return json({"success": False, "error": "站点ID已存在"}, status=400)
    
    sites_config[site_id] = {
        "name": site_name,
        "enabled": True,
        "checker_class": checker_class,
        "accounts": []
    }
    
    save_sites_config(sites_config)
    
    return json({"success": True, "message": "站点添加成功"})


@bp.route("/api/delete/<site_id>", methods=["DELETE"])
@require_auth
async def delete_site(request, site_id):
    sites_config = load_sites_config()
    
    if site_id not in sites_config:
        return json({"success": False, "error": "站点不存在"}, status=404)
    
    del sites_config[site_id]
    save_sites_config(sites_config)
    
    return json({"success": True, "message": "站点删除成功"})


@bp.route("/api/toggle/<site_id>", methods=["POST"])
@require_auth
async def toggle_site(request, site_id):
    sites_config = load_sites_config()
    
    if site_id not in sites_config:
        return json({"success": False, "error": "站点不存在"}, status=404)
    
    sites_config[site_id]["enabled"] = not sites_config[site_id].get("enabled", True)
    save_sites_config(sites_config)
    
    return json({
        "success": True,
        "enabled": sites_config[site_id]["enabled"],
        "message": "状态更新成功"
    })


@bp.route("/api/add_account/<site_id>", methods=["POST"])
@require_auth
async def add_account(request, site_id):
    data = request.json
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return json({"success": False, "error": "用户名和密码不能为空"}, status=400)
    
    sites_config = load_sites_config()
    
    if site_id not in sites_config:
        return json({"success": False, "error": "站点不存在"}, status=404)
    
    if "accounts" not in sites_config[site_id]:
        sites_config[site_id]["accounts"] = []
    
    sites_config[site_id]["accounts"].append({
        "username": username,
        "password": password,
        "enabled": True
    })
    
    save_sites_config(sites_config)
    
    return json({"success": True, "message": "账户添加成功"})


@bp.route("/api/check/<site_id>", methods=["POST"])
@require_auth
async def check_site_now(request, site_id):
    sites_config = load_sites_config()
    
    if site_id not in sites_config:
        return json({"success": False, "error": "站点不存在"}, status=404)
    
    site = Site.from_config(site_id, sites_config[site_id])
    
    scheduler = CheckScheduler()
    results = await scheduler.check_site(site)
    
    return json({
        "success": True,
        "results": [
            {
                "success": r.success,
                "message": r.message,
                "timestamp": r.timestamp.isoformat()
            } for r in results
        ]
    })
