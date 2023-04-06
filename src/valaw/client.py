### Imports ###
import aiohttp
import json

### Variables ###
regions = ["ap", "br", "esports", "eu", "kr", "latam", "na"]
clusters = ["americas", "asia", "esports", "europe"]

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

### Client ###
class Client:
    def __init__(self, token: str, cluster: str):
        """Initialize the client."""

        # Checking if the arguments are valid
        if cluster.lower() not in clusters:
            raise Exceptions.InvalidCluster(f"Invalid cluster, valid clusters are: {clusters}.")
        
        self.token = token
        self.cluster = cluster

        # Subclasses
        self.account = Account(token, cluster)

class Account:
    def __init__(self, token: str, cluster: str):
        self.token = token
        self.cluster = cluster

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
                return await verify_content(resp)
            
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
                return await verify_content(resp)
            
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
                return await verify_content(resp)
            
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
                return await verify_content(resp)
