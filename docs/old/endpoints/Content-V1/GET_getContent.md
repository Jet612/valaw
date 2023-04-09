# GET_getContent
Riot Documentation: `https://developer.riotgames.com/apis#val-content-v1/GET_getContent`

API URL: `https://{region}.api.riotgames.com/val/content/v1/contents{locale}`
## Description
Get content optionally filtered by locale. A locale is recommended to be used for faster response times.
```py
async def GET_getContent(self, region: str, locale: str = "") -> dict:
```
# Arguments
- [region](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#regions): String
### Keyword Arguments
- [locale](https://github.com/Jet612/valaw/tree/main/docs/glossary.md#locale): String = "" (None)
# Examples
Basic example (Just required arguments)
*!!! Notice !!!* This example is not recommended as it is not using a locale; this will result in a slower response time.
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    content_data = await client.content.GET_getContent("region")
```
Advanced example (With Keyword Arguments)
```py
import valaw

client = valaw.Client("riot_api_token", "cluster")

async def func():
    content_data = await client.content.GET_getContent("region", locale="locale")
```