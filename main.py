from telebot import TeleBot
import db
from time import sleep
TOKEN ='6828348723:AAF9TZH0KlDjxG4geA2rTbDcRABK-5N8rZg'
bot = TeleBot(TOKEN)
game = False
night = False


def game_loop(message):
    global night,game
    bot.send_message(message.chat.id,"Добро пожаловать в игру! Вам дается 2 минуты, что-бы познакомиться")
    sleep(2)
    while True:
        msg = get_killed(night)
        bot.send_message(message.chat.id,msg)
        if night:
            bot.send_message(message.chat.id,"Город засыпает, просыпается мафия. Наступила ночь")
        else:
            bot.send_message(message.chat.id,"Город просыпается. Наступил день")
        winner = db.check_winner()
        if winner == 'мафия' or winner == 'горожане':
            bot.send_message(message.chat.id,'Победил: '+ winner)
            game = False
            break
        db.clear(dead=False)
        night = not night
        alive = db.get_all_alive()
        alive = "\n".join(alive)
        bot.send_message(message.chat.id,f'В игре:\n{allive}')
        sleep(2)



@bot.message_handler(commands=['play'])
def play (message):
    bot.send_message(message.chat.id, text ='что-бы начать игру,напиши мне в лс')


@bot.message_handler(func=lambda m:m.text.lower() == 'готов играть' and m.chat.type=='private')
def send_text(message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name} играет")
    bot.send_message(message.from_user.id, 'Вы добавлены в игру')
    db.insert_player(message.chat.id,username=message.from_user.first_name)


@bot.message_handler(commands=["game"])
def game_start(message):
    global game
    players = db.players_amount()
    if players >= 2 and not game:
        db.set_roles(players)
        players_roles = db.get_players_roles()
        mafia_usernames = db.get_mafia_usernames()
        for player_id, role in players_roles:
            bot.send_message(player_id, text=role)
            if role == 'mafia':
                bot.send_message(player_id,
                                 text=f'Все члены мафии:\n{mafia_usernames}')
        game = True
        db.clear(dead=True)
        game_loop(message)
        bot.send_message(message.chat.id, text='Игра началась!')
        return
    bot.send_message(message.chat.id, text='недостаточно людей!')


@bot.message_handler(commands=['kick'])
def kick(message):
    username = ' '.join(message.text.split(' ')[1:])
    usernames = db.get_all_alive()
    if not night:
        if not username in usernames:
            bot.send_message(message.chat.id,'Такого имени нет')
            return
        voted = db.vote('citizen_vote',username,message.from_user.id)
        if voted:
            bot.send_message(message.chat.id,'Ваш голос учитан')
            return
        bot.send_message(message.chat.id,'У вас больше нет права голосовать')
        return
    bot.send_message(message.chat.id,'Сейчас ночь вы не можете никого выгнать')

@bot.message_handler(commands=['kill'])
def kill(message):
    username = ' '.join(message.text.split(' ')[1:])
    usernames = db.get_all_alive()
    mafia_usernames = db.get_mafia_usernames()
    if message.from_user.first_name not in mafia_usernames:
         bot.send_message(message.chat.id, 'Вы не мафия, вы не можете голосовать!')
    if night:
        if not username in usernames:
            bot.send_message(message.chat.id, 'Такого имени нет')
            return
        voted = db.vote('mafia_vote', username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, 'Ваш голос учтён')
            return
        bot.send_message(message.chat.id, 'У вас больше нет права голосовать')
        return
    bot.send_message(message.chat.id, 'Сейчас день, вы не можете никого убить')


def get_killed(night):
    if not night:
        username_killed = db.citizens_kill()
        return f'Горожане выгнали: {username_killed}'
    username_killed = db.mafia_kill()
    return f'Мафия убила: {username_killed}'
#хахахахахаха


bot.polling()
