#!/bin/bash

ODIR="source"
PDIR="${PWD}/../kiwifarmer"

sphinx-apidoc \
--separate \
--private \
--module-first \
-o "${ODIR}" \
"${PDIR}"

rm -vf "${ODIR}/modules.rst"