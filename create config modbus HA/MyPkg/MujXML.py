# -*- coding: cp1250 -*-
# verze 2013-02
# vytvořil Milan Hutera


import os
import mmap
import codecs
from shutil import copyfile
from glob import glob
import re


class XML:
    def XMLgroups(self,Source,Index,Count = '',ShortEnd ='/>',Start = '<[A-z]+',End = '</[A-z]+',Separator = '<',StartShortEnd='</'):
        regexStart = re.compile(Start)
        regexEnd = re.compile(End)
        regexShortEnd = re.compile(ShortEnd)
        Groups = []
        StartGroups = []
        for i in regexStart.finditer(Source):
            Groups.append([i.start(), i.group(0)])
        for i in regexEnd.finditer(Source):
            Groups.append([i.start(), i.group(0)])
        for i in regexShortEnd.finditer(Source):
            Groups.append([i.start(), i.group(0)])        
        Groups.sort()
        StartIndex = -1
        GroupsResult = []
        StartGroup = 0
        ID = 0
        
        for i in Groups:
            if i[1]==(Separator+Index):
                AuxGroup = 0
                for ii in Groups[ID:]:
                    if ii[1].count(StartShortEnd)>0 or ii[1].count(ShortEnd)>0:
                        AuxGroup = AuxGroup-1
                    else:
                        AuxGroup = AuxGroup+1                    
                    if AuxGroup==0:  
                        if Source[i[0]:ii[0]].count(Count)>0:
                            GroupsResult.append(Source[i[0]:ii[0]])
                        break
            ID = ID+1
        return GroupsResult,Groups
        
        

    


    def Keys(self,Source,Regex="[A-z0-9]+=",ReKeyStart = '"',ReKeyEnd = '"',KeyReplace = ['=']):
        "Vrátí všechny klíče, Result[Klič]=...."
        Result = {}
        regex = re.compile(Regex)
        Place = regex.findall(Source)
        for i in regex.findall(Source):
            Key = i
            for ii in KeyReplace:
                Key = Key.replace(ii,'')
            Result[Key] = self.FirstGroupXML2(Source,i+ReKeyStart,ReKeyEnd)
        return Result
    
    def FirstGroupXML2(self,Source,Start,End):    
        IndexS = 0
        IndexE = 0
        Start = Start
        End = End
        IndexS = Source[IndexS:].find(Start)+IndexS+len(Start) 
        IndexE = Source[IndexS:].find(End)+IndexS
        return (Source[IndexS:IndexE])

    def AddTable(self,List,Key,What):
        if List.has_key(Key):
            if List[Key].count(What)==0:
                List[Key].append(What)
        else:
            List[Key]=[What]

    def NewGroupsXML2(self,Source,Start,End,Count=''):
        
        Result = []
        IndexS = 0
        IndexE = 0
        AuxStart = 0
        AuxEnd = 0
        Start = Start
        End = End
        aa = 0
        bb = 0
        for i in range(Source.count(Start)):
##            aa += 1
##            if aa>100:
##                bb += 1
##                aa = 1
##                print "dalsi 100",bb
            
            AuxStart = IndexS
            AuxEnd = IndexE
            IndexS = Source[IndexS:].find(Start)+IndexS
            IndexE = Source[IndexS+1:].find(End)+IndexS+1+len(End)
            #print IndexS, IndexE

            while Source[IndexS:IndexE].count(Start) > Source[IndexS:IndexE].count(End):
                aa += 1
                if aa>100:
                    bb += 1
                    aa = 1
                    print "dalsi 100",bb
                    print IndexS,IndexE
                IndexE = Source[IndexE+1:].find(End)+IndexE+1+len(End)
            if Source[IndexS:IndexE].count(Count)>0:
                Result.append(Source[IndexS:IndexE])
            IndexS = IndexS+1
        return Result

    def textBetweenStartEnd(self,Source,Start,End,Count=''):
        regex = re.compile(Start + '.*?' + Count + '.*?' + End)
        Source = Source.replace("\r\n","XXXNewLine")
        r = regex.findall(Source)
        print "found:",len(r)
        Result = []
        a = 0
        for i in r:
            a += 1
            print "done: ",a
            Result.append(i.replace("XXXNewLine","\r\n"))
        return Result    
    
    
