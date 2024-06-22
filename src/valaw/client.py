### Imports ###
import aiohttp
import json
from dataclass_wizard import fromdict
from typing import Union, Dict, List

from .objects import (
    AccountDto,
    ActiveShardDto,
    ContentDto,
    MatchDto,
    MatchlistDto,
    RecentMatchesDto,
    LeaderboardDto,
    PlatformDataDto
)

### Variables ###
regions = ["ap", "br", "esports", "eu", "kr", "latam", "na"]
"""List of valid regions."""
clusters = ["americas", "asia", "esports", "europe"]
"""List of valid clusters."""
locales = ['ar-ae', 'de-de', 'en-gb', 'en-us', 'es-es', 'es-mx', 'fr-fr', 'id-id', 'it-it', 'ja-jp', 'ko-kr', 'pl-pl', 'pt-br', 'ru-ru', 'th-th', 'tr-tr', 'vi-vn', 'zh-cn', 'zh-tw']
"""List of valid locales."""
queues = ["competitive", "unrated", "spikerush", "tournamentmode", "deathmatch", "onefa", "ggteam", "hurm"]
"""List of valid queues."""

### Custom Exceptions ###
class Exceptions:
    class InvalidCluster(ValueError):
        """Invalid Cluster.
        
        Valid clusters are: americas, asia, esports, europe.
        """

    class InvalidRegion(ValueError):
        """Invalid Region.
        
        Valid regions are: ap, br, esports, eu, kr, latam, na.
        """

    class RiotAPIResponseError(Exception):
        """Riot API Response Error.
        
        More information about response errors can be found at: https://developer.riotgames.com/docs/portal#web-apis_response-codes
        """
        def __init__(self, status_code: int, status_message: str):
            self.status_code = status_code
            self.status_message = status_message
            self.message = str(status_code) + " - " + status_message
            super().__init__(self.message)

    class FailedToParseJSON(Exception):
        """Failed to parse JSON."""

    class InvalidLocale(ValueError):
        """Invalid Locale.
        
        Valid locales are: ar-ae, de-de, en-gb, en-us, es-es, es-mx, fr-fr, id-id, it-it, ja-jp, ko-kr, pl-pl, pt-br, ru-ru, th-th, tr-tr, vi-vn, zh-cn, zh-tw.
        """

### Content Verify ###
async def verify_content(response: aiohttp.ClientResponse):
    """
    Helper function to verify response content-type & deal
    with the response appropriately 
    """
    content_type = response.headers.get("Content-Type")
    if content_type == "application/json; charset=utf-8" or content_type == "application/json" or content_type == "application/json;charset=utf-8":
        return await response.json()
    elif content_type == "text/plain; charset=utf-8" or content_type == "text/plain" or content_type == "text/plain;charset=utf-8":
        return json.loads(await response.text())
    else:
        raise Exceptions.FailedToParseJSON(f"Failed to parse JSON, content-type: {content_type}.")

