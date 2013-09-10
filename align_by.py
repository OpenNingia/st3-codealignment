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

class AlignByCommand(sublime_plugin.WindowCommand):
    def run(self):
        w          = self.window
        w.show_quick_panel(
            [
                [" = ", "align by equal sign blabla"],
                [",", "align by comma"],
                [":", "align by colon"],
                [";", "align by semicolon"]
            ],
            self.on_done)

        self.seps  = ['=', ',', ':', ';']
        self.sep  = '='

    def on_done(self, param):
        if param >= 0 and param < len(self.seps):
            self.sep = self.seps[param]
        self.align_by(self.sep)

    def align_by(self, sep):
        self.window.active_view().run_command("align_by_separator", {'sep': sep})

class AlignBySeparatorCommand(sublime_plugin.TextCommand):
    def run(self, edit, sep = '='):
        self.sep = sep
        for sel in self.view.sel():
            self.align_by(edit, sel)

    def align_by(self, edit, reg):
        text = self.view.substr(reg)

        # calculate
        max_be = 0
        tuples = []
        for l in text.split('\n'):
            if self.sep not in l:
                tuples.append( (l,) )
            else:
                before_equal, the_sep, after_equal = [x.rstrip() for x in l.partition(self.sep)]
                if len(before_equal) > max_be:
                    max_be = len(before_equal)
                tuples.append( (before_equal, after_equal.lstrip()) )

        # apply
        out = []
        for t in tuples:
            out_fmt = '{{0:{ll}}} {sep} {{1}}'.format(ll=max_be, sep=self.sep)
            if len(t) == 1:
                out.append(t[0])
            else:
                out.append(out_fmt.format(t[0], t[1]))
        self.view.replace(edit, reg, '\n'.join(out))

