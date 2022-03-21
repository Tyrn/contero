Contero
*******

Power supply manager

Development
===========

- `Buildozer <https://github.com/kivy/buildozer>`__
- `KivyMD <https://github.com/kivymd/KivyMD>`__; MDDropdownMenu `1 <https://github.com/kivymd/KivyMD/issues/1203>`__, `2 <https://stackoverflow.com/questions/71510107/kivymd-update-mddropdownmenu-open-generates-an-error>`__
- `Kivy Garden <https://github.com/kivy-garden>`__

Use Git Hooks
-------------

::

    $ pre-commit install
    ...
    $ pre-commit run --all-files

Poetry (Desktop)
----------------

::

    $ poetry install
    $ poetry shell
    (.venv) $ python contero/main.py

Check memory usage
^^^^^^^^^^^^^^^^^^

::

    (.venv) $ mprof run -C python contero/main.py
    ...
    (.venv) $ mprof plot -o profile.png

Buildozer (Mobile)
------------------

- `Build Docker Image <https://github.com/kivy/buildozer#buildozer-docker-image>`__

::

    $ docker-compose run buildozer android [debug | release]
    $ adb install -r bin/*.apk
