import os
import importlib
import inspect
from bot.base import BotCommand, CommandStrategy


class HelpMenuStrategy(CommandStrategy):
    def handle(self, text, chat_id, user_id):
        # Генеруємо команди прямо тут
        commands_dir = os.path.dirname(__file__)
        command_infos = {}
        for file in os.listdir(commands_dir):
            if file.endswith(".py") and file not in ("__init__.py", "help_menu.py", "role.py"):
                module_name = f"bot.commands.{file[:-3]}"
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, BotCommand) and obj is not BotCommand:
                        info = getattr(obj, "info", "No description")
                        command_infos[f"/{file[:-3]}"] = info
                        break
        command_infos["/help"] = "Показати це меню"
        command_infos["/add_reminder"] = "Додати нагадування"
        command_infos["/view_reminder"] = "Показати всі нагадування"
        command_infos["/delete"] = "Видалити нагадування"

        help_text = "Це меню довідка. Доступні команди:\n"
        for cmd, info in sorted(command_infos.items()):
            help_text += f"{cmd} - {info}\n"

        return help_text


class HelpMenuCommand(BotCommand):
    def __init__(self):
        self.strategy = HelpMenuStrategy()

    def execute(self, text, chat_id, user_id):
        return self.strategy.handle(text, chat_id, user_id)
