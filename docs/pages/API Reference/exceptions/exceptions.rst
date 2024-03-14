==========
Exceptions
==========

Custom exceptions for VALAW.

InvalidCluster
==============

- Description: Invalid Cluster
- Type: `ValueError <https://docs.python.org/3/library/exceptions.html#ValueError>`_

.. code-block:: python

    class InvalidCluster(ValueError):
        """Invalid Cluster."""

InvalidRegion
=============

- Description: Invalid Region
- Type: `ValueError <https://docs.python.org/3/library/exceptions.html#ValueError>`_

.. code-block:: python

    class InvalidRegion(ValueError):
        """Invalid Region."""

RiotAPIResponseError
====================

- Description: An error from the Riot API
- Type: `Exception <https://docs.python.org/3/library/exceptions.html#Exception>`_
- Arguments
    - status_code: The status code of the response
    - status_message: The status message of the response
    - message: The message of the exception


.. code-block:: python

    class RiotAPIResponseError(Exception):
        """Riot API Response Error."""
        def __init__(self, status_code: int, status_message: str):
            self.status_code = status_code
            self.status_message = status_message
            self.message = str(status_code) + " - " + status_message
            super().__init__(self.message)

