# coding=utf-8

__author__ = 'Alexandre Plateau'
"""
Licence MIT
Voir le GUIDELINES avant de modifier quoi que ce soit
User et abuser de # todo : note
"""

import core

import subprocess
import traceback
import sys
import os
import msvcrt


def post_mortem(exc_type, exc_val, exc_tb):
    os.system('cls') if os.name == 'nt' else os.system('clear')
    os.system("color 9f")
    print(core.constants.ascii_name + "\n")
    message_err = ["Une erreur fatale est survenue.", "", ""]
    for i in message_err:
        print("\t\t" + i)
    print(''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
    print("Appuyez sur une touche pour relancer %s ..." % core.constants.name)
    msvcrt.getch()
    os.system('cls')
    main() or subprocess.Popen(['py', '-3.4', 'main.py'])

sys.excepthook = post_mortem


def main():
    os.system("color 0f")
    print(core.constants.ascii_name + "\n")
    o = core.Core()
    o.run()


if __name__ == '__main__':
    main()