# Glossary
# Contents
- [Cluster(s)](#clusters)
- [gameName](#gamename)
- [PUUID](#puuid)
- [Region(s)](#regions)
- [Riot Id](#riot-id)
- [tagLine](#tagline)

## Cluster(s)
A cluster is a group of servers that are used to connect to the Riot Games API. Valid clusters are: `americas`, `asia`, `esports`, `europe`. You should almost always use the cluster that is closest to you.

You can use any cluster to get valid data. Although it may be faster to use the cluster that is closest to you.

## gameName
The gameName is the username of the account. The username is the name displayed to the left of the # (hashtag) in their [Riot Id](#riotid).

## PUUID
A PUUID stands for: Player Universally Unique Identifier, simply put it's a players ID.

Each account has a unique ID. The PUUID that the Official Riot API uses is different from the puuid the unofficial PUUID is. The PUUID's used in the official API is a encrypted form of the actual users ID. More information about PUUID's can be found in the Riot Games article [here](https://www.riotgames.com/en/DevRel/player-universally-unique-identifiers-and-a-new-security-layer)

## Queue(s)
A queue is the type of match that is being played. Valid queues are: `competitive`, `unrated`, `spikerush`, `tournamentmode`, `deathmatch`, `onefa`, `ggteam`.

## Region(s)
A region is a group of servers that are used to connect to the Riot Games API. Normally each continent has its own region. Valid regions are: `ap`, `br`, `esports`, `eu`, `kr`, `latam`, `na`. You should always use the region that the account is connected to, even if you or the server you are using is in a different region and is closer to you.

If you use a region that is not associated with the account you will get a 404: "Data not found - resource not found" error.

## Riot Id
The Riot Id is the username ([gameName](#gamename)) and tag ([tagLine](#tagline)) of the account. The Riot Id is displayed as `gameName#tagLine` with the username and tag separated by a # (hashtag).

## tagLine
The tagLine is the tag of the account. The tag is the name displayed to the right of the # (hashtag) in their [Riot Id](#riotid).
