from flask_login import current_user
from flask import Flask, Response
from flask_login import LoginManager, UserMixin, login_required
from flask import Response, request
from app.user import get_login_form_html
from os.path import join as path_join
from configs.config import parameter
from app.scedules_app import Schedules
from app.interesting_app import InterestingClass
from app.home_page import get_app, get_sudo_app
from app.contacts_app import ContactsClass
from app.staff_only_login import LoginProcess, User
from flask import send_from_directory, url_for
from os.path import join as path_join



app = Flask(__name__)


login_process_obj = LoginProcess()

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/stuff_only/"

app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx',
    TESTING=False,
    LOGIN_DISABLED=False
)



@app.route("/stuff_only/", methods=['GET', 'POST'])
def index():
    # try:
    password = request.form.get("password")
    username = request.form.get("username")
    # except Exception as ex:
    #     print("!!!!!", ex)
    #     return ex
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



@app.route('/stuff_room/', methods=['GET', 'POST'])
@login_required
def fk():
    print("try enter stuff room")
    print("exactly ", current_user.name)
    return app_home_sudo.index()


@app.route('/sudo/', methods=['GET', 'POST'])
@login_required
def fsudo():
    print(current_user.name)
    return app_home_sudo.index()

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

@app.route('/favicon.ico')
@login_required
def favicon():
    print(current_user.name)
    return send_from_directory(path_join(parameter["assets_dir"]), "favicon.ico", mimetype="image")

extra_files_lst = []

asset_dir = parameter["assets_dir"]
dummy_text = "СТОРІНКА ЗНАХОДИТСЯ НА СТАДІЇ РОЗРОБКИ"
many_thanks_text = "ДЯКУЄМО ЩО СКОРИСТАЛИСЯ СЕРВІСОМ!"
obj_schedule = Schedules("/", "НА ГОЛОВНУ")
schedules = obj_schedule.get_app(app, "/schedules/")

dir_ = path_join(asset_dir,"interesting_K")
interesting_k_obj = InterestingClass("/", "Цікавинки карате", dir_, fig_ext="jpeg", limit_objects_number=5)
interesting_k_app = interesting_k_obj.get_app(app, "/interesting_K/")

