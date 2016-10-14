# coding=utf-8

__author__ = 'Alexandre Plateau'
"""
Licence MIT
Voir le GUIDELINES avant de modifier quoi que ce soit
User et abuser de # todo : note
"""

import os
import pickle
import webbrowser
import re
import subprocess
import socket
import platform as p
import glob
import sys

from . import colors
from . import cst


def add(dct2, command, args):
    colors.clprint("Code for '%s' :" % command)
    if not args:
        code = []
        line = colors.clinput()
        while line.strip():
            code.append(line)
            line = colors.clinput()
        code = '\n'.join(code)
    else:
        code = ' '.join(args)

    dct2[command] = code
    colors.clprint("End of statement, '%s' was succesfully added" % command)


def ls(_, d, args):
    """
    List all the files in a directory
    Option 'r' will search recursively
    If 'r' option is given, you can add a number to choose the deep of the recursive search
    """
    if not args:
        dname = colors.clinput("Path to directory ? ")
    else:
        dname = args[0]
    if "r" in args:
        recursive = True
        n_in = False
        for a in args:
            try:
                j = int(a)
                deep = j
                n_in = True
                break
            except ValueError:
                pass
        if not n_in:
            deep = 1
    else:
        recursive = False
        deep = 0

    def _ls(directory, recur, i=0):
        nonlocal deep
        for fname in glob.glob(directory + "/*.*") + glob.glob(directory + "/*"):
            e = "⎹ " if os.path.isfile(fname) else "⎿ "
            colors.clprint("⎹ " * i + e + os.path.basename(fname))
            if os.path.isdir(fname) and recursive and i + 1 <= deep:
                _ls(fname, recur, i + 1)

    _ls(dname, recursive)


def identity(*_):
    """
    Print informations about the user
    Take no arguments
    """
    result = subprocess.Popen(['ipconfig', '/all'], stdout=subprocess.PIPE).stdout.read()
    adresse_mac = re.search('([0-9A-F]{2}-?){6}', str(result)).group()
    adresse_mac = adresse_mac.split('-')
    adresse_mac = ':'.join(adresse_mac)
    systeme = p.system()
    jeu, format_fichier = p.architecture()
    distribution = p.version()
    hote = socket.gethostbyname(socket.gethostname())
    to_test = [
        ("Username", os.getenv('USERNAME')),
        ("Operating System", systeme),
        ("Version", distribution),
        ("Local IP Address", hote),
        ("MAC Address", adresse_mac),
        ("Architecture", jeu),
        ("File Format", format_fichier)
    ]
    for k in to_test:
        colors.clprint(k[0] + " : " + k[1])


