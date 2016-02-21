Rate Limiting
#############

If you don't know what a rate limit is, make sure you read `this page <https://developer.riotgames.com/docs/rate-limiting>`_.

Cassiopeia will automatically throttle the number of API requests made to Riot to prevent you from going over your rate limit.

By default, Cassiopeia sets your rate limit to the standard development key rate limit: 10 requests every 10 seconds and 500 requests every 10 minutes (600 seconds) using ``riotapi.set_rate_limits([(10, 10), (500, 600)])``. 

You can override this default behavior (for example if you have a production key) using the ``set_rate_limit`` and ``set_rate_limits`` `functions <cassiopeia/riotapi.html#cassiopeia.riotapi.set_rate_limit>`_.

Rate limiting is provided for both ``riotapi`` and ``baseriotapi``.

