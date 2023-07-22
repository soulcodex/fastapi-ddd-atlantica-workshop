#!/bin/bash

DEP=$(read -rp "Package name to install: " dep; echo "$dep")
DEV=$(read -rp "Is a development / testing stage package? [yes|no] " dev; echo "$dev")

case $DEV in
  "yes")
  pipenv install --dev "$DEP";;
  "no")
  pipenv install "$DEP";;
  *)
  echo "Invalid option to install a package only >>>yes<<< or >>>no<<< allowed."
esac