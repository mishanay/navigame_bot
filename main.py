# -*- coding: utf-8 -*-
import telebot
import time
import random
import os
import json





bot = telebot.TeleBot(token)
#users_inf = {}
#coord = {}
phrazes = [
    "Яндекс новости показывают, что в Москве большие пробки с голодными \
водителями. Имеет смысл послать продавцов туда.\n*Адрес*: %s.\
\n*Координаты*: %f %f\n*Навиадрес*: %s", "Ваш отдел \
анализа рынка провел кропотливую работу и пришел к выводу, \
что самой прибыльной точкой на данный момент является %s.\
\nКоординаты: %f %f\n*Навиадрес*: %s"]
phraze = " в \
Москве и дает открытый концерт! Срочно отправьте продавцов со свежими \
плюшками туда.\n*Адрес*: %s.\n*Координаты*: %f %f\n*Навиадрес*: %s"
phrazes.append("Наташа Королева"+phraze)
phrazes.append("Бритни Спирс"+phraze)
phrazes.append("Лепс"+phraze)

navi_addresses = ['310985', '109019', '210131', '210975', '117504', '711502', '141052', '151050', '212207', '421250']

f = open('info_dump.txt', 'r')
r = f.read()
users_inf = json.loads(r)
f.close()

f = open('coord_dump.txt', 'r')
r = f.read()
coord = json.loads(r)
f.close()




