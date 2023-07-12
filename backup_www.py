#!/usr/bin/python3

""" Backup critical data and system files """

# pylint: disable=unspecified-encoding


import argparse
import configparser
import logging
import logging.handlers
import os
import re
import subprocess
import sys


def compress_file(file_name):
    """Compress a file using gzip."""

    cmd = ["gzip", "-9", file_name]

    with subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as proc:
        _, _ = proc.communicate()


def create_arg_parser():
    """Creates command line argument parser."""

    parser = argparse.ArgumentParser(usage="%(prog)s [options]")

    parser.add_argument(
        "-c", "--config", metavar="/path/to/config", help="path to config file"
    )

    parser.add_argument(
        "-e", "--err", action="store_true", help="enable display of errors"
    )

    parser.add_argument(
        "--outfile",
        "-o",
        metavar="/path/to/outfile",
        help="path to output cpio archive file",
    )

    return parser


def clean_file_list(files, patterns):
    """Delete entries from a list based on regular expression."""

    contents = []

    for content in files:
        add_file = True
        for pattern in patterns:
            match = pattern.search(content)
            if match:
                add_file = False
                continue
        if add_file:
            contents.append(content)

    return sorted(contents)


def create_cpio_file(files, outfile_name):
    """Creates a cpio archive."""

    files = list(files)

    # Strips off leading / so we do not have absolute paths in the archive.
    for index, line in enumerate(files):
        files[index] = line.lstrip("/")

    os.chdir("/")

    cmd = ["cpio", "-o"]

    with open(outfile_name, "w") as output_fh:
        with subprocess.Popen(
            cmd,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stdout=output_fh,
        ) as proc:
            _, error = proc.communicate("\n".join(files).encode())
            error = error.decode()
    return error.split("\n")


def create_logger(log_level="warning"):
    """Creates logging object"""

    log_levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
    }

    log_level = log_levels[log_level]

    handler = logging.handlers.SysLogHandler(address="/dev/log")

    formatter = logging.Formatter("%(filename)s[%(process)d]: %(message)s")

    handler.setFormatter(formatter)

    my_logger = logging.getLogger("MyLogger")

    # my_logger.setLevel(logging.DEBUG)

    my_logger.setLevel(log_level)

    my_logger.addHandler(handler)

    return my_logger


def get_dir_list(dir_name):
    """Gets a listing of files and directories in dir_name"""

    dir_contents = []

    cmd = ["find", dir_name]

    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        stdout = proc.communicate()[0]
        dir_contents = stdout.decode().split("\n")

    return dir_contents


def main():
    """Main logic"""

    my_logger = create_logger("info")

    parser = create_arg_parser()
    args = parser.parse_args()

    if not args.outfile:
        parser.print_help()
        sys.exit(1)

    if not args.config:
        parser.print_help()
        sys.exit(1)

    conf = configparser.ConfigParser()

    conf.read(args.config)

    ignore_re = [re.compile(x) for x in conf["ignore"].values()]

    dir_contents = []

    try:
        for dir_entry in list(conf["dirs"].values()):
            dir_contents.extend(get_dir_list(dir_entry))

        dir_contents = clean_file_list(files=dir_contents, patterns=ignore_re)

        errors = create_cpio_file(
            files=dir_contents, outfile_name=args.outfile
        )

        if args.err:
            my_logger.info(
                "error output during execution: %s", "\n".join(errors)
            )

        compress_file(args.outfile)
    except OSError as ex:
        my_logger.info("error creating backup: %s", ex)

    sys.exit(0)


if __name__ == "__main__":
    main()
