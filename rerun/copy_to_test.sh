#!/bin/bash

cp -uv rerun_return.py /srv/salt/_returners
salt \* saltutil.sync_returners

