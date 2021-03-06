""" Module for definitions
"""
from __future__ import (print_function, absolute_import, division, unicode_literals)

from astropy.table import Table


def instruments():
    """ Dict to convert instrument to bitwise flag
    WARNING: Modifying any of the following is a *bad* idea
      Adding is ok

    Returns
    -------
    instr_dict : Table

    """
    instr_dict = {}
    #
    instr_dict['LRISr'] = 2**0
    instr_dict['LRISb'] = 2**1
    instr_dict['Kastb'] = 2**2
    instr_dict['Kastr'] = 2**3
    instr_dict['DEIMOS'] = 2**4
    instr_dict['NIRSPEC'] = 2**5
    #
    return instr_dict

def lines():
    """ Dict of lines included in this database
    WARNING: Modifying any of the following is a *bad* idea
      Adding is ok

    Returns
    -------
    lamp_dict : dict

    """
    line_dict = {}
    #
    line_dict['ArI'] = 2**0
    line_dict['HgI'] = 2**1
    line_dict['KrI'] = 2**2
    line_dict['NeI'] = 2**3
    line_dict['XeI'] = 2**4
    line_dict['CdI'] = 2**5
    line_dict['ZnI'] = 2**6
    line_dict['HeI'] = 2**7
    line_dict['OH_R24000'] = 2**8
    #
    return line_dict


def str_len():
    """ Hard-codes length of strings in the database
    WARNING: Modifying any of the following is a *bad* idea

    Returns
    -------
    strlen_dict : dict

    """
    strlen_dict = {}
    # Length of ion name
    strlen_dict['ion'] = 6
    # Length of data file name for line source
    strlen_dict['Source'] = 30
    # Return
    return strlen_dict
