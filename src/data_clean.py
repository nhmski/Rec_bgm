import pandas as pd
import numpy as np
# dataset = pd.read_csv('bgm_anime.csv', sep=r'\t', engine='python')

# 清除冷门item以及非活跃用户（用来进一步压缩数据）
def remove_unpopular(dataset):
    user_collect_count_list = dataset["user_id"].value_counts()
    subject_scored_count_list = dataset["subject_id"].value_counts()
    
    user_bool = user_collect_count_list > 50 # 29160 用户
    subject_bool = subject_scored_count_list > 30 # 9831 条目
    
    user = user_collect_count_list[user_bool]
    item = subject_scored_count_list[subject_bool]

    df1 = dataset[dataset["user_id"].isin(user.index)]
    df2 = df1[df1["subject_id"].isin(item.index)]
    return df2

# 移除未评分项目
def remove_zero_score(dataset):
    bool = dataset["rate"] != 0
    dataset = dataset[bool]
    return dataset

# 作品按类别拆分
def split(df):
    # R18  = np.load("R18_list.npy")
    R18  = np.load("partition_index/R18_list_time2005__.npy")
    df_R18 = df[df["subject_id"].isin(R18)]
    # all_ages = np.load("all_ages_list.npy")
    all_ages = np.load("partition_index/all_ages_list_time2005__.npy")
    df_all_ages = df[df["subject_id"].isin(all_ages)]
    return df_R18,df_all_ages

