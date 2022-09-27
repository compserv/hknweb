There have been cases where Anaconda can conflict and mess with the Operating System installed libraries, which can confuse why some things are breaking. Following the instructions to set up the development environment will prevent such a thing.

# Choosing Anaconda or Miniconda
It doesn't matter which one you choose, Anaconda has a lot of packages at once (and is large) while Miniconda allows you to pick and choose (so it's small at first).

We just need Python and its dependencies, so Miniconda will suffice. If you have Anaconda already or prefer Anaconda, that's fine too.

If you have Anaconda already, you can skip to the `Setup` instructions in the README, but feel free to follow the steps below as appropriate to help you avoid Conda and System conflicts.

# Recommended Install Instructions
Get the executables here: https://conda.io/projects/conda/en/latest/user-guide/install/
Follow the `Regular Installation` instructions alongside the below instructions
## Unix (Windows WSL, Linux, MacOS)
1. There are no options given during installation. Follow and complete it all normally.
2. Disable automatic `base` environment activation with `conda config --set auto_activate_base false`. You can activate the base environment if you so choose manually anytime using `conda activate`.
    * If next time you open a terminal and it will show `(base)`. That is the conda base environment. This step disables that from starting (and is recommended).
3. Open a fresh new terminal and type `conda`. If "help" stuff pops up, that means `conda` is ready for you.
## Windows
The official terminal standard chosen for `hknweb` is `Git Bash`, so all instructions follow that. We officially won't write instructions for other terminals.
1. We ask you to keep the default directory for the install (Generally: `C:\Users\<USERNAME>\[miniconda3|Anaconda3]`). If you choose to install it somewhere else, please note where this folder is.
2. We **HIGHLY RECOMMEND** in `Advanced Options` to leave ALL checkboxes **blank** (PATH and default Python). This will keep all things conda inside conda, and won't mix or conflict with your system installs.
3. On the finish install page, unless you want to see the documentation and tutorial offered, uncheck the two boxes and click "Finish"
4. Open the Git Bash terminal
5. Run: `export PATH=$PATH:/c/Users/<USERNAME>/[miniconda3|Anaconda3]/Scripts/`, where you substitute the current Windows user's Username folder in the `Users` folder AND choose whether you installed `miniconda` or `Anaconda`. For example, if you installed miniconda and your username is "oski", it would be something like this: `export PATH=$PATH:/c/Users/oski/miniconda3/Scripts/`
    * If you installed "conda" somewhere else, replace the drive name (like "D:") and lowercase it with a forward slash at the beginning (Example: "/d"). Then add `/Scripts/` at the end of it. For example, if you installed in `D:\Programs\Anaconda3`, you would use `export PATH=$PATH:/d/Programs/Anaconda3/Scripts/`
6. Run `conda init bash`
7. If you ever see `(base)` next time you open Git Bash, that is the conda base environment. Disable future automatic `base` environment activation with `conda config --set auto_activate_base false`. You can activate the base environment if you so choose manually anytime using `conda activate`.
8. Open a fresh new terminal and type `conda`. If "help" stuff pops up, that means `conda` is ready for you.
