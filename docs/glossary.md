# Glossary
# Contents
- [PUUID](#puuid)
- [Cluster(s)](#clusters)
## PUUID (Player Universally Unique Identifier)
A PUUID or Player Universally Unique Identifier simply put is a players ID.

Each account has a unique ID. The PUUID that the Official Riot API uses is different from the puuid the unofficial PUUID is. The PUUID's used in the official API is a encrypted form of the actual users ID. More information about PUUID's can be found in the Riot Games article [here](https://www.riotgames.com/en/DevRel/player-universally-unique-identifiers-and-a-new-security-layer)
## Cluster(s)
A cluster is a group of servers that are used to connect to the Riot Games API. Valid clusters are: `americas`, `asia`, `esports`, `europe`. You should almost always use the cluster that is closest to you.

You can use any cluster to get valid data. Although it may be faster to use the cluster that is closest to you.

## Region(s)
A region is a group of servers that are used to connect to the Riot Games API. Normally each continent has its own region. Valid regions are: `ap`, `br`, `esports`, `eu`, `kr`, `latam`, `na`. You should always use the region that the account is connected to, even if you or the server you are using is in a different region and is closer to you.

If you use a region that is not associated with the account you will get a 404: "Data not found - resource not found" error.