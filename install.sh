#!/usr/bin/env bash
sudo cp microscope_control.service /lib/systemd/system/microscope_control.service
sudo chmod 644 /lib/systemd/system/microscope_control.service
sudo systemctl daemon-reload
sudo systemctl enable microscope_control.service
