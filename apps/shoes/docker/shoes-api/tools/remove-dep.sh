#!/bin/bash

PS3="Select the package to uninstall: "
select pkg in $(yq '.packages * .dev-packages|keys|join(" ")' -oy -p toml "$PIPENV_PIPFILE")
do
  if [ -n "$pkg" ]; then
    pipenv uninstall $pkg;
    exit;
  fi;
  echo "Invalid package selected" && exit;
done