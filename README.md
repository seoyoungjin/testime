# TestIME

I found out that there is an incomprehensible problem
when I input Korean to SDL2 with Ibus on Linux.
It would not be easy to analyze either side,
so I decided to simply recreate that bug with python.

![TestIME](screenshot/TestIME_20200815.png TestIME)

## Todo

- [x] gui log
- [ ] view text and preedit text in different color
- [ ] backspace handling
- [ ] finish keysym adn keycode
- [ ] fcitx
- [ ] cursor positon
- [ ] batch test set
- [ ] other language and IME(?)

## System and tools version

- ubuntu 20.04
- ibus 1.5.22
- python 3.8.2
- pip3 install pyside2

## IBus

IBus have the following conventions:

- Input method engine (IME): Actual input method.
- Configuration: Handles the configuration for IBus and other services such as IME.
- Panel: User interface such as language bar and candidate selection table.

IBus is almost standard input protocol, so I thought it would be well managed,
but there's no protocol description.
Furthermore python source code in github was also old version, so it dosen't work.

- It's hard to understand for me because IBus highly depends on GLib/Gnome. 
- it hides the dbus protocol.

After a few attempts I give up making a protype with IBus and I decided to make
it with direct DBus protocol. TT

# DBus library and python bindings

There are many dbus implementations and python bindings.

- libdbus
- GDBus
- QtDBus
- sd-dbus

- dbus-python
- pydbus
- pysdbus
- QtDBus with PyQt5 / PySide2

After triral and error, I selected dbus-python and PySide2.

## DConf

I want to know current cnnfiguration of IBus hangul.
But it seems to store setting data to DConf inseat of DBus property.

```
dconf list /org/freedesktop/ibus/engine/hangul/
auto-reorder
hangul-keyboard
hanja-keys
initial-input-mode
switch-keys
word-commit
```
## Directories

- ibus/     sample in ibus. currently not working
- pyside2/  pyside2 dbus communication sample

## Reference

- https://lispholic.tistory.com/38
- http://0pointer.net/blog/the-new-sd-bus-api-of-systemd.html
