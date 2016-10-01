#!/usr/bin/env python
import argparse
import logging

from core import ShellGui
from core import Utils
from core.CrontabManager import CrontabManager
from core.MainController import MainController
import signal
import sys

from core.SynapseLauncher import SynapseLauncher


def signal_handler(signal, frame):
        print "\n"
        Utils.print_info("Ctrl+C pressed. Killing Jarvis")
        sys.exit(0)

ACTION_LIST = ["start", "gui", "load-events"]


def main():
    """
    Entry point of jarvis program
    """
    # create arguments
    parser = argparse.ArgumentParser(description='JARVIS')
    parser.add_argument("action", help="[start|gui|load-events]")
    parser.add_argument("--run-synapse", help="Name of a synapse to load surrounded by quote")
    parser.add_argument("--brain-file", help="Full path of a brain file")

    # parse arguments from script parameters
    args = parser.parse_args()
    logging.debug("jarvis args: %s" % args)
    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        sys.exit(1)

    # by default, no brain file is set. Use the default one: brain.yml in the root path
    brain_file = None

    # check the user provide a valid action
    if args.action not in ACTION_LIST:
        Utils.print_warning("%s is not a recognised action\n" % args.action)
        parser.print_help()

    if args.action == "start":
        # check if user set a brain.yml file
        if args.brain_file:
            brain_file = args.brain_file

        # user set a synapse to start
        if args.run_synapse is not None:
            SynapseLauncher.start_synapse(args.run_synapse, brain_file=brain_file)

        if args.run_synapse is None:
            Utils.print_success("Starting JARVIS")
            Utils.print_info("Press Ctrl+C for stopping")
            # catch signal for killing on Ctrl+C pressed
            signal.signal(signal.SIGINT, signal_handler)
            # start the main controller
            main_controller = MainController(brain_file=brain_file)
            main_controller.start()

    if args.action == "gui":
        ShellGui()

    if args.action == "load-events":
        crontab_manager = CrontabManager(brain_file=brain_file)
        crontab_manager.load_events_in_crontab()
        Utils.print_success("Event loaded in crontab")

if __name__ == '__main__':
    main()
