import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
# from database import data_access
from app.dummy_page_pattern import Dummy
# from templates import navigation as nav
import time
import dash_dangerously_set_inner_html
from configs import config

from configs.config import parameter
# import flask_login
# from additional import security as sec
from dash.dependencies import Input, Output, State
# import flask
import uuid
import flask
import os
from os.path import join as path_join
import base64
import pandas as pd
import dash_table as dt
from urllib import parse
from os.path import join as path_join
from os.path import exists as path_exists

class ContactsClass:
    def __init__(self,  home_url, title):
        self.title = title
        self.dummy = Dummy(home_url, "НА ГОЛОВНУ")

    def get_layout(self):
        inner_part_ = []
        ways = parameter["way_to_connect"]
        df = pd.DataFrame({ways[wkey]: [parameter[wkey]] for wkey in ways.keys()})
        df = df.T
        df.reset_index(drop=False, inplace=True)
        df.columns = ["way", "connection_id"]
        transate_col = {"way":"засіб зв'язку", "connection_id": "номер"}

        table = dt.DataTable(
                id='contacts-table',
                columns=[{"name": transate_col[id_], "id": id_} for id_ in df.columns],
                editable=False,
                row_deletable=False,
                style_cell={'fontSize': 20, 'font-family': 'Arial', 'padding': '15px'},
                style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
                },
                data=df.to_dict('records'))

        inner_part_.append(table)
        inner_part_.append(html.Br())

        children_ = self.dummy.get_children(self.title, inner_part_)
        return html.Div(children=children_)


    def get_app(self, server, url):

        app = Dash(__name__, url_base_pathname=url, server=server, assets_folder=parameter["assets_dir"])
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.layout = self.get_layout()
        app.config['suppress_callback_exceptions'] = True

        ################################################################


        return app

