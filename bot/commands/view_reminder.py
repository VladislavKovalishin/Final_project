from bot.base import BotCommand, CommandStrategy
from bot.db import search_entry


class AddReminderStrategy(CommandStrategy):

    def handle(self, text, chat_id, user_id):
        result = search_entry(user_id)
        reminders = ""
        for i in result:
            reminder = f'''id: {i[0]}
Дата: {i[2]}
Час: {i[3]}
Текст: {i[4]}

'''
            reminders += reminder
        return reminders


class AddReminderCommand(BotCommand):
    def __init__(self):
        self.strategy = AddReminderStrategy()

    def execute(self, text, chat_id, user_id):
        return self.strategy.handle(text, chat_id, user_id)
