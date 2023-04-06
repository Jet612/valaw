# GET_getByAccessToken
Riot Documentation: `https://developer.riotgames.com/apis#account-v1/GET_getByAccessToken`

API URL: `https://{cluster}.api.riotgames.com/riot/account/v1/accounts/me`
## Description
Get account by access token.
```py
async def GET_getByAccessToken(self, authorization: str, cluster: str = None) -> dict:
```
# Arguments
- [authorization](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#authorization): String - The access token
### Keyword Arguments
- [cluster](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#clusters): String = None
# Examples
Basic example (Just required arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    account_data = await client.account.GET_getByAccessToken("Authorization")
```
Advanced example (With Keyword Arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    account_data = await client.account.GET_getByAccessToken("authorization", cluster="cluster")
```