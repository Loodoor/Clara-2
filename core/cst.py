# coding=utf-8

__author__ = 'Alexandre Plateau'
"""
Licence MIT
Voir le GUIDELINES avant de modifier quoi que ce soit
User et abuser de # todo : note
"""

import os


ascii_name = "\n".join([
    "  ____   _", " / ___| | |  __ _  _ __  __ _", "| |     | | / _` || '__// _` |",
    "| |___  | || (_| || |  | (_| |", " \____| |_| \__,_||_|   \__,_|"
])
name = "Clara"
names_alias = ["Clara", "Lava", "Nova"]
version = "2.1"

in_, out_ = ">> ", "<< "


def type_converting(string):
    try:
        if string[0] not in ('"', "'") and string[-1] not in ('"', "'"):
            try:
                return eval(string)
            except SyntaxError:
                pass
        return string
    except NameError:
        return string


def remove_same(content):
    datas = []
    for e in content:
        if e not in datas:
            datas.append(e)
    return datas


def qsd(*files):
    return os.path.join(os.getcwd(), *files)


def aze(*files):
    return os.path.exists(os.path.join(*files))