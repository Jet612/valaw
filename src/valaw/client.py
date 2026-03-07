### Imports ###
import aiohttp
import json
from dataclass_wizard import fromdict
from typing import Union, Dict, List, Optional
from urllib.parse import quote

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

### Constants ###
REGIONS = {"ap", "br", "esports", "eu", "kr", "latam", "na"}
"""Set of valid regions."""
CLUSTERS = {"americas", "asia", "esports", "europe"}
"""Set of valid clusters."""
LOCALES = {
    'ar-ae': 'ar-AE', 'de-de': 'de-DE', 'en-gb': 'en-GB', 'en-us': 'en-US',
    'es-es': 'es-ES', 'es-mx': 'es-MX', 'fr-fr': 'fr-FR', 'id-id': 'id-ID',
    'it-it': 'it-IT', 'ja-jp': 'ja-JP', 'ko-kr': 'ko-KR', 'pl-pl': 'pl-PL',
    'pt-br': 'pt-BR', 'ru-ru': 'ru-RU', 'th-th': 'th-TH', 'tr-tr': 'tr-TR',
    'vi-vn': 'vi-VN', 'zh-cn': 'zh-CN', 'zh-tw': 'zh-TW'
}
"""Dict mapping lowercase locale to its properly-cased form for the API."""
QUEUES = {
    "competitive", "unrated", "spikerush", "tournamentmode",
    "deathmatch", "onefa", "ggteam", "hurm"
}
"""Set of valid queues."""

CONSOLE_QUEUES = {
    "console_unrated", "console_swiftplay", "console_hurm", "console_competitive",
    "console_deathmatch"
}
"""Set of valid console queues."""

PLATFORM_TYPES = {"playstation", "xbox"}
"""Set of valid platform types."""

### Custom Exceptions ###
class Exceptions:
    class InvalidCluster(ValueError):
        """Invalid Cluster. Valid clusters are: americas, asia, esports, europe."""
    
    class InvalidRegion(ValueError):
        """Invalid Region. Valid regions are: ap, br, esports, eu, kr, latam, na."""
    
    class RiotAPIResponseError(Exception):
        """Riot API Response Error.

        More information about response errors can be found at:
        https://developer.riotgames.com/docs/portal#web-apis_response-codes
        """
        def __init__(self, status_code: int, status_message: str):
            self.status_code = status_code
            self.status_message = status_message
            self.message = f"{status_code} - {status_message}"
            super().__init__(self.message)

    class FailedToParseJSON(Exception):
        """Failed to parse JSON."""
    
    class InvalidLocale(ValueError):
        """Invalid Locale. Valid locales are: ar-ae, de-de, en-gb, en-us, ..."""
    
    class InvalidQueue(ValueError):
        """Invalid Queue. Valid queues are: competitive, unrated, spikerush, ..."""

    class InvalidPlatformType(ValueError):
        """Invalid Platform Type. Valid platform types are: playstation, xbox."""

    class InvalidRiotAPIKey(ValueError):
        """Invalid Riot API Key. A Riot API key is required."""

### Helper Functions ###
def validate_region(region: str):
    """Validate the provided region.

    :param region: The region to validate.
    :raises InvalidRegion: If the region is not valid.
    """
    if region.lower() not in REGIONS:
        raise Exceptions.InvalidRegion(f"Invalid region, valid regions are: {REGIONS}.")

def validate_cluster(cluster: str):
    """Validate the provided cluster.

    :param cluster: The cluster to validate.
    :raises InvalidCluster: If the cluster is not valid.
    """
    if cluster.lower() not in CLUSTERS:
        raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {CLUSTERS}.")
    
def validate_platform_type(platformType: str):
    """Validate the provided platform.

    :param platformType: The platform type to validate.
    :raises InvalidPlatformType: If the platform type is not valid.
    """
    if platformType.lower() not in PLATFORM_TYPES:
        raise Exceptions.InvalidPlatformType(f"Invalid platform type, valid platforms are: {PLATFORM_TYPES}.")
    
def validate_key(key: str):
    """Validate the provided key.

    :param key: The key to validate.
    :raises InvalidKey: If the key is not valid.
    """
    if key is None or key == "":
        raise Exceptions.InvalidRiotAPIKey("A Riot API key is required.")

