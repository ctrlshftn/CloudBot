import operator
import re
from collections import defaultdict

import sqlalchemy
from sqlalchemy import Table, String, Column, Integer, PrimaryKeyConstraint

from cloudbot import hook
from cloudbot.util import database

karmaplus_re = re.compile('^.*\+\+$')
karmaminus_re = re.compile('^.*--$')

karma_table = Table(
    'karma',
    database.metadata,
    Column('name', String),
    Column('chan', String),
    Column('thing', String),
    Column('score', Integer),
    PrimaryKeyConstraint('name', 'chan', 'thing')
)


@hook.on_start
def remove_non_channel_points(db):
    """Temporary on_start hook to remove non-channel points"""
    db.execute(karma_table.delete().where(sqlalchemy.not_(karma_table.c.chan.startswith('#'))))
    db.commit()


@hook.command("pp", "addpoint")
def addpoint(text, nick, chan, db):
    """<thing> - adds a point to the <thing>"""
    if nick.casefold() == chan.casefold():
        # This is a PM, don't set points in a PM
        return

    text = text.strip()
    karma = db.execute("select score from karma where name = :name and chan = :chan and thing = :thing",
                       {'name': nick, 'chan': chan, 'thing': text.lower()}).fetchone()
    if karma:
        score = int(karma[0])
        score += 1
        db.execute("insert or replace into karma(name, chan, thing, score) values (:name, :chan, :thing, :score)",
                   {'name': nick, 'chan': chan, 'thing': text.lower(), 'score': score})
        db.commit()
        # return "{} is now worth {} in {}'s eyes.".format(text, score, nick)
    else:
        db.execute("insert or replace into karma(name, chan, thing, score) values (:name, :chan, :thing, :score)",
                   {'name': nick, 'chan': chan, 'thing': text.lower(), 'score': 1})
        db.commit()
        # return "{} is now worth 1 in {}'s eyes.".format(text, nick)


@hook.regex(karmaplus_re)
def re_addpt(match, nick, chan, db, conn, notice):
    """no useful help txt"""
    thing = match.group().split('++')[0]
    if thing:
        addpoint(thing, nick, chan, db)
        # return out
    else:
        notice(pluspts(nick, chan, db))


@hook.command("mm", "rmpoint")
def rmpoint(text, nick, chan, db):
    """<thing> - subtracts a point from the <thing>"""
    if nick.casefold() == chan.casefold():
        # This is a PM, don't set points in a PM
        return

    text = text.strip()
    karma = db.execute("select score from karma where name = :name and chan = :chan and thing = :thing",
                       {'name': nick, 'chan': chan, 'thing': text.lower()}).fetchone()
    if karma:
        score = int(karma[0])
        score -= 1
        db.execute("insert or replace into karma(name, chan, thing, score) values (:name, :chan, :thing, :score)",
                   {'name': nick, 'chan': chan, 'thing': text.lower(), 'score': score})
        db.commit()
        # return "{} is now worth {} in {}'s eyes.".format(text, score, nick)
    else:
        db.execute("insert or replace into karma(name, chan, thing, score) values (:name, :chan, :thing, :score)",
                   {'name': nick, 'chan': chan, 'thing': text.lower(), 'score': -1})
        db.commit()
        # return "{} is now worth -1 in {}'s eyes.".format(text, nick)


@hook.command("pluspts", autohelp=False)
def pluspts(nick, chan, db):
    """- prints the things you have liked and their scores"""
    output = ""
    likes = db.execute(
        "select thing, score from karma where name = :name and chan = :chan and score >= 0 order by score desc",
        {'name': nick, 'chan': chan}).fetchall()
    for like in likes:
        output = output + str(like[0]) + " has " + str(like[1]) + " points "
    return output


@hook.command("minuspts", autohelp=False)
def minuspts(nick, chan, db):
    """- prints the things you have disliked and their scores"""
    output = ""
    likes = db.execute(
        "select thing, score from karma where name = :name and chan = :chan and score <= 0 order by score",
        {'name': nick, 'chan': chan}).fetchall()
    for like in likes:
        output = output + str(like[0]) + " has " + str(like[1]) + " points "
    return output


@hook.regex(karmaminus_re)
def re_rmpt(match, nick, chan, db, conn, notice):
    """no useful help txt"""
    thing = match.group().split('--')[0]
    if thing:
        rmpoint(thing, nick, chan, db)
        # return out
    else:
        notice(minuspts(nick, chan, db))


@hook.command("points", autohelp=False)
def points(text, chan, db):
    """<thing> - will print the total points for <thing> in the channel."""
    score = 0
    thing = ""
    if text.endswith("-global") or text.endswith(" global"):
        thing = text[:-7].strip()
        karma = db.execute("select score from karma where thing = :thing and chan like :chan", {'thing': thing.lower(), 'chan':'#%'}).fetchall()
    else:
        text = text.strip()
        karma = db.execute("select score from karma where thing = :thing and chan = :chan",
                           {'thing': text.lower(), 'chan': chan}).fetchall()
    if karma:
        pos = 0
        neg = 0
        for k in karma:
            if int(k[0]) < 0:
                neg += int(k[0])
            else:
                pos += int(k[0])
            score += int(k[0])
        if thing:
            return "{} has a total score of {} (+{}/{}) across all channels I know about.".format(thing, score, pos,
                                                                                                  neg)
        return "{} has a total score of {} (+{}/{}) in {}.".format(text, score, pos, neg, chan)
    else:
        return "I couldn't find {} in the database.".format(text)


@hook.command("topten", "pointstop", "loved", autohelp=False)
def pointstop(text, chan, db):
    """- prints the top 10 things with the highest points in the channel. To see the top 10 items in all of the channels the bot sits in use .topten global."""
    points = defaultdict(int)
    if text == "global" or text == "-global":
        items = db.execute("select thing, score from karma").fetchall()
        out = "The top {} favorite things in all channels are: "
    else:
        items = db.execute("select thing, score from karma where chan = :chan", {'chan': chan}).fetchall()
        out = "The top {} favorite things in {} are: "
    if items:
        for item in items:
            thing = item[0]
            score = int(item[1])
            points[thing] += score
        scores = points.items()
        sorts = sorted(scores, key=operator.itemgetter(1), reverse=True)
        ten = str(len(sorts))
        if int(ten) > 10:
            ten = "10"
        out = out.format(ten, chan)
        for i in range(0, int(ten)):
            out += "{} with {} points \u2022 ".format(sorts[i][0], sorts[i][1])
        out = out[:-2]
        return out


@hook.command("bottomten", "pointsbottom", "hated", autohelp=False)
def pointsbottom(text, chan, db):
    """- prints the top 10 things with the lowest points in the channel. To see the bottom 10 items in all of the channels the bot sits in use .bottomten global."""
    points = defaultdict(int)
    if text == "global" or text == "-global":
        items = db.execute("select thing, score from karma").fetchall()
        out = "The {} most hated things in all channels are: "
    else:
        items = db.execute("select thing, score from karma where chan = :chan", {'chan': chan}).fetchall()
        out = "The {} most hated things in {} are: "
    if items:
        for item in items:
            thing = item[0]
            score = int(item[1])
            points[thing] += score
        scores = points.items()
        sorts = sorted(scores, key=operator.itemgetter(1))
        ten = str(len(sorts))
        if int(ten) > 10:
            ten = "10"
        out = out.format(ten, chan)
        for i in range(0, int(ten)):
            out += "{} with {} points \u2022 ".format(sorts[i][0], sorts[i][1])
        out = out[:-2]
        return out
