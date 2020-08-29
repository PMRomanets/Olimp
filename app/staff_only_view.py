import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
# from database import data_access
from templates.dummy_page_pattern import Dummy
# from templates import navigation as nav
import time
import dash_dangerously_set_inner_html
from configs import config

from configs.config import parameter

from os.path import join as path_join
import base64
import pandas as pd
import dash_table as dt
from urllib import parse

class StuffOnly:

    def __init__(self, addr, user_class):
        self.addr = addr
        self.user_class = user_class

    def get_layout(self):

            r_style = parameter["radiobutton_labels_style"]
            r_items = dcc.RadioItems(
                id="edit-radio",
                options=[{'label': parameter[], 'value': value_} for value_ in
                         parameter["stuff_only_permissions_list"][self.user_class]],
                value=list(parameter["terminal_types"].values())[0],
                style=r_style,
                inputStyle={"margin-right": "20px", "margin-left": "10px"}

            )
            translate_segment = parameter["translate_segment"]
            style = parameter["dropdown_labels_style"]
            translate_terminal = parameter["translate_terminal"]

            dropdown_list = [html.H1("термінал:", style=style),
                             html.Div(id='terminal-dropdown1', style=dict(
                                 width='60%',
                                 verticalAlign="middle",
                                 labelStyle={'display': 'inline-block', 'text-align': 'justify'})
                                      # insert default dropdown for terminal
                                      , children=[dcc.Dropdown(
                                     id='terminal-dropdown',
                                     options=opt_,
                                     value=5063,
                                     placeholder='Please select the terminal id.',
                                     style=dict(
                                         width='70%',
                                         verticalAlign="middle",
                                         labelStyle={'display': 'inline-block', 'text-align': 'justify'}))])
                , html.H1("зона:", style=style),
                             html.Div(id='segment-dropdown1', style=dict(
                                 width='60%',
                                 verticalAlign="middle",
                                 labelStyle={'display': 'inline-block', 'text-align': 'justify'}),
                                      # insert default dropdown for segments
                                      children=[dcc.Dropdown(
                                          id='segment-dropdown',
                                          options=[{'label': translate_segment[i], 'value': i} for i in
                                                   self.get_drop_segments_lst(5063)],
                                          value=self.get_drop_segments_lst(5063)[0],
                                          placeholder='Please select a date',
                                          style=dict(
                                              width='50%',
                                              verticalAlign="middle",
                                              labelStyle={'display': 'inline-block', 'text-align': 'justify'}))])
                , html.H1("дата:", style=style)
                , html.Div(id='date-dropdown1', style=dict(
                    width='60%',
                    verticalAlign="middle",
                    labelStyle={'display': 'inline-block', 'text-align': 'justify'}),
                           # insert default dropdown for dates
                           children=[dcc.Dropdown(
                               id='date-dropdown',
                               options=[{'label': str(i), 'value': i} for i in self.get_drop_dates(5063)],
                               value=self.get_drop_dates(5063)[0],
                               placeholder='Please select a date',
                               style=dict(
                                   width='50%',
                                   verticalAlign="middle",
                                   labelStyle={'display': 'inline-block', 'text-align': 'justify'}))])

                             ]

            if self.add_table:
                title = "РОЗКЛАД ДЛЯ СПІВРОБІТНИКІВ ТЕРМІНАЛІВ"

            elif self.add_graph:
                if self.fact:
                    title = "ПОРІВНЯННЯ ПРОГНОЗНИХ ТА ФАКТИЧНИХ ДАННИХ"
                else:
                    title = "ПРОГНОЗ В МЕЖАХ ДНЯ"

            inner_part_ = [html.Div(r_items, className="radiobuttons", style={'padding': 30}),
                           html.Div(dropdown_list, className="float-clear", style={'display': 'flex'})
                           ]

            if self.add_graph:
                inner_part_.append(dcc.Graph(id='terminal_segment_graph',
                                             config={"displayModeBar": bool(parameter["displayModeBar"]),
                                                     'displaylogo': False, "modeBarButtonsToRemove": parameter[
                                                     "modeBarButtonsToRemove"]}))  # {modeBarButtonsToRemove: ['toImage']}
            if self.add_table:
                inner_part_.append(html.Div(id='terminal_schedule_table'))

            assets_folder = config.parameter["excel-path"]
            image_filename = path_join(assets_folder, "Disk-download.png")
            # image_filename = path_
            encoded_image_download = base64.b64encode(open(image_filename, 'rb').read())
            image_filename = path_join(assets_folder, "View.png")
            encoded_image_view = base64.b64encode(open(image_filename, 'rb').read())
            on_click_images = [
                html.Img(src=f'data:image/png;base64,{encoded_image_download.decode()}', className="download_img",
                         id="download_img_id", n_clicks=0, title="Вивантаження даних (*.xlsx, *.csv)"),
                html.Img(src=f'data:image/png;base64,{encoded_image_view.decode()}', className="view_img",
                         id="view_img_id", n_clicks=0, title="Перегляд даних")]
            inner_part_.append(html.Div(on_click_images))
            # inner_part_.append(html.Button(id='submit-val', n_clicks=0, children= [html.Abbr(title="somth.-"), "g"]))
            inner_part_.append(html.Div(id='input-on-submit'))
            inner_part_.append(html.Div(id="download_links_id", children=[html.A(id="download_csv_id"),
                                                                          html.A(id="download_xlsx_id")]))

            #     [ html.P(' ')
            # ,html.A('Download CSV', id='my-link', download="data.csv",
            #     href="",
            #     target="_blank")
            # ]))

            # html.A('Download CSV', id='my-link', download="data.csv",
            #        href="",
            #        target="_blank")
            inner_part_.append(html.Div(id='data-table'))
            # inner_part_.append(dcc.Upload(id="download_predicted_back_btn", children=["enter_predicted_back"]))
            # inner_part_.append(dcc.Upload(id="download_predicted_forward_btn", children=["enter_predicted_forward"]))
            # inner_part_.append(html.A(id="A_id"))

            children_ = self.dummy.get_children(title, inner_part_)
            return html.Div(children=children_)
