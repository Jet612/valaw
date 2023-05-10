==============
Quick Tutorial
==============

First, install the valaw module. See :ref:`Installation` for directions. 
After, you have installed valaw, you can import it into your project::

    import valaw

Then, you can initialize the client::

    client = valaw.Client("Riot_API_Token", "cluster")

.. note:: 
    Before you can use the client, you will need a Riot Games API token. 
    If you don't already have one you can follow :ref:`Getting a Riot API Token` to get one.

The :term:`cluster` should be the :term:`cluster` that is closest to you.

After you have initialized the client, you can use it to make requests to the API.
For example, if you want to get the content you can do::

    async def func():
        content_data = await client.GET_getContent("region")

For other endpoints and examples see :ref:`List of Endpoints`

All of that put together looks like::

    import valaw

    client = valaw.Client("Riot_API_Token", "cluster")

    async def func():
        content_data = await client.GET_getContent("region")

Raw Request Data
================

If you want to get the raw requests data instead of the data as an object, you can do::

    client = valaw.Client("Riot_API_Token", "cluster", raw_data=True)

This will return the raw data from the request as dictionary.