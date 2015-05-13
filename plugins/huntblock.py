from cloudbot import hook

@hook.command("start", "starthun", autohelp=False)
def huntfoil():
    """dummmy command to make sure people use the full starthunt command so OPS can block it if they need to."""
    return "I think you are looking for .starthunt"
