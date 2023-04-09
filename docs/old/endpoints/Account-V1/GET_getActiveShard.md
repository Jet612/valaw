# GET_getActiveShard
Riot Documentation: `https://developer.riotgames.com/apis#account-v1/GET_getActiveShard`

API URL: `https://{cluster}.api.riotgames.com/riot/account/v1/active-shards/by-game/val/by-puuid/{puuid}`
## Description
Get active shard for a player.
```py
async def GET_getActiveShard(self, puuid: str, cluster: str = None) -> dict:
```
# Arguments
- [puuid](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#puuid): String
### Keyword Arguments
- [cluster](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#clusters): String = None
# Examples
Basic example (Just required arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    account_data = await client.account.GET_getActiveShard("PUUID")
```
Advanced example (With Keyword Arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    account_data = await client.account.GET_getActiveShard("puuid", cluster="cluster")
```