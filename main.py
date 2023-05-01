'''

Этот чат бот написан для лагеря Звездный(Орленок)
В нем можно найти новые знакомста на смену заранее


'''
# Импортируем необходимые библиотеки
import telebot
from telebot import types
from sqlalchemy.orm import sessionmaker
from db import engine
from crud import get_all, create_user, check_user, get_random_user, check_use, create_used, get_used_us

# Создаем сессию базы данных для общения с ней
session = sessionmaker(bind=engine)
s = session()

# Подключаемя к боту через токен (в дальнейшем токен нужно переместить в переменную среды)
bot = telebot.TeleBot('AAFqz5NZcSOIEpoOWBfjW5hDvf38')

# Обработчик стартовой команды
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    prog = types.KeyboardButton(text='Поехали! 🚀🚀🚀') # Кнопка Поехали, которая будет стартовать регистрацию
    markup.add(prog)
    # Отправление приветственного сообщения с информацией о боте
    bot.send_photo(message.chat.id, photo='https://static.tildacdn.com/tild3961-3032-4634-b862-613437323966/content_hotel_56fd20.jpg', caption=f'Приветствую тебя {message.from_user.first_name} в чат-боте лагеря Звёздный!\n \nЭтот бот создан для того, чтобы заранее знакомиться с ребятами, которые будут на смене с тобой.\n\n Для начала заполни небольшую анкету о себе : )\n\nЕсли вам нужна помощь в использовании, напишите /help', reply_markup=markup)

# Обработчик текстовых сообщений пользователя и фоток
@bot.message_handler(content_types = ['text', 'photo'])
def main(message):
    user={}
    c_u = check_user(s, message.from_user.id) # Проверка зарегистрирован ли пользователь

    if message.text == 'Поехали! 🚀🚀🚀': # Если сообщение поехали, проверяем зарегестрирован ли пользователь( это важно, если да, то в базе данных будет ошибка)
        if c_u:
            r_k = types.ReplyKeyboardRemove()
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            prog = types.KeyboardButton(text='ИСКАТЬ 🔎')
            markup.add(prog)
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы!', reply_markup = r_k)
            bot.send_message(message.chat.id, 'Но ничего страшного, вы можете начать искать', reply_markup = markup)

        else: # Если пользователь не зареган, начинаем опрос
            r_k = types.ReplyKeyboardRemove()
            msg_1 = bot.send_message(message.chat.id, 'Как вас зовут (Сначала введите фамилию, потом имя через пробел)?', reply_markup = r_k)
            bot.register_next_step_handler(msg_1, name_handler, user)
    elif message.text == 'ИСКАТЬ 🔎': # Если пользователь отправил сообщение ИСКАТЬ, начинаем поиск пользователей, если они есть и сам пользователь зареган
        if c_u:

            users = get_all(s) # Получение информации о всех пользователях
            last = False
            while True: # в цикле ждем пока выпадет рандомный пользователь, которого еще не было( вся инфа хранится в бд )
                user = get_random_user(users)
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("ОБЩАТЬСЯ!", url=f'https://t.me/{user["username"]}')# Ссылка на аккаунт пользоватлея
                print(user['name'])
                if not(check_use(s, message.from_user.id,user['telid'])):
                    create_used(s, user['telid'], message.from_user.id)
                    markup.add(button1)
                    if len(users) == get_used_us(s, message.from_user.id):
                        last=True
                    break
                elif len(users) == get_used_us(s, message.from_user.id):
                    break
            print(get_used_us(s, message.from_user.id))
            if len(users) == get_used_us(s, message.from_user.id) and not(last): # Если кол-во просмотренных пользователей равно кол-ву всех, значит все пользователи просмотрены
                bot.send_message(message.chat.id, 'К сожалению, пользователи кончились, вы просмотрели всех. Вернитесь чуть позже')
            else:
                bot.send_message(message.chat.id, f"{user['name']}\n\nИз города:{user['city']}\n\nВозраст:{user['age']}\n\nЕдет на {user['smen']}-ю смену\n\nО себе:{user['about_me']}", reply_markup = markup)
        else: 
            bot.send_message(message.chat.id, 'Вы еще не зарегистрированы! Но ничего страшного, вы можете начать регистрацию, нажав ПОЕХАЛИ') # Выводим, если пользователь не зареган
# Весь опросник выполнен в нескольких функциях, каждая из которых последовательно вызывается
# НАДО ДОДЕЛАТЬ: ФИЛЬТРЫ ДЛЯ ВВОДА
def name_handler(message, user): # функция получения имени пользователя
    name = message.text
    user['name'] = name # Записываем имя в словарь пользователя
    msg_2 = bot.send_message(message.chat.id, 'Из какого ты города, области, края и т.д?')
    bot.register_next_step_handler(msg_2, city_handler, user) # Когда пользователь ввел имя, переходим в функцию получения региона


def city_handler(message, user): # функция получения региона
    city = message.text
    user['city'] = city # Записываем город в словарь пользователя
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) # Создаем кнопки выбора предпочтения по полу (Мальчи/девочки) для следующего вопроса
    boy_button = types.KeyboardButton(text='Мальчики')
    girl_button = types.KeyboardButton(text='Девочки')
    markup.add(boy_button)
    markup.add(girl_button)
    msg_3 = bot.send_message(message.chat.id, 'С кем ты хочешь знакомиться? ( Мальчики/девочки )', reply_markup=markup)
    bot.register_next_step_handler(msg_3, meet_pref_handler, user)
            

def meet_pref_handler(message, user): # Функция получения предпочтений( кнопки гарантируют нам бинарный ввод, те либо мальчики либо девочки)
    r_k = types.ReplyKeyboardRemove()
    meet_pref = message.text
    user['meet_pref'] = meet_pref # Записываем предпочтение в словарь пользователя
    msg_4 = bot.send_message(message.chat.id, 'Сколько вам лет?', reply_markup=r_k)
    bot.register_next_step_handler(msg_4, age_handler, user)


def age_handler(message, user): # Функция получения возраста
    age = message.text
    user['age'] = age

    # Здесь мы получаем и записываем username и id пользователя в Telegram
    user['telid'] = message.from_user.id
    user['username'] = message.from_user.username


    msg_5 = bot.send_message(message.chat.id, 'На какую смену ты поедешь? (номер смены и год)')
    bot.register_next_step_handler(msg_5, smen_handler, user)

# Дальше ничего интересного, просто получение номера смены и информации о пользователе, по сути копипаст
def smen_handler(message, user):
    smen = message.text
    user['smen'] = smen
    msg_6 = bot.send_message(message.chat.id, 'Расскажи немного о себе, чем ты занимаешься, твои увлечения')
    bot.register_next_step_handler(msg_6, about_me_handler, user)


def about_me_handler(message, user): # Заключающая функция, получение инфы о юзере и создание его в БД
    about_me = message.text
    user['about_me'] = about_me
    print(user)
    create_user(s, user) # Функция добавления пользователя в ББД
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    prog = types.KeyboardButton(text='ИСКАТЬ 🔎')
    markup.add(prog)

    bot.send_message(message.chat.id, f"Вы успешно прошли регистрацию! Следующий шаг - нахождение новых знакомств!")

    bot.send_message(message.chat.id, f"Если хотите начать поиск, просто нажмите кнопку ИСКАТЬ", reply_markup=markup)
    

bot.polling(none_stop=True) # Запускаем бот


