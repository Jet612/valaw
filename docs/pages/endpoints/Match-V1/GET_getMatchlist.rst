================
GET_getMatchlist
================

* `Riot Documentation <https://developer.riotgames.com/apis#val-match-v1/GET_getMatchlist>`_
* API URL::

    https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}

Description
===========

Get matchlist for games played by puuid.

.. code-block:: python
    
    async def GET_getMatchlist(self, puuid: str, region: str) -> dict:

Arguments
---------

* :term:`puuid`: String
* :term:`region`: String

Examples
========

Basic example (Just required arguments)
---------------------------------------

.. code-block:: python
    
    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        matchlist_data = await client.match.GET_getMatchlist("puuid", "region")