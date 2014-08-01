#!/usr/local/bin/bash
export PATH=$PATH:$HOME/local/django_src/django/bin
export PYTHONPATH=$PYTHONPATH:$HOME/local:$HOME/local/django_src:$HOME/django_projects

PROJECT_NAME="labzine"
PROJECT_DIR="$HOME/django_projects/$PROJECT_NAME"
PID_FILE="$PROJECT_DIR/$PROJECT_NAME.pid"
SOCKET_FILE="$PROJECT_DIR/$PROJECT_NAME.socket"
MANAGE_FILE="$PROJECT_DIR/manage.py"
METHOD="prefork"

case "$1" in
    start)
      # Starts the Django process
      echo "Starting Django project"
      /usr/local/bin/python $MANAGE_FILE runfcgi maxchildren=2 maxspare=2 minspare=1 method=$METHOD socket=$SOCKET_FILE pidfile=$PID_FILE
  ;;
    stop)
      # stops the daemon by cat'ing the pidfile
      echo "Stopping Django project"
      kill `/bin/cat $PID_FILE`
  ;;
    restart)
      ## Stop the service regardless of whether it was
      ## running or not, start it again.
      echo "Restarting process"
      $0 stop
      $0 start
  ;;
    *)
      echo "Usage: init.sh (start|stop|restart)"
      exit 1
  ;;
esac
