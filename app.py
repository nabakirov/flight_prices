from sanic import Sanic

from extentions import redis, scheduler
from flights.views import blueprint as flights_blueprint


def create_app(config):
    app = Sanic(__name__)
    app.config.update(config)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    redis.init_app(app)
    scheduler.init_app(app)


def register_blueprints(app):
    app.blueprint(flights_blueprint)

