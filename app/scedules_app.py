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

class Schedules:
    def __init__(self,  home_url, home_name, table=True, graph=False, daily=False, fact=False):
        self.dummy = Dummy(home_url, home_name)
        self.fact = fact
        self.add_table = table
        self.add_graph = graph
        self.daily = daily
        self.model_ = {}



    def get_layout(self):
        #
        r_style = parameter["radiobutton_labels_style"]
        r_items = dcc.RadioItems(
            id="sport-types-radio",
            options=[{'label': key, 'value': parameter["sport_types"][key]} for key in parameter["sport_types"].keys()],
            value=list(parameter["sport_types"].values())[0],
            style=r_style,
            inputStyle={"margin-right": "20px", "margin-left": "10px"}

        )

        style = parameter["dropdown_labels_style"]

        opt_ = [{'label': parameter["K"][i], 'value': i} for i in parameter["K"].keys()]

        dropdown_list = [html.H1("тренер:", style=style),
                         html.Div(id='instructor-dropdown1', style=dict(
                             width='80%',
                             verticalAlign="middle",
                             labelStyle={'display': 'inline-block', 'text-align': 'justify'})
                                  # insert default dropdown for terminal
                                  , children=[dcc.Dropdown(
                    id='instructor-dropdown',
                    options=opt_,
                    value=opt_[0]["value"],
                    placeholder='Please select instructor name',
                    style=dict(
                    width='90%',
                    verticalAlign="middle", labelStyle={'display': 'inline-block', 'text-align': 'justify'}))])


                   ]


        title = "РОЗКЛАД ЗАНЯТЬ З ІНСТРУКТОРАМИ КЛУБУ"


        inner_part_ = [html.Div(r_items, className="radiobuttons", style={'padding': 30}), html.Div(dropdown_list, className="float-clear",  style={'display': 'flex'})
            ]
        inner_part_.append(html.Div(id='instructor_photo'))
        inner_part_.append(html.Div(id='terminal_schedule_table'))

        assets_folder = config.parameter["assets_dir"]
        image_filename = path_join(assets_folder, "Disk-download.png")
        # image_filename = path_
        encoded_image_download = base64.b64encode(open(image_filename, 'rb').read())
        image_filename = path_join(assets_folder, "View.png")
        encoded_image_view = base64.b64encode(open(image_filename, 'rb').read())
        on_click_images =[
        html.Img(src=f'data:image/png;base64,{encoded_image_download.decode()}', className="download_img",
                 id="download_img_id", n_clicks=0, title="Вивантаження розкладу (*.xlsx, *.csv)"),
        html.Img(src=f'data:image/png;base64,{encoded_image_view.decode()}', className="view_img",
                 id="view_img_id", n_clicks=0, title="Приховати розклад")]
        inner_part_.append(html.Div(on_click_images))
        # inner_part_.append(html.Button(id='submit-val', n_clicks=0, children= [html.Abbr(title="somth.-"), "g"]))
        inner_part_.append(html.Div(id='input-on-submit'))
        inner_part_.append(html.Div(id="download_links_id", children=[html.A(id="download_csv_id"),
                                                                      html.A(id="download_xlsx_id")]))

        inner_part_.append(html.Div(id='data-table'))

        children_ = self.dummy.get_children(title,  inner_part_)
        return html.Div(children=children_)
