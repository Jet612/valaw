# Contents
- [Getting Started](#getting-started)
    - [Installing the Package](#installing-the-package)
    - [Importing the Package](#importing-the-package)
    - [Examples](#examples)
- [Getting a Riot API Token](#getting-a-riot-api-token)
- [Endpoints](#endpoints)

# Getting Started
- [Installing the Package](#installing-the-package)
    - [Installing the newest version](#installing-the-newest-version)
    - [Installing a specific version](#installing-a-specific-version)
    - [Installing directly from GitHub](#installing-directly-from-github)
- [Importing the Package](#importing-the-package)
## Installing the Package
- [Installing the newest version](#installing-the-newest-version)
- [Installing a specific version](#installing-a-specific-version)
- [Installing directly from GitHub](#installing-directly-from-github)
#### Installing the newest version
```
pip install valorantClientAPI
```
#### Installing a specific version
```
pip install valorantClientAPI==[version]
```
Example:
```
pip install valorantClientAPI==0.0.1
```
#### Installing directly from GitHub
!!!Installing from the main branch without specifying a version is not recommended!!!
```
pip install git+https://github.com/Jet612/valaw/tree/[version]
```
Example:
```
pip install git+https://github.com/Jet612/valaw/tree/0.0.1
```
You can find versions by going to the [releases](https://github.com/Jet612/valaw/releases) and looking in the description of the release. If the version is not there use the tag.

[Back to top](#contents)
## Importing the Package
```py
import valaw
```

[Back to top](#contents)
## Examples
```py
import valaw

client = valaw.Client("Riot_API_Token", "Cluster")

async def func():
    account_data = await client.account.GET_getByPuuid("PUUID", "Region")
```
Valid clusters can be found [here](#clusters) and valid regions can be found [here](#regions).

[Back to top](#contents)
# Getting a Riot API Token
You will need a Riot Games API token to use 90% of the VALORANT API. You can get one by following these steps:
1. Go to [developer.riotgames.com](https://developer.riotgames.com/)
2. Login with your Riot account
3. Click on "Register Product"
4. Click on either "Personal API Key" or "Production API Key"
5. Fill out the form

A Production API Key could take up to a month to receive. (I'm not sure if this is always the case, make sure to check Official Riot Games Documentation for more information.)

More information can be found in the [Riot Games Developer Documentation](https://developer.riotgames.com/docs/portal#product-registration).

[Back to top](#contents)
# Endpoints
These are the list of endpoints that are currently implemented in the package. If you see a missing endpoint, please open an [issue](https://github.com/Jet612/valaw/issues) or visit the [Riot Games Documentation](https://developer.riotgames.com/apis) for a full list of the available endpoints.

These examples are the most basic use cases, for a detailed list of all the endpoints with advanced usages and examples, please visit the [Examples](https://github.com/Jet612/valaw/docs/examples).

Assume that the following code is used for all examples:
```py
import valaw

client = valaw.Client("Riot_API_Token", "Cluster")
```

- [Account-V1](#account-v1)
    - [GET_getByPuuid](#get_getbypuuid)
    - [GET_getByRiotId](#get_getbyriotid)
    - [GET_getByAccessToken](#get_getbyaccesstoken)
    - [GET_getActiveShard](#get_getactiveshard)

## Account-V1
https://developer.riotgames.com/apis#account-v1
- [GET_getByPuuid](#get_getbypuuid)
- [GET_getByRiotId](#get_getbyriotid)
- [GET_getByAccessToken](#get_getbyaccesstoken)
- [GET_getActiveShard](#get_getactiveshard)

#### GET_getByPuuid
https://developer.riotgames.com/apis#account-v1/GET_getByPuuid
```py
await client.account.GET_getByPuuid("PUUID")
```
#### GET_getByRiotId
https://developer.riotgames.com/apis#account-v1/GET_getByRiotId
```py
await client.account.GET_getByRiotId("GameName", "TagLine")
```
#### GET_getByAccessToken
https://developer.riotgames.com/apis#account-v1/GET_getByAccessToken
```py
await client.account.GET_getByAccessToken("Authorization")
```
#### GET_getActiveShard
https://developer.riotgames.com/apis#account-v1/GET_getActiveShard
```py
await client.account.GET_getActiveShard("PUUID")
```

[Back to top](#contents)


