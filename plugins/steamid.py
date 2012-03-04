from util import hook, steam
from util.steam import SteamCommunityProfile, SteamIDError

@hook.command
def steamid(inp):
    ".steamid <user> -- Gets information on <user> using the Steam API"
    try:
        profile = SteamCommunityProfile.input_to_profile(inp)
    except SteamIDError,e:
        return str(e)
    
    if profile is None:
        return "Could not recognize your input."
    else:
        return str(profile)

