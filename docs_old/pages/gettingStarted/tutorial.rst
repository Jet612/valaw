==============
Quick Tutorial
==============

First, install the valaw module. See :ref:`Installation` for directions.
After you have installed valaw, you can import it into your project::

    import valaw
    import asyncio

Then, initialize the client with your API token and the :term:`cluster` closest to you::

    client = valaw.Client("Riot_API_Token", "americas")

.. note::
    Before you can use the client, you will need a Riot Games API token.
    If you don't already have one, follow :ref:`Getting a Riot API Token` to get one.

After you have initialized the client, you can use it to make requests to the API.
For example, to get the content for the ``na`` region::

    async def main():
        content_data = await client.GET_getContent("na", "en-US")
        await client.close()

    asyncio.run(main())

.. note::
    All API methods are ``async`` and must be called inside an ``async`` function.
    Always call ``client.close()`` when you are done to cleanly shut down the session.

A full working example::

    import valaw
    import asyncio

    async def main():
        client = valaw.Client("Riot_API_Token", "americas")
        try:
            content_data = await client.GET_getContent("na", "en-US")
            print(content_data)
        finally:
            await client.close()

    asyncio.run(main())

Raw Request Data
================

If you want to get the raw JSON data instead of a typed object, pass ``raw_data=True``::

    client = valaw.Client("Riot_API_Token", "americas", raw_data=True)

This will return the raw response as a dictionary instead of a typed object.

Back to :ref:`top of page<Quick Tutorial>`
