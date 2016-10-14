# coding=utf-8

__author__ = 'Alexandre Plateau'
"""
Licence MIT
Voir le GUIDELINES avant de modifier quoi que ce soit
User et abuser de # todo : note
"""

from . import Colorama
from . import cst

import os


def clprint(texte, error=False):
    if error:
        print('%s%s%s' % (Colorama.Fore.RED, texte, Colorama.Fore.WHITE))
    else:
        print('%s%s%s' % (Colorama.Fore.YELLOW, texte, Colorama.Fore.WHITE))


def clinput(question=""):
    return input("%s%s: %s%s " % (Colorama.Fore.CYAN, cst.in_, question, Colorama.Fore.WHITE))