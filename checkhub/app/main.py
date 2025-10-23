from sanic import Sanic
from app import create_app
from app.utils.scheduler import CheckScheduler
from app.utils.logger import get_main_logger

app = create_app()
scheduler = CheckScheduler()
logger = get_main_logger()


@app.before_server_start
async def setup_scheduler(app, loop):
    logger.info("正在启动 CheckHub...")
    scheduler.start()


@app.after_server_stop
async def shutdown_scheduler(app, loop):
    logger.info("正在关闭 CheckHub...")
    scheduler.stop()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
        auto_reload=True
    )
