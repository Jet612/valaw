# GET_getMatchlist
Riot Documentation: `https://developer.riotgames.com/apis#val-match-v1/GET_getMatchlist`

API URL: `https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}`
## Description
Get matchlist for games played by puuid.
```py
async def GET_getMatchlist(self, puuid: str, region: str) -> dict:
```
# Arguments
- [puuid](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#puuid): String
- [region](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#regions): String
# Examples
Basic example (Just required arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    matchlist_data = await client.match.GET_getMatchlist("puuid", "region")
```