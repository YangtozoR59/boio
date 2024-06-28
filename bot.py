import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import logging
from datetime import datetime

# Obtenez le token API depuis les variables d'environnement
API_TOKEN = '7499675140:AAHcCTCsEzKDZvofjWoQAbnGS_4u8a7k340'

# Configurer le logger
date_str = datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(filename=f'{date_str}.log', level=logging.INFO, format='%(asctime)s - %(message)s')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bienvenue au jeu de lancer de dés de Cyd (WhatsApp : 620621375) ! Tapez /play pour commencer à jouer.")
    logging.info(f"Utilisateur {message.from_user.username} a démarré le bot.")

@bot.message_handler(commands=['play'])
def start_game(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Le lancé sera égal à 7", callback_data='7'),
        InlineKeyboardButton("Le lancé sera inférieur à 7", callback_data='moins_7'),
        InlineKeyboardButton("Le lancé sera supérieur à 7", callback_data='plus_7')
    )
    bot.send_message(message.chat.id, "Faites un choix :", reply_markup=markup)
    logging.info(f"Utilisateur {message.from_user.username} a commencé une nouvelle partie.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user = call.from_user
    choice = call.data

    # Si l'utilisateur veut recommencer
    if choice == 'replay':
        start_game(call.message)
        return

    dice_roll = random.randint(1, 6) + random.randint(1, 6)
    
    if choice == '7' and dice_roll == 7:
        result = "Bravo ! Vous avez deviné correctement. Le résultat était 7."
        won = True
    elif choice == 'moins_7' and dice_roll < 7:
        result = f"Bravo ! Vous avez deviné correctement. Le résultat était {dice_roll}, inférieur à 7."
        won = True
    elif choice == 'plus_7' and dice_roll > 7:
        result = f"Bravo ! Vous avez deviné correctement. Le résultat était {dice_roll}, supérieur à 7."
        won = True
    else:
        result = f"Désolé, vous avez perdu. Le résultat était {dice_roll}."
        won = False

    # Enregistrement des informations dans le fichier
    logging.info(f"Utilisateur: {user.username} ({user.id}), Choix: {choice}, Résultat: {dice_roll}, Gagné: {won}")

    # Ajout du bouton "Recommencer"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Recommencer", callback_data='replay'))
    bot.send_message(call.message.chat.id, result, reply_markup=markup)

bot.polling()
