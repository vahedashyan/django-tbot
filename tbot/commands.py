from tbot.utils import get_bot

bot = get_bot()


@bot.command(command_name="docs")
def unknown_handler(chat_id, *args, **kwargs):
    message = "Please read the docs-->"
    bot.send_message(chat_id, message)


@bot.command(command_name="unknown")
def unknown_handler(chat_id, *args, **kwargs):
    message = "Sorry, invalid command: {}".format(kwargs.get('input_command'))
    bot.send_message(chat_id, message)
