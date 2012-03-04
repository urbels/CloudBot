from util import hook, steam
reload(steam)
from util.steam import SteamCommunityProfile, SteamIDError


@hook.command
def steamid(inp):
    ".steamid -- stuff"
    try:
      profile = SteamCommunityProfile.input_to_profile(inp)
    except SteamIDError,e:
      return str(e)
    
    if profile is None:
      return "could not recognize your input."
    else:
      return str(profile)

