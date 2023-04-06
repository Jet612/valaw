# GET_getByPuuid
Riot Documentation: `https://developer.riotgames.com/apis#account-v1/GET_getByPuuid`

API URL: `https://{cluster}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}`
## Description
Get account by PUUID.
```py
async def GET_getByPuuid(self, puuid: str, cluster: str = None) -> dict:
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
    account_data = await client.account.GET_getByPuuid("puuid")
```
Advanced example (With Keyword Arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    account_data = await client.account.GET_getByPuuid("puuid", cluster="cluster")
```