hknweb
======

Welcome! This is the in-progress redesign for the HKN (Mu Chapter) website, built with Django.

## Prerequisites
These are the software you are **required** to download and install. Unless noted, default settings are OK. Consult with officers on advice for preferences of certain settings.

There are other ways to install the following items. The instructions here will provide the EASIEST and SUFFICIENT way to install them. Ultimately, it is up to you on how to get them and install them if you want to do a more centalized way (i.e. Chocolatey for Windows) or a fancy pants method (i.e. Build from Scratch).

When `Unix` is used, it includes (not limited to) Linux, Windows WSL, and MacOS

* git
    * Unix systems usually have this out of the box
    * [Windows] [git bash](https://git-scm.com/downloads)
* Terminal
    * Unix can use the default terminal (usually `zsh` or `bash`)
    * [Windows] [git bash](https://git-scm.com/downloads) **ONLY** (due to Makefile syntax)
* make (GNU Make)
    * Unix systems usually have this out of the box
    * [Windows] Follow [instructions here using Winget](https://www.technewstoday.com/install-and-use-make-in-windows/#using-winget)
        * **CORRECTION**: For **Step 10**: Under `Variable value`, enter `C:\Program Files (x86)\GnuWin32\bin`
        * Article has other options too, but Winget is more out of the box. Next best thing is using Chocolatey which requires install of Chocolatey itself.
* Python 3.7 (https://www.python.org/)
    * This is the OFFICIAL hknweb Python version, as it matches the OCF Version (As of Fall 2022, currently Python 3.7.3)
    * Major and Minor MUST match, but Patch version we generally don't care
    * NOTE: You can have multiple Python versions installed and set one of them as default
        * You don't need Python 3.7 as system default, but will the default in the Virtual Environment if following [Setup](#setup)
    * **RECOMMENDED VERSION**: [Python 3.7.9](https://www.python.org/downloads/release/python-379/) is latest version with prebuilt binaries for Windows and MacOS

## Setup

Supported Terminals
* Any Unix Terminals (including Windows WSL) -- usually `zsh` or `bash`
* Windows Git Bash (**ONLY**) -- this is due to the Makefile syntax

Developing on `hknweb` requires a virtual environment so that every developer has the exact same development environment (i.e. Any errors that a developer has is not due to difference in configuration). We will be using Python's built-in [`venv`](https://docs.python.org/3/library/venv.html) to make our virtual environment. This command creates our virtual environment.
```sh
$ make venv
```

Next, we need to have our current terminal/shell use the virtual environment we just created.
* For Unix OSes: `source .venv/bin/activate`
* For Windows (Git Bash): `source .venv/Script/activate`

Finally, we need to install all of our dependencies:
```sh
$ make install
```

In summary, the setup looks like:
```sh
$ cd hknweb                     # enter our main directory
$ make venv                     # create our Virtual Environment
$ # enter our virtual environment
$ source .venv/bin/activate     # Unix
$ # OR
$ source .venv/Script/activate  # Windows Git Bash
$ #######
$ make install                  # install our dependencies
$ make migrate                  # apply all database changes
$ make permissions              # initialize our database
$ make dev                      # start local web server
$ deactivate                    # Exit the Virtual Environment
```

## Development

To run the Django development server (which runs a web server locally), run
```sh
$ make dev
```
which will make the web site available at `http://localhost:3000`.

If you would like to access the admin interface in the local web server, run
```sh
$ make createsuperuser
```

You will be prompted for some login info, after which you should be able to access the admin interface with your super user credentials at `http://localhost:3000/admin`.


## FAQ
This is a compilation of past errors and how they were solved.

None so far
