# configuration and launch file for nuitka compilation

# Make executable standalone
# nuitka-project-if: {OS} in ("Windows", "Linux", "Darwin", "FreeBSD"):
#    nuitka-project: --onefile
#    nuitka-project: --onefile-tempdir-spec="{CACHE_DIR}/SideJITServer"
# nuitka-project-else:
#    nuitka-project: --standalone

# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --output-filename=SideJITServer-windows-x86_64.exe
#    nuitka-project: --include-module=jinxed.terminfo.vtwin10
#    nuitka-project: --include-module=jinxed.terminfo.ansicon
#    nuitka-project: --include-module=jinxed.terminfo.xterm
#    nuitka-project: --include-module=jinxed.terminfo.xterm_256color
#    nuitka-project: --user-package-configuration-file=sidejitserver-nuitka-package.config.yml
# nuitka-project-if: {OS} == "Linux":
#    nuitka-project: --output-filename=SideJITServer-linux-x86_64.bin
# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --output-filename=SideJITServer-mac-arm64.bin

# nuitka-project: --include-module=zeroconf._utils.ipaddress
# nuitka-project: --include-module=zeroconf._handlers.answers
# nuitka-project: --include-module=pkg_resources.extern

# nuitka-project: --report=compilation-report.xml

from SideJITServer import start_server

if __name__ == '__main__':
    start_server()
