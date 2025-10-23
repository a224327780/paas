from sanic import Blueprint, response, request
from sanic.response import html, redirect
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import uuid
from app.config import load_settings

bp = Blueprint("auth", url_prefix="/auth")

template_dir = Path(__file__).parent.parent / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(str(template_dir)),
    autoescape=select_autoescape(['html', 'xml'])
)


def get_session(request):
    session_id = request.cookies.get("session_id")
    if session_id and session_id in request.app.ctx.sessions:
        return request.app.ctx.sessions[session_id]
    return None


def create_session(request, user_data):
    session_id = str(uuid.uuid4())
    request.app.ctx.sessions[session_id] = user_data
    return session_id


def require_auth(func):
    async def wrapper(request, *args, **kwargs):
        session = get_session(request)
        if not session:
            return redirect("/auth/login")
        return await func(request, *args, **kwargs)
    return wrapper


@bp.route("/login", methods=["GET"])
async def login_page(request):
    template = jinja_env.get_template("login.html")
    return html(template.render())


@bp.route("/login", methods=["POST"])
async def login(request):
    username = request.form.get("username")
    password = request.form.get("password")
    
    settings = load_settings()
    admin = settings.get("admin", {})
    
    if username == admin.get("username") and password == admin.get("password"):
        session_id = create_session(request, {"username": username})
        resp = redirect("/")
        resp.cookies["session_id"] = session_id
        resp.cookies["session_id"]["httponly"] = True
        return resp
    
    template = jinja_env.get_template("login.html")
    return html(template.render(error="用户名或密码错误"))


@bp.route("/logout")
async def logout(request):
    session_id = request.cookies.get("session_id")
    if session_id and session_id in request.app.ctx.sessions:
        del request.app.ctx.sessions[session_id]
    
    resp = redirect("/auth/login")
    resp.cookies["session_id"] = ""
    resp.cookies["session_id"]["max-age"] = 0
    return resp
