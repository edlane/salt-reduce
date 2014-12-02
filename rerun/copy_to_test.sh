#!/bin/bash -v

cp -uv rerun_runner.py /srv/salt/_runners
cp -uv mapper.py /srv/salt/_runners
cp -uv rerun_return.py /srv/salt/_returners
cp -uv mapit.py /srv/salt/_modules
salt \* saltutil.sync_returners
salt \* saltutil.sync_modules

