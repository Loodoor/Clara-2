# coding=utf-8

__author__ = 'Alexandre Plateau'
"""
Licence MIT
Voir le GUIDELINES avant de modifier quoi que ce soit
User et abuser de # todo : note
"""

from . import tts
from . import speech_manager as srm
from . import cst
from . import colors
from . import commands


class Core:
    def __init__(self):
        self.voice_engine = tts.init()
        self.recognizer = srm.SpeechRecognition(self.voice_engine, names=cst.names_alias)
        self.done = False
        self.commands = {
            "ttsmessage": lambda d, d2, a: "Of course Sir",
            "tts": lambda d, d2, a: False,
            "say": lambda d, d2, a: commands.say(d, d2, a, self.recognizer.speak),
            "listen": lambda d, d2, a: commands.listen(d, d2, a, self.recognizer.listen),
            "cls": commands.cls,
            "backup": commands.backup,
            "loadbackup": commands.load,
            "help": commands.help,
            "search": commands.search,
            "disabletts": commands.disable_tts,
            "enabletts": commands.enable_tts,
            "identity": commands.identity,
            "ls": commands.ls,
            "rewrite": commands.rewrite,
            "modules": commands.modules,
            "del": commands.del_
        }
        self.commands["ttsmessage"].__doc__ = "Message to say when an action is performed using the voice engine\n"
        self.commands["tts"].__doc__ = "Indicate if the text-to-speech is enable or not\n"
        self.commands["say"].__doc__ = commands.say.__doc__
        self.commands["listen"].__doc__ = commands.listen.__doc__
        self.user_commands = {}

    def run_voice(self):
        inputusr = self.recognizer.you_talk_to_me()
        if inputusr and inputusr != -1:
            colors.clprint(inputusr)
            self.voice_engine.say(self.commands["ttsmessage"](self.commands, self.user_commands, []))
            self.voice_engine.runAndWait()
            self.act(inputusr, [])

    def run(self):
        commands.modules()

        while not self.done:
            cmd, *args = colors.clinput().split(" ")
            args = [cst.type_converting(arg) for arg in args]
            self.act(cmd, args)
            if self.commands["tts"](self.commands, self.user_commands, args):
                self.run_voice()

    def act(self, command, args):
        if command.strip():
            if command not in self.user_commands.keys() and command not in self.commands.keys():
                commands.add(self.user_commands, command, args)
            elif command in self.user_commands.keys():
                code = self.user_commands[command]
                kwargs = dict(zip(
                    cst.remove_same([kw[1:-1] for kw in code.replace(' ', '')
                        .replace('{', ' {')
                        .replace('}', '} ')
                        .split(' ')
                        if '{' in kw and '}' in kw]),
                    args if args else [None] * 99
                ))
                # noinspection PyBroadException
                try:
                    ret = exec(code.format(**kwargs), globals(), locals())
                    if ret:
                        colors.clprint(ret)
                except Exception as e:
                    colors.clprint("Impossible to execute command", error=True)
                    colors.clprint("Exception was : '%s: %s'" % (type(e).__name__, e), error=True)
            elif command in self.commands:
                ret = self.commands[command](self.commands, self.user_commands, args)
                if ret:
                    colors.clprint(ret)