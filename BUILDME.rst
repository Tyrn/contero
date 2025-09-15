Contero
*******

Power supply manager

Development
===========

- `Buildozer <https://github.com/kivy/buildozer>`__
- `KivyMD <https://github.com/kivymd/KivyMD>`__; MDDropdownMenu `1 <https://github.com/kivymd/KivyMD/issues/1203>`__, `2 <https://stackoverflow.com/questions/71510107/kivymd-update-mddropdownmenu-open-generates-an-error>`__
- `Kivy Garden <https://github.com/kivy-garden>`__

Use Git Hooks (optional)
------------------------

::

    (.venv) $ pre-commit install
    ...
    (.venv) $ pre-commit run --all-files

Poetry (Desktop)
----------------

::

    $ poetry install
    $ poetry shell
    (.venv) $ python contero/main.py

To leave Poetry Shell press Ctrl+D

Instead of ``poetry shell`` one can employ the usual

::

    $ source .venv/bin/actcivate
    ...
    (.venv) $ deactivate

Check memory usage
^^^^^^^^^^^^^^^^^^

::

    (.venv) $ mprof run -C python contero/main.py
    ...
    (.venv) $ mprof plot -o profile.png

Buildozer (Mobile, tested on Android)
------------------

- `Build Docker Image <https://github.com/kivy/buildozer#buildozer-docker-image>`__ (obsolete, not recommended)

::

    $ cd ~
    $ git clone https://github.com/kivy/buildozer.git
    $ cd buildozer

2023-12-11: Today it's essential to check Buildozer's Dockerfile and update openjdk, if necessary:

::

    -    openjdk-13-jdk \
    +    openjdk-17-jdk \    

Build the image:

::

    $ docker build --tag=buildozer .

Build the project:

::

    $ docker-compose run buildozer android [debug | release]
    $ adb install -r bin/*.apk

- `Use <https://github.com/kivy/buildozer#usage>`__ ``buildozer`` from dev dependencies, like this

::

    (.venv) $ buildozer android clean
    (.venv) $ buildozer android debug deploy run

*NB*, 2022-11-26: The above works for ``debug`` only. ``release`` requires explicit signing.

*NB* Be careful of the ``.buildozer`` directory. All the gigabytes precipitate there. If you delete
its contents manually, always make sure to keep ``.gitignore`` with a single asterisk in it inside ``.buildozer``
directory.
The same applies to ``.gradle``. 

- `Direnv <https://direnv.net/>`__ (``.envrc`` file); requires *direnv* to be installed and
  `configured <https://github.com/direnv/direnv/wiki/Python>`__. Is optional.
