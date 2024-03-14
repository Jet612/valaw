======
Client
======

Description
===========

Get VALORANT status for the given platform.

.. code-block:: python

    def __init__(self, token: str, cluster: str, raw_data: bool = False):

Arguments
---------

* `token`: String
* `cluster`: String

Keyword Arguments
-----------------

* `raw_data`: Boolean = False

Examples
========

Basic example (Just required arguments)
---------------------------------------

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster")

.. code-block:: python

    import valaw

    client = valaw.Client("riot_api_token", "cluster", raw_data=True)

Methods
=======

.. toctree::
    :maxdepth: 1
    :glob:
    :caption: Account-V1

    Account-V1/*

.. toctree::
    :maxdepth: 1
    :glob:
    :caption: Content-V1

    Content-V1/*

.. toctree::
    :maxdepth: 1
    :glob:
    :caption: Match-V1

    Match-V1/*

.. toctree::
    :maxdepth: 1
    :glob:
    :caption: Ranked-V1

    Ranked-V1/*

.. toctree::
    :maxdepth: 1
    :glob:
    :caption: Status-V1

    Status-V1/*