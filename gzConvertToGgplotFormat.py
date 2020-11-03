#-*- coding:utf-8 -*-
import re,sys,os,math,json,gzip
import argparse
import numpy as np
from collections import OrderedDict

def getPositionValue(start,end,inputfile,sampleNum,sampleIndex,averageType):
    tempDict = OrderedDict()
    samplerPerCol = 0
    for line in gzip.open(inputfile,"r"):
        if re.search("^@", line):
            continue
        samplerPerCol = len(line.rstrip("\n").split("\t")[6:])/int(sampleNum) #统计每个sample的bin数目，均分
        for index in range(samplerPerCol):
            tempDict[index+1] = []
        break
    n = 0
    for line in gzip.open(inputfile,"r"):
        if re.search("^@",line):
            continue
        if int(start) <= n and n < int(end):
            newlist = line.rstrip("\n").split("\t")[6:]  #获取该sample的列范围
            for num,element in enumerate(newlist[int(sampleIndex)*samplerPerCol:(int(sampleIndex)+1)*samplerPerCol]):
                tempDict[num+1].append(float(element))
        n += 1
    finalDict = OrderedDict()
    for key in tempDict:
        finalDict[key] = []
        for staticsType in averageType.split(","):
            if staticsType == "mean":
                finalDict[key].append(str(np.mean(tempDict[key])))
            elif staticsType == "median":
                finalDict[key].append(str(np.median(tempDict[key])))
            elif staticsType == "min":
                finalDict[key].append(str(np.min(tempDict[key])))
            elif staticsType == "max":
                finalDict[key].append(str(np.max(tempDict[key])))
            elif staticsType == "sum":
                finalDict[key].append(str(np.sum(tempDict[key])))
            elif staticsType == "std":
                finalDict[key].append(str(np.std(tempDict[key])))
            else:
                print("Error averageType : {} not in [\"mean\",\"median\",\"min\",\"max\",\"sum\",\"std\"]".format(staticsType))
                sys.exit()
    return finalDict

def output(deeptoolsFile,outputPrefix,averageType,sample):
    deeptoolsFile = deeptoolsFile
    labelList = []
    sampleList = []
    labelAndBoundaries = OrderedDict()
    for line in gzip.open(deeptoolsFile, "r"):
        if re.search("^@", line):
            gBoundaries = []
            noteDict = json.loads(line.split("@")[1].rstrip("\n"))
            labelList = noteDict["group_labels"]
            sampleList = noteDict["sample_labels"]
            gBoundaries = noteDict["group_boundaries"]
            for index, key in enumerate(labelList):   #记录边界顺序
                labelAndBoundaries[key] = {}
                labelAndBoundaries[key]["bound"] = int(gBoundaries[index + 1])
            break
    out = open("{}.GgplotFormat.txt".format(outputPrefix),"a")
    headers = ["bin"]
    for x in averageType.split(","):
        headers.append(x)
    headers.append("sampleName")
    headers.append("peakName")
    out.write("\t".join(headers)+'\n')
    ### output
    if sample == "":
        for num,samplename in enumerate(sampleList):
            for index, key in enumerate(labelList):
                if index == 0:
                    finalDict = getPositionValue(0, labelAndBoundaries[key]["bound"], deeptoolsFile, len(sampleList), num, averageType)
                    for element in finalDict:
                        out.write(str(element) + '\t' + "\t".join(finalDict[element]) + '\t' + samplename + "\t" + key + '\n')
                else:
                    finalDict = getPositionValue(labelAndBoundaries[labelList[index - 1]]["bound"], labelAndBoundaries[key]["bound"], deeptoolsFile, len(sampleList), num, averageType)
                    for element in finalDict:
                        out.write(str(element) + '\t' + "\t".join(finalDict[element]) + '\t' + samplename + "\t" + key + '\n')
        out.close()
    else:
        for samplename in sample.split(","):
            if samplename not in sampleList:
                print("Error sample: {} not in [{}]".format(samplename,",".join(sampleList)))
                sys.exit()
            for index, key in enumerate(labelList):
                if index == 0:
                    finalDict = getPositionValue(0, labelAndBoundaries[key]["bound"], deeptoolsFile, len(sampleList), sampleList.index(samplename), averageType)
                    for element in finalDict:
                        out.write(str(element) + '\t' + "\t".join(finalDict[element]) + '\t' + samplename + "\t" + key + '\n')
                else:
                    finalDict = getPositionValue(labelAndBoundaries[labelList[index - 1]]["bound"], labelAndBoundaries[key]["bound"], deeptoolsFile, len(sampleList), sampleList.index(samplename), averageType)
                    for element in finalDict:
                        out.write(str(element) + '\t' + "\t".join(finalDict[element]) + '\t' + samplename + "\t" + key + '\n')
        out.close()

def main():
    parser = argparse.ArgumentParser(usage='\n\npython gzConvertToGgplotFormat.py --input sample.gz --outputPrefix ... [option]', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--input', '-I', required=True, help='Input of gz format file')
    parser.add_argument('--outputPrefix', '-O', required=True, help='PrefixName of the result file')
    parser.add_argument('--averageType', '-t', default="mean", help='The type of statistic that should be used for the profile. The options are:'
                            '"mean","median","min","max","sum","std";\nSpecify more than one averageType, separate with commas')
    parser.add_argument('--sample', '-s', default="", help='Enter the sample list to be extracted, separated by commas: sample1,sample2,...,sampleN')
    args = parser.parse_args()
    inputfile = args.input
    outputPrefix = args.outputPrefix
    averageType =  args.averageType
    sample = args.sample
    output(inputfile,outputPrefix,averageType,sample)

if __name__ == '__main__':
    main()