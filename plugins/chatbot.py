from cleverbot import Cleverbot
from cloudbot import hook


#Clone cleverbot.py from https://github.com/folz/cleverbot.py
# Then run python3 setup.py install
# At the time of this commit version 1.0.2 works but is not yet in pypi

# Define channels that have opted out of this command.

opt_out = ['#linuxmasterrace']
 
cb = Cleverbot('gonzobot')

@hook.command("ask", "gonzo", "gonzobot", "cleverbot", "cb")
def chitchat(text, chan):
    """chat with cleverbot.com"""
    if chan in opt_out:
        return
    return cb.ask(text)
