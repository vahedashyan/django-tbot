

django-tbot
=============================

Docs: Soon

Django app to write Telegram bots. Just define commands with python decorators.



Documentation
-------------

The full documentation is at readthedocs.org soon

Telegram API documentation at https://core.telegram.org/bots/api

Quickstart
----------

Install django-tbot

    pip install django-tbot
    
Add ``tbot``  and ``rest_framework`` to your ``INSTALLED_APPS``

       #settings.py
       
       INSTALLED_APPS = (
           ...
           'tbot',
           ...
       )

	

After creating a bot in Telegram Platform, create at least one bot with django admin. Token is the only
required field. You may need to provided public key certificate for your server. https://core.telegram.org/bots/self-signed
Heroku has https and ssl by default so it is a good option if you dont want to deal with that.

Add webhook url to your urlpatterns

	url(r'^bot/', include('tbot.urls')),	



``APP_PATH`` is the bot instance path. You must create BotApp instance and call function ``start()``

    #your_app/bot_app.py
    
    from tbot import BotApp
    bot = BotApp(bot_name="Django Telegram Bot")
    bot.start()


For defining commands you mast create python file and write all your command there.
For example ``your_app/commands.py``.

    #your_app.commands.py

    from .your_app.bot_app import bot

    
    @bot.command(command_name="start")
    def foo(chat_id, *args, **kwargs):
        //do_somthing




Set the following settings in your project's ``settings.py``

    # settings.py      
    
    DJANGO_TBOT_CONFIGS = {
        "TUTORIAL_BOT_TOKEN": "registered bot authentication token",
        "COMMAND_ROOT_PATH": "defined commands path. E.g your_app.commands",
        "WEBHOOK_URL": "dhe url for webhook. E.g. https://projectwebsite.com",
        "APP_PATH": "defined app instance app. E.g.your_app.bot_app.bot (dir. your_app/bot_app.py)"
    }

The  main class in ``django-tbot`` extends the telegram's Bot class. It means that you can use all telegram bot functionality. 

Activate bot: ``/bot/activate``