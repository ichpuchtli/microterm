#!/usr/bin/sh

PYTHON=/usr/bin/python2
UTERM_PATH=/home/sam/src/microterm
UTERM_PY=/home/sam/src/microterm/uterm.py

UTERM_LOG=$UTERM_PATH/log.txt
UTERM_ERROR_LOG=$UTERM_PATH/errorlog.txt

#TODO
# create log files if don't exist
# graceful exit of daemon, with systemd
# incorporate more debug information


while true; do


  echo >> $UTERM_LOG
  echo >> $UTERM_ERROR_LOG

  echo "##################################################" >> $UTERM_LOG
  echo "##################################################" >> $UTERM_ERROR_LOG

  echo "New Microterm Instance" >> $UTERM_LOG
  echo "New Microterm Instance" >> $UTERM_ERROR_LOG

  echo "##################################################" >> $UTERM_LOG
  echo "##################################################" >> $UTERM_ERROR_LOG

  $PYTHON $UTERM_PY >> $UTERM_LOG 2>> $UTERM_ERROR_LOG

  sleep 1 # sleep here to prevent massive logs

done
