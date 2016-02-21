Advanced Topics
###############

Using Both Core and Dto Datatypes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use both ``cassiopeia.riotapi`` and ``cassiopeia.baseriotapi`` within the same program and the rate limiting will still work correctly. This may be useful if you want to use advanced functionality for some types but not others.

Retry 500s
^^^^^^^^^^

By default, Cassiopeia will wait and retry if a request returns a 429 (although this should rarely happen). If you are running a long gather data script, it can be helpful to do the same on 500s. See the decorator `here <https://github.com/meraki-analytics/cassiopeia/blob/master/example/match_collection.py>`_ for an example on how to extend Cassiopeia's request functionality to retry under certain conditions (such as 500s).

Changing the Value of Attributes Cassiopeia Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All Core objects in Cassiopeia are immutable. This is deliberate to prevent users from modifying the underlying data which may break functionality.

For example, if a user was able to run

.. code-block:: python

    match.red_team = 5  # This raises AttributeError: can't set attribute
    
this would break functionality that relied on ``match.red_team`` being a ``Team`` object.

If you wish to modify Cassiopeia objects you can create a new class that uses the Cassiopeia class to during initialization. For example:

.. code-block:: python

    class Champion(cassiopeia.type.core.staticdata.Chamption):
        def __init__(self, champion):
            self.name = champion.name
            self.id = champion.id

    annie = riotapi.get_champion_by_name("Annie")
    annie = Champion(annie)
    annie.id = 100  # Does not raise an exception
    print(annie.id)

Alternatively, you can edit the underlying Dto object (which is mutable) to alter the return values from the Core type. For example:

.. code-block:: python

    annie = riotapi.get_champion_by_name("Annie")
    dto = annie.data  # Get the underlying Dto object
    dto.id = 100
    print(annie.id)

Be careful when using the second method, as radically changing object types could break code which relies on data having a certain type.


Additional Setup
^^^^^^^^^^^^^^^^

During development it can be very useful to quickly boot up a terminal to test a command. To make this easy, you can create an entirely new python package (which you can call ``cass``, for example) that automatically runs the usual setup functions. Here is an example:

.. code-block:: python

    cass/__init__.py:
        from cassiopeia import riotapi

        # Sets the region, API key, and output for riotapi
        def setup(region="NA", print_calls=True, key="development"):
            riotapi.set_region(region)
            riotapi.print_calls(print_calls)

            key = key.lower()
            if(key in ("d", "dev", "development")):
                key = os.environ["DEV_KEY"]
            elif(key in ("p", "prod", "production")):
                key = os.environ["PROD_KEY"]
                riotapi.set_rate_limits((3000, 10), (180000, 600))
            riotapi.set_api_key(key)

        setup()

After this, you can run ``from cass import riotapi`` and the ``set_region`` and ``set_api_key`` functions will be run for you automatically. Also, ``print_calls`` will be true (which is helpful for development).

