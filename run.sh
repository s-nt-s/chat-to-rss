#!/bin/bash
cd "$(dirname "$0")"
for m in $(find . -name "run.py" | sed -e s'/.\///' -e 's/\//./g' -e 's/\.py$//' ); do
    if [ -f "${m}.pid" ]; then
        PID=$(<"${m}.pid")
        if ps -p $PID > /dev/null; then
            if [ "$1" != "-s" ]; then
                echo "${m} is running with pid $PID"
            fi
            continue
        fi
    fi
    echo "Running ${m}"
    nohup python3 -m "$m" > "${m}.log" &
    echo "$!" > "${m}.pid"
done
