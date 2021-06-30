Selenium bot
##############################################################

.. contents:: Contents
    :local:

Install
*****************************************
- Install `Python <https://www.python.org/>`_
- Install `PyCharm <https://www.jetbrains.com/pycharm/>`_
- Open PyCharm
    - Create a new project by cloning this github repository
    - Attach a `Python interpreter <https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html>`_
- Install Selenium following `this guide <https://selenium-python.readthedocs.io/installation.html#installation>`_
- Copy downloaded ``chromedriver.exe`` file in ``./_files/chromedriver.exe`` of your project

Configuration
*****************************************
- Create an Application Service of F5 *Integrated Bot Defense*
    - *Shape Endpoints Configuration* >> *Mitigation Action*: block
    - *Define Mitigation Actions* >> *Response Body*:

.. code-block:: html

    <h1 class="page-title">Demo | Blocked by Shape | Demo</h1>


Run demo
*****************************************










