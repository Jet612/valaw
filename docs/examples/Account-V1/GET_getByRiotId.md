# GET_getByRiotId
`https://developer.riotgames.com/apis#account-v1/GET_getByRiotId`
## Description
Get account by riot id.
```py
async def GET_getByRiotId(self, gameName: str, tagLine: str, cluster: str = None):
```
# Arguments
- [gameName](https://github.com/Jet612/valaw/docs/glossary.md#gamename): String
- [tagLine](https://github.com/Jet612/valaw/docs/glossary.md#tagline): String
### Keyword Arguments
- [cluster](https://github.com/Jet612/valaw/docs/glossary.md#clusters): String = None
# Examples
Basic example (Just required arguments)
```py
import valaw

client = valaw.Client("Riot_API_Token", "Cluster")

async def func():
    account_data = await client.account.GET_getByRiotId("gameName", "tagLine")
```
Advanced example (With Keyword Arguments)
```py
import valaw

client = valaw.Client("Riot_API_Token", "Cluster")

async def func():
    account_data = await client.account.GET_getByRiotId("gameName", "tagLine", cluster="Cluster")
```