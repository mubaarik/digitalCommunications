#!/usr/bin/python

'''User-defined exceptions for Audiocom.'''

class PreambleDetectionError(Exception):
    '''Raised when the preamble of a transmission cannot be detected.'''

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
