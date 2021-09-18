#!/bin/bash
python3 main.py > server.log 2>&1 &
python3 main_bot.py