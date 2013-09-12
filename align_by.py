# -*- coding: utf-8 -*-
# Copyright (C) 2011 Daniele Simonetti
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import sublime, sublime_plugin
import sys
is_py2k = sys.version_info < (3, 0)

class AlignmentGroup(object):
    def __init__(self, line_length = 0, separator = '='):
        self.ll     = line_length
        self.sep    = separator
        self.tuples = []

    def append(self, t):
        self.tuples.append(t)

    def align(self):
        out = []
        for t in self.tuples:
            out_fmt = '{{0:{ll}}} {sep} {{1}}'.format(ll=self.ll, sep=self.sep)
            if len(t) == 1:
                out.append(t[0])
            else:
                out.append(out_fmt.format(t[0], t[1]))
        return out

class AlignByCommand(sublime_plugin.WindowCommand):
    def run(self):
        w          = self.window
        w.show_quick_panel(
            [
                ["=", "align by equal sign"],
                [",", "align by comma"],
                [":", "align by colon"],
                [";", "align by semicolon"]
            ],
            self.on_done)

        self.seps = ['=', ',', ':', ';']
        self.sep  = '='

    def on_done(self, param):
        if param >= 0 and param < len(self.seps):
            self.sep = self.seps[param]
        self.align_by(self.sep)

    def align_by(self, sep):
        self.window.active_view().run_command("align_by_separator", {'sep': sep})

class AlignBySeparatorCommand(sublime_plugin.TextCommand):
    def run(self, edit, sep = '='):

        s = sublime.load_settings("st3-codealignment.sublime-settings")
        self.use_groups = s.get("block_alignment", False)
        self.prefix     = s.get("symbols_prefix", "")
        self.suffix     = s.get("symbols_suffix", "")
        #print('block_alignment', self.use_groups, self.view.settings().__dict__, s.__dict__)

        self.sep = sep
        for sel in self.view.sel():
            self.align_by(edit, sel)

    def align_by(self, edit, reg):
        text = self.view.substr(reg)

        # calculate
        group_list = [ AlignmentGroup(separator=self.sep) ]
        group      = group_list[0]

        for l in text.split('\n'):

            # if group alignment is enabled then
            # add a new group when an empty line is found
            if l.strip() == '' and self.use_groups:
                group_list.append(AlignmentGroup(separator=self.sep))
                group = group_list[-1]

            if self.sep not in l:
                group.append( (l,) )
            else:
                before_equal, the_sep, after_equal = [x.rstrip() for x in l.partition(self.sep)]
                # prefix and suffix
                if self._check_prefix(before_equal) or self._check_suffix(after_equal):
                    group.append( (l,) )
                else:
                    if len(before_equal) > group.ll:
                        group.ll = len(before_equal)
                    group.append( (before_equal, after_equal.lstrip()) )

        # apply
        out = []
        for x in group_list:
            out += x.align()

        self.view.replace(edit, reg, '\n'.join(out))

    def _check_prefix(self, text):
        if text is None or len(text) < 1: return False
        return text[-1] in self.prefix

    def _check_suffix(self, text):
        if text is None or len(text) < 1: return False
        return text[0] in self.suffix

def plugin_loaded():
    #global s
    s = sublime.load_settings("st3-codealignment.sublime-settings")
    print('onload', s.get('block_alignment'))

if is_py2k:
    plugin_loaded()

