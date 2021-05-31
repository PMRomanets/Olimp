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
import pandas as pd
import dash_table as dt
from urllib import parse
from os.path import join as path_join
from os.path import exists as path_exists
import sys
# sys.path.append("/home/ubuntu/.local/lib/python3.6/site-packages/")
#from gmaps import maps
from app.util.googlemap import Map, GoogleMaps
from flask import render_template


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
        # map_html = "<iframe src=\"https://www.google.com/maps/d/u/0/embed?mid=1tl1LmxhIp0uPd0h0e3-9uW2_QoXiCSnq\" width="640" height="480"></iframe>"
        inner_part_.append(html.Embed(src="https://www.google.com/maps/d/u/0/embed?mid=1tl1LmxhIp0uPd0h0e3-9uW2_QoXiCSnq", width="640", height="480"))
###################
        # mymap = Map(
        #     identifier="view-side",
        #     lat=37.4419,
        #     lng=-122.1419,
        #     markers=[(37.4419, -122.1419)]
        # )
        # sndmap = Map(
        #     identifier="sndmap",
        #     lat=37.4419,
        #     lng=-122.1419,
        #     markers=[
        #         {
        #             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        #             'lat': 37.4419,
        #             'lng': -122.1419,
        #             'infobox': "<b>Hello World</b>"
        #         },
        #         {
        #             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        #             'lat': 37.4300,
        #             'lng': -122.1400,
        #             'infobox': "<b>Hello World from other place</b>"
        #         }
        #     ]
        # )
        # MapComponent = render_template('example.html', mymap=mymap, sndmap=sndmap)
        # inner_part_.append(MapComponent)
        ##########################

        children_ = self.dummy.get_children(self.title, inner_part_)
        return html.Div(children=children_)


    def get_app(self, server, url):

        app = Dash(__name__, url_base_pathname=url, server=server, assets_folder=parameter["assets_dir"])
        # GoogleMaps(server, key='AIzaSyDtCnDWyEJt3hM4o1SF2TbtDfa1700rOF0')
        app.scripts.config.serve_locally = True
        app.layout = self.get_layout()
        app.config['suppress_callback_exceptions'] = True

        ################################################################
        # @server.route("/map/")
        # def mapview():
        #     # creating a map in the view
        #     mymap = Map(
        #         identifier="view-side",
        #         lat=37.4419,
        #         lng=-122.1419,
        #         markers=[(37.4419, -122.1419)]
        #     )
        #     sndmap = Map(
        #         identifier="sndmap",
        #         lat=37.4419,
        #         lng=-122.1419,
        #         markers=[
        #             {
        #                 'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        #                 'lat': 37.4419,
        #                 'lng': -122.1419,
        #                 'infobox': "<b>Hello World</b>"
        #             },
        #             {
        #                 'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        #                 'lat': 37.4300,
        #                 'lng': -122.1400,
        #                 'infobox': "<b>Hello World from other place</b>"
        #             }
        #         ]
        #     )
        #     return render_template('tamplate.html', mymap=mymap, sndmap=sndmap)

        return app

