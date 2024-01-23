from .enums import TimerStatus


def phrase_for_start_first_greeting(first_name: str):
    return f"<b>Намаскар, {first_name}! Я таймер-бот для йогических практик!\n\n Рекомендую в настройках этого чата установить другую мелодию оповещения, чтобы ты мог отличать сообщения таймера от других по звуку и не отвлекался от практики!\n\n\nДА ПРИБУДЕТ С ТОБОЙ СИЛА!</b>"

def phrase_for_choose_practice():
    return 'Выбери раздел и следуй инструкциям. \nЖелаю хорошей практики...'

def phrase_asana():
    return 'Введи количество асан в твоём комплексе: '

def phrase_asana_time():
    return 'Введи количество секунд в асане.\n\n\nМожно ввести целое число - это будет количество секунд.\nМожно ввести значение в формате 00:00, \nгде первая пара числе - это минуты,\n а вторая - секунды.'

def phrase_asana_relax_time():
    return 'Введи количество секунд на отдых между асанами.\n\n\nМожно ввести целое число - это будет количество секунд.\nМожно ввести значение в формате 00:00, \nгде первая пара числе - это минуты,\n а вторая - секунды.'

def phrase_shavasana_time():
    return 'Введи количество минут на шавасаную.\n\n\nМожно ввести целое число - это будет количество минут.\nМожно ввести значение в формате 00:00, \nгде первая пара числе - это минуты,\n а вторая - секунды.'

def phrase_pranayama():
    return 'Введи количество пранаям в твоём комплексе: '

def phrase_wrong_prana_asana_count():
    return 'Не похоже на целое число. \n\nПовтори ввод и продолжи формировать комплекс.'

def phrase_prana_time():
    return 'Введи количество минут на упражнение пранаямы.\n\n\nМожно ввести целое число - это будет количество минут.\nМожно ввести значение в формате 00:00, \nгде первая пара числе - это минуты,\n а вторая - секунды.'

def phrase_prana_reload():
    return 'Введи количество секунд на перевод дыхания между упражнениями.\n\n\nМожно ввести целое число - это будет количество секунд.\nМожно ввести значение в формате 00:00, \nгде первая пара числе - это минуты,\n а вторая - секунды.'

def phrase_wrong_prana_asana_time():
    return 'Не похоже на целое число или на формат 00:00, где первая пара чисел - минуты, вторая пара чисел - секунды.\n\nПовтори ввод и продолжи формировать комплекс.'

def phrase_prana_meditation_time():
    return 'Введи количество минут на медитацию после пранаямы.\n\n\nМожно ввести целое число - это будет количество минут.\nМожно ввести значение в формате 00:00, \nгде первая пара числе - это минуты,\n а вторая - секунды.'

def phrase_meditation():
    return 'Введи количество минут для медитации и начинай практику.\n\nЯ прерву её звуком сообщения в назначенный срок!\n\n\nМожно ввести целое число - это будет количество минут.\nМожно ввести значение в формате 00:00, \nгде первая пара числе - это минуты,\n а вторая - секунды.'

def phrase_wrong_meditation():
    return 'Не похоже на целое число или на формат 00:00, где первая пара чисел - минуты, вторая пара чисел - секунды.\n\nПовтори ввод и начни практику.'



def phrase_for_answer_to_main_menu_buttons(button_title: str):
    return f"You pressed {button_title}"


def phrase_for_notify_admins_about_some_event(
    user_name: str, user_nickname: str, weekday: str, date: str, time: str
):
    return f"❗️{user_name} {user_nickname} что-то сделал в {weekday} <b>{date}</b> в <b>{time}</b>"


def phrase_for_timer_message(
    total: str, 
    rest: str, 
    status: TimerStatus = TimerStatus.RUNNING,
):
    text = f"========================\n\nИдёт медитация\n\nВыбранное время: {total}"
    if rest:
        text += f"\n\nОставшееся время: {rest}"
    text += f"\n\n==========[ {status.value} ]=========="

    return text


def phrase_for_pranasana_timer_message(
    count: int,
    cnt: int,
    practice_time: str,
    reload_time: str,
    meditation_time: str,
    flag: str,
    status: TimerStatus = TimerStatus.RUNNING,
):

    if flag == 'go':
        print('PRANA_TIME---->', practice_time)
        text = f"========================\n\nПрактика пранаямы!\n\nВсего упражнений: {count} \n\nУпражнение №: {cnt}\n\nОставшееся время: {practice_time}"
        text += f"\n\n==========[ {status.value} ]=========="
        return text

    if flag == 'relax':
        print('reload_TIME---->', reload_time)
        text = f"========================\n\nПереведи дух перед следующим упражнением!\n\nОставшееся время для отдыха: {reload_time}"
        text += f"\n\n==========[ {status.value} ]=========="
        return text

    if flag == 'meditation':
        print('meditation_TIME---->', meditation_time)
        text = f"========================\n\nМедитация\n\nОставшееся время: {meditation_time}"
        text += f"\n\n==========[ {status.value} ]=========="
        return text
    
    if flag == 'asana_go':
        print('ASANA_TIME---->', practice_time)
        text = f"========================\n\nПрактика асаны!\n\nВсего упражнений: {count} \n\nУпражнение №: {cnt}\n\nОставшееся время: {practice_time}"
        text += f"\n\n==========[ {status.value} ]=========="
        return text

    if flag == 'asana_relax':
        print('reload_TIME---->', reload_time)
        text = f"========================\n\nКомпенсурующая асана или шавасана!\n\nОставшееся время для отдыха: {reload_time}"
        text += f"\n\n==========[ {status.value} ]=========="
        return text

    if flag == 'asana_meditation':
        print('meditation_TIME---->', meditation_time)
        text = f"========================\n\nШавасана\n\nОставшееся время: {meditation_time}"
        text += f"\n\n==========[ {status.value} ]=========="
        return text
    