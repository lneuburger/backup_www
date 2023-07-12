#!/bin/bash

current_date_time=$(date +"%Y%m%d_%H%M%S")

backup_conf=/usr/local/etc/backup/backup.conf

backup_dir=/var/lib/backup

backup_file="${backup_dir}/${current_date_time}.cpio"

backup_script=/usr/local/bin/backup_www.py

python=/usr/bin/python3

max_versions=3

mkdir -p $backup_dir

find $backup_dir -type f -mtime +${max_versions} -exec rm {} ';'

$python $backup_script -c $backup_conf -e -o $backup_file

exit 0