async def verify_content(response: aiohttp.ClientResponse):
    """Helper function to verify response content-type and handle the response appropriately.

    :param response: The aiohttp response object.
    :raises FailedToParseJSON: If the content type is not valid.
    :return: Parsed JSON response.
    """
    content_type = (response.headers.get("Content-Type") or "").strip().lower()
    mime_type = content_type.split(";", 1)[0].strip()
    valid_json_types = {"application/json", "text/json"}

    if mime_type in valid_json_types:
        try:
            return await response.json(content_type=None)
        except json.JSONDecodeError as exc:
            raise Exceptions.FailedToParseJSON(
                f"Failed to parse JSON, content-type: {content_type or 'missing'}."
            ) from exc

    raw_text = await response.text()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise Exceptions.FailedToParseJSON(
            f"Failed to parse JSON, content-type: {content_type or 'missing'}."
        ) from exc


### Client ###
class Client:
    """The client that connects to the Riot Games API.

    :param token: A Riot Games API access token used to authenticate requests.
    :type token: str
    :param cluster: The default cluster to use in requests. The nearest cluster to the host computer/server should be selected.
    :type cluster: str
    :param raw_data: Whether or not to send raw JSON data or not. If False, Riot Games API requests will return an object. Defaults to False.
    :type raw_data: bool
    """
    
    def __init__(self, token: str, cluster: str, raw_data: bool = False):
        """Initialize the client."""
        validate_cluster(cluster)
        validate_key(token)

        self.token = token
        self.cluster = cluster
        self.raw_data = raw_data
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/112.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.token
        }
        self._timeout = aiohttp.ClientTimeout(total=30)
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def _ensure_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self._timeout)
        return self.session

    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def _request(self, url: str, headers: dict) -> dict:
        """Make a GET request and return parsed JSON."""
        session = self._ensure_session()
        async with session.get(url, headers=headers) as resp:
            if resp.status >= 400:
                try:
                    payload = await verify_content(resp)
                    status_message = (
                        payload.get("status", {}).get("message")
                        if isinstance(payload, dict) else None
                    ) or str(payload)
                except Exceptions.FailedToParseJSON:
                    status_message = await resp.text()
                raise Exceptions.RiotAPIResponseError(resp.status, status_message)
            return await verify_content(resp)

    async def GET_getByPuuid(self, puuid: str, cluster: Optional[str] = None) -> Union[AccountDto, Dict]:
        """Get account by PUUID.

        :param puuid: The PUUID of the account.
        :type puuid: str
        :param cluster: The cluster to retrieve from. Defaults to self.cluster.
        :type cluster: str, optional
        :rtype: Union[AccountDto, Dict]
        :raises InvalidCluster: If the provided cluster is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        cluster = cluster or self.cluster
        validate_cluster(cluster)

        puuid = quote(puuid, safe="")
        raw_response = await self._request(f"https://{cluster}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(AccountDto, raw_response)

    async def GET_getByRiotId(self, gameName: str, tagLine: str, cluster: Optional[str] = None) -> Union[AccountDto, Dict]:
        """Get account by Riot ID.

        :param gameName: The game name of the account (gameName#tagLine).
        :type gameName: str
        :param tagLine: The tag line of the account (gameName#tagLine).
        :type tagLine: str
        :param cluster: The cluster to retrieve from. Defaults to self.cluster.
        :type cluster: str, optional
        :rtype: Union[AccountDto, Dict]
        :raises InvalidCluster: If the provided cluster is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        cluster = cluster or self.cluster
        validate_cluster(cluster)

        gameName = quote(gameName, safe="")
        tagLine = quote(tagLine, safe="")
        raw_response = await self._request(f"https://{cluster}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(AccountDto, raw_response)

    async def GET_getByAccessToken(self, authorization: str, cluster: Optional[str] = None) -> Union[AccountDto, Dict]:
        """Get account by access token.

        :param authorization: The access token.
        :type authorization: str
        :param cluster: The cluster to retrieve from. Defaults to self.cluster.
        :type cluster: str, optional
        :rtype: Union[AccountDto, Dict]
        :raises InvalidCluster: If the provided cluster is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        cluster = cluster or self.cluster
        validate_cluster(cluster)

        headers = {**self._headers, "Authorization": authorization}
        raw_response = await self._request(f"https://{cluster}.api.riotgames.com/riot/account/v1/accounts/me", headers)
        if self.raw_data:
            return raw_response
        return fromdict(AccountDto, raw_response)

    async def GET_getActiveShard(self, puuid: str, cluster: Optional[str] = None) -> Union[ActiveShardDto, Dict]:
        """Get active shard for a player.

        :param puuid: The PUUID of the account.
        :type puuid: str
        :param cluster: The cluster to retrieve from. Defaults to self.cluster.
        :type cluster: str, optional
        :rtype: Union[ActiveShardDto, Dict]
        :raises InvalidCluster: If the provided cluster is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        cluster = cluster or self.cluster
        validate_cluster(cluster)

        puuid = quote(puuid, safe="")
        raw_response = await self._request(f"https://{cluster}.api.riotgames.com/riot/account/v1/active-shards/by-game/val/by-puuid/{puuid}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(ActiveShardDto, raw_response)

    ######################
    ### VAL-CONTENT-V1 ###
    ######################

    async def GET_getContent(self, region: str, locale: Optional[str] = "") -> Union[ContentDto, Dict]:
        """Get content optionally filtered by locale.

        A locale is recommended to be used for faster response times.

        :param region: The region to execute against.
        :type region: str
        :param locale: The locale to retrieve data for, defaults to "".
        :type locale: str, optional
        :rtype: Union[ContentDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises InvalidLocale: If the provided locale is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)

        if locale and locale.lower() not in LOCALES:
            raise Exceptions.InvalidLocale(f"Invalid locale, valid locales are: {list(LOCALES.values())}.")
        locale_query = f"?locale={quote(LOCALES[locale.lower()], safe='')}" if locale else ""

        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/content/v1/contents{locale_query}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(ContentDto, raw_response)

    ####################
    ### VAL-MATCH-V1 ###
    #################### 

    async def GET_getMatch(self, matchId: str, region: str) -> Union[MatchDto, Dict]:
        """Get match by id.

        :param matchId: The match id.
        :type matchId: str
        :param region: The region to execute against.
        :type region: str
        :rtype: Union[MatchDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)

        matchId = quote(matchId, safe="")
        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/match/v1/matches/{matchId}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(MatchDto, raw_response)

    async def GET_getMatchlist(self, puuid: str, region: str) -> Union[MatchlistDto, Dict]:
        """Get matchlist for games played by puuid.

        :param puuid: The PUUID of the account.
        :type puuid: str
        :param region: The region to execute against.
        :type region: str
        :rtype: Union[MatchlistDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)

        puuid = quote(puuid, safe="")
        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}", self._headers)
        if self.raw_data:
            return raw_response
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
        :type queue: str
        :param region: The region to execute against.
        :type region: str
        :rtype: Union[RecentMatchesDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises InvalidQueue: If the provided queue is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)
        if queue.lower() not in QUEUES:
            raise Exceptions.InvalidQueue(f"Invalid queue, valid queues are: {QUEUES}.")

        queue = quote(queue, safe="")
        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/match/v1/recent-matches/by-queue/{queue}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(RecentMatchesDto, raw_response)

    #####################
    ### VAL-RANKED-V1 ###
    #####################

    async def GET_getLeaderboard(self, actId: str, region: str, size: int = 200, startIndex: int = 0) -> Union[LeaderboardDto, Dict]:
        """Get leaderboard for the competitive queue.

        :param actId: The act id.
        :type actId: str
        :param region: The region to execute against.
        :type region: str
        :param size: The amount of entries to retrieve, defaults to 200.
        :type size: int
        :param startIndex: The index to start from, defaults to 0.
        :type startIndex: int
        :rtype: Union[LeaderboardDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises ValueError: If the size is not between 1 and 200.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)

        if size > 200 or size < 1:
            raise ValueError("Invalid size, valid values: 1 to 200.")
        
        actId = quote(actId, safe="")
        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{actId}?size={size}&startIndex={startIndex}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(LeaderboardDto, raw_response)
        
    ############################
    ### VAL-CONSOLE-MATCH-V1 ###
    ############################

    async def GET_getConsoleMatch(self, matchId: str, region: str) -> Union[MatchDto, Dict]:
        """Get match console data.

        :param matchId: The match id.
        :type matchId: str
        :param region: The region to execute against.
        :type region: str
        :rtype: Union[MatchDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)
        matchId = quote(matchId, safe="")
        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/match/console/v1/matches/{matchId}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(MatchDto, raw_response)
        
    async def GET_getConsoleMatchlist(self, puuid: str, region: str, platformType: str) -> Union[MatchlistDto, Dict]:
        """Get matchlist for console games played by puuid.

        :param puuid: The PUUID of the account.
        :type puuid: str
        :param region: The region to execute against.
        :type region: str
        :param platformType: The platform type to retrieve matchlist for.
        :type platformType: str
        :rtype: Union[MatchlistDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises InvalidPlatformType: If the provided platform type is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)
        validate_platform_type(platformType)

        puuid = quote(puuid, safe="")
        platformType = quote(platformType, safe="")
        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/match/console/v1/matchlists/by-puuid/{puuid}?platformType={platformType}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(MatchlistDto, raw_response)
        
    async def GET_getConsoleRecent(self, queue: str, region: str) -> Union[RecentMatchesDto, Dict]:
        """Get recent console matches.

        Returns a list of match ids that have completed 
        in the last 10 minutes for live regions and 12 hours 
        for the esports routing value. NA/LATAM/BR share a 
        match history deployment. As such, recent matches 
        will return a combined list of matches from those 
        three regions. Requests are load balanced so you may 
        see some inconsistencies as matches are added/removed 
        from the list.

        :param queue: The queue to retrieve recent matches for.
        :type queue: str
        :param region: The region to execute against.
        :type region: str
        :rtype: Union[RecentMatchesDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises InvalidQueue: If the provided queue is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)
        if queue.lower() not in CONSOLE_QUEUES:
            raise Exceptions.InvalidQueue(f"Invalid queue, valid queues are: {CONSOLE_QUEUES}.")

        queue = quote(queue, safe="")
        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/match/console/v1/recent-matches/by-queue/{queue}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(RecentMatchesDto, raw_response)
        
    #############################
    ### VAL-CONSOLE-RANKED-V1 ###
    #############################

    async def GET_getConsoleLeaderboard(self, actId: str, region: str, platformType: str, size: int = 200, startIndex: int = 0) -> Union[LeaderboardDto, Dict]:
        """Get leaderboard for the console competitive queue.

        :param actId: The act id.
        :type actId: str
        :param region: The region to execute against.
        :type region: str
        :param platformType: The platform type to retrieve leaderboard for.
        :type platformType: str
        :param size: The amount of entries to retrieve, defaults to 200.
        :type size: int
        :param startIndex: The index to start from, defaults to 0.
        :type startIndex: int
        :rtype: Union[LeaderboardDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises InvalidPlatformType: If the provided platform type is invalid.
        :raises ValueError: If the size is not between 1 and 200.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)
        validate_platform_type(platformType)

        if size > 200 or size < 1:
            raise ValueError("Invalid size, valid values: 1 to 200.")
        
        actId = quote(actId, safe="")
        platformType = quote(platformType, safe="")
        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/console/ranked/v1/leaderboards/by-act/{actId}?size={size}&startIndex={startIndex}&platformType={platformType}", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(LeaderboardDto, raw_response)

    #####################
    ### VAL-STATUS-V1 ###
    #####################

    async def GET_getPlatformData(self, region: str) -> Union[PlatformDataDto, Dict]:
        """Get VALORANT status for the given platform.

        :param region: The region to execute against.
        :type region: str
        :rtype: Union[PlatformDataDto, Dict]
        :raises InvalidRegion: If the provided region is invalid.
        :raises RiotAPIResponseError: If the API response indicates an error.
        """
        validate_region(region)

        raw_response = await self._request(f"https://{region}.api.riotgames.com/val/status/v1/platform-data", self._headers)
        if self.raw_data:
            return raw_response
        return fromdict(PlatformDataDto, raw_response)

    ###########
    ### RSO ###
    ###########

    def create_RSO_link(self, redirect_uri: str, client_id: str, response_type: str, scopes: List[str], login_hint: Optional[str] = None, ui_locales: Optional[List[str]] = None, state: Optional[str] = None) -> str:
        """Create a Riot Sign-On Link.

        :param redirect_uri: OAuth2 callback route.
        :type redirect_uri: str
        :param client_id: Client ID of the RSO application.
        :type client_id: str
        :param response_type: OAuth2 response type, should be 'code' for authorization code flow.
        :type response_type: str
        :param scopes: List of scopes to request, must include 'openid' to authenticate, additional scopes are 'cpid', and 'offline_access'.
        :type scopes: List[str]
        :param login_hint: Used to specify hints to pre-populate data on the login page. Formats {regioncode}, {regioncode}|{username}, {regioncode}#{userid}. Defaults to None.
        :type login_hint: str, optional
        :param ui_locales: List of BCP47 language tag values in order of most to least preferred. Defaults to None.
        :type ui_locales: List[str], optional
        :param state: Opaque value provided to authorize the endpoint, the same value will be returned to the redirect_uri. Defaults to None.
        :type state: str, optional
        :return: The constructed Riot Sign-On link.
        :rtype: str
        """
        scope = "+".join(quote(s, safe="") for s in scopes)

        login_hint_query = f"&login_hint={quote(login_hint, safe='')}" if login_hint else ""
        ui_locales_query = f"&ui_locales={quote(' '.join(ui_locales), safe='')}" if ui_locales else ""
        state_query = f"&state={quote(state, safe='')}" if state else ""

        return (
            f"https://auth.riotgames.com/authorize"
            f"?redirect_uri={quote(redirect_uri, safe='')}"
            f"&client_id={quote(client_id, safe='')}"
            f"&response_type={quote(response_type, safe='')}"
            f"&scope={scope}"
            f"{login_hint_query}{ui_locales_query}{state_query}"
        )
