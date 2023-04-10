==============
Quick Tutorial
==============

First, install the valaw module. See :ref:`gettingStarted-installation` for directions. 
After, you have installed valaw, you can import it into your project::

    import valaw

Then, you can initialize the client::

    client = valaw.Client("Riot_API_Token", "cluster")

Before you can use the client, you will need a Riot Games API token. 
If you don't already have one you can follow :ref:`gettingStarted-apiToken` to get one.
The :ref:`glossary-cluster` should be the :ref:`glossary-cluster` that is closest to you.

After you have initialized the client, you can use it to make requests to the API.
For example, if you want to get the content you can do::

    async def func():
        content_data = await client.content.GET_getContent("region")

For other endpoints and examples see 



