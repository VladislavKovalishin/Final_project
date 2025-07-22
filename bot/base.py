from abc import ABC, abstractmethod


# Command pattern: Абстрактний клас для всіх команд
class BotCommand(ABC):
    @abstractmethod
    def execute(self, text, chat_id, user_id):
        pass


# Strategy pattern: Базовий клас для різних стратегій поведінки
class CommandStrategy(ABC):
    @abstractmethod
    def handle(self, text, chat_id, user_id):
        pass
