# -*- coding: utf-8 -*-
import info
import os


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.2']:
           # self.targets[ver] = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?bincats/GSC_' + ver
            self.targets[ver] = 'http://www.indilib.org/jdownloads/kstars/gsc-1.2.tar.gz'
            self.archiveNames[ver] = "gsc-%s.tar.gz" % ver
            #self.targetInstSrc[ver] = 'gsc-' + ver
        self.description = 'The Guide Star Catalog I'
        self.defaultTarget = '1.2'

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"

from Package.MakeFilePackageBase import *

class Package(MakeFilePackageBase):
    def __init__(self, **args):
        MakeFilePackageBase.__init__(self)
        self.subinfo.options.useShadowBuild = False
        
    def configure(self):
        sourcedir = self.sourceDir()
        utils.rmtree(os.path.join(sourcedir, 'bin-dos'))
        return True
    
    def make(self):
        sourcedir = str(self.sourceDir())
        sourcesrc = os.path.join(sourcedir, 'src')
        os.chdir(sourcesrc)
        utils.system(" ".join([self.makeProgram, self.makeOptions(self.subinfo.options.make.args)]))
        utils.copyFile(os.path.join(sourcesrc,'gsc.exe'), os.path.join(sourcesrc,'gsc'))
        utils.copyFile(os.path.join(sourcesrc,'decode.exe'), os.path.join(sourcesrc,'decode'))
        
        utils.copyFile(os.path.join(sourcesrc,'gsc.exe'), os.path.join(sourcedir, 'bin'))
        utils.copyFile(os.path.join(sourcesrc,'gsc'), os.path.join(sourcedir, 'bin'))
        
        utils.copyFile(os.path.join(sourcesrc,'decode.exe'), os.path.join(sourcedir, 'bin'))
        utils.copyFile(os.path.join(sourcesrc,'decode'), os.path.join(sourcedir, 'bin'))
        
        return True
        
    def install(self):
            
        sourcedir = str(self.sourceDir())
        sourcesrc = os.path.join(sourcedir, 'src')
        craftbindir = os.path.join(CraftCore.standardDirs.craftRoot(), 'bin')
        gscdir = os.path.join(CraftCore.standardDirs.craftRoot(), 'gsc')
        
        self.enterSourceDir()
        
        utils.copyDir(sourcedir, gscdir)
        utils.rmtree(os.path.join(gscdir, 'src'))
        utils.copyFile(os.path.join(sourcedir, 'bin', 'gsc'), craftbindir)

        return True





