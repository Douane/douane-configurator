# douane-configurator

Configurator process for the Douane firewall at application layer

## Douane ?

[Douane](https://github.com/zedtux/Douane) is a firewall at application layer for Linux kernel 2.6.x and 3.x version. This application allow you to filter the out going network traffic.

## Screenshot

![douane configurator](https://pbs.twimg.com/media/BQCUQp7CEAE7wXi.png:large)

## Dependencies

To make it works, you must install python version 3 and the following packages:

    sudo apt-get install python3-gi python3-lxml python3-dbus

## Install

You can install it easily using the following PPA:

    git clone https://github.com/Douane/douane-configurator
    cd douane-configurator
    sudo python setup.py install

## License

This application is under [the LGPL licence](http://www.gnu.org/licenses/lgpl.html).
