#!/usr/bin/env python

import sys
import os
import logging
import argparse

# Quick'n'Dirty! Change!
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gosum import GOTree 
from gosum import AnnotationReader as ar
from gosum import Utils


############
#
#   Main class to start gosum
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



class Main():

        def __init__(self):
            logging.basicConfig(format='',level=logging.INFO)
            self.logger = logging.getLogger()

    
        def run_gosum(self,args):
            go_tree = GOTree.Tree(args.obo)
            reader = ar.Reader(args.annotation)
            gene_list = Utils.read_list(args.gene_list)
            go_list = self.get_terms(reader,gene_list)
            lvl_terms = go_tree.get_lvl_terms(args.level,args.aspect)
            
            summary = {}
            for x in lvl_terms:
                summary[x] = 0
                sub_tree = go_tree.get_sub_tree(args.aspect,x)
                # x below given level, i.e., no sub_tree
                if not sub_tree:
                    continue
                for g in go_list:
                    if go_tree.is_child(g,sub_tree):
                        summary[x]+=1
            self.write_output(summary,args,go_tree)


        def write_output(self,s,args,g):
            out = open(args.output,"w")
            klist = s.keys()
            klist.sort()
            for x in klist:
                if s[x] or args.complete:
                    out.write("%s\t%s\t%s\n" % (x,g.term_hash[x]['name'],s[x]))

            out.close()


        def get_terms(self,reader,gl):
            term_list = set()
            for g in gl:
                annotation = reader.get_annotation(g)
                if annotation:
                    term_list = term_list.union(annotation)
                else:
                    print("No annotation found for gene " + g)
            return term_list





