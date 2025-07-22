from bot.base import BotCommand, CommandStrategy
from bot.db import delete_entry, get_reminder_id


class AddReminderStrategy(CommandStrategy):

    def id_check(self, text, user_id):
        id_reminder = get_reminder_id(user_id)
        text = text.strip()
        for id_r in id_reminder:
            if str(id_r[0]) == text:
                return True
            else:
                return False

    def handle(self, text, chat_id, user_id):
        import re
        command_pattern = r'/\b[a-zA-Z0-9_]+'
        text = re.sub(command_pattern, '', text)
        if self.id_check(text, user_id):
            delete_entry(text)
            return "Нагадування видалено"
        else:
            return "Нагадування з таким id не існує"


class AddReminderCommand(BotCommand):
    def __init__(self):
        self.strategy = AddReminderStrategy()

    def execute(self, text, chat_id, user_id):
        return self.strategy.handle(text, chat_id, user_id)

