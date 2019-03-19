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
        # If this returns nothing we are done
        tokensCompound = ['tirakita','tita']
        tokensSimple = ['dha','dhi','ghe','tun','na','ti','ta','ka','ta','S']
        
        alltokens = tokensSimple + tokensCompound
        if len(matra) == 0:
            return(matraDensity)
        else:
            for C in tokensCompound:
                loc = matra.find(C)
                if loc != -1:
                    print('found ' + C)                    
                    matra = matra.replace(C,'',1)
                    print(matra)
                    if C == 'tirakita':
                        matraDensity.append([4])
                    if C == 'tita':
                        matraDensity.append([2])
                    if len(matra) == 0:
                        return(matraDensity)
                    # else:
                    #     self.tokenize(matra,matraDensity)
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
                        print('found ' + S)
                        count += 1
                        matra = matra.replace(S,'',1)
                        print(matra)
            matraDensity.append([count])
            #print(matraDensity)
            return(matraDensity)
                
                    
            
    def getDensity(self):
        """
        TODO: Figure out how to correctly tokenize a Matra
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
                print(v)
                for mat in self.Matra[st:en]:
                    print(mat)
                    vd.append(self.tokenize(mat,[]))
                  
                    st = en 
                    en = en + size
                    
                ad.append(vd)
            matraDensity.append(ad)

            
        return(matraDensity)
            
    def guessTaal(self):
        matra_per_avartan = int(float(len(self.Matra))/float(len(self.Avartan)))
        for taal in self.taaldict.keys():
            if matra_per_avartan == self.taaldict[taal]['matra']:
                return(taal)
