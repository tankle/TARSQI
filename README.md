#TARSQI

##Temporal Awareness and Reasoning Systems for Question Interpretation

原官方网站: http://timeml.org/site/tarsqi/index.html

[English](https://github.com/tankle/TARSQI/blob/master/README.en.md)

本项目是TARSQI的一个镜像，由于原始项目貌似没有继续开发（至少官方发给我的是这个）。

由于实验室项目的需要，我将继续改进这个软件。

本软件主要是用于对文档时间标签和事件标签的识别，并能够通过时间来抽取事件之间的先后关系

[SemEval 2015](http://alt.qcri.org/semeval2015/task5/) 中的task 5 也是类似的任务。但是将语料格式进行了归一化，同意使用xml格式。
因此不能直接使用本软件。这也是我将要主要做的工作。

###TODO
1. 修改读取文档创建时间，统一从xml文档中读取
2. 增加说明文档

如有任何问题，欢迎联系！


Email:tankle120#gmail.com(替换#为@）



##License

The Tarsqi Toolkit is copyright  ©2007 of Brandeis University and is licensed under a [Creative Commons Attribution-Noncommercial-Share Alike 3.0 United States License](http://creativecommons.org/licenses/by-nc-sa/3.0/us/).

The Tempex module is copyright of The MITRE corporation and is distributed under the license in [tempex-license.pdf](https://github.com/tankle/TARSQI/blob/master/docs/manual/tempex-license.pdf).

The Python wrapper for the TreeTagger ([treetaggerwrapper.py](http://www.limsi.fr/Individu/pointal/python/treetaggerwrapper.py)) is copyright ©2004 of CNRS and distributed under the GNU-GPL Version 2. It was developed by [Laurent Pointal](http://www.limsi.fr/Individu/pointal/).

The data in data/in/TimeBank are copyrighted by the various content providers and can be used for academic purposes only .