### Client ###
class Client:
    """The client that connects to the Riot Games API.

    :param token: A Riot Games API access token used to authenticate requests.
    :type token: :class:`str`
    :param cluster: The default cluster to use in requests. The nearest cluster to the host computer/server should be selected.
    :type cluster: :class:`str`
    :param raw_data: Whether or not to send raw JSON data or not. If False, Riot Games API requests will return an object. Defaults to False.

    """
    def __init__(self, token: str, cluster: str, raw_data: bool = False):
        """Initialize the client."""

        # Checking if the arguments are valid
        if cluster.lower() not in clusters:
            raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {clusters}.")
        
        self.token = token
        self.cluster = cluster
        self.raw_data = raw_data

    def change_cluster(self, cluster: str):
        """Change the cluster."""

        if cluster.lower() not in clusters:
            raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {clusters}.")
        self.cluster = cluster

    def change_raw_data(self, raw_data: bool):
        """Change the raw_data."""

        self.raw_data = raw_data

    ##################
    ### ACCOUNT-V1 ###
    ##################

    async def GET_getByPuuid(self, puuid: str, cluster: str = None) -> Union[AccountDto, Dict]:
        """Get account by PUUID.
        
        :param puuid: The PUUID of the account.
        :type puuid: :class:`str`
        :param cluster: The cluster to retreive from. Defaults to self.cluster.
        :type cluster: :class:`str`
        :rtype: Union[AccountDto, :class:`Dict`]
        """

        if cluster != None:
            if cluster.lower() not in clusters:
                raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {clusters}.")
        else:
            cluster = self.cluster 

        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token
            }
            async with session.get(f"https://{cluster}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                
                # Checking if the response is an error, then returning the appropriate object/exception
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(AccountDto, raw_response)
            
    async def GET_getByRiotId(self, gameName: str, tagLine: str, cluster: str = None) -> Union[AccountDto, Dict]:
        """Get account by Riot ID.
        
        :param gameName: The game name of the account (gameName#tagLine).
        :type gameName: :class:`str`
        :param tagLine: The tag line of the account (gameName#tagLine).
        :type tagLine: :class:`str`
        :param cluster: The cluster to retreive from. Defaults to self.cluster.
        :type cluster: :class:`str`
        :rtype: Union[AccountDto, :class:`Dict`]
        """

        if cluster != None:
            if cluster.lower() not in clusters:
                raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {clusters}.")
        else:
            cluster = self.cluster 

        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token
            }
            async with session.get(f"https://{cluster}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(AccountDto, raw_response)
            
    async def GET_getByAccessToken(self, authorization: str, cluster: str = None) -> Union[AccountDto, Dict]:
        """Get account by access token.
        
        :param authorization: The access token.
        :type authorization: :class:`str`
        :param cluster: The cluster to retreive from. Defaults to self.cluster.
        :type cluster: :class:`str`
        :rtype: Union[AccountDto, :class:`Dict`]
        """

        if cluster != None:
            if cluster.lower() not in clusters:
                raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {clusters}.")
        else:
            cluster = self.cluster 

        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token,
                "Authorization": authorization
            }
            async with session.get(f"https://{cluster}.api.riotgames.com/riot/account/v1/accounts/me", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(AccountDto, raw_response)
            
    async def GET_getActiveShard(self, puuid: str, cluster: str = None) -> Union[ActiveShardDto, Dict]:
        """Get active shard for a player.
        
        :param puuid: The PUUID of the account.
        :type puuid: :class:`str`
        :param cluster: The cluster to retreive from. Defaults to self.cluster.
        :type cluster: :class:`str`
        :rtype: Union[ActiveShardDto, :class:`Dict`]
        """

        if cluster != None:
            if cluster.lower() not in clusters:
                raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {clusters}.")
        else:
            cluster = self.cluster 

        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token
            }
            async with session.get(f"https://{cluster}.api.riotgames.com/riot/account/v1/active-shards/by-game/val/by-puuid/{puuid}", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(ActiveShardDto, raw_response)

    ######################
    ### VAL-CONTENT-V1 ###
    ######################

    async def GET_getContent(self, region: str, locale: str = "") -> Union[ContentDto, Dict]:
        """Get content optionally filtered by locale. A locale is recommended to be used for faster response times.
        
        :param region: The region to execute against.
        :type region: :class:`str`
        :param locale: The locale to retrieve data for, defaults to "".
        :type locale: :class:`str`
        :rtype: Union[ContentDto, :class:`Dict`]
        """

        if region.lower() not in regions:
            raise Exceptions.InvalidRegion(f"Invalid region, valid regions are: {regions}.")

        if locale != None:
            if locale.lower() not in locales:
                raise Exceptions.InvalidLocale(f"Invalid locale, valid locales are: {locales}.")
            locale = f"?locale={locale}"

        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token
            }
            async with session.get(f"https://{region}.api.riotgames.com/val/content/v1/contents{locale}", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(ContentDto, raw_response)

    ####################
    ### VAL-MATCH-V1 ###
    #################### 

    async def GET_getMatch(self, matchId: str, region: str) -> Union[MatchDto, Dict]:
        """Get match by id.
        
        :param matchId: The match id.
        :type matchId: :class:`str`
        :param region: The region to execute against.
        :type region: :class:`str`
        :rtype: Union[MatchDto, :class:`Dict`]
        """

        if region.lower() not in regions:
            raise Exceptions.InvalidRegion(f"Invalid region, valid regions are: {regions}.")

        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token
            }
            async with session.get(f"https://{region}.api.riotgames.com/val/match/v1/matches/{matchId}", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(MatchDto, raw_response)
            
    async def GET_getMatchlist(self, puuid: str, region: str) -> Union[MatchlistDto, Dict]:
        """Get matchlist for games played by puuid.
        
        :param puuid: The PUUID of the account.
        :type puuid: :class:`str`
        :param region: The region to execute against.
        :type region: :class:`str`
        :rtype: Union[MatchlistDto, :class:`Dict`]
        """

        if region.lower() not in regions:
            raise Exceptions.InvalidRegion(f"Invalid region, valid regions are: {regions}.")

        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token
            }
            async with session.get(f"https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(MatchlistDto, raw_response)
            
    async def GET_getRecent(self, queue: str, region: str) -> Union[RecentMatchesDto, Dict]:
        """Get recent matches.

        Returns a list of match ids that have completed 
        in the last 10 minutes for live regions and 12 hours 
        for the esports routing value. NA/LATAM/BR share a 
        match history deployment. As such, recent matches 
        will return a combined list of matches from those 
        three regions. Requests are load balanced so you may 
        see some inconsistencies as matches are added/removed 
        from the list.

        :param queue: The queue to retrieve recent matches for.
        :type queue: :class:`str`
        :param region: The region to execute against.
        :type region: :class:`str`
        :rtype: Union[RecentMatchesDto, :class:`Dict`]
        """

        if region.lower() not in regions:
            raise Exceptions.InvalidRegion(f"Invalid region, valid regions are: {regions}.")
        if queue.lower() not in queues:
            raise Exceptions.InvalidQueue(f"Invalid queue, valid queues are: {queues}.")

        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token
            }
            async with session.get(f"https://{region}.api.riotgames.com/val/match/v1/recent-matches/by-queue/{queue}", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(RecentMatchesDto, raw_response)
    
    #####################
    ### VAL-RANKED-V1 ###
    #####################

    async def GET_getLeaderboard(self, actId: str, region: str, size: int = 200, startIndex: int = 0) -> Union[LeaderboardDto, Dict]:
        """Get leaderboard for the competitive queue.
        
        :param actId: The act id.
        :type actId: :class:`str`
        :param region: The region to execute against.
        :type region: :class:`str`
        :param size: The amount of entries to retrieve, defaults to 200.
        :type size: :class:`int`
        :param startIndex: The index to start from, defaults to 0.
        :type startIndex: :class:`int`
        :rtype: Union[LeaderboardDto, :class:`Dict`]
        """

        if region.lower() not in regions:
            raise Exceptions.InvalidRegion(f"Invalid region, valid regions are: {regions}.")
        
        if size > 200 or size < 1:
            raise ValueError(f"Invalid size, valid values: 1 to 200.")
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token
            }
            async with session.get(f"https://{region}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{actId}?size={size}&startIndex={startIndex}", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(LeaderboardDto, raw_response)

    #####################
    ### VAL-STATUS-V1 ###
    #####################

    async def GET_getPlatformData(self, region: str) -> Union[PlatformDataDto, Dict]:
        """Get VALORANT status for the given platform.
        
        :param region: The region to execute against.
        :type region: :class:`str`
        :rtype: Union[PlatformDataDto, :class:`Dict`]
        """

        if region.lower() not in regions:
            raise Exceptions.InvalidRegion(f"Invalid region, valid regions are: {regions}.")

        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.token
            }
            async with session.get(f"https://{region}.api.riotgames.com/val/status/v1/platform-data", headers=headers) as resp:
                raw_response = await verify_content(response=resp)
                if self.raw_data == True:
                    return raw_response
                if raw_response.get("status") != None:
                    raise Exceptions.RiotAPIResponseError(raw_response["status"]["status_code"], raw_response["status"]["message"])
                else:
                    return fromdict(PlatformDataDto, raw_response)

    ###########
    ### RSO ###
    ###########

    def create_RSO_link(self, redirect_uri: str, client_id: str, response_type: str, scopes: List[str], login_hint: str = None, ui_locales: List[str] = None, state: str = None):
        """Create a Riot Sign-On Link.

        :param redirect_uri: OAuth2 callback route
        :type redirect_uri: :class:`str`
        :param client_id: Client ID of the RSO application
        :type client_id: :class:`str`
        :param response_type: OAuth2 response type, should be 'code' for authorization code flow
        :type response_type: :class:`str`
        :param scopes: List of scopes to request, must include 'openid' to authenticate, addition scopes are 'cpid', and 'offline_access'
        :type scopes: List[:class:`str`]
        :param login_hint: Used to specify hints to pre-populate data on the login page. Formats {regioncode}, {regioncode}|{username}, {regioncode}#{userid}. Defaults to None
        :type login_hint: :class:`str`
        :param ui_locales: List of BCP47 language tag values in order of most to least preferred. Defaults to None
        :type ui_locales: List[:class:`str`]
        :param state: Opaque value provided to authorize the endpoint, the same value will be returned to the redirect_uri. Defaults to None
        :type state: :class:`str`

        :returns: :class:`str`

        For more information on RSO, visit https://developer.riotgames.com/docs/valorant#rso-integration
        """

        scopes = "+".join(scopes)

        if login_hint != None:
            login_hint = f"&login_hint={login_hint}"
        else:
            login_hint = ""
        
        if ui_locales != None:
            ui_locales = f"&ui_locales={' '.join(ui_locales)}"
        else:
            ui_locales = ""

        if state != None:
            state = f"&state={state}"
        else:
            state = ""

        return f"https://auth.riotgames.com/authorize?redirect_uri={redirect_uri}&client_id={client_id}&response_type={response_type}&scope={scopes}{login_hint}{ui_locales}{state}"