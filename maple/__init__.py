#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: __init__.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-18 08:03:11
# *************************************************************************
from flask import (Flask, send_from_directory, request, g)
from flask_mail import Mail
from flask_principal import Principal
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from .extensions import (register_maple, register_form, register_babel,
                         register_login)
from .extensions import register_redis, register_cache
from .filters import register_jinja2


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object('config.development')
    return app


def register(app):
    register_babel(app)
    register_form(app)
    register_jinja2(app)
    register_db(app)
    register_login(app)
    register_maple(app)
    register_routes(app)


def register_routes(app):
    from maple.index.views import site
    app.register_blueprint(site, url_prefix='')
    from maple.user.views import site
    app.register_blueprint(site, url_prefix='/u')
    from maple.blog.views import site
    app.register_blueprint(site, url_prefix='/blog')
    from maple.question.views import site
    app.register_blueprint(site, url_prefix='/question')
    from maple.books.views import site
    app.register_blueprint(site, url_prefix='/books')
    import maple.auth.auth
    import maple.admin.admin


def register_db(app):
    db.init_app(app)


app = create_app()
db = SQLAlchemy()
mail = Mail(app)
principals = Principal(app)
redis_data = register_redis(app)
cache = register_cache(app)
register(app)


@app.before_request
def before_request():
    from maple.main.mark_record import allow_ip, mark_online, mark_visited
    from maple.blog.forms import SearchForm
    allow_ip(request.remote_addr)
    g.search_form = SearchForm()
    g.user = current_user
    mark_online(request.remote_addr)
    if '/static/' in request.path:
        pass
    elif '/favicon.ico' in request.path:
        pass
    elif '/robots.txt' in request.path:
        pass
    else:
        path = request.path
        mark_visited(request.remote_addr, path)


@app.route('/robots.txt')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
