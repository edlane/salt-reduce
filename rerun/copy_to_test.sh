#!/bin/bash

cp -uv rerun_return.py /srv/salt/_returner
salt \* saltutil.sync_returners

