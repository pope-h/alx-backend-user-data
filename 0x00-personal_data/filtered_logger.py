#!/usr/bin/env python3
""" Personal data """

import os
import re


def filter_datum(fields: str, redaction: str,
                 message: str, separator: str) -> str:
    """ Replacing """
    for f in fields:
        message = re.sub(rf"{f}=(.*?)\{separator}",
                         f"{f}={redaction}{separator}", message)
    return message
