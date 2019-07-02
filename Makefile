SHELL := /bin/bash

build: src/doksi.peg
	canopy src/doksi.peg --lang python
	mv src/doksi.py dist/doksi_parser.py