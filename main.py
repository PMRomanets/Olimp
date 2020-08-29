import pandas as pd
from configs.config import parameter
from os.path import join
from flask import Flask
from app.scedules_app import Schedules
from app.interesting_app import InterestingClass
from app.home_page import get_app
from flask_login import current_user

from app.staff_only_login import LoginProcess, User
from flask import Flask, Response
from flask_login import LoginManager, UserMixin, login_required
from flask import Response, request
from app.user import get_login_form_html
from os.path import join as path_join


server = Flask(__name__)


login_process_obj = LoginProcess()

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/"

server.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx',
    TESTING=False,
    LOGIN_DISABLED=False
)



@server.route("/stuff_only/", methods=['GET', 'POST'])
def index():
    password = request.form.get("password")
    username = request.form.get("username")
    if (username is None) or (password is None):
        return Response(get_login_form_html())
    else:
        return login_process_obj.login(username, password)

@login_manager.user_loader
def load_user(id):
     if login_process_obj.username_check(id):
        return User(id)
     else:
         return None

@server.route('/stuff_room_K/', methods=['GET', 'POST'])
@login_required
def fk():
    print(current_user.name)
    return app_home.index()

@server.route('/stuff_room_Y/', methods=['GET', 'POST'])
@login_required
def fy():
    print(current_user.name)
    return app_home.index()

@server.route('/stuff_room_D/', methods=['GET', 'POST'])
@login_required
def fd():
    print(current_user.name)
    return app_home.index()

@server.route('/stuff_room_chief/', methods=['GET', 'POST'])
@login_required
def fchief():
    print(current_user.name)
    return app_home.index()

if __name__ == '__main__':
    asset_dir = parameter["assets_dir"]
    dummy_text = "СТОРІНКА ЗНАХОДИТСЯ НА СТАДІЇ РОЗРОБКИ"
    many_thanks_text = "ДЯКУЄМО ЩО СКОРИСТАЛИСЯ СЕРВІСОМ!"
    obj_schedule = Schedules("/", "НА ГОЛОВНУ")
    schedules = obj_schedule.get_app(server, "/schedules/")
    dir_ = path_join(asset_dir,"interesting_K")
    interesting_k_obj = InterestingClass("/", "Цікавинки карате", dir_, fig_ext="jpeg", limit_objects_number=3)
    interesting_k_app = interesting_k_obj.get_app(server, "/interesting_K/")
    dir_ = path_join(asset_dir, "interesting_Y")
    interesting_y_obj = InterestingClass("/", "Цікавинки йоги", dir_, fig_ext="jpeg", limit_objects_number=3)
    interesting_y_app = interesting_y_obj.get_app(server, "/interesting_Y/")
    dir_ = path_join(asset_dir, "interesting_D")
    interesting_d_obj = InterestingClass("/", "Цікавинки у світі танцю", dir_, fig_ext="jpeg", limit_objects_number=1)
    interesting_d_app = interesting_d_obj.get_app(server, "/interesting_D/")

    dir_ = path_join(asset_dir, "summertime")
    interesting_d_obj = InterestingClass("/", "Цікавинки у світі танцю", dir_, fig_ext="jpeg", limit_objects_number=1)
    interesting_d_app = interesting_d_obj.get_app(server, "/summertime/")


    # obj_main = Schedules(f"/home/", "НА ГОЛОВНУ")
    app_home = get_app(server, f"/")
    server.run(port=5500, debug=True)
