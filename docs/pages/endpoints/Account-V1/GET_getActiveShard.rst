==================
GET_getActiveShard
==================

* `Riot Documentation <https://developer.riotgames.com/apis#account-v1/GET_getActiveShard>`_
* API URL::

    https://{cluster}.api.riotgames.com/riot/account/v1/active-shards/by-game/val/by-puuid/{puuid}

Description
===========

Get active shard for a player.

.. code-block:: python

    async def GET_getActiveShard(self, puuid: str, cluster: str = None) -> dict:

Arguments
---------

* :term:`puuid`: String

Keyword Arguments
-----------------

* :term:`cluster`: String = None

Examples
========

Basic example (Just required arguments)
---------------------------------------

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        account_data = await client.account.GET_getActiveShard("PUUID")

Advanced example (With Keyword Arguments)
-----------------------------------------


.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        account_data = await client.account.GET_getActiveShard("puuid", cluster="cluster")