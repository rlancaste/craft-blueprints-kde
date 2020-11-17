import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['1.900.1-2'] = 'http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-1.900.1.zip'
        self.targetInstSrc['1.900.1-2'] = os.path.join('jasper-1.900.1', 'src', 'libjasper')
        self.patchToApply['1.900.1-2'] = ("jasper-1.900.1-20130523.diff", 3)
        self.description = "A library to manipulate JPEG-2000 images"
        self.defaultTarget = '1.900.1-2'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root,  'lib')
        self.subinfo.options.configure.args = "-DCMAKE_INSTALL_PREFIX=" + root + " -DCMAKE_BUILD_TYPE=Debug -DCMAKE_MACOSX_RPATH=1 -DCMAKE_INSTALL_RPATH=" + craftLibDir
