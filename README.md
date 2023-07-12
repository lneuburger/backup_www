# Backup Existing Files/Directories on DO Hosted Web Server

## Components
- Wrapper script
    + backup.sh
    + invokes primary Python3 utility
- Configuration files
    + example.conf (rename to /usr/local/etc/backup/backup.conf in prod)
    + Sample configuration
- Python3 backup utility
    + Primary backup utility
    + Builds list of files to process
    + Creates cpio archive of files/directories
    + Compresses resultant cpio files with gzip

## Usage
- Copy repo contents to remote server
    + backup.sh to /usr/local/bin
    + backup_www.py to /usr/local/bin
    + example.conf to /usr/local/etc/backup/backup.conf
        * Modify the content of backup.conf to suit needs
    + Create directory /var/lib/backup on remote server
    + Copy the example Cron job to remote server
        * /etc/cron.d/backup
        * Replace MAILTO with a valid email

### Example Cron Job
```
MAILTO=<someuser@example.com>

45 23 * * * root /usr/local/bin/backup.sh
```