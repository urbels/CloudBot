"""
remember.py: written by Scaevolus 20101
"""

from util import hook
import re


# some simple "shortcodes" for formatting purposes
shortcodes = {
'<b>': '\x02',
'</b>': '\x02',
'<u>': '\x1F',
'</u>': '\x1F',
'<i>': '\x16',
'</i>': '\x16'}


def db_init(db):
    db.execute("create table if not exists mem(word, data, nick,"
               " primary key(word))")
    db.commit()


def get_memory(db, word):
    rows = db.execute("select data from mem where word=lower(?)", [word]).fetchone()
    print rows
    if rows:
        return rows[0]
    else:
        return None
        
def set_memory(db, word, data, nick):
    db.execute("replace into mem(word, data, nick) values"
               " (lower(?),?,?)", (word, data, nick))
    db.commit()
    return True



def multiwordReplace(text, wordDic):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, wordDic)))

    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)


@hook.command("r", adminonly=True)
@hook.command(adminonly=True)
def remember(inp, nick='', db=None, say=None, input=None, notice=None):
    ".remember <word> [+]<data> -- Remembers <data> with <word>. Add +"
    " to <data> to append."
    db_init(db)

    append = False

    try:
        word, data = inp.split(None, 1)
    except ValueError:
        notice(remember.__doc__)
        return

    old_data = get_memory(db, word)

    if data[0] == '+' and old_data:
        append = True
        # ignore + symbol
        new = data[1:]
        import string
        if len(data) > 1 and data[1] in (string.punctuation + ' '):
            data = old_data + new
        else:
            data = old_data + ' ' + new
            
    set_memory(db, word, data, nick)

    if old_data:
        if append:
            notice('Appending "%s" to "%s".' % (new, old_data))
        else:
            notice('Forgetting existing data (%s), remembering this instead!'
                    % old_data)
            return
    else:
        notice('Remembered!')
        return


@hook.command("f", adminonly=True)
@hook.command(adminonly=True)
def forget(inp, db=None, input=None, notice=None):
    ".forget <word> -- Forgets a remembered <word>."

    db_init(db)
    data = get_memory(db, inp)

    if data:
        db.execute("delete from mem where word=lower(?)",
                   [inp])
        db.commit()
        notice('"%s" has been forgotten.' % data.replace('`', "'"))
        return
    else:
        notice("I don't know about that.")
        return


@hook.regex(r'^\? ?(.+)')
def factoid(inp, say=None, db=None, bot=None):
    "?<word> -- Shows what data is associated with <word>."
    try:
        prefix_on = bot.config["plugins"]["factoids"]["prefix"]
    except KeyError:
        prefix_on = False
        
    requested_factoid = inp.group(1).strip()

    db_init(db)

    data = get_memory(db, requested_factoid)
    if data:
        out = multiwordReplace(data, shortcodes)
        if prefix_on:
            say("\x02[%s]:\x02 %s" % (requested_factoid, out))
        else:
            say(out)
