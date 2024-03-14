==================
GET_getLeaderboard
==================

* `Riot Documentation <https://developer.riotgames.com/apis#val-ranked-v1/GET_getLeaderboard>`_
* API URL::

    https://{region}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{actId}?size={size}&startIndex={startIndex}

Description
===========

Get leaderboard for the competitive queue

.. code-block:: python

    async def GET_getLeaderboard(self, actId: str, region: str, size: int = 200, startIndex: int = 0) -> dict:

Arguments
---------

* actId: String
* :term:`region`: String

Keyword Arguments
-----------------

* size: Integer = 200
* startIndex: int = 0

Examples
========

Basic example (Just required arguments)
---------------------------------------

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        leaderboard_data = await client.GET_getLeaderboard("actId", "region")

Advanced example (With Keyword Arguments)
-----------------------------------------

.. code-block:: python
    
    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        leaderboard_data = await client.GET_getLeaderboard("actId", "region", size=200, startIndex=0)