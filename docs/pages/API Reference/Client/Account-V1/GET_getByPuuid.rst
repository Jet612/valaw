==============
GET_getByPuuid
==============

* `Riot Documentation <https://developer.riotgames.com/apis#account-v1/GET_getByPuuid>`_
* API URL::

    https://{cluster}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}

Description
===========

Get account by PUUID.

.. code-block:: python

    async def GET_getByPuuid(self, puuid: str, cluster: str = None) -> dict:

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
        account_data = await client.GET_getByPuuid("puuid")

Advanced example (With Keyword Arguments)
-----------------------------------------

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        account_data = await client.GET_getByPuuid("puuid", cluster="cluster")