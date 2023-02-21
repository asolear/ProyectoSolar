
import streamlit as st

import telebot
from telebot import types
import threading
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


TOKEN = {
    "proyectosolarbot": "6177224605:AAGpKvAJ6920c9ApFTxuvd21_FcJ9gtIUPU",
    "wattbucketbot": "6161424950:AAHSkRZtCtpSosLqDYIsvhOw4B7RWnL7304",
    "asolearbot": "5736935748:AAEkfjVPqgj-P62ArNixnS8lgAlnhVdlZKU",
    "tejadosolarbot": "6237437211:AAFLkhrsUutu1k9-g0HX7iwSukesFBHlSNc",
    "comunidadenergeticasolarbot": "6096277657:AAGSoPgcV2CrHbfJ2qHTF5Qsd6YrpJ6jACU",
}
f'''# BOTs en telegram
{TOKEN}
'''


option = st.selectbox(
    'Arrancar ', list(TOKEN.keys()))

st.write(
    f'''- Debe estar diponible en [{option[:-3]}](https://web.telegram.org/k/#@{option})''')


bot = telebot.TeleBot(TOKEN[option])


def texto():
    return f'''
Bienvenid@ al Telegram de [📚 {option[:-8]}.solar](https://{option[:-8]}.solar/).
Por aquí podras:
- Disenar tu instalacion.
- Documentar tu instlacion.
'''


def botones():
    mk = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton(
        '📚 Exp. Modelo', url=f'https://{option[:-8]}.solar/')
    b2 = InlineKeyboardButton(
        '🆘 Ayuda', url=f'https://{option[:-8]}.solar/Ayuda')
    Formulario = InlineKeyboardButton(
        '📥 Desc. Formulario', callback_data='📥 Desc. Formulario')
    cerrar = InlineKeyboardButton(
        '📤 Carga Formulario', url=f'https://{option[:-8]}.solar/Formulario')
    mk.add(b1, b2, Formulario, cerrar,)
    return mk


@bot.message_handler(commands=["start"])
def cmd_botones(message):
    '''mostrara botones inline'''
    bot.send_message(
        message.chat.id, texto(), parse_mode="markdown")
    bot.send_message(
        message.chat.id, 'Menu', reply_markup=botones())


@bot.message_handler(content_types=["document"])
def addfile(message):
    ''' recepcion de '''
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(
        message.chat.id, 'Recibido archivo', parse_mode="markdown")


@bot.message_handler(content_types=["text"])
def cmd_texto(message):
    '''respuesta al texto'''
    bot.send_message(
        message.chat.id, f'{option[:-8]}👇 Selecciona una opcion', reply_markup=botones())


@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "Still alive and kicking!")


@bot.callback_query_handler(func=lambda x: True)
def respuesta_botones(call):
    '''gestiona los callback delos botones'''
    cid = call.from_user.id
    mid = call.message.id
    if 0:
        bot.send_message(
            cid, 'Perdona, no te he entendido', parse_mode="markdown")
    elif call.data == '📥 Desc. Formulario':
        bot.send_document(cid, open(
            "docs/Expediente/pdfs/220_🏦 Ayuntamiento_⬜ Representación ante la GMU.pdf", "rb"))


def recibir_mensajes():
    ''' bule infinito para recibir los mensajes'''
    bot.infinity_polling()


# globals()[option] = threading.Thread(name=option, target=recibir_mensajes)
globals()[option] = threading.Thread(name=option, target=recibir_mensajes)
globals()[option].start()
