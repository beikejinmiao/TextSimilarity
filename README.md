## Usage
总共训练、测试、Web服务三种模式。      
由于原始数据和训练好的模型文件过大，需单独从百度网盘下载[model.zip](https://pan.baidu.com/s/1XMW0ZoH_lFOMMxfF-GFzIg)(提取码:8n3y)，解压后将内容拷贝至`resources`目录下。   

 - 训练模式       
将`accountant_qa_dataset.csv`(model.zip中已包含该文件)拷贝至`resources`目录下；       
启动命令：`python iqa.py --mode=train`，重新分词并训练所有模型， 用于首次部署项目      
 - 测试模型       
启动命令：`python iqa.py --mode=test`，用于验证已训练好的模型。  
 - Web服务模式     
启动命令：`python iqa.py --mode=server`，然后访问 http://127.0.0.1:8080/  查看使用说明。       
目前已部署至线上服务器http://47.104.224.226:8080/，可以直接使用。    

**[注]**    
 - 重新训练模型比较耗时，建议直接使用训练好的[model.zip](https://pan.baidu.com/s/1XMW0ZoH_lFOMMxfF-GFzIg)(提取码:8n3y)，直接启动Web服务。
 - 线上服务器配置较低、带宽较小，仅供演示。  

## 项目结构介绍

### conf
配置文件目录
 - config.py       
系统基本配置，包括模型列表、Web端口等
 - logger.json      
系统日志功能配置，包括日志等级、存储路径等
 - paths.py        
系统常用路径配置，包括项目根目录等

### libs
核心库         
 - logger.py         
实现打印日志功能         
 - resource.py       
实现读取系统资源功能，主要读取字典和停顿词
 - score.py         
实现bleu和cosine计算
 - segment.py         
实现数据清洗和分词功能
 - singleton.py         
单例父类，主要保证系统资源单例
 - util.py         
实现基础工具函数，比如排序、读取文件
 - wrapper.py         
系统常用装饰器实现

### model
实现相似度计算模型，即Embedding部分，包括
 - base.py         
embedding模型基类，定义常用函数
     - tfidf.py      
    基于TF-IDF计算、查询文本相似性
     - lsi.py   
    基于LSA/LSI计算、查询文本相似性
     - word2vec.py      
    基于Word2Vec计算、查询文本相似性；      
    文本向量为把所有词向量加和后取平均值，然后使用KDTree查找最相似文本
     - doc2vec.py     
    基于Doc2Vec计算、查询文本相似性
      
后续需持续补充。

### [resources](https://github.com/beikejinmiao/IQA/blob/master/resources/README.md)
存放系统资源文件，包括字典、停顿词和原始的问答数据

### server
 - socket.py         
系统socket接口(未实现)
 - webserver.py         
系统Web API

### iqa.py
系统主文件，用于解析参数、启动系统

### mode.py
负责系统流程和执行具体的任务

