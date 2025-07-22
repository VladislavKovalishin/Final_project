from bot.commands.help_menu import HelpMenuCommand
from bot.commands import COMMAND_CLASSES


class CommandFactory:
    commands_map = COMMAND_CLASSES.copy()
    commands_map["/help"] = HelpMenuCommand

    @staticmethod
    def create_command(command_name):
        CommandClass = CommandFactory.commands_map.get(command_name)
        if CommandClass:
            return CommandClass()
        return None
