============
GET_getMatch
============

* `Riot Documentation <https://developer.riotgames.com/apis#val-match-v1/GET_getMatch>`_
* API URL::

    https://{region}.api.riotgames.com/val/match/v1/matches/{matchId}

Description
===========

Get match by id.

.. code-block:: python

    async def GET_getMatch(self, matchId: str, region: str) -> dict:

Arguments
---------

* matchId: String
* :term:`region`: String

Examples
========

Basic example (Just required arguments)
---------------------------------------

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        match_data = await client.GET_getMatch("matchId", "region")