Regions
=======

Regions are an important component to using Cassiopeia and the Riot API.

Regions are used to identify unique accounts/summoners, return text data in the region's default local, and interact with the Riot API under the hood.

Generally speaking, you will always need to specify a region when creating an entity using Cassiopeia. For example, to create an ``Account`` you specify the region to uniquely identify the account: ``account = Account(name="Kalturi", tagline="NA1", region="NA")``.

Regions are typically specified as strings (e.g. ``region="NA"`` or ``region="EUNE"``, but you can also the enum (e.g. ``region=Region.north_america``).

As of writing this, the available regions are below. You can find an updated list in the [code](https://github.com/meraki-analytics/cassiopeia/blob/master/cassiopeia/data.py#L4).

.. code-block:: python

    brazil = "BR"
    europe_north_east = "EUNE"
    europe_west = "EUW"
    japan = "JP"
    korea = "KR"
    latin_america_north = "LAN"
    latin_america_south = "LAS"
    north_america = "NA"
    oceania = "OCE"
    turkey = "TR"
    russia = "RU"
    philippines = "PH"
    singapore = "SG"
    thailand = "TH"
    taiwan = "TW"
    vietnam = "VN"
