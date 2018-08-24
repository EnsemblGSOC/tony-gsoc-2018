#!/usr/bin bash
source $HOME/.bashrc
tail -n +2 $1 | tr -d '\n' | md5sum