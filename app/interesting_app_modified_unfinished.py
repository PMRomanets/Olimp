import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
# from database import data_access
from app.dummy_page_pattern import Dummy
# from templates import navigation as nav
import time
import dash_dangerously_set_inner_html
from configs import config
from urllib.parse import quote as urlquote
from configs.config import parameter
# import flask_login
# from additional import security as sec
from dash.dependencies import Input, Output, State
# import uuid
from flask import redirect
# from os import remove
# from os.path import join as path_join
import base64
# import pandas as pd
# import dash_table as dt
# from urllib import parse
from os.path import join as path_join, curdir, abspath
from os.path import exists as path_exists
from os.path import isfile, getsize
from os import mkdir, remove, listdir, utime
import shutil
from time import sleep
from dash.dependencies import ALL
from datetime import datetime

# from pathlib import Path

class InterestingClass:
    def __init__(self,  home_url, title, assets_dir_path, fig_ext="png", limit_objects_number=3, sudo=False):
        self.title = title
        self.url = None
        self.dummy = Dummy(home_url, "НА ГОЛОВНУ")
        self.assets_dir_path = assets_dir_path
        self.tmp_assets_dir_path = path_join(assets_dir_path, "tmp")
        self.fig_ext = fig_ext
        self.limit_objects_number = limit_objects_number
        self.sudo = sudo
        self.images_status = {img: True for img in range(1, limit_objects_number+1)}
        if (not path_exists(self.tmp_assets_dir_path)) and sudo:
            mkdir(self.tmp_assets_dir_path)
            self.initial_source_path = self.tmp_assets_dir_path
        else:
            self.initial_source_path = self.assets_dir_path

    def _copy_all_to_tmp(self):
        if not path_exists(self.tmp_assets_dir_path):
            mkdir(self.tmp_assets_dir_path)

        for file in self._get_files_list():
            src_path = path_join(self.assets_dir_path, file)
            desc_path = path_join(self.tmp_assets_dir_path, file)
            shutil.copy(src_path, desc_path)

    def _copy_all_from_tmp(self):
        if not path_exists(self.tmp_assets_dir_path):
            mkdir(self.tmp_assets_dir_path)

        for file in self._get_tmp_files_list():
            src_path = path_join(self.tmp_assets_dir_path, file)
            if getsize(src_path) == 0:
                continue
            desc_path = path_join(self.assets_dir_path, file)
            shutil.copy(src_path, desc_path)

    def _delete_tmp(self):
        if path_exists(self.tmp_assets_dir_path):
            shutil.rmtree(self.tmp_assets_dir_path)

    def _empty_tmp(self):
        if not path_exists(self.tmp_assets_dir_path):
            mkdir(self.tmp_assets_dir_path)

        for file in self._get_tmp_files_list():
            target_path = path_join(self.tmp_assets_dir_path, file)
            remove(target_path)

    def _empty_assert(self):
        for file in self._get_files_list():
            target_path = path_join(self.assets_dir_path, file)
            remove(target_path)

    def get_layout(self):
        # if self.sudo:
        inner_part_ = []
        # else:
        #################################  append image:   #####################
        for idx in range(1, self.limit_objects_number+1):
            image_filename = path_join(self.initial_source_path, f"fig{idx}."+self.fig_ext)
            src_ = f'data:image/{self.fig_ext};base64, '
            if path_exists(image_filename):
                encoded_image = base64.b64encode(open(image_filename, 'rb').read())
                src_ = f'data:image/{self.fig_ext};base64,{encoded_image.decode()}'
                img_child = html.Img(src=src_, className=f"img{idx}",
                         id=f"img-id-{idx}")
                inner_part_.append(img_child)

            else:

                if self.sudo:

                    img_child = html.Img(src=src_,
                                         className=f"img{idx}",
                                         id=f"img-id-{idx}")
                    inner_part_.append(img_child)
            if self.sudo:
                ############################### append 'upload' - tool
                image_ltst = html.Div(id=f"images-list-id-{idx}", children="")
                upload_child = dcc.Upload(id=f'upload-data-{idx}', filename=image_filename,
                                          contents=src_.split(";base64,")[-1],
                                          children=html.Div([
                                                f'перетягніть {self.fig_ext}-файл або ',
                                                html.A(f'ВИБЕРІТЬ {self.fig_ext}-ФАЙЛ')
                                            ]),
                                          style={
                                                'width': '100%',
                                                'height': '60px',
                                                'lineHeight': '60px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'dashed',
                                                'borderRadius': '5px',
                                                'textAlign': 'center',
                                                'margin': '10px'
                                            },
                                            # Allow multiple files to be uploaded
                                            multiple=False
                                        )
                inner_part_.append(image_ltst)
                inner_part_.append(upload_child)
                inner_part_.append(html.Button(parameter["sudo_delete_image_name"], id=f'btn-delete-{idx}', n_clicks=0))
            # for txt_object in (, f"body{idx}.txt", f"ref{idx}.txt"):
            header_filename = path_join(self.initial_source_path, f"header{idx}.txt")
            ######################### append header ###########################
            if self.sudo:
                if path_exists(header_filename):
                    with open(header_filename, "r") as file:
                        text_ = file.read()
                else:
                    text_ = ""
                header_child = dcc.Textarea(value=text_, id=f"header-text-{idx}", style={'width': '100%', 'height': 100})
                inner_part_.append(header_child)
            else:
                if path_exists(header_filename):
                    with open(header_filename, "r") as file:
                        for txt_line in file.readlines():
                            header_child = html.H1(children=txt_line, contentEditable=False)
                            inner_part_.append(header_child)
                else:
                    print(f"no header file {idx}")
            ########################## append body ############
            body_filename = path_join(self.initial_source_path, f"body{idx}.txt")

            if self.sudo:
                if path_exists(body_filename):
                    with open(body_filename, "r") as file:
                        text_ = file.read()
                else:
                    text_ = ""
                body_child = dcc.Textarea(value=text_, id=f"body-text-{idx}", style={'width': '100%', 'height': 600})
                inner_part_.append(body_child)
            else:
                if path_exists(body_filename):
                    with open(body_filename, "r") as file:
                        for txt_line in file.readlines():
                            body_child = html.Li(children=txt_line)
                            inner_part_.append(body_child)
                else:
                    print(f"no body file {idx}")
            inner_part_.append(html.Br())

            ######################### append ref #########################
            ref_filename = path_join(self.initial_source_path, f"ref{idx}.txt")

            if self.sudo:
                if path_exists(ref_filename):
                    with open(ref_filename, "r") as file:
                        text_ = file.read()
                else:
                    text_ = ""
                inner_part_.append(html.Div("Більше інформації за посиланнями:"))
                ref_child = dcc.Textarea(value=text_, id=f"ref-text-{idx}", style={'width': '100%', 'height': 300})
                inner_part_.append(ref_child)
            else:
                if path_exists(ref_filename):
                    with open(ref_filename, "r") as file:
                        lines_ = file.readlines()
                        if len(lines_) > 0:
                            inner_part_.append(html.Div("Більше інформації за посиланнями:"))
                        for ref_idx, txt_line in enumerate(lines_):
                            # ref_child = html.A(children=f"see {idx}.{ref_idx}", href=txt_line)
                            ref_child = html.A(children=f"див. {ref_idx+1}): {txt_line}", href=txt_line,
                                               contentEditable=False)
                            inner_part_.append(ref_child)
                            inner_part_.append(html.Br())
                else:
                    print(f"no ref file {idx}")
            inner_part_.append(html.Br())
            inner_part_.append(html.P("", id=f'header-output-{idx}'))
            inner_part_.append(html.P("", id=f'body-output-{idx}'))
            inner_part_.append(html.P("", id=f'ref-output-{idx}'))

        ref_filename = path_join(self.initial_source_path, f"ref_youtube.txt")

        if self.sudo:
            inner_part_.append(html.Div("Радимо для перегляду (джерело-youtube):"))
            if path_exists(ref_filename):
                with open(ref_filename, "r") as file:
                    text_ = file.readline(1)
                    s = text_.split("/")[-1]

            else:
                text_ = ""
            ref_child = dcc.Textarea(value=text_, id="ref-youtube", style={'width': '100%', 'height':720})
            inner_part_.append(ref_child)
            inner_part_.append(html.P("", id='ref-youtube-output'))
        else:
            if path_exists(ref_filename):
                # inner_part_.append(html.Div("Радимо для перегляду (джерело-youtube):"))
                with open(ref_filename, "r") as file:
                    text_ = file.read()
                    s = "https://www.youtube.com/embed/" + text_.split("/")[-1]
                    inner_part_.append(html.Div("Радимо для перегляду (джерело-youtube):"))
                    inner_part_.append(html.Embed(src=s, width=1280, height=720))
            else:
                s = ""

        if self.sudo:
            inner_part_.append(html.A(html.Button(parameter["sudo_get_default_name"]), href=self.url))
            inner_part_.append(html.Button(parameter["sudo_save_all_name"], id='btn-save-all-id'))
            inner_part_.append(html.P("", id='save-all-output'))
            inner_part_.append(html.P("", id='get-default-output'))


        children_ = self.dummy.get_children(self.title, inner_part_)

        children_.append(
    html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(list("ABC"), id="data", style={"display":"none"}),
    html.Div(id='page-content')
        ]))

        return html.Div(children=children_)

    def _get_files_list(self):
        lst_ = []
        for file_ in listdir(self.assets_dir_path):
            file_a = path_join(self.assets_dir_path, file_)
            if isfile(file_a):
                lst_.append(file_)
        return lst_

    def _get_tmp_files_list(self):
        lst_ = []
        if not path_exists(self.tmp_assets_dir_path):
            mkdir(self.tmp_assets_dir_path)
        for file_ in listdir(self.tmp_assets_dir_path):
            file_a = path_join(self.tmp_assets_dir_path, file_)
            if isfile(file_a):
                lst_.append(file_)
        return lst_

    def get_app(self, server, url):
        self.url = url
        app = Dash(__name__, url_base_pathname=url, server=server, assets_folder=parameter["assets_dir"])
        # app.css.config.serve_locally = True
        # app.scripts.config.serve_locally = True
        app.layout = self.get_layout()
        # app.config['suppress_callback_exceptions'] = False

        #
        ################################################################

        def save_file(name, content):
            """Decode and store a file uploaded with Plotly Dash."""
            if not content is None:
                data = content.encode("utf8").split(b";base64,")[-1]
                if not path_exists(self.tmp_assets_dir_path):
                    print("saving fig. ", self.tmp_assets_dir_path)
                    mkdir(self.tmp_assets_dir_path)
                with open(path_join(self.tmp_assets_dir_path, name), "wb") as fp:
                    fp.write(base64.decodebytes(data))
                return data

        def _upload_figure(image_filename, image_data):
            encoded_image = save_file(image_filename, image_data)
            if encoded_image is not None:
                return f'data:image/{self.fig_ext};base64,{encoded_image.decode()}'

        def _delete_figure(image_filename):
            if not path_exists(self.tmp_assets_dir_path):
                mkdir(self.tmp_assets_dir_path)
            image_abs_filename = path_join(self.tmp_assets_dir_path, image_filename)
            if path_exists(image_abs_filename):
                remove(image_abs_filename)
                # return f'data:image/{self.fig_ext};base64,'
                return image_filename

        def _header_to_txt(idx, text):
            if not path_exists(self.tmp_assets_dir_path):
                mkdir(self.tmp_assets_dir_path)
            file_ = path_join(self.tmp_assets_dir_path, f"header{idx}.txt")
            with open(file_, 'w') as f:
                f.write(text)

        def _body_to_txt(idx, text):
            if not path_exists(self.tmp_assets_dir_path):
                mkdir(self.tmp_assets_dir_path)
            file_ = path_join(self.tmp_assets_dir_path, f"body{idx}.txt")
            print("_body_to_txt:")
            print(abspath(curdir))
            print(path_exists(self.tmp_assets_dir_path))
            print(path_exists(self.assets_dir_path))
            print(file_)
            print(abspath(__file__))
            print("body_to_txt end")
            with open(file_, 'w') as f:
                f.write(text)

        def _ref_to_txt(idx, text):
            if not path_exists(self.tmp_assets_dir_path):
                mkdir(self.tmp_assets_dir_path)
            file_ = path_join(self.tmp_assets_dir_path, f"ref{idx}.txt")
            with open(file_, 'w') as f:
                f.write(text)

        def _ref_youtube_to_txt(text):
            if not path_exists(self.tmp_assets_dir_path):
                mkdir(self.tmp_assets_dir_path)
            file_ = path_join(self.tmp_assets_dir_path, f"ref_youtube.txt")
            with open(file_, 'w') as f:
                f.write(text)

        if self.sudo:

            @app.callback(Output('header-output-1', 'value'),
                          [Input(f"header-text-1", "value")])
            def editing_header1(text):
                _header_to_txt(1, text)
                return ""

            @app.callback(Output('header-output-2', 'value'),
                          [Input(f"header-text-2", "value")])
            def editing_header2(text):
                _header_to_txt(2, text)
                return ""

            @app.callback(Output('header-output-3', 'value'),
                          [Input(f"header-text-3", "value")])
            def editing_header3(text):
                _header_to_txt(3, text)
                return ""

            @app.callback(Output('header-output-4', 'value'),
                          [Input(f"header-text-4", "value")])
            def editing_header4(text):
                _header_to_txt(4, text)
                return ""

            @app.callback(Output('header-output-5', 'value'),
                          [Input(f"header-text-5", "value")])
            def editing_header5(text):
                _header_to_txt(5, text)
                return ""

            @app.callback(Output('header-output-5', 'value'),
                          [Input(f"header-text-5", "value")])
            def editing_header5(text):
                _header_to_txt(5, text)
                return ""

            # @app.callback(Output('header-output-6', 'value'),
            #               [Input(f"header-text-6", "value")])
            # def editing_header6(text):
            #     _header_to_txt(6, text)
            #     return ""
            #
            # @app.callback(Output('header-output-7', 'value'),
            #               [Input(f"header-text-7", "value")])
            # def editing_header7(text):
            #     _header_to_txt(7, text)
            #     return ""
            #
            # @app.callback(Output('header-output-8', 'value'),
            #               [Input(f"header-text-8", "value")])
            # def editing_header8(text):
            #     _header_to_txt(8, text)
            #     return ""
            #
            # @app.callback(Output('header-output-9', 'value'),
            #               [Input(f"header-text-9", "value")])
            # def editing_header9(text):
            #     _header_to_txt(9, text)
            #     return ""
            #
            # @app.callback(Output('header-output-10', 'value'),
            #               [Input(f"header-text-10", "value")])
            # def editing_header10(text):
            #     _header_to_txt(10, text)
            #     return ""


            @app.callback(Output('body-output-1', 'value'),
                          [Input(f"body-text-1", "value")])
            def editing_body1(text):
                _body_to_txt(1, text)
                return ""

            @app.callback(Output('body-output-2', 'value'),
                          [Input(f"body-text-2", "value")])
            def editing_body2(text):
                _body_to_txt(2, text)
                return ""

            @app.callback(Output('body-output-3', 'value'),
                          [Input(f"body-text-3", "value")])
            def editing_body3(text):
                _body_to_txt(3, text)
                return ""

            @app.callback(Output('body-output-4', 'value'),
                          [Input(f"body-text-4", "value")])
            def editing_body4(text):
                _body_to_txt(4, text)
                return ""

            @app.callback(Output('body-output-5', 'value'),
                          [Input(f"body-text-5", "value")])
            def editing_body5(text):
                _body_to_txt(5, text)
                return ""

            # @app.callback(Output('body-output-6', 'value'),
            #               [Input(f"body-text-6", "value")])
            # def editing_body6(text):
            #     _body_to_txt(6, text)
            #     return ""
            #
            # @app.callback(Output('body-output-7', 'value'),
            #               [Input(f"body-text-7", "value")])
            # def editing_body7(text):
            #     _body_to_txt(7, text)
            #     return ""
            #
            # @app.callback(Output('body-output-8', 'value'),
            #               [Input(f"body-text-8", "value")])
            # def editing_body8(text):
            #     _body_to_txt(8, text)
            #     return ""
            #
            # @app.callback(Output('body-output-9', 'value'),
            #               [Input(f"body-text-9", "value")])
            # def editing_body9(text):
            #     _body_to_txt(9, text)
            #     return ""

            # @app.callback(Output('body-output-10', 'value'),
            #               [Input(f"body-text-10", "value")])
            # def editing_body10(text):
            #     _body_to_txt(10, text)
            #     return ""

            # ref - youtube
            @app.callback(Output('ref-youtube-output', 'value'),
                          [Input(f"ref-youtube", "value")])
            def editing_ref_youtube(text):
                _ref_youtube_to_txt(text)
                return ""


            @app.callback(Output('ref-output-1', 'value'),
                          [Input(f"ref-text-1", "value")])
            def editing_ref1(text):
                _ref_to_txt(1, text)
                return ""

            @app.callback(Output('ref-output-2', 'value'),
                          [Input(f"ref-text-2", "value")])
            def editing_ref2(text):
                _ref_to_txt(2, text)
                return ""

            @app.callback(Output('ref-output-3', 'value'),
                          [Input(f"ref-text-3", "value")])
            def editing_ref3(text):
                _ref_to_txt(3, text)
                return ""

            @app.callback(Output('ref-output-4', 'value'),
                          [Input(f"ref-text-4", "value")])
            def editing_ref4(text):
                _ref_to_txt(4, text)
                return ""

            @app.callback(Output('ref-output-5', 'value'),
                          [Input(f"ref-text-5", "value")])
            def editing_ref5(text):
                _ref_to_txt(5, text)
                return ""

            # @app.callback(Output('ref-output-6', 'value'),
            #               [Input(f"ref-text-6", "value")])
            # def editing_ref6(text):
            #     _ref_to_txt(6, text)
            #     return ""
            #
            # @app.callback(Output('ref-output-7', 'value'),
            #               [Input(f"ref-text-7", "value")])
            # def editing_ref7(text):
            #     _ref_to_txt(7, text)
            #     return ""
            #
            # @app.callback(Output('ref-output-8', 'value'),
            #               [Input(f"ref-text-8", "value")])
            # def editing_ref8(text):
            #     _ref_to_txt(8, text)
            #     return ""
            #
            # @app.callback(Output('ref-output-9', 'value'),
            #               [Input(f"ref-text-9", "value")])
            # def editing_ref9(text):
            #     _ref_to_txt(9, text)
            #     return ""
            #
            # @app.callback(Output('ref-output-10', 'value'),
            #               [Input(f"ref-text-10", "value")])
            # def editing_ref10(text):
            #     _ref_to_txt(10, text)
            #     return ""

            @app.callback(Output('get-default-output', 'children'),
                          [Input(f"btn-save-all-id", "n_clicks")])
            def save_all_button(n_cklicks):
                if n_cklicks is not None:
                    self._empty_assert()
                    self._copy_all_from_tmp()
                    # self._delete_tmp()
                    touch_file = parameter["touch_file"]
                    print("touch file", touch_file)
                    if path_exists(touch_file):
                        utime(touch_file, None)
                        sleep(5)
                    return dcc.Location(pathname="/", id="09-99")

            @app.callback(Output(f"img-id-1", 'src'),
                          [Input(f"upload-data-1", "filename"),
                           Input(f"upload-data-1", "contents"), Input("images-list-id-1", "children")])
            def upload_figure(image_filename, image_data, image_status):
                if self.images_status[1]:
                    return _upload_figure("fig1." + self.fig_ext, image_data)
                else:
                    self.images_status[1] = True
                    return ""

            @app.callback(Output(f"img-id-2", 'src'),
                          [Input(f"upload-data-2", "filename"),
                           Input(f"upload-data-2", "contents"), Input("images-list-id-2", "children")])
            def upload_figure(image_filename, image_data, image_status):
                if self.images_status[2]:
                    return _upload_figure("fig2." + self.fig_ext, image_data)
                else:
                    self.images_status[2] = True
                    return ""

            @app.callback(Output(f"img-id-3", 'src'),
                          [Input(f"upload-data-3", "filename"),
                           Input(f"upload-data-3", "contents"), Input("images-list-id-3", "children")])
            def upload_figure(image_filename, image_data, image_status):
                if self.images_status[3]:
                    return _upload_figure("fig3." + self.fig_ext, image_data)
                else:
                    self.images_status[3] = True
                    return ""

            @app.callback(Output(f"img-id-4", 'src'),
                          [Input(f"upload-data-4", "filename"),
                           Input(f"upload-data-4", "contents"), Input("images-list-id-4", "children")])
            def upload_figure(image_filename, image_data, image_status):
                if self.images_status[4]:
                    return _upload_figure("fig4." + self.fig_ext, image_data)
                else:
                    self.images_status[4] = True
                    return ""

            @app.callback(Output(f"img-id-5", 'src'),
                          [Input(f"upload-data-5", "filename"),
                           Input(f"upload-data-5", "contents"), Input("images-list-id-5", "children")])
            def upload_figure(image_filename, image_data, image_status):
                if self.images_status[5]:
                    return _upload_figure("fig5." + self.fig_ext, image_data)
                else:
                    self.images_status[5] = True
                    return ""
            #
            # @app.callback(Output(f"img-id-6", 'src'),
            #               [Input(f"upload-data-6", "filename"),
            #                Input(f"upload-data-6", "contents"), Input("images-list-id-6", "children")])
            # def upload_figure(image_filename, image_data, image_status):
            #     if self.images_status[6]:
            #         return _upload_figure("fig6." + self.fig_ext, image_data)
            #     else:
            #         self.images_status[6] = True
            #         return ""
            #
            # @app.callback(Output(f"img-id-7", 'src'),
            #               [Input(f"upload-data-7", "filename"),
            #                Input(f"upload-data-7", "contents"), Input("images-list-id-7", "children")])
            # def upload_figure(image_filename, image_data, image_status):
            #     if self.images_status[7]:
            #         return _upload_figure("fig7." + self.fig_ext, image_data)
            #     else:
            #         self.images_status[7] = True
            #         return ""
            #
            # @app.callback(Output(f"img-id-8", 'src'),
            #               [Input(f"upload-data-8", "filename"),
            #                Input(f"upload-data-8", "contents"), Input("images-list-id-8", "children")])
            # def upload_figure(image_filename, image_data, image_status):
            #     if self.images_status[8]:
            #         return _upload_figure("fig8." + self.fig_ext, image_data)
            #     else:
            #         self.images_status[8] = True
            #         return ""
            #
            # @app.callback(Output(f"img-id-9", 'src'),
            #               [Input(f"upload-data-9", "filename"),
            #                Input(f"upload-data-9", "contents"), Input("images-list-id-9", "children")])
            # def upload_figure(image_filename, image_data, image_status):
            #     if self.images_status[9]:
            #         return _upload_figure("fig9." + self.fig_ext, image_data)
            #     else:
            #         self.images_status[9] = True
            #         return ""

            @app.callback(Output('page-content', 'children'),
                          [Input('url', 'pathname')])
            def display_page(pathname):
                if self.sudo:
                    if not path_exists(self.tmp_assets_dir_path):
                        mkdir(self.tmp_assets_dir_path)
                    elif len(self._get_tmp_files_list()) > 0:
                        self._empty_tmp()
                        self._copy_all_to_tmp()
                        return """Увага, хтось не закінчив редагування сторінки. Тимчасові фали були видалені,
                                щоб підготувати середовище для вас.
                                 Уникайте одночасного редагування сторінок з іншими тренерами"""
                    else:
                        self._copy_all_to_tmp()
                return ""



            @app.callback(Output("images-list-id-1", 'children'), (Input(f'btn-delete-1', 'n_clicks'),))
            def delete_figures1(n_clicks):
                if n_clicks > 0:
                    self.images_status[1] = False
                    return _delete_figure("fig1." + self.fig_ext)

            @app.callback(Output("images-list-id-2", 'children'), (Input(f'btn-delete-2', 'n_clicks'),))
            def delete_figures2(n_clicks):
                if n_clicks > 0:
                    self.images_status[2] = False
                    return _delete_figure("fig2." + self.fig_ext)

            @app.callback(Output("images-list-id-3", 'children'), (Input(f'btn-delete-3', 'n_clicks'),))
            def delete_figures3(n_clicks):
                if n_clicks > 0:
                    self.images_status[3] = False
                    return _delete_figure("fig3." + self.fig_ext)

            @app.callback(Output("images-list-id-4", 'children'), (Input(f'btn-delete-4', 'n_clicks'),))
            def delete_figures4(n_clicks):
                if n_clicks > 0:
                    self.images_status[4] = False
                    return _delete_figure("fig4." + self.fig_ext)

            @app.callback(Output("images-list-id-5", 'children'), (Input(f'btn-delete-5', 'n_clicks'),))
            def delete_figures5(n_clicks):
                if n_clicks > 0:
                    self.images_status[5] = False
                    return _delete_figure("fig5." + self.fig_ext)

            # @app.callback(Output("images-list-id-6", 'children'), (Input(f'btn-delete-6', 'n_clicks'),))
            # def delete_figures6(n_clicks):
            #     if n_clicks > 0:
            #         self.images_status[6] = False
            #         return _delete_figure("fig6." + self.fig_ext)
            #
            # @app.callback(Output("images-list-id-7", 'children'), (Input(f'btn-delete-7', 'n_clicks'),))
            # def delete_figures7(n_clicks):
            #     if n_clicks > 0:
            #         self.images_status[7] = False
            #         return _delete_figure("fig7." + self.fig_ext)
            #
            # @app.callback(Output("images-list-id-8", 'children'), (Input(f'btn-delete-8', 'n_clicks'),))
            # def delete_figures8(n_clicks):
            #     if n_clicks > 0:
            #         self.images_status[8] = False
            #         return _delete_figure("fig8." + self.fig_ext)
            #
            # @app.callback(Output("images-list-id-9", 'children'), (Input(f'btn-delete-9', 'n_clicks'),))
            # def delete_figures9(n_clicks):
            #     if n_clicks > 0:
            #         self.images_status[9] = False
            #         return _delete_figure("fig9." + self.fig_ext)
            #
            # @app.callback(Output("images-list-id-10", 'children'), (Input(f'btn-delete-10', 'n_clicks'),))
            # def delete_figures10(n_clicks):
            #     if n_clicks > 0:
            #         self.images_status[10] = False
            #         return _delete_figure("fig10." + self.fig_ext)

        # return app
        if self.sudo:
            extra_files_lst = []
            for file in self._get_files_list():
                src_path = path_join(self.assets_dir_path, file)
                extra_files_lst.append(src_path)

            return app## test:
        else:
            return app
