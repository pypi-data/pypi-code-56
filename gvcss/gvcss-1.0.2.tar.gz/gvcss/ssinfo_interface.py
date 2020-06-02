from collections import  defaultdict


class Singleton(object):
    _instance = None
    def __new__(cls,*args,**kw):
        if not cls._instance:
            cls._instance = super(Singleton,cls).__new__(cls,*args,**kw)
        return cls._instance


class ssInfoInterface(Singleton):
    ssInfoDict = defaultdict(type(defaultdict()))
    
    def set_vcf(self,variant,vcf):
        self.ssInfoDict[variant] = vcf

    def set_bam(self,bam):
        self.ssInfoDict['bam'] = bam

    def set_SVbam(self, SVbam):
	self.ssInfoDict['svbam'] = SVbam
	
    def get_info(self):
        return self.ssInfoDict