@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, """В этой игре вы бизнесмен, \
который продает плюшки на улице. Ищите места с наибольшим скоплением голодных людей \
(в пробках, на гуляниях) и отправляйте туда ваших продавцов со свежими плюшками, \
а в этом вам поможет новая система адресов - *Навиадреса*.
Подробности на сайте:\nhttps://about.naviaddress.com/
Вопросы и предложения присылайте на почту:\nmp@naviworldcorp.com""", parse_mode="Markdown")
    users_inf[str(message.chat.id)] = {}
    users_inf[str(message.chat.id)]['prestige'] = 0
    users_inf[str(message.chat.id)]['money'] = 0
    users_inf[str(message.chat.id)]['last'] = list()
    users_inf[str(message.chat.id)]['workers'] = 3
    users_inf[str(message.chat.id)]['last_action'] = time.time()
    print(users_inf)
    base_menu(message.chat.id)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        check(message.chat.id)
        users_inf[str(message.chat.id)]['last_action'] = time.time()
        print(users_inf)
        log_f = open('log_file.txt', 'a')
        log_f.write(time.ctime()+'\n')
        log_f.write(json.dumps(users_inf))
        log_f.write('\n')
        if message.text == 'Развитие бизнеса🏢':
            bot.send_message(message.chat.id, "Ваш престиж = %d\nДеньги = %d\nСвободных продавцов = %d" %
                             (users_inf[str(message.chat.id)]['prestige'],
                              users_inf[str(message.chat.id)]['money'],
                              users_inf[str(message.chat.id)]['workers'])
                             )
            resources_menu(message.chat.id)
        elif message.text == 'Работа💰':
            random.shuffle(phrazes)
            random.shuffle(navi_addresses)
            bot.send_message(message.chat.id, phrazes[0] %
                             (coord[navi_addresses[0]]['address'], coord[navi_addresses[0]]['lon'],
                              coord[navi_addresses[0]]['lat'], navi_addresses[0]), parse_mode="Markdown")
            cur_dir = os.getcwd()
            pic = cur_dir + '/picture/' + coord[navi_addresses[0]]['picture'] + '.png'
            img = open(pic, 'rb')
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id, img)
            management_menu(message.chat.id)
        elif message.text == 'Анализ рынка📈':
            random.shuffle(phrazes)
            random.shuffle(navi_addresses)
            bot.send_message(message.chat.id, phrazes[0] %
                             (coord[navi_addresses[0]]['address'],
                              coord[navi_addresses[0]]['lon'],
                              coord[navi_addresses[0]]['lat'],
                              navi_addresses[0]),
                             parse_mode="Markdown"
                             )
            cur_dir = os.getcwd()
            pic = cur_dir + '/picture/' + coord[navi_addresses[0]]['picture'] + '.png'
            img = open(pic, 'rb')
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id, img)
            management_menu(message.chat.id)
        elif message.text == 'Помощь🎓':
            bot.send_message(message.chat.id, """В этой игре вы бизнесмен, \
который продает плюшки на улице. Ищите места с наибольшим скоплением голодных людей \
(в пробках, на гуляниях) и отправляйте туда ваших продавцов со свежими плюшками, \
а в этом вам поможет новая система адресов - Навиадреса.
Подробности на сайте:\nhttps://about.naviaddress.com/
Вопросы и предложения присылайте на почту: mp@naviworldcorp.com""")
            base_menu(message.chat.id)
        elif message.text == 'Отправить продавца👷':
            if users_inf[str(message.chat.id)]['workers'] > 0:
                go(message.chat.id)
            else:
                new = users_inf[str(message.chat.id)]['last'][0]
                bot.send_message(message.chat.id, "Все продавцы отправлены на\
заработки. Ближайший вернется в %s" % time.strftime("%H:%M", time.gmtime(new + 10800)))
                management_menu(message.chat.id)
        elif message.text in navi_addresses:
            cur_time = time.time()
            if users_inf[str(message.chat.id)]['workers'] > 0:
                payment = 35
                str_mess = ("Еда отправлена по навиадресу %s, подробная информация про место всегда"
                            " доступна на сайте http://naviaddress.com/7495/")
                str_mess += message.text
                str_mess += "\nПродавец вернется через 30 минут.\nВаша прибыль 35 монет."
                bot.send_message(message.chat.id, str_mess % message.text)
                bot.send_chat_action(message.chat.id, 'find_location')
                bot.send_location(message.chat.id, coord[message.text]['lon'], coord[message.text]['lat'])
                users_inf[str(message.chat.id)]['money'] += payment + users_inf[str(message.chat.id)]['prestige']
                users_inf[str(message.chat.id)]['workers'] -= 1
                users_inf[str(message.chat.id)]['last'].append(cur_time + 1800)
                f = open("check_files/new_"+str(random.randint(0, 100000000) % 1000)+".txt", 'a')
                f.write(str(message.chat.id)+' ')
                f.write(str(cur_time + 1800)+'\n')
                f.close()
            else:
                new = users_inf[str(id)]['last'][0]
                bot.send_message(message.chat.id, "Все продавцы отправлены на\
заработки. Ближайший вернется в %s" % time.strftime("%H:%M", new))
            management_menu(message.chat.id)
        elif message.text == 'Нанять продавца🏃':
            if users_inf[str(message.chat.id)]['money'] > 500:
                users_inf[str(message.chat.id)]['money'] -= 500
                users_inf[str(message.chat.id)]['workers'] += 1
            else:
                bot.send_message(message.chat.id, ("Новый продавец стоит 300 монет,"
                                                   " денег пока не хватает😢")
                                 )
            resources_menu(message.chat.id)
        elif message.text == 'Купить рекламу📰':
            if users_inf[str(message.chat.id)]['money'] > 200:
                users_inf[str(message.chat.id)]['money'] -= 200
                users_inf[str(message.chat.id)]['prestige'] += 10
            else:
                bot.send_message(message.chat.id, ("Разместить рекламу стоит 200 монет,"
                                                   " денег пока не хватает😢")
                                 )
            resources_menu(message.chat.id)
        elif message.text == 'Вернутся в главное меню⬅':
            base_menu(message.chat.id)
        elif message.text == 'Отчет📝':
            report(message.chat.id)
            management_menu(message.chat.id)
        elif message.text == 'Бонус🎁':
            bot.send_message(message.chat.id, "Продавцы👷 - основной ресурс\
 вашего бизнеса. Отправляя их на точки, вы продаете плюшки🍩 и получаете деньги💰. Пригласи друга\
 и получи бонус. Будет реализовано в следующей версии.")
            base_menu(message.chat.id)
        else:
            bot.send_message(message.chat.id, ("Работник выехал по данному адресу,"
                                               " но потерялся по пути и вернулся ни с чем!😢")
                             )
            management_menu(message.chat.id)
        check_activity()
        log_f.close()
    except:
        pass


