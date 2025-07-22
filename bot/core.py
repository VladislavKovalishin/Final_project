import requests
import time
from bot.factories import CommandFactory
from bot.db import search_entry, delete_entry


class TelegramBot:
    _instance = None

    def __new__(cls, token):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, token):
        self.token = token
        self.url = f"https://api.telegram.org/bot{self.token}/"

    def handle_message(self, text, chat_id, user_id):
        command_name = text.split()[0]
        command = CommandFactory.create_command(command_name)
        if command:
            return command.execute(text, chat_id, user_id)
        return "Unknown command. Type /help."

    def get_last_update(self):
        url = self.url + "getUpdates?timeout=10"
        response = requests.get(url)
        result = response.json()["result"]
        if result:
            return result[-1]
        return None

    def get_chat_id(self, update):
        return update["message"]["chat"]["id"]

    def get_user_id(self, update):
        return update["message"]["from"]["id"]

    def get_message_text(self, update):
        return update["message"]["text"]

    def send_message(self, chat_id, text):
        url = self.url + "sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        requests.post(url, json=payload)

    def send_reminder(self, user_id):
        import datetime
        reminders = search_entry(user_id)
        now = datetime.datetime.now()
        today = now.date()
        current_time = now.time()

        for reminder in reminders:
            reminder_date = datetime.datetime.strptime(reminder[2], "%Y-%m-%d").date()
            reminder_time = datetime.datetime.strptime(reminder[3], "%H:%M:%S").time()

            if reminder_date == today and reminder_time.hour == current_time.hour and reminder_time.minute == current_time.minute:
                send_text = reminder[4]
                delete_entry(reminder[0])
                url = self.url + "sendMessage"
                payload = {"chat_id": user_id, "text": send_text}
                requests.post(url, json=payload)

    def run(self):
        update = self.get_last_update()
        if update:
            self.last_update_id = update['update_id']
        else:
            self.last_update_id = None
        while True:
            time.sleep(1.5)
            user_id = self.get_user_id(update)
            update = self.get_last_update()
            self.send_reminder(user_id)
            if update and update["update_id"] != self.last_update_id:
                chat_id = self.get_chat_id(update)
                user_id = self.get_user_id(update)
                message_text = self.get_message_text(update)
                reply = self.handle_message(message_text, chat_id, user_id)
                self.send_message(chat_id, reply)
                self.last_update_id = update["update_id"]
