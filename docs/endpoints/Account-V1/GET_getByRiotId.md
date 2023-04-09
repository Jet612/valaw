# GET_getByRiotId
Riot Documentation: `https://developer.riotgames.com/apis#account-v1/GET_getByRiotId`

API URL: `https://{cluster}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}`
## Description
Get account by riot id.
```py
async def GET_getByRiotId(self, gameName: str, tagLine: str, cluster: str = None) -> dict:
```
# Arguments
- [gameName](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#gamename): String
- [tagLine](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#tagline): String
### Keyword Arguments
- [cluster](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#clusters): String = None
# Examples
Basic example (Just required arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    account_data = await client.account.GET_getByRiotId("gameName", "tagLine")
```
Advanced example (With Keyword Arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    account_data = await client.account.GET_getByRiotId("gameName", "tagLine", cluster="cluster")
```