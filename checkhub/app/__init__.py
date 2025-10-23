from sanic import Sanic
from sanic_ext import Extend

def create_app():
    app = Sanic("CheckHub")
    
    app.config.SECRET_KEY = "change-this-secret-key-in-production"
    app.config.FALLBACK_ERROR_FORMAT = "html"
    
    Extend(app)
    
    app.ctx.sessions = {}
    
    from app.views import auth, sites, dashboard
    app.blueprint(auth.bp)
    app.blueprint(sites.bp)
    app.blueprint(dashboard.bp)
    
    return app
