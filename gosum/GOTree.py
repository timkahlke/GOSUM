#!/usr/bin/env python

import sys
import os
import logging
import re

# Quick'n'Dirty! Change!
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



############
#
#   Class for classification
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



class Tree():
    def __init__(self,obo_path):
        self.obo_path = obo_path
        self._init_trees()


    def _init_trees(self):
        self.biological_process = {}
        self.molecular_function = {}
        self.cellular_component = {}
        self._parse_obo()


    def _parse_obo(self):
        current_term = ""
        i = re.compile('^id:\s(GO:\d+)$')
        n = re.compile('^name:\s(.*)$')
        ns = re.compile('^namespace:\s(.*)$')
        d = re.compile('^def:\s(.*)$')
        a = re.compile('^is_a:\s(GO:\d+)\s.*$')
        o = re.compile('^is_obsolete:\strue.*$')
        children = []
        tree = {}

        with open(self.obo_path,"r") as f:
            for line in f:
                if i.match(line):
                    current_term = i.match(line).group(1)
                    if not current_term in tree:
                        tree[current_term] = {'id':current_term}
                elif n.match(line):
                        tree[current_term]['name'] = n.match(line).group(1)
                elif ns.match(line):
                    tree[current_term]['namespace'] =ns.match(line).group(1)
                elif d.match(line):
                    tree[current_term]['definition'] = d.match(line).group(1)
                elif a.match(line):
                    if not a.match(line).group(1) in tree:
                        tree[a.match(line).group(1)] = {}
                    try:
                        tree[a.match(line).group(1)]['child'][current_term] = tree[current_term] 
                    except KeyError, e:
                        tree[a.match(line).group(1)]['child'] = {}
                        tree[a.match(line).group(1)]['child'][current_term] = tree[current_term]
                    if not current_term in children:
                        children.append(current_term)
                elif o.match(line):
                    del tree[current_term]
                else:
                    continue;
      
        for c in children:
            try:
                del tree[c]
            except KeyError, e:
                print(e)

        for k in tree.keys():
            if tree[k]['name'] == "biological_process":
                self.biological_process = tree[k]
            elif tree[k]['name'] == "molecular_function":
                self.molecular_function = tree[k]
            elif tree[k]['name'] == "cellular_component":
                self.cellular_component = tree[k]
            else:
                print("Unknown name for 3 main classes: " + k)
                exit(1)

