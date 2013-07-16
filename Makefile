# From http://ghantoos.org/2008/10/19/creating-a-deb-package-from-a-python-setuppy/

PYTHON=`which python3`
DESTDIR=/
BUILDIR=$(CURDIR)/debian/douane-configurator
PROJECT=douane-configurator
VERSION=$(shell $(PYTHON) setup.py --version)

all:
	@echo "make source - Create source package"
	@echo "make install - Install on local system"
	@echo "make buildrpm - Generate a rpm package"
	@echo "make builddeb - Generate a deb package"
	@echo "make clean - Get rid of scratch and byte files"

source:
	$(PYTHON) setup.py sdist $(COMPILE)

install:
	@sed -i 's/self\.set_version(\"UNKNOWN\")/self\.set_version\(\"$(VERSION)\")/' ./douane/gui/aboutdialog.py
	$(PYTHON) setup.py install --prefix=/usr --root $(DESTDIR) $(COMPILE)
	@sed -i 's/self\.set_version(\".*\")/self\.set_version\(\"UNKNOWN\")/' ./douane/gui/aboutdialog.py

buildrpm:
	$(PYTHON) setup.py bdist_rpm --post-install=rpm/postinstall --pre-uninstall=rpm/preuninstall

builddeb:
	# build the source package in the parent directory
	# then rename it to project_version.orig.tar.gz
	$(PYTHON) setup.py sdist $(COMPILE) --dist-dir=../ --prune
	rename -f 's/$(PROJECT)-(.*)\.tar\.gz/$(PROJECT)_$$1\.orig\.tar\.gz/' ../*
	# build the package
	dpkg-buildpackage -i -I -rfakeroot

clean:
	$(PYTHON) setup.py clean
	# $(MAKE) -f $(CURDIR)/debian/rules clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete
