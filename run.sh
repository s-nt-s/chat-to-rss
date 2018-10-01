#!/bin/bash
cd "$(dirname "$0")"
for MOD in $(find . -name "run.py" ); do
    DIR="$(dirname "$MOD")"
    MOD=$(echo "$MOD" | sed -e s'/.\///' -e 's/\//./g' -e 's/\.py$//')
    for YML in $(find $DIR -name "*.yml" ); do
        YML=$(basename $YML)
        FN="${MOD}_${YML}"
        if [ -f "${FN}.pid" ]; then
            PID=$(<"${FN}.pid")
            if ps -p $PID > /dev/null; then
                if [ "$1" != "-s" ]; then
                    echo "${FN} is running with pid $PID"
                fi
                continue
            fi
        fi
        echo "Running ${MOD} with ${YML}"
        nohup python3 -m "$MOD" "$YML" > "${FN}.log" 2>&1 &
        echo "$!" > "${FN}.pid"
    done
done
