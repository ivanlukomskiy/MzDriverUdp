#!/usr/bin/env bash
cd $MICROSCOPE_CONTROLLER_HOME
pwd
git pull
python udp_controller.py
