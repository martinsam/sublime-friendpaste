# -*- coding: utf-8 -*-

import os
import sublime
import sublime_plugin
from httplib import HTTPConnection
import json

FRIENDPASTE_URL = "friendpaste.com"

SYNTAXES = {
'ActionScript.tmLanguage': 'as',
'AppleScript.tmLanguage': 'applescript',
'ASP.tmLanguage': 'asp',
'Bibtex.tmLanguage': 'bibtex',
'C.tmLanguage': 'c',
'C#.tmLanguage': 'csharp',
'C++.tmLanguage': 'cpp',
'Clojure.tmLanguage': 'clojure',
'CoffeeScript.tmLanguage': 'coffeescript',
'CSS.tmLanguage': 'css',
'D.tmLanguage': 'd',
'Diff.tmLanguage': 'diff',
'DOT.tmLanguage': 'dot',
'Erlang.tmLanguage': 'erlang',
'Go.tmLanguage': 'go',
'Groovy.tmLanguage': 'groovy',
'Haskell.tmLanguage': 'haskell',
'HTML.tmLanguage': 'html5',
'Java.tmLanguage': 'java',
'JavaScript.tmLanguage': 'javascript',
'JSON.tmLanguage': 'javascript',
'JSON Generic Array Elements.tmLanguage': 'javascript',
'LaTeX.tmLanguage': 'latex',
'LaTeX Beamer.tmLanguage': 'latex',
'LaTeX Memoir.tmLanguage': 'latex',
'Lisp.tmLanguage': 'lisp',
'Literate Haskell.tmLanguage': 'haskell',
'Lua.tmLanguage': 'lua',
'Makefile.tmLanguage': 'make',
'Matlab.tmLanguage': 'matlab',
'Objective-C.tmLanguage': 'objc',
'Objective-C++.tmLanguage': 'objc',
'OCaml.tmLanguage': 'ocaml',
'OCamllex.tmLanguage': 'ocaml',
'OCamlyacc.tmLanguage': 'ocaml',
'Perl.tmLanguage': 'perl',
'PHP.tmLanguage': 'php',
'Plain text.tmLanguage': 'text',
'Python.tmLanguage': 'python',
'R.tmLanguage': 'rsplus',
'R Console.tmLanguage': 'rsplus',
'Regular Expressions (Python).tmLanguage': 'python',
'Ruby.tmLanguage': 'ruby',
'Ruby Haml.tmLanguage': 'ruby',
'Ruby on Rails.tmLanguage': 'rails',
'Scala.tmLanguage': 'scala',
'SCSS.tmLanguage': 'css',
'Shell-Unix-Generic.tmLanguage': 'bash',
'SQL.tmLanguage': 'sql',
'SQL (Rails).tmLanguage': 'sql',
'Tcl.tmLanguage': 'tcl',
'TeX.tmLanguage': 'latex',
'TeX Math.tmLanguage': 'latex',
'Textile.tmLanguage': 'latex',
'XML.tmLanguage': 'xml',
'YAML.tmLanguage': 'yaml'
}


class PasteToFriendpastePrompt(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Paste Name:", "", self.on_done, None, None)
        # self.window.show_input_panel("Paste Password:", "", self.on_done, None, None)

    def on_done(self, paste_name):
        if self.window.active_view():
            self.window.active_view().run_command("paste_to_friendpaste", {"paste_name": paste_name})


class PasteToFriendpaste(sublime_plugin.TextCommand):
    def run(self, view, paste_name=None):
        pass
        if paste_name is None:
            paste_name = self.view.file_name()
        if paste_name is not None:
            paste_name = os.path.basename(paste_name)   # Extract base name
        else:
            paste_name = "Untitled"

        for region in self.view.sel():

            syntax = SYNTAXES.get(self.view.settings().get('syntax').split('/')[-1], 'text')
            text = self.view.substr(region).encode('utf8')

            if not text:
                sublime.status_message('Error sending to %s: Nothing selected' % FRIENDPASTE_URL)
            else:
                data = json.dumps({
                    'title': paste_name,
                    'snippet': text,
                    'language': syntax
                })

                http = HTTPConnection(FRIENDPASTE_URL)
                http.request("POST", data, headers={"Content-Type": "application/json", "Accept": "application/json", "Connection": "close"})
                resp = http.getresponse()
                try:
                    ret = json.loads(resp.read())
                    sublime.set_clipboard(ret['url'])
                    sublime.status_message('PasteBin URL copied to clipboard: ' + ret['url'])
                except ValueError:
                    sublime.status_message("Sorry Friendpaste is down")
                http.close()