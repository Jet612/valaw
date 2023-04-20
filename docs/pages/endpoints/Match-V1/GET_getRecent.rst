=============
GET_getRecent
=============

* `Riot Documentation <https://developer.riotgames.com/apis#val-match-v1/GET_getRecent>`_
* API URL::

    https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}
    
Description
===========

Get recent matches.

Returns a list of match ids that have completed 
in the last 10 minutes for live regions and 12 hours 
for the esports routing value. NA/LATAM/BR share a 
match history deployment. As such, recent matches 
will return a combined list of matches from those 
three regions. Requests are load balanced so you may 
see some inconsistencies as matches are added/removed 
from the list.

.. code-block:: python

    async def GET_getRecent(self, queue: str, region: str) -> dict:

Arguments
---------

* :term:`queue`: String
* :term:`region`: String

Examples
========

Basic example (Just required arguments)
---------------------------------------

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        recent_data = await client.GET_getRecent("queue", "region")