###################
    def _get_current_dataframe(self, s_type, instructor):
        assets_folder = config.parameter["data_dir"]
        filename = path_join(assets_folder, f"schedule_{s_type}_{instructor}.csv")
        if os.path.exists(filename):
            df = pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=["день тижня", "час", "група"])
        return df

    def _get_instructor_photo(self, s_type, instructor):
        assets_folder = config.parameter["assets_dir"]
        filename = path_join(assets_folder, f"photo_{s_type}_{instructor}.png")
        if not os.path.exists(filename):
            filename = path_join(assets_folder, f"photo_unknown.png")
        return filename

    def get_app(self, server, url):

        app = Dash(__name__, url_base_pathname=url, server=server, assets_folder=parameter["assets_dir"])
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.layout = self.get_layout()
        app.config['suppress_callback_exceptions'] = True

        ################################################################
        @app.callback(Output('input-on-submit', 'children'), [Input('sport-types-radio', 'values'), Input('instructor-dropdown', 'values'),
                                                              Input("download_img_id", "n_clicks")])
        def submit_filename(sport_type, instructor, n_click):

            if n_click & 1:
                if instructor is None:
                    instructor_ = ""
                else:
                    instructor_ = parameter[sport_type][instructor]
                if sport_type is None:
                    sport_type_ = ""
                else:
                    sport_type_ = parameter["sport_types_inv"][sport_type]
                val = f"розклад_{instructor_}_{sport_type_}"
                return dcc.Input(id="input-on-submit-value", type='text', value=val)
            else:
                return ""



        @app.callback(Output("download_links_id", 'children'),
                      [Input("download_img_id", 'n_clicks'), Input('input-on-submit-value', 'value')])
        def download_data(n_click, value_):
            if n_click & 1:
                return [html.A(f"SAVE AS '{value_}.csv'; ", id="download_csv_id", download=value_+".csv", href="")
                    , html.Div(" "),
                html.A(f" SAVE AS '{value_}.xlsx';", id="download_xlsx_id", download=value_+".xlsx", href="")]
            else:
                return [html.A(id="download_csv_id"), html.A(id="download_xlsx_id")]

        @app.callback(Output("download_csv_id", 'href'),
                      [Input("download_csv_id", 'n_clicks'), Input('sport-types-radio', 'value'), Input('instructor-dropdown', 'value')])
        def download_csv(n_click, s_type, instructor):
            # if n_click is not None:
            df = self._get_current_dataframe(s_type, instructor)
            csv_string = df.to_csv(index=False, encoding='utf-8')
            csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + parse.quote(csv_string)
            return csv_string

        @app.callback(Output("download_xlsx_id", 'href'),
                      [Input("download_xlsx_id", 'n_clicks'), Input('sport-types-radio', 'value'), Input('instructor-dropdown', 'value')])
        def download_excel(n_click, s_type, instructor):
            # if n_click is not None:
            try:
                df = self._get_current_dataframe(s_type, instructor)
                xlsx_string = df.to_csv(index=False, encoding='utf-8')
                xlsx_string = "data:text/xlsx;charset=utf-8,%EF%BB%BF" + parse.quote(xlsx_string)
            except Exception as ex:
                print(ex)
                xlsx_string = "data:text/xlsx;charset=utf-8,%EF%BB%BF" + parse.quote("")
            return xlsx_string


        @app.callback(Output('data-table', 'children'),
                      [Input("view_img_id", 'n_clicks'), Input('sport-types-radio', 'value'), Input('instructor-dropdown', 'value')])
        def look_at_the_shedule(n_click, s_type, instructor):
            if n_click & 1:
                return ""
            else:
                df = self._get_current_dataframe(s_type, instructor)

                return dt.DataTable(
                id='model-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                editable=False,
                row_deletable=False,
                style_cell={'fontSize': 20, 'font-family': 'Arial', 'padding': '15px'},
                style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
                },
                data=df.to_dict('records'))



        @app.callback(Output('instructor-dropdown1', 'children'),
                      [Input('sport-types-radio', 'value')])
        def update_instructor_drop_dow(s_type):
            opt_ = [{'label': parameter[s_type][i], 'value': i} for i in
                    parameter[s_type].keys()]
            return dcc.Dropdown(
                    id='instructor-dropdown',
                    options=opt_,
                    value="0",
                    placeholder='Please select instructor name',
                    style=dict(
                    width='90%',
                    verticalAlign="middle", labelStyle={'display': 'inline-block', 'text-align': 'justify'}))


        @app.callback(Output('instructor_photo', 'children'),
                      [ Input('sport-types-radio', 'value'), Input('instructor-dropdown', 'value')])
        def update_figure(s_type, instructor):
            try:
                image_filename = self._get_instructor_photo(s_type, instructor)
                encoded_image_view = base64.b64encode(open(image_filename, 'rb').read())
                # print("update_figure:", s_type," ", instructor)
                if instructor in parameter[s_type].keys():
                    title_ = parameter[s_type][instructor]
                else:
                    title_ = ""
                return html.Img(src=f'data:image/png;base64,{encoded_image_view.decode()}', className="photo_img",
                             id="instructor_photo_id", n_clicks=0, title=title_)
            except:
                return ""

        #
        #
        # @app.callback(Output('terminal_schedule_table', 'children'),
        #               [Input('terminal-dropdown', 'value'),
        #                Input('date-dropdown', 'value'),
        #                Input('segment-dropdown', 'value'),
        #                Input("terminal-types-radio", 'value')])
        # def update_table(terminal_id, date, segment, terminal_type):
        #     log.info('VIEW :: update_table')
        #     if terminal_type == "I":
        #         if terminal_id is None:
        #             terminal_id = 5063
        #     elif terminal_type == "VL":
        #         if terminal_id is None:
        #             terminal_id = 1294
        #     elif terminal_type == "MT":
        #         if terminal_id is None:
        #             terminal_id = 4371
        #     elif terminal_type == "U4":
        #         if terminal_id is None:
        #             terminal_id = 4360
        #     return self.model_[int(terminal_id)].get_table(name=segment, date=date)

        return app

