# Compilation notes for standalone no-python executable

Compilation happens using a package called nuitka, which transpiles everything to C and then uses the appropriate C compiler to build an executable. It is handled in three files in this repo:

1. `./sidejitserver-nuitka-package.config.yml` for platform-specific (Windows) dylib linking
2. `./SideJITServer/launch.py` which is a duplicate of `main.py`, but using a package import and including necessary nuitka compilation flags including critical hidden imports
3. `./.github/workflows/compile.yml` which lists compilation instructions on release or manual trigger.

Compilation lasts between 25-50 minutes depending on platform from an empty cache, on the free tier GitHub Actions runners. Recompilation with an existing cache usually takes 7-15 minutes.

When making a release, wait for the compilation to finish, and then download + attach the executables to the release after the jobs are finished.

If you want to compile it yourself on your own machine, study the launch.py file and the github workflow to understand how to do it, and change any configs as necessary to fit your machine architecture.

Note: currently pinned to python 3.11 and nuitka 2.2.3 since nuitka 2.3 does not work on Mac.
