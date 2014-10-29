from distutils.core import setup

setup(
    name = "douane-configurator",
    packages = ["douane"],
    package_data = {"douane" : ["gui/*.py", "data/douane.png", "data/glade/*.glade"]},
    scripts = ["douane-configurator"],
    version = "0.1.9",
    description = "The configuration tool for the Douane firewall.",
    author = "Guillaume Hain",
    author_email = "zedtux@zedroot.org",
    url = "https://github.com/zedtux/douane-configurator",
    download_url = "https://github.com/zedtux/douane-configurator",
    keywords = ["gtk", "firewall"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Desktop Environment :: Gnome",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = "The configuration tool for the Douane firewall"
)
