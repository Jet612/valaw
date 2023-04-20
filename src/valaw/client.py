### Imports ###
import aiohttp
import json

### Variables ###
regions = ["ap", "br", "esports", "eu", "kr", "latam", "na"]
clusters = ["americas", "asia", "esports", "europe"]
locales = ['ar-ae', 'de-de', 'en-gb', 'en-us', 'es-es', 'es-mx', 'fr-fr', 'id-id', 'it-it', 'ja-jp', 'ko-kr', 'pl-pl', 'pt-br', 'ru-ru', 'th-th', 'tr-tr', 'vi-vn', 'zh-cn', 'zh-tw']
queues = ["competitive", "unrated", "spikerush", "tournamentmode", "deathmatch", "onefa", "ggteam"]

### Custom Exceptions ###
class Exceptions:
    class InvalidCluster(ValueError):
        """Invalid Cluster."""
    class InvalidRegion(ValueError):
        """Invalid Region."""

### Content Verify ###
async def verify_content(response):
    """
    Helper function to verify response content-type & deal
    with the response appropriately 
    """
    content_type = response.headers.get("Content-Type")
    if content_type == "application/json; charset=utf-8" or content_type == "application/json":
        return await response.json()
    elif content_type == "text/plain; charset=utf-8" or content_type == "text/plain":
        return json.loads(await response.text())
    return response

### Client ###
class Client:
    def __init__(self, token: str, cluster: str):
        """Initialize the client."""

        # Checking if the arguments are valid
        if cluster.lower() not in clusters:
            raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {clusters}.")
        
        self.token = token
        self.cluster = cluster

        # Beta/Development message
        print("valaw: This library is still in development, please report any bugs to https://github.com/Jet612/valaw/issues.")

    def change_cluster(self, cluster: str):
        """Change the cluster."""

        if cluster.lower() not in clusters:
            raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {clusters}.")
        self.cluster = cluster

    ##################
    ### ACCOUNT-V1 ###
    ##################

    async def GET_getByPuuid(self, puuid: str, cluster: str = None) -> dict:
        """Get account by PUUID."""

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
                return await verify_content(response=resp)
            
    async def GET_getByRiotId(self, gameName: str, tagLine: str, cluster: str = None) -> dict:
        """Get account by Riot ID."""

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
                return await verify_content(response=resp)
            
    async def GET_getByAccessToken(self, authorization: str, cluster: str = None) -> dict:
        """Get account by access token."""

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
                return await verify_content(response=resp)
            
    async def GET_getActiveShard(self, puuid: str, cluster: str = None) -> dict:
        """Get active shard for a player."""

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
                return await verify_content(response=resp)

    ######################
    ### VAL-CONTENT-V1 ###
    ######################

    async def GET_getContent(self, region: str, locale: str = "") -> dict:
        """Get content optionally filtered by locale. A locale is recommended to be used for faster response times."""

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
                return await verify_content(response=resp)

    ####################
    ### VAL-MATCH-V1 ###
    #################### 

    async def GET_getMatch(self, matchId: str, region: str) -> dict:
        """Get match by id."""

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
                return await verify_content(response=resp)
            
    async def GET_getMatchlist(self, puuid: str, region: str) -> dict:
        """Get matchlist for games played by puuid."""

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
                return await verify_content(response=resp)
            
    async def GET_getRecent(self, queue: str, region: str) -> dict:
        """
        Get recent matches.

        Returns a list of match ids that have completed 
        in the last 10 minutes for live regions and 12 hours 
        for the esports routing value. NA/LATAM/BR share a 
        match history deployment. As such, recent matches 
        will return a combined list of matches from those 
        three regions. Requests are load balanced so you may 
        see some inconsistencies as matches are added/removed 
        from the list.
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
                return await verify_content(response=resp)
    
    #####################
    ### VAL-RANKED-V1 ###
    #####################

    async def GET_getLeaderboard(self, actId: str, region: str, size: int = 200, startIndex: int = 0) -> dict:
        """Get leaderboard for the competitive queue"""

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
                return await verify_content(response=resp)

    #####################
    ### VAL-STATUS-V1 ###
    #####################

    async def GET_getPlatformData(self, region: str) -> dict:
        """Get VALORANT status for the given platform."""

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
                return await verify_content(response=resp)