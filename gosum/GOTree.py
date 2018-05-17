#!/usr/bin/env python

import sys
import os
import logging
import re

# Quick'n'Dirty! Change!
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



############
#
#   Class for reading obo files and providing data structures to work with 
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
        self.trees = {'biological_process':{}, 'molecular_function':{},'cellular_component':{}}
        self._parse_obo()


    def get_sub_tree(self,asp,n):
        return self._get_sub(self.trees[asp],n)


    def _parse_obo(self):
        current_term = ""
        i = re.compile('^id:\s(GO:\d+)$')
        n = re.compile('^name:\s(.*)$')
        ns = re.compile('^namespace:\s(.*)$')
        d = re.compile('^def:\s(.*)$')
        a = re.compile('^is_a:\s(GO:\d+)\s.*$')
        o = re.compile('^is_obsolete:\strue.*$')
        children = set()
        tree = {}
        self.term_hash = {}

        with open(self.obo_path,"r") as f:
            for line in f:
                if i.match(line):
                    current_term = i.match(line).group(1)
                    self.term_hash[current_term] = {}
                    if not current_term in tree:
                        tree[current_term] = {}
                elif n.match(line):
                        self.term_hash[current_term]['name'] = n.match(line).group(1)
                elif ns.match(line):
                    self.term_hash[current_term]['namespace'] =ns.match(line).group(1)
                elif d.match(line):
                    self.term_hash[current_term]['definition'] = d.match(line).group(1)
                elif a.match(line):
                    if not a.match(line).group(1) in tree:
                        tree[a.match(line).group(1)] = {}
                    tree[a.match(line).group(1)][current_term] = tree[current_term] 
                    children.add(current_term)
                elif o.match(line):
                    children.add(current_term)
                    del self.term_hash[current_term]
                else:
                    continue;
     
        for c in children:
            try:
                del tree[c]
            except KeyError, e:
                print(" Can not delete " + str(e))

        for k in tree.keys():
            if self.term_hash[k]['name'] == "biological_process":
                self.trees['biological_process'] = tree[k]
            elif self.term_hash[k]['name'] == "molecular_function":
                self.trees['molecular_function'] = tree[k]
            elif self.term_hash[k]['name'] == "cellular_component":
                self.trees['cellular_component'] = tree[k]
            else:
                print("Unknown name for 3 main classes: " + k)
                exit(1)
            del self.term_hash[k]
            self._walk_lvls(0,tree[k])
          

    def _walk_lvls(self,lvl,tree):
        for k in tree.keys():
            self.term_hash[k]['index'] = lvl + 1
            self._walk_lvls(lvl + 1,tree[k])


    def _get_sub(self,tree,node):
        for k in tree:
            if k == node:
                return tree[k]
            else:
                t =  self._get_sub(tree[k],node)
                if t:
                    return t
            

    def is_child(self,c,tree):
        for k in tree:
            if k == c:
                return 1
            else:
                if self.is_child(c,tree[k]):
                    return 1 


    def get_lvl_terms(self,lvl,asp):
        terms = [x for x in self.term_hash if self.term_hash[x]['index'] == lvl and self.term_hash[x]['namespace'] == asp]
        return terms