interesting_k_obj_s = InterestingClass("/", "Цікавинки карате", dir_, fig_ext="jpeg", limit_objects_number=5, sudo=True)
list_ = interesting_k_obj_s.get_app(app, "/sudo_interesting_K/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "interesting_Y")
interesting_y_obj = InterestingClass("/", "Цікавинки йоги", dir_, fig_ext="jpeg", limit_objects_number=5)
interesting_y_app = interesting_y_obj.get_app(app, "/interesting_Y/")

interesting_y_obj_s = InterestingClass("/", "Цікавинки йоги", dir_, fig_ext="jpeg", limit_objects_number=5, sudo=True)
list_ = interesting_y_obj_s.get_app(app, "/sudo_interesting_Y/")

extra_files_lst += list_

dir_ = path_join(asset_dir, "interesting_D")

interesting_d_obj = InterestingClass("/", "Цікавинки у світі танцю", dir_, fig_ext="jpeg", limit_objects_number=3)
interesting_d_app = interesting_d_obj.get_app(app, "/interesting_D/")

interesting_d_obj_s = InterestingClass("/stuff_room/", "Цікавинки у світі танцю", dir_, fig_ext="jpeg", limit_objects_number=3, sudo=True)
list_ = interesting_d_obj_s.get_app(app, "/sudo_interesting_D/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "interesting_A")
interesting_d_obj = InterestingClass("/", "Цікавинки у світі акробатики", dir_, fig_ext="jpeg", limit_objects_number=3)
interesting_d_app = interesting_d_obj.get_app(app, "/interesting_A/")

interesting_d_obj_s = InterestingClass("/stuff_room/", "Цікавинки у світі акробатики", dir_, fig_ext="jpeg", limit_objects_number=3, sudo=True)
list_ = interesting_d_obj_s.get_app(app, "/sudo_interesting_A/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "summertime")
interesting_d_obj = InterestingClass("/", "Літній відпочинок та тренування...", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/summertime/")

interesting_d_obj_s = InterestingClass("/stuff_room/", "Літній відпочинок та тренування...", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj_s.get_app(app, "/sudo_summertime/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "club_history")
interesting_d_obj = InterestingClass("/", "Втілюйте мрії у життя разом з нами!", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/club_history/")


interesting_d_obj_s = InterestingClass("/stuff_room/", "Втілюйте мрії у життя разом з нами!", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj_s.get_app(app, "/sudo_club_history/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "about_instructors_K")
interesting_d_obj = InterestingClass("/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/about_instructors_K/")

interesting_d_obj_s = InterestingClass("/stuff_room/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj_s.get_app(app, "/sudo_about_instructors_K/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "about_instructors_Y")
interesting_d_obj = InterestingClass("/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/about_instructors_Y/")

interesting_d_obj_s = InterestingClass("/stuff_room/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj_s.get_app(app, "/sudo_about_instructors_Y/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "about_instructors_HH")
interesting_d_obj = InterestingClass("/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/about_instructors_HH/")

interesting_d_obj_s = InterestingClass("/stuff_room/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj_s.get_app(app, "/sudo_about_instructors_HH/")
extra_files_lst += list_


dir_ = path_join(asset_dir, "events")
interesting_d_obj = InterestingClass("/", "УЧАСТЬ У ЗМАГАННЯХ — ЦЕ НЕПЕРЕСІЧНИЙ ДОСВІД, НЕЗАЛЕЖНО ВІД РЕЗУЛЬТАТУ", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/events/")

interesting_d_obj_s = InterestingClass("/stuff_room/", "УЧАСТЬ У ЗМАГАННЯХ — ЦЕ НЕПЕРЕСІЧНИЙ ДОСВІД, НЕЗАЛЕЖНО ВІД РЕЗУЛЬТАТУ", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj_s.get_app(app, "/sudo_events/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "about_instructors_G")
interesting_d_obj = InterestingClass("/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/about_instructors_G/")

interesting_d_obj = InterestingClass("/stuff_room/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj.get_app(app, "/sudo_about_instructors_G/")
extra_files_lst += list_


dir_ = path_join(asset_dir, "about_instructors_SH")
interesting_d_obj = InterestingClass("/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/about_instructors_SH/")


interesting_d_obj = InterestingClass("/stuff_room/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj.get_app(app, "/sudo_about_instructors_SH/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "about_instructors_A")
interesting_d_obj = InterestingClass("/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/about_instructors_A/")


interesting_d_obj = InterestingClass("/stuff_room/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj.get_app(app, "/sudo_about_instructors_A/")
extra_files_lst += list_


dir_ = path_join(asset_dir, "about_equipment")
interesting_d_obj = InterestingClass("/", "Комфорт, Ефективність, Безпека", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/about_equipment/")

interesting_d_obj = InterestingClass("/stuff_room/", "Комфорт, Ефективність, Безпека", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj.get_app(app, "/sudo_about_equipment/")
extra_files_lst += list_

dir_ = path_join(asset_dir, "about_politics")
interesting_d_obj = InterestingClass("/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5)
interesting_d_app = interesting_d_obj.get_app(app, "/about_politics/")

dir_ = path_join(asset_dir, "about_politics")
interesting_d_obj = InterestingClass("/stuff_room/", "Наш досвід + Ваше бажання = результат!", dir_, fig_ext="jpg", limit_objects_number=5, sudo=True)
list_ = interesting_d_obj.get_app(app, "/sudo_about_politics/")
extra_files_lst += list_

contacts_obj = ContactsClass("/", "Вдячні за Вашу цікавіть до клубу! Зв'яжіться з нами!")
contacts_app = contacts_obj.get_app(app, "/contacts/")
# obj_main = Schedules(f"/home/", "НА ГОЛОВНУ")
app_home = get_app(app, "/")
app_home_sudo = get_sudo_app(app, "/stuff_room/")
# app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))
if __name__ == '__main__':
    app.run(port=5550, debug=True, extra_files=extra_files_lst)
