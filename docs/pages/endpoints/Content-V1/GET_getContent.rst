==============
GET_getContent
==============

* `Riot Documentation <https://developer.riotgames.com/apis#val-content-v1/GET_getContent>`_
* API URL::

    https://{region}.api.riotgames.com/val/content/v1/contents{locale}

Description
===========

Get content optionally filtered by locale. A locale is recommended to be used for faster response times.

.. code-block:: python

    async def GET_getContent(self, region: str, locale: str = "") -> dict:

Arguments
---------

* :term:`region`: String

Keyword Arguments
----------------

* :term:`locale`: String = "" (None)

Examples
========

Basic example (Just required arguments)
--------------------------------------

.. note::
    
    This example is not recommended as it is not using a locale; this will result in a slower response time.

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        content_data = await client.content.GET_getContent("region")

Advanced example (With Keyword Arguments)
-----------------------------------------

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

    async def func():
        content_data = await client.content.GET_getContent("region", locale="locale")