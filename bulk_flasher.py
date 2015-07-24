#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import subprocess
import argparse
from utilities.arg_parse import Parser
from controller.console_controller import ConsoleApp, BaseController
from utilities.console_dialog import ConsoleDialog
from utilities.adb_helper import AdbHelper
from utilities.path_parser import PathParser


def ArgParse(input):
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--full_flash', help='flash full image of device')
        parser.add_argument('-g', '--gaia', help='shallow flash gaia into device')
        parser.add_argument('-G', '--gecko', help='shallow flash gaia into device')
        options = parser.parse_args(input)
        return options


class FlashOnlyApp(ConsoleApp):
    def __init__(self):
        BaseController.__init__(self)
        self.flash_params = []
        self.dialog = ConsoleDialog()
    
    def after_flash_action(self):
        pass


def main():
    if not AdbHelper.has_adb():
        print("No adb installed; terminated")
        sys.exit(1)
    archives = {}
    option = ArgParse(sys.argv[1:])
    try:
        prog = FlashOnlyApp()
        if option.full_flash:
            prog.flash_params.append(PathParser._IMAGES)
            archives[PathParser._IMAGES] = option.full_flash
        else:
            if option.gecko:
                prog.flash_params.append(PathParser._GECKO)
                archives[PathParser._GECKO] = option.gecko
            if option.gaia:
                prog.flash_params.append(PathParser._GAIA)
                archives[PathParser._GAIA] = option.gaia
        if not archives:
            print("Nothing to flash; terminated")
            sys.exit(1)
        ret_obj = prog.dialog.yes_no('Bulk Flasher Prompt', 'Warning: this program will flash all devices! Please make sure devices are the same. continue?', ConsoleDialog._NO_CMD_INDEX)
        devices = AdbHelper.adb_devices().keys()
        if not devices:
            print("Error: No device found")
            sys.exit(1)

        for serial in devices:
            prog.do_flash(prog.flash_params, archives, serial)
    except KeyboardInterrupt:
        print ''
        print '### Quit'
        sys.exit(0)


if __name__ == '__main__':
    main()
