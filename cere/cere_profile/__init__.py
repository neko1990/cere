#!/usr/bin/env python

import os
import subprocess
import sys
import cere_configure
import logging
import shutil
import argparse
import common.variables as var
from create_graph import create_graph

logger = logging.getLogger('Profile')

def init_module(subparsers, cere_plugins):
    cere_plugins["profile"] = run
    profile_parser = subparsers.add_parser("profile", help="Profiles an application")
    profile_parser.add_argument("--app", action='store_true', help="measures application cycles")
    profile_parser.add_argument("--regions", action="store_true", help="instruments regions and generates a call graph")
    profile_parser.add_argument('--force', '-f', action="store_true", help="overwrites any previous CERE measures. (default False)")

def run(args):
    if not cere_configure.init():
        return False

    if not args.app and not args.regions:
        args.app = True
        args.regions = True
    if args.regions:
        res_1 = instrument_application(cere_configure.cere_config["run_cmd"], cere_configure.cere_config["build_cmd"], cere_configure.cere_config["cere_measures_path"], args.force)
    if args.app:
        res_2 = measure_application(cere_configure.cere_config["run_cmd"], cere_configure.cere_config["build_cmd"], cere_configure.cere_config["cere_measures_path"], args.force)
    return (res_1 and res_2)

def measure_application(run_cmd, build_cmd, measures_path, force):
    logger.info('Measuring application cycles')
    if os.path.isfile("{0}/app_cycles.csv".format(measures_path)):
        if not force:
            logger.info('Keeping previous application cycles')
            return True
    try:
        logger.debug(subprocess.check_output("{0} MODE=\"original --instrument --wrapper={1}\" -B".format(build_cmd, var.RDTSC_WRAPPER), stderr=subprocess.STDOUT, shell=True))
        logger.info(subprocess.check_output(run_cmd, stderr=subprocess.STDOUT, shell=True))
    except subprocess.CalledProcessError as err:
        logger.critical(str(err))
        logger.critical(err.output)
    if not os.path.isfile("main.csv"):
        logger.critical('Measuring application failed: No output file')
        return False
    else:
        try:
            shutil.move("main.csv", "{0}/app_cycles.csv".format(measures_path))
        except IOError as err:
            logger.critical(str(err))
            return False
    logger.info('Measuring application success')
    return True

def instrument_application(run_cmd, build_cmd, measures_path, force):
    logger.info('Start instrumentation')
    if os.path.isfile("{0}/app.prof".format(measures_path)) and not force:
        logger.info('Keeping previous instrumentation')
        create_graph(force)
        return True
    try:
        logger.debug(subprocess.check_output("{0} MODE=\"original --instrument --instrument-app\" -B".format(build_cmd), stderr=subprocess.STDOUT, shell=True))
        logger.info(subprocess.check_output("LD_PRELOAD=/usr/local/lib/libprofiler.so CPUPROFILE={0}/app.prof {1}".format(measures_path, run_cmd), stderr=subprocess.STDOUT, shell=True))
    except subprocess.CalledProcessError as err:
        logger.critical(str(err))
        logger.critical(err.output)
    if not os.path.isfile("{0}/app.prof".format(measures_path)):
        logger.critical("Instrumentation failed: No output file")
        return False
    logger.info('Instrumentation success')
    create_graph(force)
    return True
