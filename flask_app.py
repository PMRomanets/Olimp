from flask_login import current_user
from flask import Flask, Response
from flask_login import LoginManager, UserMixin, login_required
from flask import Response, request
from app.user import get_login_form_html
from os.path import join as path_join
from configs.config import parameter
from app.scedules_app import Schedules
from app.interesting_app import InterestingClass
from app.home_page import get_app
from app.contacts_app import ContactsClass
from app.staff_only_login import LoginProcess, User


app = Flask(__name__)


login_process_obj = LoginProcess()

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"

app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx',
    TESTING=False,
    LOGIN_DISABLED=False
)



@app.route("/stuff_only/", methods=['GET', 'POST'])
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

@app.route('/stuff_room_K/', methods=['GET', 'POST'])
@login_required
def fk():
    print(current_user.name)
    return app_home.index()

@app.route('/stuff_room_Y/', methods=['GET', 'POST'])
@login_required
def fy():
    print(current_user.name)
    return app_home.index()

@app.route('/stuff_room_D/', methods=['GET', 'POST'])
@login_required
def fd():
    print(current_user.name)
    return app_home.index()

@app.route('/stuff_room_chief/', methods=['GET', 'POST'])
@login_required
def fchief():
    print(current_user.name)
    return app_home.index()


asset_dir = parameter["assets_dir"]
dummy_text = "СТОРІНКА ЗНАХОДИТСЯ НА СТАДІЇ РОЗРОБКИ"
many_thanks_text = "ДЯКУЄМО ЩО СКОРИСТАЛИСЯ СЕРВІСОМ!"
obj_schedule = Schedules("/", "НА ГОЛОВНУ")
schedules = obj_schedule.get_app(app, "/schedules/")
dir_ = path_join(asset_dir,"interesting_K")
interesting_k_obj = InterestingClass("/", "Цікавинки карате", dir_, fig_ext="jpeg", limit_objects_number=3)
interesting_k_app = interesting_k_obj.get_app(app, "/interesting_K/")
dir_ = path_join(asset_dir, "interesting_Y")
interesting_y_obj = InterestingClass("/", "Цікавинки йоги", dir_, fig_ext="jpeg", limit_objects_number=3)
interesting_y_app = interesting_y_obj.get_app(app, "/interesting_Y/")
dir_ = path_join(asset_dir, "interesting_D")
interesting_d_obj = InterestingClass("/", "Цікавинки у світі танцю", dir_, fig_ext="jpeg", limit_objects_number=1)
interesting_d_app = interesting_d_obj.get_app(app, "/interesting_D/")

dir_ = path_join(asset_dir, "summertime")
interesting_d_obj = InterestingClass("/", "Цікавинки у світі танцю", dir_, fig_ext="jpeg", limit_objects_number=1)
interesting_d_app = interesting_d_obj.get_app(app, "/summertime/")

contacts_obj = ContactsClass("/", "Вдячні за Вашу цікавіть до клубу! Зв'яжіться з нами!")
contacts_app = contacts_obj.get_app(app, "/contacts/")
# obj_main = Schedules(f"/home/", "НА ГОЛОВНУ")
app_home = get_app(app, f"/")
if __name__ == '__main__':
    app.run(port=5500, debug=True)
