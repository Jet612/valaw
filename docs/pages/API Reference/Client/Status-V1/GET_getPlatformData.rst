===================
GET_getPlatformData
===================

* `Riot Documentation <https://developer.riotgames.com/apis#val-status-v1/GET_getPlatformData>`_
* API URL::

    https://{region}.api.riotgames.com/val/status/v1/platform-data

Description
===========

Get VALORANT status for the given platform.

.. code-block:: python

    async def GET_getPlatformData(self, region: str) -> dict:

Arguments
---------

* :term:`region`: String

Examples
========

Basic example (Just required arguments)
---------------------------------------

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        status_data = await client.GET_getPlatformData("region")