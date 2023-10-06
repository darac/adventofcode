#!/bin/bash

die() {
    printf '%s\n' "$1" >&2
    exit 1
}

# Initialise variables
version=$("${POETRY_HOME:?POETRY_HOME must be set}/bin/poetry" version)
version=${version/aoc /}
year=${version/.*/}
day=${version/*./}

while :; do
    case $1 in
    -y | --year)
        if [ "$2" ]; then
            year="$2"
            shift
        else
            die 'ERROR: "--year" requires a non-empty option argument.'
        fi
        ;;
    -d | --day)
        if [ "$2" ]; then
            day="$2"
            shift
        else
            die 'ERROR: "--day" requires a non-empty option argument.'
        fi
        ;;
    -?*)
        printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
        ;;
    *)
        break
        ;;
    esac

    shift
done

# Now call poetry to run aoc
$POETRY_HOME/bin/poetry run aoc -y $year -d $day
