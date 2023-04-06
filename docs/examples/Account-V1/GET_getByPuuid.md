# GET_getByPuuid
`https://developer.riotgames.com/apis#account-v1/GET_getByPuuid`
## Description
Get account by PUUID.
```py
async def GET_getByPuuid(self, puuid: str, cluster: str = None):
```
# Arguments
- [puuid](https://github.com/Jet612/valaw/docs/glossary.md#puuid): String
### Keyword Arguments
- [cluster](https://github.com/Jet612/valaw/docs/glossary.md#clusters): String = None
# Examples
Basic example (Just required arguments)
```py
import valaw

client = valaw.Client("Riot_API_Token", "Cluster")

async def func():
    account_data = await client.account.GET_getByPuuid("PUUID")
```
Advanced example (With Keyword Arguments)
```py
import valaw

client = valaw.Client("Riot_API_Token", "Cluster")

async def func():
    account_data = await client.account.GET_getByPuuid("PUUID", cluster="Cluster")
```