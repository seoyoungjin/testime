#!/usr/bin/env python
# vim:set et sts=4 sw=4:
#
# ibus - The Input Bus
#
# Copyright (c) 2011 Peng Huang <shawn.p.huang@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA


from gi import require_version as gi_require_version
gi_require_version('GLib', '2.0')
gi_require_version('GdkX11', '3.0')
gi_require_version('Gio', '2.0')
gi_require_version('Gtk', '3.0')
gi_require_version('IBus', '1.0')

from gi.repository import GLib
from gi.repository import Gio
from gi.repository import IBus

IBus.init()
main = GLib.MainLoop()
bus = IBus.Bus()
ic = bus.create_input_context("ibus-test")
ic.get_engine()
ic.get_engine()
ic.get_engine()

e = ic.get_engine()
print( ic.get_engine() )
print(e.get_name(), e.get_description(), e.get_language())
