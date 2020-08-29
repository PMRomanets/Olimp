import dash_html_components as html
from dash import Dash
from app.navigations import get_navigation
import time
from configs import config
import dash_dangerously_set_inner_html
from app import base
# import flask_login
import flask
# import dash
# def get_base_template(server, body, title, user_name):
from flask_login import LoginManager
from configs.config import parameter
# from config.config import user_parameter
# from cached_property import cached_property


def get_layout():
    return html.Div(children=[
        html.Link(href='/assets/my.css' + "?t=" + str(time.time()), rel='stylesheet'),
        base.get_header("ДИТЯЧО-ЮНАЦЬКИЙ СПОРТИВНИЙ КЛУБ \"ОЛІМП\""),
        html.Div(children=get_navigation(), className="float-clear"),
        html.Div(id='output-container',
                 className="home-text",
                 children=[dash_dangerously_set_inner_html.DangerouslySetInnerHTML("""   """)]),
        html.Div(style=parameter["footer_style"],
                 children=[" дзвоніть нам: " + str(parameter["main_mobile_phone_number"])
                     , " пішіть у Viber:" + str(parameter["viber_phone_number"])
                     , " пішіть на електронну пошту:" + str(parameter["club_email"])])
    ])


def get_app(server, url_path):

    assets_folder = config.parameter["assets_dir"]
    app = Dash(name='home', url_base_pathname=url_path, server=server, assets_folder=assets_folder)

    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True

    app.layout = get_layout()

    app.config['suppress_callback_exceptions'] = True

    return app


def update_output():
    return None


if __name__ == "__main__":
    server = flask.Flask(__name__)

    server.secret_key = 'xxxxyyyyyzzzzz'

    login_manager = LoginManager()
    login_manager.init_app(server)
    login_manager.login_view = 'login'
    app = get_app(server, "/home/")
    app.run_server(debug=True)
    # app = dash.Dash(__name__, server=server)

