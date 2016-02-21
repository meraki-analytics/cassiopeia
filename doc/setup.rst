Setup
#####


Install using pip
===============
Simply ``pip install cassiopeia`` to get the latest release. (See the `pip <https://pip.pypa.io/en/stable/installing/>`_ install page if you do not have ``pip`` installed.)


Install from Source
===================
If you would like to get Cassiopeia with the most recent updates (even before they have been pushed in an official release), you can clone this repository. Go to `Cassiopeia's Github page <https://github.com/meraki-analytics/cassiopeia>`_ and either download the zip or ``git clone https://github.com/meraki-analytics/cassiopeia`` into a directory of your choice.

Next, add the location of this download to your ``PYTHONPATH`` environment variable. If a ``PYTHONPATH`` environment variable does not exist on your system (which may be true if you have a newly installed version of python), you will need to create it.

On Windows, follow the instructions `here <https://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/sysdm_advancd_environmnt_addchange_variable.mspx?mfr=true>`_. Note that if you need multiple paths on your ``PYTHONPATH``, you can separate them by a ``;``.

On Mac or Linux, add ``export PYTHONPATH=$PYTHONPATH:$HOME/cassiopeia`` to the end of your ``~/.bashrc`` file, where ``$HOME`` is the location where you downloaded or git cloned Cassiopeia.

Restart your terminal.

For more information, consult Google.


Setting Additional Environment Variables
========================================
By default, the examples in Cassiopeia look for an environment variable on your system called ``DEV_KEY`` to set your API key within ``cassiopeia.riotapi`` and ``cassiopeia.baseriotapi``. You can create a new environment variable called ``DEV_KEY``, and a similarly named environment variable for your production key if you have one (although Cassiopeia will never use your production key unless you change the code).

To create an environment variable on Windows, follow the directions `here <https://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/sysdm_advancd_environmnt_addchange_variable.mspx?mfr=true>`_.

On Linux or Mac, add ``export DEV_KEY='paste_your_developer_key_here'`` to the end of your ``~/.bashrc`` file.

Restart your terminal.

