from module_base import *

class Castles():

    def __init__(self, db, bot):
        self.name = 'Castles'
        self.db = db
        self.bot = bot

    def execute(self, msg_text, user_id, user_action):
        if 'замки' in msg_text:
            logging.info(f'Module {self.name} started for user_id {user_id}...')
            self.start(user_id)

    def start(self, user_id):
        gameName = "Castles"
        self.bot.send_game(user_id, gameName)
        return True

    def multigame(self, call):
        if call.game_short_name == self.name and call.message:
            self.bot.answer_callback_query(callback_query_id=call.id, url = "https://nichuldin.github.io/Castles?"+str(call.message.chat.id)+"?"+str(self.db.take_token(int(call.message.chat.id))))