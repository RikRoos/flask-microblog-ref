#!/bin/bash
echo
echo Starting the Microblog app:
echo  - apply an upgrade to the database
echo  - then starting the gunicorn webserver
echo
echo Using arguments:
echo $1
echo $2

echo Waiting a few seconds to let the database boot up...
sleep 10
echo

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade db-command failed, retrying in 5 secs...
    sleep 5
done

# Starting the gunicorn process:
#
# "exec" replaces the current bash process with the gunicorn process instead of
# starting a new sub-process. This is important as Docker associates the life of
# the container to the first process that runs on it (the bash process).
#
# An interesting aspect of Docker is that anything that the container writes to
# the 'stdout' and 'stderr' will be captured and stored as logs for the container.
# For that reason the '--access-logile' and 'error-logfile' are both configured 
# with a '-'  (dash), which sends the log to the standard output so that they are
# stored as logs by Docker.
#
#exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
