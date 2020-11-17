# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.runtimeDependencies["dev-utils/perl"] = None
        self.runtimeDependencies["libs/expat"] = None

    def setTargets(self):
        for ver in ["2.44"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/T/TO/TODDR/XML-Parser-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"XML-Parser-{ver}"
        self.targetDigests["2.44"] = (['1ae9d07ee9c35326b3d9aad56eae71a6730a73a116b9fe9e8a4758b7cc033216'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["2.44"] = 1

        self.tags = 'XML::Parser'
        self.defaultTarget = '2.44'


class Package(PerlPackageBase):
    def __init__(self, **args):
        PerlPackageBase.__init__(self)
        root = str(CraftCore.standardDirs.craftRoot())
        self.subinfo.options.configure.args += f"EXPATINCPATH=\"{os.path.join(root, 'include')}\" EXPATLIBPATH=\"{os.path.join(root, 'lib')}\""
