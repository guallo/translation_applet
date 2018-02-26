#!/usr/bin/python

import os
import sys

LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'lib'))
sys.path.append(LIB_DIR)
sys.path.append('/mnt/datos')  # translation_client

from translation_applet import translation_applet


ta = translation_applet.TranslationApplet()
ta.run()
