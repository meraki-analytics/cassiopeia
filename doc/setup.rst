Setup
#####

**Cassiopeia requires Python 3.6 and we highly recommend installing Anaconda with Python 3.6.**

Install using pip
=================
Simply ``pip install cassiopeia`` to get the latest release. (See the `pip <https://pip.pypa.io/en/stable/installing/>`_ install page if you do not have ``pip`` installed.) If you want to pull the most recent version, you can install directly from GitHub using ``pip install git+https://github.com/meraki-analytics/cassiopeia.git`` instead. We may not make a PyPy release (which ``pip`` usually pulls from) for small changes to the code.


PyCurl Issues
=============

You may have some issues during installation due to PyCurl. Try the installation first, and if you have issues with pycurl come back and read this section. If Cass installed properly but is throwing certificate errors, skip to the 3rd paragraph.

At the moment PyCurl does not fully support installation with Python 3.6 and many people have had issues. The easiest thing to do (and what we *highly* recommend) is to install Python 3.6 via `Anaconda <https://www.anaconda.com/download/>`_. Anaconda is a package manager for Python and provides many packages that are difficult to install without Anaconda. If you do not or can't use Anaconda, you'll need download and install Curl, then use ``easy_install`` to install PyCurl and link it to the proper Curl libraries. This isn't much fun, and again we recommend Anaconda to ease the process.

If you successfully installed Cass but it's throwing a certificate error, you probably just need to ``pip install certifi``. This should solve any certificate errors.

If you are having more problems, let us know via the Riot API discord server or our Meraki discord server.


Install from Source
===================
If you would like to get Cassiopeia with the most recent updates (even before they have been pushed in an official release), you can clone the repository. Go to `Cassiopeia's Github page <https://github.com/meraki-analytics/cassiopeia>`_ and either download the zip or ``git clone https://github.com/meraki-analytics/cassiopeia`` into a directory of your choice.

Next, add the newly downloaded cassiopeia source directory to your ``PYTHONPATH`` environment variable. If a ``PYTHONPATH`` environment variable does not exist on your system (which may be true if you have a newly installed version of python), you will need to create it.

On Windows, follow the instructions `here <https://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/sysdm_advancd_environmnt_addchange_variable.mspx?mfr=true>`_. Note that if you need multiple paths on your ``PYTHONPATH``, you can separate them with a ``;``.

On Mac or Linux, add ``export PYTHONPATH=$PYTHONPATH:<CASSIOPEIA PATH>`` to the end of your shell rc file (this should be ``~/.bashrc`` for most), where ``<CASSIOPEIA PATH>`` is the path of the directory you cloned, or the cassiopeia.zip file you downloaded.

Restart your terminal/IDE.

Google can probably give you more information as well, and note that the path name you add your your ``PYTHONPATH`` should end in ``.../cassiopeia``.


Setting Your API Key and Other Settings
=======================================
By default, Cass's settings are stored in a json file located ``cassiopeia/configuration/default.json``. You can modify this file or create a custom settings file and pass it in as the first argument to your program.

In order to set your API key, Cass will look for an environment variable on your system called ``RIOT_API_KEY``. You can change this by manually specifying your API key in your settings file, or changing the name of the environment variable. To create an environment variable on Windows, follow the directions `here <https://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/sysdm_advancd_environmnt_addchange_variable.mspx?mfr=true>`_. On Linux or Mac, add ``export RIOT_API_KEY='<YOUR_API_KEY>'`` to the end of your shell rc file (this should be ``~/.bashrc`` for most), where ``<YOUR_API_KEY>`` is your Riot-issued API key. Then your terminal/IDE.

In your settings file, you can also set a default region. This region will be used if you did not provide a region when using Cassiopeia objects.

We will add more customizable settings in the future, so feel free to check this section every so often.
