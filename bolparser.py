__author__ = 'Amogh Jalihal'

import json
import re

class bolParser:
    def __init__(self, bol):
        self.bol = bol
        self.Avartan = list()
        self.Vibhaag = list()
        self.Akshar = list()
        self.num_avartans = 0
        self.taaldict = {}
        
        self.__cleanupBol()
        self.__getTaalDict()
        self.__getAvartan()
        self.__getVibhaag()
        self.__getAkshar()
        self.num_avartans = len(self.Avartan)

    def __cleanupBol(self):
        # Replace multiple spaces in input with single space
        self.bol = " ".join(self.bol.split())
        # Remove padded | if any
        self.bol = re.sub("[ ]*\|[ ]*","|",self.bol)#"|".join(self.bol.split(" | "))
        # Remove padded || if any
        self.bol = "||".join(self.bol.split(" || "))
        
    def __getTaalDict(self):
        with open("data/taals.json",'r') as f:
            self.taaldict = json.load(f)
        
    def __getAvartan(self):
        self.Avartan = self.bol.split('||')[:-1]

    def __getVibhaag(self):
        self.Vibhaag = [av.split('|') for av in self.Avartan]

    def __getAkshar(self):
        GroupedAkshars = [[v.split(' ') for v in V] for V in self.Vibhaag]
        for av in GroupedAkshars:
            for v in av:
                for a in v:
                    self.Akshar.append(a)
        

    def guessTaal(self):
        matra_per_avartan = int(float(len(self.Akshar))/float(len(self.Avartan)))
        for taal in self.taaldict.keys():
            if matra_per_avartan == self.taaldict[taal]['matra']:
                return(taal)
