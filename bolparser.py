__author__ = 'Amogh Jalihal'

import json
import re
import sys

class bolParser:
    def __init__(self, bol):
        self.bol = bol
        self.Avartan = list()
        self.Vibhaag = list()
        self.Matra = list()
        self.num_avartans = 0
        self.taaldict = {}
        
        self.__cleanupBol()
        self.__getTaalDict()
        self.__getAvartan()
        self.__getVibhaag()
        self.__getMatra()
        
        self.num_avartans = len(self.Avartan)

    def __cleanupBol(self):
        # Replace multiple spaces in input with single space
        self.bol = " ".join(self.bol.split())
        # Remove padded | if any
        self.bol = re.sub("[ ]*\|[ ]*","|",self.bol)

    def __getTaalDict(self):
        with open("data/taals.json",'r') as f:
            self.taaldict = json.load(f)
        
    def __getAvartan(self):
        self.Avartan = self.bol.split('||')[:-1]

    def __getVibhaag(self):
        self.Vibhaag = [av.split('|') for av in self.Avartan]

    def __getMatra(self):
        GroupedAkshars = [[v.split(' ') for v in V] for V in self.Vibhaag]
        for av in GroupedAkshars:
            for v in av:
                for a in v:
                    self.Matra.append(a)
        
    def tokenize(self,matra,matraDensity):
        tokensCompound = ['tirakita','tita']
        tokensSimple = ['dha','dhi','ghe','tun','na','ti','ta','ka','S']
        
        alltokens = tokensSimple + tokensCompound
        if len(matra) == 0:
            return(matraDensity)
        else:
            for C in tokensCompound:
                loc = matra.find(C)
                if loc != -1:
                    matra = matra.replace(C,'',1)
                    if C == 'tirakita':
                        matraDensity.append(4)
                    if C == 'tita':
                        matraDensity.append(2)
                    if len(matra) == 0:
                        return(matraDensity)
            count = 0
            while len(matra) > 0:
                valid = False
                for cs in alltokens:
                    if cs in matra:
                        valid = True
                if not valid:
                    print("Unidentified akshar!\n Dump:")
                    print(matra)
                    print("Exiting..")
                    sys.exit()
                
                for S in tokensSimple:
                    loc = matra.find(S)
                    if loc != -1:
                        count += 1
                        matra = matra.replace(S,'',1)
            matraDensity.append(count)
            return(matraDensity)
            
    def getMatraDensity(self):
        """
        Returns list of lists containing number of grouped strokes per beat
        """
        matraDensity = []
        numvibhaags = self.num_avartans*len(self.Vibhaag[0])
        size = int(float(len(self.Matra))/float(numvibhaags))
        st = 0
        en = st + size
        for i in range(self.num_avartans):
            ad = []
            for v in self.Vibhaag[i]:
                vd = []
                for mat in self.Matra[st:en]:
                    vd.append(self.tokenize(mat,[]))
                st = en 
                en = en + size
                ad.append(vd)
            matraDensity.append(ad)
        return(matraDensity)

    # TEST
    # bol = "dhati tadha tita  dhadha| tirakita dhaghe dhina dhinatita|"\
    #       "S tadha titatirakitadha  dhadha| tirakita dhaghe dhina dhinatita||"
    # m = bolParser(bol)
    # print(m.getDensity())
    # Output: [[[[2], [2], [2], [2]], [[4], [2], [2], [2, 2]], [[1], [2], [4, 2, 1], [2]], [[4], [2], [2], [2, 2]]]]
    
    
    def guessTaal(self):
        matra_per_avartan = int(float(len(self.Matra))/float(len(self.Avartan)))
        for taal in self.taaldict.keys():
            if matra_per_avartan == self.taaldict[taal]['matra']:
                return(taal)
