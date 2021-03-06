#!/usr/bin/env python
# This file is part of CERE.
#
# Copyright (c) 2013-2015, Universite de Versailles St-Quentin-en-Yvelines
#
# CERE is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# CERE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERE.  If not, see <http://www.gnu.org/licenses/>.
import os
import argparse
import logging
import subprocess
import cere_configure
import common.variables as var

logger = logging.getLogger('Hybrid')

def init_module(subparsers, cere_plugins):
  cere_plugins["hybrid"] = run
  flag_parser = subparsers.add_parser("hybrid", help="test optimal optimization flags")
  flag_parser.add_argument('--regions-file', required=True, help="file to compile")
  flag_parser.add_argument('--region', help="Region to instrument")

def run(args):
  if not cere_configure.init():
    return False
  args.regions_file = os.path.realpath(args.regions_file)
  if not os.path.isfile(cere_configure.cere_config["regions_infos"]):
    logger.error("No such file: {0}".format(cere_configure.cere_config["regions_infos"]))
    logger.error("Did you run cere regions?")
    return False
  region_input=""
  if args.region:
    region_input="--region={0}".format(args.region)
  try:
    logger.debug(subprocess.check_output("{0} MODE=\"original --hybrid --instrument {5} --wrapper={1} --hybrid-regions={2} \
    --regions-infos={3} --cere-objects={4}\"".format(cere_configure.cere_config["build_cmd"], var.RDTSC_WRAPPER, args.regions_file, \
    cere_configure.cere_config["regions_infos"], os.path.realpath("__cere__objects"), region_input), stderr=subprocess.STDOUT, shell=True))
  except subprocess.CalledProcessError as err:
    logger.critical(str(err))
    logger.critical(err.output)
    return False
  return True
