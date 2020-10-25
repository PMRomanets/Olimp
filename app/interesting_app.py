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

class InterestingClass:
    def __init__(self,  home_url, title, assets_dir_path, fig_ext="png", limit_objects_number=3):
        self.title = title
        self.dummy = Dummy(home_url, "НА ГОЛОВНУ")
        self.assets_dir_path = assets_dir_path
        self.fig_ext = fig_ext
        self.limit_objects_number = limit_objects_number


    def get_layout(self):
        inner_part_ = []
        for idx in range(1, self.limit_objects_number+1):
            image_filename = path_join(self.assets_dir_path, f"fig{idx}."+self.fig_ext)
            if path_exists(image_filename):
                encoded_image = base64.b64encode(open(image_filename, 'rb').read())
                img_child = html.Img(src=f'data:image/{self.fig_ext};base64,{encoded_image.decode()}', className=f"img{idx}",
                         id=f"img_id_{idx}")
                inner_part_.append(img_child)
            else:
                print(f"wrong path {image_filename}")

            # for txt_object in (, f"body{idx}.txt", f"ref{idx}.txt"):
            header_filename = path_join(self.assets_dir_path, f"header{idx}.txt")
            if path_exists(header_filename):
                with open(header_filename, "r") as file:
                    for txt_line in file.readlines():
                        header_child = html.H1(children=txt_line)
                        inner_part_.append(header_child)
            else:
                print(f"no header file {idx}")
            body_filename = path_join(self.assets_dir_path, f"body{idx}.txt")
            if path_exists(body_filename):
                with open(body_filename, "r") as file:
                    for txt_line in file.readlines():
                        body_child = html.Li(children=txt_line)
                        inner_part_.append(body_child)
            else:
                print(f"no body file {idx}")
            inner_part_.append(html.Br())

            ref_filename = path_join(self.assets_dir_path, f"ref{idx}.txt")
            if path_exists(ref_filename):
                with open(ref_filename, "r") as file:
                    lines_ = file.readlines()
                    if len(lines_)>0:
                        inner_part_.append(html.Div("Більше інформації за посиланнями:"))
                    for ref_idx, txt_line in enumerate(lines_):
                        # ref_child = html.A(children=f"see {idx}.{ref_idx}", href=txt_line)
                        ref_child = html.A(children=f"див. {ref_idx+1}): {txt_line}", href=txt_line)
                        inner_part_.append(ref_child)
                        inner_part_.append(html.Br())
            else:
                print(f"no ref file {idx}")
            inner_part_.append(html.Br())
        # return html.Div(children=inner_part_)
        # title = "ЦІКАВО ЗНАТИ:"
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

