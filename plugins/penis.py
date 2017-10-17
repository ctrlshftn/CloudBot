import random

from cloudbot import hook

balls = ['(_)_)', '8', 'B', '(___)__)', '(_)(_)', '(@)@)', '3']
shaft = ['=', '==', '===', '====', '=====', '========', '/////////////////////////', '|||||||||||||', '\u2248\u2248\u2248']
head = ['D', 'Q', '>', '|\u2283' '\u22d1', '\u22d9', '\u22d7']
emission = ['~ ~ ~ ~', '~ * ~ &', '', '*~* *~* %']
bodypart = ['face', 'glasses', 'thigh', 'tummy', 'back', 'hiney', 'hair', 'boobs', 'tongue']
optin = ['#conversations', '#thelair', '#conversationsmods', '#thelairmods', '#nosleepooc', '#downthepub', '#misunderstood', '##flotwig', '##partymansion', '#redditsquaredcircle', '#memenetics', '#nofear', '#pinkonwednesdays', '#banwomen', '#groove', '#grace', '#srotd', '#letsfilmtomorrow', '##doctorwho', '##neopets', '#dppafterhours', '#destinythegame', '#dc', '#foreveralone', '#britishpolitics', '#protectandserve', '##gonzobot', '#mturk', '#shenanigans', '#shenanigansmods', '#private256', '#tretki', '#breakingparents', '#torontomods', '#legaladvice', '#breakingdad', '#goml', '#linuxmasterrace', '#legaladvicegonewild', '#mnfh_nsfw', '#penis', '#guildrs', '##movienight', '#destroyersofworlds', '#thebatcave', '#notcuntparents', '#casualab', '#the_donald','#sigh', '#ems', '##ils', '#disputedzone', '#hotelcraft', '#luvduck', '#bagelsexual', '#aspergers-afterdark', '#vault108', '#burlington', '#psychic', '#psychicnsfw', '#offtopic', '#bolamod', '##the-lair', '#psychicdumb', '#irrationalfears','#psychicmoderators', '#portland', '#psychiccheeto', '#metalgigsscotland', '#psychicart', '##prolesftw','#duckfuck', '#textfriends']

@hook.command("penis", "bepis", autohelp=False)
def penis(text, message, chan, notice, nick):
    """much dongs, very ween, add a user nick as an arguement for slightly different 'output'"""
    if chan not in optin and '#' in chan:
        notice("this channel does not have access to this command.", nick)
        return
    if not text:
        message("{}{}{}".format(random.choice(balls), random.choice(shaft), random.choice(head)))
    else:
        person = text.split(' ')[0]
        message("{}{}{}{} all over {}'s {}".format(random.choice(balls), random.choice(shaft), random.choice(head),random.choice(emission), person, random.choice(bodypart)))
