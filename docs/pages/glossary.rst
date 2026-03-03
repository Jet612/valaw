=====
Terms
=====

.. glossary::
    Cluster
        A cluster is a group of servers used to connect to the Riot Games API. Valid clusters are: `americas`, `asia`, `esports`, `europe`. You should use the cluster closest to you.

        You can use any cluster to get valid data, although it may be faster to use the one closest to you.

    gameName
        The gameName is the username of the account, displayed to the left of the ``#`` in their :term:`Riot Id`.

    locale
        The locale is the language that the data will be returned in. Valid locales are: `ar-AE`, `de-DE`, `en-GB`, `en-US`, `es-ES`, `es-MX`, `fr-FR`, `id-ID`, `it-IT`, `ja-JP`, `ko-KR`, `pl-PL`, `pt-BR`, `ru-RU`, `th-TH`, `tr-TR`, `vi-VN`, `zh-CN`, `zh-TW`

    PUUID
        A PUUID stands for Player Universally Unique Identifier — simply put, it's a player's ID.

        Each account has a unique PUUID. The PUUID used by the Official Riot API is an encrypted form of the actual user's ID. More information can be found in the Riot Games article `here <https://www.riotgames.com/en/DevRel/player-universally-unique-identifiers-and-a-new-security-layer>`_.

    Queue
        A queue is the type of match being played. Valid queues are: `competitive`, `unrated`, `spikerush`, `tournamentmode`, `deathmatch`, `onefa`, `ggteam`, `hurm`.

        For console queues, see :term:`platformType`.

    Region
        A region is a group of servers used to connect to the Riot Games API. Valid regions are: `ap`, `br`, `esports`, `eu`, `kr`, `latam`, `na`. You should always use the region associated with the account, even if you or your server is in a different region.

        If you use a region not associated with the account you will get a 404: "Data not found - resource not found" error.

    Riot Id
        The Riot Id is the username (:term:`gameName`) and tag (:term:`tagLine`) of the account, displayed as ``gameName#tagLine``.

    tagLine
        The tagLine is the tag of the account, displayed to the right of the ``#`` in their :term:`Riot Id`.

    platformType
        The platformType is the console platform of the player. Valid platform types are: `playstation`, `xbox`. These are only used for the console endpoints.

        Valid console queues are: `console_unrated`, `console_swiftplay`, `console_hurm`, `console_competitive`, `console_deathmatch`.

Back to :ref:`top of page<Terms>`
