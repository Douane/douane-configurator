# douane-configurator

Configurator process for the Douane firewall at application layer

## Douane ?

[Douane](https://github.com/zedtux/Douane) is a firewall at application layer for Linux kernel 2.6.x and 3.x version. This application allow you to filter the out going network traffic.

## Screenshot

![douane configurator](https://pbs.twimg.com/media/BQCUQp7CEAE7wXi.png:large)

The configurator is using [the GtkTwitterBox](https://github.com/zedtux/gtktwitterbox) widget.

## Dependencies

To make it works, you must install python version 3 and the following packages:

    sudo apt-get install python3-gi python3-lxml python3-dbus

## Install

You can install it easily using the following PPA:

    sudo add-apt-repository ppa:zedtux/douane
    sudo apt-get update
    sudo apt-get install douane-configurator


## License

This application is under [the LGPL licence](http://www.gnu.org/licenses/lgpl.html).
