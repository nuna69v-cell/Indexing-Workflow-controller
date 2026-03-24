#!/bin/bash
echo "Note: crontab is not available in this environment. If deploying to a VPS, run:"
echo 'crontab -e'
echo 'And add the following line:'
echo "0 0 * * * cd $(pwd) && ./jules_schedule.sh > logs/cron.log 2>&1"
