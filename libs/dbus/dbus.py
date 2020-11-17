# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.8.4", "1.10.4", "1.11.4", "1.11.8", "1.11.14", "1.12.12"]:
            self.targets[ver] = f"http://dbus.freedesktop.org/releases/dbus/dbus-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"dbus-{ver}"
            self.targetConfigurePath[ver] = "cmake"

        self.svnTargets["master"] = "git://anongit.freedesktop.org/git/dbus/dbus"
        self.targetSrcSuffix["master"] = "git"
        self.targetConfigurePath["master"] = "cmake"

        self.patchToApply["1.8.4"] = [("dont_include_afxres.diff", 1)]
        self.patchToApply["1.10.4"] = [("dont_include_afxres.diff", 1)]
        self.patchToApply["1.11.4"] = [("dbus-1.11.4-20160903.diff", 1)]
        self.patchToApply["1.11.14"] = [("dbus-1.11.4-20160903.diff", 1),
                                        ("dbus-fix_data_dir.diff", 1)]
        self.patchToApply["1.12.12"] = [("dbus-1.11.4-20160903.diff", 1),
                                        ("dbus-fix_data_dir.diff", 1)]
        self.patchLevel["1.11.14"] = 2

        self.targetDigests["1.10.4"] = "ec1921a09199c81ea20b20448237146a414d51ae"
        self.targetDigests["1.11.4"] = (["474de2afde8087adbd26b3fc5cbf6ec45559763c75b21981169a9a1fbac256c9"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.11.8'] = (['fa207530d694706e33378c87e65b2b4304eb99fff71fc6d6caa6f70591b9afd5'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.11.14'] = (['55cfc7fdd2cccb2fce1f75d2132ad4801b5ed6699fc2ce79ed993574adf90c80'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.12.12'] =  (['9546f226011a1e5d9d77245fe5549ef25af4694053189d624d0d6ac127ecf5f8'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Freedesktop message bus system (daemon and clients)"
        self.webpage = "http://www.freedesktop.org/wiki/Software/dbus/"
        self.defaultTarget = "1.12.12"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/glib"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = (
            "-DDBUS_BUILD_TESTS=OFF "
            "-DDBUS_ENABLE_XML_DOCS=OFF ")

        if (self.buildType() == "Debug"):
            self.subinfo.options.configure.args += "-DDBUS_ENABLE_VERBOSE_MODE=ON "
        else:
            self.subinfo.options.configure.args += (
                "-DDBUS_ENABLE_VERBOSE_MODE=OFF "
                "-DDBUS_DISABLE_ASSERT=ON ")

        if OsUtils.isWin():
            # kde uses debugger output, so dbus should do too
            self.subinfo.options.configure.args += "-DDBUS_USE_OUTPUT_DEBUG_STRING=ON "
            self.subinfo.options.configure.args += "-DCMAKE_INSTALL_DATADIR:STRING=bin/data "
            self.subinfo.options.configure.args += (
                "-DDBUS_SESSION_BUS_LISTEN_ADDRESS:STRING=autolaunch:scope=*install-path "
                "-DDBUS_SESSION_BUS_CONNECT_ADDRESS:STRING=autolaunch:scope=*install-path "
                "-DDBUS_SYSTEM_BUS_DEFAULT_ADDRESS:STRING=autolaunch:scope=*install-path ")

        if OsUtils.isMac():
            self.subinfo.options.configure.args += "-DDBUS_BUILD_X11:BOOL=OFF "

    def install(self):
        if not CMakePackageBase.install(self): return False
        # TODO: fix
        if self.buildType() == "Debug":
            imagedir = os.path.join(self.installDir(), "lib")
            if CraftCore.compiler.isMSVC():
                if os.path.exists(os.path.join(imagedir, "dbus-1d.lib")):
                    utils.copyFile(os.path.join(imagedir, "dbus-1d.lib"), os.path.join(imagedir, "dbus-1.lib"))
                if not os.path.exists(os.path.join(imagedir, "dbus-1d.lib")):
                    utils.copyFile(os.path.join(imagedir, "dbus-1.lib"), os.path.join(imagedir, "dbus-1d.lib"))
            if CraftCore.compiler.isMinGW():
                if os.path.exists(os.path.join(imagedir, "libdbus-1.dll.a")):
                    utils.copyFile(os.path.join(imagedir, "libdbus-1.dll.a"),
                                   os.path.join(imagedir, "libdbus-1d.dll.a"))

        return True
    
    # This method needs to be revised.  I tried to get it to add the rpath to the library first, so it could then link the bin files with rpath correctly
    # But no matter what I tried, I could not get it to add the rpath to the library in time to set the bin files to link correctly with rpath.
    # Either it ended up adding the rpath to the library and then overwriting the change with files from the archive,
    # or it ended up adding the rpath to the library after it already had linked all the files to the wrong library path.
    # Also note that I only changed the two files we need for the mac version of KStars and the library file.
        
    def postQmerge(self):
        packageName = "libdbus-1.3"
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root,  'lib')
        libDir = os.path.join(self.imageDir(), "lib")
        binDir = os.path.join(self.imageDir(), "bin")
        utils.system("install_name_tool -add_rpath " + craftLibDir + " " + libDir +"/" + packageName + ".dylib")
        utils.system("install_name_tool -id @rpath/" + packageName + ".dylib " + libDir +"/" + packageName + ".dylib")
        
        utils.system("install_name_tool -change " + packageName + ".dylib @rpath/" + packageName + ".dylib " + binDir + "/dbus-daemon")
        utils.system("install_name_tool -change " + packageName + ".dylib @rpath/" + packageName + ".dylib " + binDir + "/dbus-send")
        return True
        
