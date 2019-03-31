#!/usr/bin/env bash
cd $MICROSCOPE_CONTROLLER_HOME
git pull
python udp_controller.py
