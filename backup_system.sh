#!/bin/bash

function show_usage {
    echo "usage: $0 -c CONF_FILE | -h"
    exit 1
}

conf_file="/usr/local/etc/backup_wrapper.conf"

while getopts "c:h" option; do
    case $option in
    c)
        conf_file=$OPTARG
        ;;
    h)
        show_usage
        ;;
    \?)
        show_usage
        ;;
        
    esac
done

if [ ! -f "$conf_file" ]; then
    echo "$conf_file does not exist or is not readable"
    exit 1
fi

source $conf_file

current_date_time=$(date +"%Y%m%d_%H%M%S")

backup_file="${backup_dir}/${current_date_time}.cpio"

python=$(which python3)

mkdir -p $backup_dir

find $backup_dir -type f -mtime +${max_versions} -exec rm {} ';'

$python $backup_script -c $backup_conf -e -o $backup_file

exit 0
