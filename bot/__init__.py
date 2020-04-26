import logging
import os
import threading
import time
from distutils.util import strtobool as stb

import aria2p
import telegram.ext as tg
from dotenv import load_dotenv
import socket

socket.setdefaulttimeout(600)

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

load_dotenv('config.env')

Interval = []


def getConfig(name: str, default: str):
    return os.environ.get(name, default)


LOGGER = logging.getLogger(__name__)

if stb(getConfig('_____REMOVE_THIS_LINE_____', 'False')):
    logging.error('The README.md file there to be read! Exiting now!')
    exit()

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret="",
    )
)


download_dict_lock = threading.Lock()
status_reply_dict_lock = threading.Lock()
# Key: update.effective_chat.id
# Value: telegram.Message
status_reply_dict = {}
# Key: update.message.message_id
# Value: An object of DownloadStatus
download_dict = {}
# Stores list of users and chats the bot is authorized to use in
AUTHORIZED_CHATS = set()
if os.path.exists('authorized_chats.txt'):
    with open('authorized_chats.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            #    LOGGER.info(line.split())
            AUTHORIZED_CHATS.add(int(line.split()[0]))

BOT_TOKEN = getConfig('BOT_TOKEN', None)
parent_id = getConfig('GDRIVE_FOLDER_ID', None)
DOWNLOAD_DIR = getConfig('DOWNLOAD_DIR', None)
if DOWNLOAD_DIR[-1] != '/' or DOWNLOAD_DIR[-1] != '\\':
    DOWNLOAD_DIR = DOWNLOAD_DIR + '/'
DOWNLOAD_STATUS_UPDATE_INTERVAL = int(getConfig('DOWNLOAD_STATUS_UPDATE_INTERVAL', 5))
OWNER_ID = int(getConfig('OWNER_ID', 0))
AUTO_DELETE_MESSAGE_DURATION = int(getConfig('AUTO_DELETE_MESSAGE_DURATION', 20))
USER_SESSION_STRING = getConfig('USER_SESSION_STRING', None)
TELEGRAM_API = getConfig('TELEGRAM_API', None)
TELEGRAM_HASH = getConfig('TELEGRAM_HASH', None)
INDEX_URL = getConfig('INDEX_URL', None)
IS_TEAM_DRIVE = stb(getConfig('IS_TEAM_DRIVE', 'False'))
USE_SERVICE_ACCOUNTS = stb(getConfig('USE_SERVICE_ACCOUNTS', 'False'))


updater = tg.Updater(token=BOT_TOKEN,use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher
