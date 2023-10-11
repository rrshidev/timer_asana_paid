
def phrase_for_start_first_greeting(data):
    return f'<b>Намаскар, {data.get("name")}! Я таймер-бот для йогических практик!\n\n Рекомендую в настройках этого чата установить другую мелодию оповещения, чтобы ты мог отличать сообщения таймера от других по звуку и не отвлекался от практики!\n\n\nДА ПРИБУДЕТ С ТОБОЙ СИЛА!</b>'

def phrase_for_choose_practice():
    return 'Выбери раздел и следуй инструкциям. \nЖелаю хорошей практики...'

def phrase_asana():
    return 'Введи количество асан в твоём комплексе: '

def phrase_asana_time():
    return 'Введи количество секунд в асане: '

def phrase_asana_relax_time():
    return 'Введи количество секунд на отдых между асанами: '

def phrase_shavasana_time():
    return 'Введи количество минут на шавасану: '

def phrase_pranayama():
    return 'Введи количество пранаям в твоём комплексе: '

def phrase_prana_time():
    return 'Введи количество минут на упражнение пранаямы: '

def phrase_prana_reload():
    return 'Введи количество секунд на перевод дыхания между упражнениями: '

def phrase_prana_meditaion_time():
    return 'Введи количество минут на медитацию после пранаямы: '

def phrase_meditation():
    return 'Введи количество минут для медитации и начинай практику.\n' \
               'Я прерву её звуком сообщения в назначенный срок!'

def phrase_wrong():
    return 'Не похоже на нужное значение. \n\nПовтори ввод: '


def phrase_for_answer_to_main_menu_buttons(data):
    return "You pressed " + data["button_title"]

def phrase_for_notify_admins_about_some_event(data):
    return "❗️" + data["user_name"] + " " + data["user_nickname"] + " что-то сделал в " + data["weekday"] + " <b>" + data["date"] + "</b> в <b>" + data["time"]