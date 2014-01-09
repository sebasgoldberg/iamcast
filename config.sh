#!/bin/bash
if [ ! -f 'alternativa/ambiente.py' ]
then
  cp alternativa/ambiente.default.py alternativa/ambiente.py
fi

vim alternativa/ambiente.py
