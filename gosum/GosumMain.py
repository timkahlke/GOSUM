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
#   Date:   April 2017
#



class Main():

        def __init__(self):
            logging.basicConfig(format='',level=logging.INFO)
            self.logger = logging.getLogger()

    
        def run_gosum(self,args):
            go_tree = GOTree.Tree(args.obo)
            reader = ar.Reader(args.annotation)
            gene_list = Utils.read_list(args.gene_list)
            print(gene_list)

