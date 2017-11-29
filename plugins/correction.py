import re

from cloudbot import hook
from cloudbot.util.formatting import ireplace

correction_re = re.compile(r"^[sS]/(?:(.*?)(?<!\\)/(.*?)(?:(?<!\\)/([igx]{,4}))?)\s*$")
unescape_re = re.compile(r'\\(.)')

# define channels that want this plugin disabled.

opt_out = []

def shorten_msg(msg):
    out = (msg[:500]) if len(msg) > 500 else msg
    return out
@hook.regex(correction_re)
def correction(match, conn, nick, chan, message):
    """
    :type match: re.__Match
    :type conn: cloudbot.client.Client
    :type chan: str
    """
    groups = [unescape_re.sub(r"\1", group or "") for group in match.groups()]
    find = groups[0]
    replace = groups[1]
    if find == replace:
        return "really dude? you want me to replace {} with {}?".format(find, replace)

    if not find.strip():  # Replacing empty or entirely whitespace strings is spammy
        return "really dude? you want me to replace nothing with {}?".format(replace)

    for name, timestamp, msg in reversed(conn.history[chan]):
        if correction_re.match(msg):
            # don't correct corrections, it gets really confusing
            continue

        if find.lower() in msg.lower():
            find_esc = re.escape(find)
            replace_esc = re.escape(replace)
            if msg.startswith('\x01ACTION'):
                mod_msg = msg[7:].strip(' \x01')
                fmt = "* {} {}"
            else:
                mod_msg = msg
                fmt = "<{}> {}"

            mod_msg = ireplace(mod_msg, find_esc, "\x02" + replace_esc + "\x02")

            message("Correction, {}".format(fmt.format(name, mod_msg)))

            msg = ireplace(msg, find_esc, replace_esc)
            if nick.lower() == name.lower():
                conn.history[chan].append((name, timestamp, msg))

            break
