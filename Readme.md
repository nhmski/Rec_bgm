# Rec_bgm
Rec_bgm 是用bangumi动漫评分数据搭建起来的 recommendation system, 使用的是基于用户的协同过滤算法，流程实现简单

* 对每个用户评分数据中心化
* 根据用户间的余弦相似度找到最相关的topk用户
* 由这些用户加权评分得出推荐的item (在bangumi上已收录的item或自动忽略)

## 安装方式
```
git clone https://github.com/klove2020/Rec_bgm.git
```

## 文件内容介绍
* src文件夹中存放源码
* partition_index中的索引数组区分R18和全年龄的作品
* data中存放2021.6爬取的用户评分数据（需要下载解压）

## 使用说明
找到bangumi上属于自己的user_id,在main.py相应位置填入,运行main即可,工作目录与该readme文件在同一目录下

## 特点
* 不会推荐05年以前的作品，以及打分数过少的冷门作品
* 每次运行main.py会自动抓取关于该用户最新的评分数据，基于此数据与2021.6月所有用户的评分数据结合给出推荐的动漫。
