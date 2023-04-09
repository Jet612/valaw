# GET_getMatch
Riot Documentation: `https://developer.riotgames.com/apis#val-match-v1/GET_getMatch`

API URL: `https://{region}.api.riotgames.com/val/match/v1/matches/{matchId}`
## Description
Get match by id.
```py
async def GET_getMatch(self, matchId: str, region: str) -> dict:
```
# Arguments
- matchId: String
- [region](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#regions): String
# Examples
Basic example (Just required arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    match_data = await client.match.GET_getMatch("matchId", "region")
```