def check(chat_id):
    try:
        while len(users_inf[str(chat_id)]['last']) > 0:
            if users_inf[str(chat_id)]['last'][0] <= time.time():
                users_inf[str(chat_id)]['last'].pop(0)
                users_inf[str(chat_id)]['workers'] += 1
                # bot.send_message(id,
                #                  "Работник вернулся с точки и снова готов к работе!\
# \nСвободных продавцов = %d\nПродавцов на точках = %d" %
#                                 (users_inf[str(id)]['workers'], len(users_inf[str(id)]['last'])))
            else:
                break
    except:
        pass


# def check_workers():
    # pass
    # while True:
    #    real_time = time.time()
    #    for key, element in users_inf.items():


def check_activity():
    real_time = time.time()
    for key, element in users_inf.items():
        if element['last_action'] + 43200 < real_time:
            bot.send_message(int(key), ("Хей, хей, хей! Ты забыл про своих работников."
                                        " Они принесли кучу бабла и готовы снова работать!")
                             )
            element['last_action'] = time.time()


# def delay_message(id):
    # while not delay_q.empty():
    #    real_time = time.time()
    #    first_elem = delay_q.get()
    #    while real_time < first_elem[1]:
    #        time.sleep(300)
    #    bot.send_message(int(first_elem[0]), "Продавец вернулся c точки\n")
    # global delay_num
    # delay_num = 0
    # bot.send_message(int(id), "Продавец вернулся c точки\n")


def base_menu(chat_id):
    try:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        first_button = 'Работа💰'
        second_button = 'Помощь🎓'
        third_button = 'Развитие бизнеса🏢'
        fourth_button = 'Бонус🎁'
        user_markup.row(first_button, second_button)
        user_markup.row(third_button, fourth_button)
        bot.send_message(chat_id, "Что дальше?", reply_markup=user_markup)
    except:
        pass


def management_menu(chat_id):
    try:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        first_button = 'Анализ рынка📈'
        second_button = 'Отправить продавца👷'
        third_button = 'Отчет📝'
        fourth_button = 'Вернутся в главное меню⬅'
        user_markup.row(first_button, second_button)
        user_markup.row(third_button, fourth_button)
        bot.send_message(chat_id, "Что дальше?", reply_markup=user_markup)
    except:
        pass


def resources_menu(chat_id):
    try:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        first_button = 'Нанять продавца🏃'
        second_button = 'Купить рекламу📰'
        fourth_button = 'Вернутся в главное меню⬅'
        user_markup.row(first_button, second_button)
        user_markup.row(fourth_button)
        bot.send_message(chat_id, "Что дальше?", reply_markup=user_markup)
    except:
        pass


def report(user_id):
    if len(users_inf[str(user_id)]['last']):
        bot.send_message(user_id, ("Свободных продавцов = %d\n"
                                   "Продавцов на точках = %d\n"
                                   "Деньги = %d\n"
                                   "Продавец вернется в %s"
                                   ) %
                         (users_inf[str(user_id)]['workers'],
                          len(users_inf[str(user_id)]['last']),
                          users_inf[str(user_id)]['money'],
                          time.strftime("%H:%M",
                                        time.gmtime(users_inf[str(user_id)]['last'][0] + 10800)
                                        )
                          )
                         )
    else:
        bot.send_message(user_id, ("Свободных продавцов = %d\n"
                                   "Продавцов на точках = %d\n"
                                   "Деньги = %d\n"
                                   ) %
                         (users_inf[str(user_id)]['workers'],
                          len(users_inf[str(user_id)]['last']),
                          users_inf[str(user_id)]['money']
                          )
                         )


def go(chat_id):
    try:
        bot.send_message(chat_id, ("Введите адрес назначения📍 в любом удобном для"
                              " вас виде: почтовый адрес, координаты или навиадрес.")
                         )
    except:
        pass


bot.polling(none_stop=True, interval=1)
