import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Blogilo"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None

        self.runtimeDependencies["kde/pim/kblog"] = None
        self.runtimeDependencies["kde/pim/pimcommon"] = None
        self.runtimeDependencies["kde/pim/kpimtextedit"] = None
        self.runtimeDependencies["kde/pim/messagelib"] = None
        self.runtimeDependencies["kde/pim/kimap"] = None
        self.runtimeDependencies["kde/pim/libkgapi"] = None
        self.runtimeDependencies["libs/qt5/qtwebengine"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
