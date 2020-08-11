# TestIME

I found out that there is an incomprehensible problem
when I input Korean to SDL2 with Ibus on Linux.
I felt that it would not be easy to analyze either side,
so I decided to simply recreate the bug with python.

## IBus

IBus have the following conventions:

- Input method engine (IME): Actual input method.
- Configuration: Handles the configuration for IBus and other services such as IME.
- Panel: User interface such as language bar and candidate selection table.

IBus is almost standard input protocol, so I thought it would be well managed,
but there's no protocol description.
Furthermore python source code in github was also an old version, so it dosen't work.

- It's hard to understand for me because IBus highly depends on GLib/Gnome. 
- it hides the dbus protocol.

After a few attempts I give up making a protype with IBus and I decided to make
it with DBus protocol. TT

# DBus

There are many dbus implementations and python bindings.

- libdubs
- GDBus
- QtDBus
- sd-dbus

- python-dbus (old?)
- pydbus
- pysdbus
- QtDBus with PyQt5

## DConf

```
dconf list /org/freedesktop/ibus/engine/hangul/
auto-reorder
hangul-keyboard
hanja-keys
initial-input-mode
switch-keys
word-commit
```
