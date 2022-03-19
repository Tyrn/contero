Contero
*******

Power supply manager

Development
===========

- `Buildozer <https://github.com/kivy/buildozer>`__
- `KivyMD <https://github.com/kivymd/KivyMD>`__; MDDropdownMenu `1 <https://github.com/kivymd/KivyMD/issues/1203>`__, `2 <https://stackoverflow.com/questions/71510107/kivymd-update-mddropdownmenu-open-generates-an-error>`__
- `Kivy Garden <https://github.com/kivy-garden>`__

Poetry (Desktop)
----------------

::

    $ poetry install
    $ poetry shell
    (.venv) $ python contero/main.py

Buildozer (Mobile)
------------------

- `Build Docker Image <https://github.com/kivy/buildozer#buildozer-docker-image>`__

::

    $ docker-compose run buildozer android [debug | release]
