from config import shoha_db
from chatterbot import ChatBot

class Shoha(object):
    def __init__(self):
        self.bot = ChatBot(
            'Shoha',
            trainer='chatterbot.trainers.ListTrainer',
            storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            input_adapter='chatterbot.input.VariableInputTypeAdapter',
            logic_adapters=[
                { 'import_path': 'chatterbot.logic.BestMatch' }
            ],
            database=shoha_db
        )

    def reply(self, msg):
        if not msg:
            return None
        else:
            try:
                bot_input = self.bot.get_response(msg)
                return bot_input
            except(KeyboardInterrupt, EOFError, SystemExit):
                return None

if __name__ == "__main__":
    shoha = Shoha()
    while True:
        msg = input("> ")
        print(shoha.reply(msg))
