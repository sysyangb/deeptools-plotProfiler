# deeptools-plotProfiler

>Input:

`computeMatrix工具得到的输出的压缩.gz矩阵文件`

>Usage:


```
python gzConvertToGgplotFormat.py --input sample.gz --outputPrefix ... [option]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -I INPUT
                        Input of gz format file
  --outputPrefix OUTPUTPREFIX, -O OUTPUTPREFIX
                        PrefixName of the result file
  --averageType AVERAGETYPE, -t AVERAGETYPE
                        The type of statistic that should be used for the profile. The options are:"mean","median","min","max","sum","std";
                        Specify more than one averageType, separate with commas
  --sample SAMPLE, -s SAMPLE
                        Enter the sample list to be extracted, separated by commas: sample1,sample2,...,sampleN
```


>Output:

|  bin   | mean | ... |sampleName| peakName|
|  ----  | ----  |   ----  |----  | ----  |
|1	|0.037430114503816794| ...	|H3K27ac	|promoter.trio|
|2	|0.03541725190839695| ...	|H3K27ac	|promoter.trio|
|3	|0.03517291348600509| ...	|H3K27ac	|promoter.trio|
|4	|0.03546380152671756| ...	|H3K27ac	|promoter.trio|
|5	|0.034288638676844785| ...	|H3K27ac	|promoter.trio|
|6	|0.03518454961832061| ...	|H3K27ac	|promoter.trio|
|7	|0.036569127226463105| ...	|H3K27ac	|promoter.trio|
|8	|0.03578956488549618| ...	|H3K27ac	|promoter.trio|
|9	|0.033881422391857506| ...	|H3K27ac	|promoter.trio|
|10	|0.03516126717557252| ...	|H3K27ac	|promoter.trio|

输出文件为可以直接用来作图的整合矩阵,第一列为bin编号,第二列...指定列为峰信号均值[...其他统计值],倒数第二列为样本名,倒数第一列为peak名.

>对比(曲线一致,前者是自动作图,后者是用graphpad作图):

**Before :**

![输入图片说明](https://images.gitee.com/uploads/images/2020/1023/111958_d385336c_7948144.png "屏幕截图.png")

**After  :**

![输入图片说明](https://images.gitee.com/uploads/images/2020/1023/112015_3651ddd4_7948144.png "屏幕截图.png")
