===============
GET_getByRiotId
===============

* `Riot Documentation <https://developer.riotgames.com/apis#account-v1/GET_getByRiotId>`_
* API URL::

    https://{cluster}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}

Description
===========

Get account by riot id.

.. code-block:: python
    
    async def GET_getByRiotId(self, gameName: str, tagLine: str, cluster: str = None) -> dict:

Arguments
---------

* :term:`gameName`: String
* :term:`tagLine`: String

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
        account_data = await client.account.GET_getByRiotId("gameName", "tagLine")

Advanced example (With Keyword Arguments)
-----------------------------------------

.. code-block:: python
    
    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        account_data = await client.account.GET_getByRiotId("gameName", "tagLine", cluster="cluster")
