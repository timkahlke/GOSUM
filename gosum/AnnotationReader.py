#!/usr/bin/env python

import sys
import os
import logging
import re

# Quick'n'Dirty! Change!
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



############
#
#   Class for reading tab and interpro gff files
#
####
#   COPYRIGHT DISCALIMER:
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
#   Author: Tim Kahlke, tim.kahlke@audiotax.is
#   Date:   May 2018
#



class Reader():
    def __init__(self,path):
        self.path = path
        self.g2g = {}
        self._parse_annotation()


    def _parse_annotation(self):
        with open(self.path, "r") as f:
            if f.readline().startswith("#"):
                self.parse_interpro()
            else:
                self.parse_tab()


    def parse_interpro(self):
        with open(self.path,"r") as f:
            for line in f:
                if "Ontology_term" in line:
                    gene = line.split("\t")[0]
                    gos = [x for x in line.split("\"") if x.startswith("GO:")]
                    if gene in self.g2g:
                        self.g2g[gene].union(set(gos))
                    else:
                        self.g2g[gene] = set(gos)


    def parse_tab(self):
        with open(self.path,"r") as f:
            for line in f:
                s = line.replace("\n","").split("\t")
                self.g2g[s[0]] = set(split(",",s[1]))

    def get_annotation(self,gene):
        try:
            return self.g2g[gene]
        except KeyError, e:
            return 0
