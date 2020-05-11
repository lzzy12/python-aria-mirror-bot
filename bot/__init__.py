import logging
import os
import threading
import time

import aria2p
import telegram.ext as tg
import socket

socket.setdefaulttimeout(600)

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)


Interval = []


def getConfig(name: str):
    return os.environ[name]


LOGGER = logging.getLogger(__name__)


aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret="",
    )
)

DOWNLOAD_DIR = None
BOT_TOKEN = None

download_dict_lock = threading.Lock()
status_reply_dict_lock = threading.Lock()
# Key: update.effective_chat.id
# Value: telegram.Message
status_reply_dict = {}
# Key: update.message.message_id
# Value: An object of DownloadStatus
download_dict = {}
# Stores list of users and chats the bot is authorized to use in


try:
    BOT_TOKEN = getConfig('BOT_TOKEN')
    parent_id = getConfig('GDRIVE_FOLDER_ID')
    DOWNLOAD_DIR = getConfig('DOWNLOAD_DIR')
    CRED_JSON = getConfig('SECRET_JSON')
    AUTHORIZED_CHATS = [int(i) for i in os.environ.get("AUTH_CHATS", "").split(" ")]
    if DOWNLOAD_DIR[-1] != '/' or DOWNLOAD_DIR[-1] != '\\':
        DOWNLOAD_DIR = DOWNLOAD_DIR + '/'
    DOWNLOAD_STATUS_UPDATE_INTERVAL = int(getConfig('DOWNLOAD_STATUS_UPDATE_INTERVAL'))
    OWNER_ID = int(getConfig('OWNER_ID'))
    AUTO_DELETE_MESSAGE_DURATION = int(getConfig('AUTO_DELETE_MESSAGE_DURATION'))
    USER_SESSION_STRING = getConfig('SESSION_STRING')
    TELEGRAM_API = getConfig('API_ID')
    TELEGRAM_HASH = getConfig('API_HASH')
except KeyError as e:
    LOGGER.error("One or more env variables missing! Exiting now")
    exit(1)
try:
    INDEX_URL = getConfig('INDEX_URL')
    if len(INDEX_URL) == 0:
        INDEX_URL = None
except KeyError:
    INDEX_URL = None
try:
    IS_TEAM_DRIVE = getConfig('IS_TEAM_DRIVE')
    if IS_TEAM_DRIVE.lower() == 'true':
        IS_TEAM_DRIVE = True
    else:
        IS_TEAM_DRIVE = False
except KeyError:
    IS_TEAM_DRIVE = False

try:
    USE_SERVICE_ACCOUNTS = getConfig('USE_SERVICE_ACCOUNTS')
    if USE_SERVICE_ACCOUNTS.lower() == 'true':
        USE_SERVICE_ACCOUNTS = True
    else:
        USE_SERVICE_ACCOUNTS = False
except KeyError:
    USE_SERVICE_ACCOUNTS = False

updater = tg.Updater(token=BOT_TOKEN,use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher
