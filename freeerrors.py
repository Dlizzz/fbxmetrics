#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Exceptions classes definition

Name: freeerrors.py
Exception classes:
    Error: base class for exceptions
    FreeboxError: communication with freebpox exceptions
"""


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class FreeboxError(Error):
    """Raised when unable to communicate with Freebox

    Attributes:
        message -- reason why we can't communicate
    """

    def __init__(self, message):
        """Constructor with message"""

        self.message = message
