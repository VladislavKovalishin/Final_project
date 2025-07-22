from bot.base import BotCommand, CommandStrategy
from bot.db import add_entry


class AddReminderStrategy(CommandStrategy):

    def search_data_time(self, text):
        import re
        date_patterns = r'(\d{1,2})\.(\d{1,2})\.(\d{4})'
        time_pattern = r'(\d{1,2}):(\d{2})'
        user_date_match = re.search(date_patterns, text)
        user_time_match = re.search(time_pattern, text)
        if not user_date_match or not user_time_match:
            return None

        day, month, year = user_date_match.groups()
        hour, minute = user_time_match.groups()

        date_str = f"{year}-{int(month):02d}-{int(day):02d}"
        time_str = f"{int(hour):02d}:{int(minute):02d}:00"

        return date_str, time_str

    def edit_text_for_add(self, text):
        import re
        date_patterns = r'(\d{1,2})\.(\d{1,2})\.(\d{4})'
        time_pattern = r'(\d{1,2}):(\d{2})'
        command_pattern = r'/\b[a-zA-Z0-9_]+'

        new_text = re.sub(date_patterns, "", text)
        new_text = re.sub(time_pattern, "", new_text)
        new_text = re.sub(command_pattern, "", new_text)
        return new_text

    def date_time_check_in_future(self, date_str, time_str):
        import datetime
        dt_input = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        return dt_input > datetime.datetime.now()

    def handle(self, text, chat_id, user_id):
        result = self.search_data_time(text)
        if result is None:
            return "Не коректно введено дату або час. Спробуйте у форматі: 01.08.2025 14:30"

        date_str, time_str = result
        if self.date_time_check_in_future(date_str, time_str):
            new_text = self.edit_text_for_add(text)
            add_entry(user_id, date_str, time_str, new_text)
            return "Нагадування збережено"
        else:
            return "Дата вже минула"


class AddReminderCommand(BotCommand):
    def __init__(self):
        self.strategy = AddReminderStrategy()

    def execute(self, text, chat_id, user_id):
        return self.strategy.handle(text, chat_id, user_id)
