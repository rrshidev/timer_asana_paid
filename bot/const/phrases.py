
def phrase_for_start_first_greeting(data):
    return f'<b>Намаскар, {data.get("name")}! Я таймер-бот для йогических практик!\n\n Рекомендую в настройках этого чата установить другую мелодию оповещения, чтобы ты мог отличать сообщения таймера от других по звуку и не отвлекался от практики!\n\n\nДА ПРИБУДЕТ С ТОБОЙ СИЛА!</b>'

def phrase_for_choose_practice():
    return 'Выбери раздел и следуй инструкциям. \nЖелаю хорошей практики...'

def phrase_for_answer_to_main_menu_buttons(data):
    return "You pressed " + data["button_title"]

def phrase_for_notify_admins_about_some_event(data):
    return "❗️" + data["user_name"] + " " + data["user_nickname"] + " что-то сделал в " + data["weekday"] + " <b>" + data["date"] + "</b> в <b>" + data["time"]