def cls(*_):
    """
    Clear the screen
    Take no arguments
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def modules(*_):
    """
    Print all the modules names which are imported
    Take no arguments
    """
    modulenames = set(sys.modules) & set(globals())
    for i in modulenames:
        print("- " + str(i) + " a été initialisé")
    print("\n")


def del_(_, dct2, args):
    """
    Delete commands determined following the arguments
    (if no arguments are given, a prompt will appear)
    """
    if not args:
        cmd = colors.clinput("Commands to delete ?").split(' ')
    else:
        cmd = args.split(' ')
    for c in cmd:
        if c in dct2.keys():
            del dct2[c]
        else:
            colors.clprint("The required command '%s' does not exist" % c, error=True)


def backup(_, dct2, args):
    """
    Save the currents commands to a specified file
    The file is named following the first argument (if no arguments are given, a prompt will appear)
    If the argument is 'available', it will list all the backup available
    If the argument is 'del', it will delete all the backups using the names given in arguments
        (if it's the only argument, a prompt will appear)
    """
    if not args:
        fname = colors.clinput("Name of the backup ?")
    else:
        if args[0] == 'available':
            for i, f in enumerate(glob.glob(cst.qsd("backups", "*"))):
                colors.clprint("[%i] %s" % (i, f))
            return
        if args[0] == "del":
            if args[1:]:
                for f in args[1:]:
                    if cst.aze(cst.qsd("backups"), f):
                        os.remove(cst.qsd("backups", f))
                    else:
                        colors.clprint("The required backup '%s' does not exist" % f, error=True)
            else:
                fs = colors.clinput("Backups to remove ?").split(' ')
            return
        fname = os.path.join(*args)
    if not os.path.exists(cst.qsd("backups")):
        os.mkdir(cst.qsd("backups"))
        colors.clprint("Creating backup directory")
    with open(cst.qsd("backups", fname), "wb") as bck:
        pickle.Pickler(bck).dump(dct2)
    colors.clprint("Backup of '%s' done" % fname)


def load(_, dct2, args):
    """
    Load a backup from memory
    The backup is determined following the arguments joined using the default os.sep
    (if no arguments are given, a prompt will appear)
    """
    if not args:
        fname = colors.clinput("Name of the backup ?")
    else:
        fname = os.path.join(*args)
    if not os.path.exists(cst.qsd("backups", fname)):
        colors.clprint("The required backup '%s' does not exist !" % fname, error=True)
    else:
        with open(cst.qsd("backups", fname), "rb") as bck:
            try:
                dct2.update(pickle.Unpickler(bck).load())
            except EOFError:
                colors.clprint("Backup '%s' is empty" % fname, error=True)
            else:
                colors.clprint("Backup '%s' succesfully loaded" % fname)


def say(_, d, args, speaker):
    """
    Make the voice engine saying a text
    The text is determined following the arguments joined by a single space
    (if not arguments are given, a prompt will appear)
    """
    if not args:
        text = colors.clinput("Text to say ?")
    else:
        text = ' '.join(args)
    speaker(text)


def listen(_, d, a, veng):
    """
    The voice engine will listen to you and print what it heard
    Take no arguments
    """
    ret = veng()
    if ret != -1:
        colors.clprint(ret)
    else:
        colors.clprint("Unable to recognize", error=True)


def search(_, d, args):
    """
    Search on Google
    The query is determined following the argumentw joined by a single space
    (if no arguments are given, a prompt will appear)
    """
    if not args:
        s = colors.clinput("Search ?")
    else:
        s = '+'.join(args)
    webbrowser.open("https://google.fr/search?q=" + s)


def disable_tts(dct, *_):
    """
    Turn off automatic voice recognition after each user input
    Take no arguments
    """
    dct["tts"] = lambda d, d2, a: False


def enable_tts(dct, *_):
    """
    Turn on automatic voice recognition after each user input
    Take no arguments
    """
    dct["tts"] = lambda d, d2, a: True


def rewrite(_, dct2, args):
    """
    Allow to rewrite a user-defined command
    The command to rewrite is determined following the first argument
    (if no arguments are given, a prompt will appear)
    Then you will be ask to type in the new code for the command
    """
    if not args:
        cmd = colors.clinput("Command to rewrite ?")
    else:
        cmd = args[0]

    if cmd not in dct2.keys():
        colors.clprint("The required command '%s' does not exist" % cmd, error=True)
    else:
        add(dct2, cmd, args[1:])


def help(dct, dct2, args):
    """
    List all the commands and display their description
    If arguments are given, only display the description of the commands given in arguments (if they exist as commands)
    """
    def _list(temp):
        for k, v in temp.items():
            if v.__doc__ is not None and not isinstance(v, (int, float, str, list, tuple)):
                colors.clprint("- " + str(k) + " : " + str(v.__doc__))
            else:
                colors.clprint("- " + str(k))

    if not args:
        _list(dct)
        _list(dct2)
    else:
        tmp = {k: v for k, v in dct.items() if k in args}
        tmp2 = {k: v for k, v in dct2.items() if k in args}
        _list(tmp)
        _list(tmp2)