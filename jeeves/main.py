#!/usr/bin/env python2
# -*- coding: utf-8-*-

import os
import sys
import shutil
import logging

import yaml
import argparse

from jeeves import diagnose, settings, stt, tts
from jeeves.conversation import Conversation


sys.path.append(settings.LIB_PATH)

parser = argparse.ArgumentParser(description='Jeeves Voice Control Center')
parser.add_argument('--local', action='store_true',
                    help='Use text input instead of a real microphone')
parser.add_argument('--no-network-check', action='store_true',
                    help='Disable the network connection check')
parser.add_argument('--diagnose', action='store_true',
                    help='Run diagnose and exit')
parser.add_argument('--debug', action='store_true', help='Show debug messages')
args = parser.parse_args()

if args.local:
    from jeeves.local_mic import Mic
else:
    from jeeves.mic import Mic


class Jeeves(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

        # Create config dir if it does not exist yet
        if not os.path.exists(settings.CONFIG_PATH):
            try:
                os.makedirs(settings.CONFIG_PATH)
            except OSError:
                self._logger.error("Could not create config dir: '%s'",
                                   settings.CONFIG_PATH, exc_info=True)
                raise

        # Check if config dir is writable
        if not os.access(settings.CONFIG_PATH, os.W_OK):
            self._logger.critical("Config dir %s is not writable. Jeeves " +
                                  "won't work correctly.",
                                  settings.CONFIG_PATH)

        # FIXME: For backwards compatibility, move old config file to newly
        #        created config dir
        old_configfile = os.path.join(settings.LIB_PATH, 'profile.yml')
        new_configfile = settings.config('profile.yml')
        if os.path.exists(old_configfile):
            if os.path.exists(new_configfile):
                self._logger.warning("Deprecated profile file found: '%s'. " +
                                     "Please remove it.", old_configfile)
            else:
                self._logger.warning("Deprecated profile file found: '%s'. " +
                                     "Trying to copy it to new location '%s'.",
                                     old_configfile, new_configfile)
                try:
                    shutil.copy2(old_configfile, new_configfile)
                except shutil.Error:
                    self._logger.error("Unable to copy config file. " +
                                       "Please copy it manually.",
                                       exc_info=True)
                    raise

        # Read config
        self._logger.debug("Trying to read config file: '%s'", new_configfile)
        try:
            with open(new_configfile, "r") as f:
                self.config = yaml.safe_load(f)
        except OSError:
            self._logger.error("Can't open config file: '%s'", new_configfile)
            raise

        try:
            stt_engine_slug = self.config['stt_engine']
        except KeyError:
            stt_engine_slug = 'sphinx'
            logger.warning("stt_engine not specified in profile, defaulting " +
                           "to '%s'", stt_engine_slug)
        stt_engine_class = stt.get_engine_by_slug(stt_engine_slug)

        try:
            slug = self.config['stt_passive_engine']
            stt_passive_engine_class = stt.get_engine_by_slug(slug)
        except KeyError:
            stt_passive_engine_class = stt_engine_class

        try:
            tts_engine_slug = self.config['tts_engine']
        except KeyError:
            tts_engine_slug = tts.get_default_engine_slug()
            logger.warning("tts_engine not specified in profile, defaulting " +
                           "to '%s'", tts_engine_slug)
        tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

        # Initialize Mic
        self.mic = Mic(tts_engine_class.get_instance(),
                       stt_passive_engine_class.get_passive_instance(),
                       stt_engine_class.get_active_instance())

    def run(self):
        if 'first_name' in self.config:
            salutation = ("How can I be of service, %s?"
                          % self.config["first_name"])
        else:
            salutation = "How can I be of service?"
        self.mic.say(salutation)

        conversation = Conversation("JEEVES", self.mic, self.config)
        conversation.handleForever()

if __name__ == "__main__":

    print("*******************************************************")
    print("*             JEEVES - THE TALKING COMPUTER           *")
    print("*******************************************************")

    logging.basicConfig()
    logger = logging.getLogger()
    logger.getChild("jeeves.stt").setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if not args.no_network_check and not diagnose.check_network_connection():
        logger.warning("Network not connected. This may prevent Jeeves from " +
                       "running properly.")

    if args.diagnose:
        failed_checks = diagnose.run()
        sys.exit(0 if not failed_checks else 1)

    try:
        app = Jeeves()
    except Exception:
        logger.error("Error occured!", exc_info=True)
        sys.exit(1)

    app.run()
