====================
GET_getByAccessToken
====================

* `Riot Documentation <https://developer.riotgames.com/apis#account-v1/GET_getByAccessToken>`_
* API URL::

    https://{cluster}.api.riotgames.com/riot/account/v1/accounts/me

Description
===========

Get account by access token.

.. code-block:: python
    
    async def GET_getByAccessToken(self, authorization: str, cluster: str = None) -> dict:

Arguments
---------

* authorization: String - The access token

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
        account_data = await client.GET_getByAccessToken("Authorization")

Advanced example (With Keyword Arguments)
-----------------------------------------

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        account_data = await client.GET_getByAccessToken("authorization", cluster="cluster")