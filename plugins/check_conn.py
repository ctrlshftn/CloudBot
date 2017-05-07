from cloudbot import hook


@hook.command(autohelp=False, permissions=["botcontrol"])
def conncheck(nick, bot, notice): 
    """This command is an effort to make the bot reconnect to a network if it has been disconnected."""
    # For each irc network return a notice on the connection state and send a message from
    # each connection to the nick that used the command.
    for conn in bot.connections:
        # I am not sure if the connected property is ever changed.
        notice("{}, {}".format(conn, bot.connections[conn].connected))
        # if the value is in fact false try to connect
        if not bot.connections[conn].connected:
            bot.connections[conn].connect()
        # Send a message from each irc network connection to the nick that issued the command
        bot.connections[conn].message(nick, "just letting you know I am here. {}".format(conn))


@hook.command(permissions=["botcontrol"])
def reconnect(text, notice, bot):
    """This command is an effort to use the connect method to manually reconnect to a network if it has been disconnected."""
    if text in bot.connections:
        notice("You are asking me to reconnect to {}. I have that network in my config and will attempt to reconnect.".format(text))
        bot.connections[text].connect()
        print(dir(bot.connections[text]))
        print("self._quit = {}, self._connected = {}, self._transport = {}".format(bot.connections[text]._quit, bot.connections[text]._connected, bot.connections[text]._transport ))
        #bot.connections[text].close()
        #bot.connections[text]._quit = False
        
    else:
        notice("You are asking me to reconnect to {}. I do not have that network in my config please specify a valid network.".format(text))
