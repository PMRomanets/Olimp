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
# import flask
import uuid
import flask
from os import remove
from os.path import join as path_join
import base64
import pandas as pd
import dash_table as dt
from urllib import parse
from os.path import join as path_join, curdir, abspath
from os.path import exists as path_exists
from os.path import isfile, getsize
from os import mkdir, remove, listdir
import shutil


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

        if sudo:
            self._empty_tmp()
            self._copy_all_to_tmp()

            self.initial_source_path = self.tmp_assets_dir_path
        else:
            self.initial_source_path = self.assets_dir_path

    def _copy_all_to_tmp(self):
        for file in self._get_files_list():
            src_path = path_join(self.assets_dir_path, file)
            desc_path = path_join(self.tmp_assets_dir_path, file)
            shutil.copy(src_path, desc_path)

    def _copy_all_from_tmp(self):
        for file in self._get_tmp_files_list():
            src_path = path_join(self.tmp_assets_dir_path, file)
            if getsize(src_path) == 0:
                continue
            desc_path = path_join(self.assets_dir_path, file)
            shutil.copy(src_path, desc_path)

    def _delete_tmp(self):
        shutil.rmtree(self.tmp_assets_dir_path)



    def _empty_tmp(self):
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
                            header_child = html.H1(children=txt_line, contentEditable=False, id=f"header-{idx}")
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

        # return html.Div(children=inner_part_)
        # title = "ЦІКАВО ЗНАТИ:"
        # inner_part_.append(html.Button(parameter["sudo_get_default_name"], id='btn-default-id'))
        if self.sudo:
            inner_part_.append(html.A(html.Button(parameter["sudo_get_default_name"]), href=self.url))
            inner_part_.append(html.Button(parameter["sudo_save_all_name"], id='btn-save-all-id'))
            inner_part_.append(html.P("", id='save-all-output'))
            inner_part_.append(html.P("", id='get-default-output'))
        children_ = self.dummy.get_children(self.title, inner_part_)
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
        for file_ in listdir(self.tmp_assets_dir_path):
            file_a = path_join(self.tmp_assets_dir_path, file_)
            if isfile(file_a):
                lst_.append(file_)
        return lst_


    def get_app(self, server, url):
        self.url = url
        app = Dash(__name__, url_base_pathname=url, server=server, assets_folder=parameter["assets_dir"])
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.layout = self.get_layout()
        app.config['suppress_callback_exceptions'] = False

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
            image_abs_filename = path_join(self.tmp_assets_dir_path, image_filename)
            if path_exists(image_abs_filename):
                remove(image_abs_filename)
                # return f'data:image/{self.fig_ext};base64,'
                return image_filename

        def _header_to_txt(idx, text):
            file_ = path_join(self.tmp_assets_dir_path, f"header{idx}.txt")
            with open(file_, 'w') as f:
                f.write(text)

        def _body_to_txt(idx, text):
            file_ = path_join(self.tmp_assets_dir_path, f"body{idx}.txt")
            print("_body_to_txt:")
            print(abspath(curdir))
            print(file_)
            print(abspath(__file__))
            print("body_to_txt end")
            with open(file_, 'w') as f:
                f.write(text)

        def _ref_to_txt(idx, text):
            file_ = path_join(self.tmp_assets_dir_path, f"ref{idx}.txt")
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



            @app.callback(Output('get-default-output', 'value'),
                          [Input(f"btn-save-all-id", "n_clicks")])
            def save_all_button(n_cklicks):
                if n_cklicks is not None:
                    self._empty_assert()
                    self._copy_all_from_tmp()
                    self._delete_tmp()
                return ""

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

            #
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


        # return app
        extra_files_lst = []
        for file in self._get_files_list():
            src_path = path_join(self.assets_dir_path, file)
            extra_files_lst.append(src_path)

        return extra_files_lst## test:

