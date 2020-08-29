import dash_core_components as dcc
import dash_html_components as html
import random
# from additional import security as sec
import flask_login

class sec:
    @staticmethod
    def can_see_navigation(user, element):
        return True



def get_navigation():

    user = str(flask_login.current_user)

    ret = []


    about_dropdown = []
    about_dropdown.append(html.Li(html.A('ПРО КЛУБ', href=f'/about_club/')))
    about_dropdown.append(html.Li(html.A('ПРО ТРЕНЕРІВ', href=f'/about_instructors')))
    about_dropdown.append(html.Li(html.A('ВНУТРІШНЯ ПОЛІТИКА', href=f'/about_politics')))
    about_dropdown.append(html.Li(html.A('УСТАТКОВАНЯ ПРИМІЩЕННЯ', href=f'/about_politics')))

    schedules_dropdown = []
    schedules_dropdown.append(html.Li(html.A('РОЗКЛАД ТРЕНУВАНЬ', href=f'/schedules/')))
    schedules_dropdown.append(html.Li(html.A('ВАЖЛИВІ ПОДІЇ', href=f'/events/')))
    # schedules_dropdown.append(html.Li(html.A('ТРЕНЕРСЬКА', href=f'/staff_only/')))

    # additional_reports = []
    # additional_reports.append(html.Li(html.A('КОНТАКТИ', href=f'/contacts/')))
    # additional_reports.append(html.Li(html.A('КОНТАКТИ', href=f'/interesting/')))
    # additional_reports.append(html.Li(html.A('КОНТАКТИ', href=f'/stuff_only/')))
    interesting_dropdown = []
    interesting_dropdown.append(html.Li(html.A('СВІТ КАРАТЕ', href=f'/interesting_K/')))
    interesting_dropdown.append(html.Li(html.A('СВІТ ЙОГИ', href=f'/interesting_Y/')))
    interesting_dropdown.append(html.Li(html.A('СВІТ ТАНЦЮ', href=f'/interesting_D/')))
    ret.append(get_dropdown_menu_item("ПРО НАС", about_dropdown, 'about/'))
    ret.append(get_dropdown_menu_item("НАШ КАЛЕНДАР", schedules_dropdown, 'calendar/'))
    ret.append(get_dropdown_menu_item("РІЗНІ ЦІКАВИНКИ", interesting_dropdown, 'interesting/'))
    ret.append(get_dropdown_menu_item("ЗБОРИ", [], 'summertime/'))
    ret.append(get_dropdown_menu_item("КОНТАКТИ", [], 'contacts/'))
    ret.append(get_dropdown_menu_item("ТРЕНЕРСЬКА", [], 'stuff_only/'))


    return ret


def get_dropdown_menu_item(title, prediction_dropdown, href='#'):
    if prediction_dropdown:
        return html.Ul(
            children=[
                # ul list components
                html.Li(
                    className='dropdown',
                    children=[
                        html.A(
                            title,
                            className='dropbtn'
                        ),
                        html.Div(
                            className='dropdown-content',
                            children=prediction_dropdown
                        )
                    ]

                )
            ]
        )
    else:
        return html.Ul(
            children=[
                html.Li(
                    className='dropdown',
                    children=[
                        html.A(
                            title,
                            href='/' + str(href),
                            className='dropbtn'
                        )

                    ]

                )
            ]
        )
