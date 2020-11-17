# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.1.5']:
            self.targets[ver] = 'https://downloads.sourceforge.net/project/libusb/libusb-compat-0.1/libusb-compat-' + ver + '/libusb-compat-'+ ver + '.tar.bz2'
            self.archiveNames[ver] = "libusb-compat-%s.tar.bz2" % ver
            self.targetInstSrc[ver] = 'libusb-compat-' + ver
        self.description = 'Library for USB device access'
        self.defaultTarget = '0.1.5'

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/libusb"] = "default"

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
       	#self.subinfo.options.configure.bootstrap = True
       	self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += " --disable-dependency-tracking" \
        " --prefix=" + prefix







