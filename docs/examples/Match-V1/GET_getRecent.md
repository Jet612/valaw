# GET_getRecent
Riot Documentation: `https://developer.riotgames.com/apis#val-match-v1/GET_getRecent`

API URL: `https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}`
## Description
Get recent matches.

Returns a list of match ids that have completed 
in the last 10 minutes for live regions and 12 hours 
for the esports routing value. NA/LATAM/BR share a 
match history deployment. As such, recent matches 
will return a combined list of matches from those 
three regions. Requests are load balanced so you may 
see some inconsistencies as matches are added/removed 
from the list.
```py
async def GET_getRecent(self, queue: str, region: str) -> dict:
```
# Arguments
- [queue](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#queues): String
- [region](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#regions): String
# Examples
Basic example (Just required arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    recent_data = await client.match.GET_getRecent("queue", "region")
```