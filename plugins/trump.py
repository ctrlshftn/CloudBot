import codecs
import json
import os
import random
import asyncio

from cloudbot import hook
from cloudbot.util import textgen

opt_out = ['#aspergers']

@hook.on_start()
def load_trumps(bot):
    """
    :type bot: cloudbot.bot.CloudBot
    """
    global trump_data

    with codecs.open(os.path.join(bot.data_dir, "trump.json"), encoding="utf-8") as f:
        trump_data = json.load(f)

@asyncio.coroutine
@hook.command
def trump(text, action, chan):
    """trump a user."""
    if chan in opt_out:
        return
    user = text.strip()
    generator = textgen.TextGenerator(trump_data["templates"], trump_data["parts"], variables={"user": user})
    action(generator.generate_string())
