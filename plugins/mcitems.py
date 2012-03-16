""" plugin by _303 (?)
    pulled from <https://github.com/blha303/skybot/commit/d4ba73d6e3f21cc60a01342f3de9d0d4abd14b3d> by lukeroge
"""

from util import hook
import re
import itertools

pattern = re.compile(r'^(?P<count>\d+)x (?P<name>.+?): (?P<ingredients>.*)$')

recipelist = []

class Recipe(object):
    __slots__ = 'output', 'count', 'ingredients', 'line'

    def __init__(self, output, count, ingredients, line):
        self.output = output
        self.count = count
        self.ingredients = ingredients
        self.line = line

    def __str__(self):
        return self.line
 
with open("./plugins/data/recipes.txt") as f:
    for line in f.readlines():
        line = line.strip()
        match = pattern.match(line)
        if not match:
            continue
        recipelist.append(Recipe(line=line,
                           output=match.group("name").lower(),
                           ingredients=match.group("ingredients"),
                           count=match.group("count")))

ids = []

with open("./plugins/data/itemids.txt") as f:
    for line in f.readlines():
        parts = line.strip().split()
        id = parts[0]
        name = " ".join(parts[1:])
        ids.append((id,name))

@hook.command
def itemid(input, reply=None):
    ".itemid <item/id> -- gets the id from an item or vice versa"
    input = input.lower().strip()

    
    all = False
    limit = 4
    parts = input.split()

    if parts[0] == "-all":
        all = True
        input = " ".join(parts[1:])

    if input == "":
        reply("no input")
        return

    results = []

    for id, name in ids:
        if input == id or input in name.lower():
            results.append("%s %s" % (id, name))

    if not len(results):
        reply("no matches found")
        return

    if not all and len(results) > limit:
        reply("Displaying %d of %d matches, use -all to get all." % (limit, len(results)))

    for result in results if all else itertools.islice(results, limit):
        reply(result)



@hook.command
def recipe(input, reply=None):
    ".recipe <item> -- gets the crafting recipe for an item"
    input = input.lower().strip()

    results = []

    for recipe in recipelist:
        if input in recipe.output:
            results.append(recipe.line)

    if not len(results):
        reply("no matches found")
        return

    for result in results:
        reply(result)


