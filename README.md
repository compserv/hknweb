hknweb
======

Welcome! This is the in-progress redesign for the HKN (Mu Chapter) website, built with Django.

## Prerequisites
These are the software you are **required** to download and install. Unless noted, default settings are OK. Consult with officers on advice for preferences of certain settings.

There are other ways to install the following items. The instructions here will provide the EASIEST and SUFFICIENT way to install them. Ultimately, it is up to you on how to get them and install them if you want to do a more centalized way (i.e. Chocolatey for Windows) or a fancy pants method (i.e. Build from Scratch).

When `Unix` is used, it includes (not limited to) Linux, Windows WSL, and MacOS

* `git` and Terminal
    * Unix systems usually have these out of the box
        * Default terminal usually `zsh` or `bash`
    * [Windows] [git bash](https://git-scm.com/downloads) **ONLY** (due to Makefile syntax)
        * You can use the default options, **with one exception**: Select `Use Windows' default console window` in the **Configuring the terminal emulator** to use with Git Bash step. **Do not use "MinTTY"**.
            * This is very important! If you do not select this option, your terminal won't work with Python!
            * If you already have Git Bash installed before, just redownload and rerun the EXE (no need to uninstall, but you may if you want or need to) and go through all the options (it should keep what you previously selected). On the **Configuring the terminal emulator** page, select `Use Windows' default console window`.
* `make` (GNU Make)
    * Unix systems usually have this out of the box
    * [Windows] Follow [instructions here using Winget](https://www.technewstoday.com/install-and-use-make-in-windows/#using-winget)
        * **CORRECTION**: For **Steps 8 to 10**: Under `User variables` (top half section), click on `Path`, click on `Edit`, click on `New`, and enter `C:\Program Files (x86)\GnuWin32\bin`
        * Article has other options too, but Winget is more out of the box. Next best thing is using Chocolatey which requires install of Chocolatey itself.
* Miniconda (or Anaconda) + Python 3.7.3
    * Our server will also use Miniconda to allow for some flexibility in installing packages without having to wait for OCF to install them for us, like upgrading the Python version. As of Fall 2022, we currently use Python 3.7.3.
    * Install instructions here: [README-CONDA.md](README-CONDA.md)
    * Commands Summary:
        * Initial setup: `conda create -n hknweb python=<VERSION>`, where VERSION is the Python version used by `hknweb`. Use `make conda` instead which does this for you.
        * Activate the conda environment with `conda activate hknweb` (do this every time you start developing on `hknweb`)
        * Deactivate conda environment with `conda deactivate`
        * Disable automatic `base` environment activation with `conda config --set auto_activate_base false`

## Setup

Supported Terminals
* Any Unix Terminals (including Windows WSL) -- usually `zsh` or `bash`
* Windows Git Bash (**ONLY**) -- this is due to the Makefile syntax

Developing on `hknweb` requires a virtual environment so that every developer has the exact same development environment (i.e. Any errors that a developer has is not due to difference in configuration). We will be using Conda Environments to make our virtual environment.

Others exist like Python's built-in [`venv`](https://docs.python.org/3/library/venv.html), but we won't use that here

This command creates our Conda Environment.
```sh
$ make conda
```

Alternatively, this command creates our Conda Environment completely from scratch: `make conda-scratch`

Next, we need to have our current terminal/shell use the Conda Environment we just created.
```sh
$ conda activate hknweb
```

Finally, we need to install all of our dependencies into the Conda Environment (and not the main computer system):
```sh
$ make install
```

In summary, the setup looks like:
```sh
$ cd hknweb                     # enter our main directory
$ make conda                    # create our Conda Environment
$ conda activate hknweb         # enter our Conda Environment
$ make install                  # install our dependencies
$ make migrate                  # apply all database changes
$ make permissions              # initialize our database
$ make dev                      # start local web server
$ conda deactivate              # Exit the Conda Environment
```

You may notice many of our Makefile commands can be ran manually.

We not only use Makefile commands to simplify and abstract away many commonly used development commands (especially setting the dev environment via `HKNWEB_MODE='dev'`), but also to sanity check to make sure we don't accidentally modify your main system (see how we call `python` in the Makefile).

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

Usually, Python code behavior between the Operating Systems is rare.
However, Windows developers have the additional responsbility to make their code Linux-friendly (since our destination OS is Linux on OCF). Therefore, if there is an error on the code on Linux and not Windows, support on Linux takes precedence!
Unix developers should also try to make their code Windows-friendly for the Window developers. [Example with `strftime`](https://github.com/compserv/hknweb/commit/3dc27dfa7556561b7c244de2c431d3c99ee2eb5a)

## FAQ
This is a compilation of past errors and how they were solved.

### Python won't load on Windows Git Bash

Git Bash's Terminal emulator should be `Use Windows' default console window`. Don't use MinTTY. Follow the instructions for reinstalling `Git Bash` in the **Prerequisites** section of this README. 
