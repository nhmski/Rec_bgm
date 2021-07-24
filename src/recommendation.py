import pandas as pd
import numpy as np

def centralization_adjust(df):
    """
    返回user_id,subject_id,Ratings adjusted组成的df
    """
    Mean = df.loc[:,["user_id","rate"]].groupby(["user_id"],as_index=False,sort=False).mean()
    Ratings = pd.merge(df,Mean,on="user_id",how="left").rename(columns={"rate_x":"rate","rate_y":"mean_rate"}) #拼接dataframe
    Ratings["Ratings_adjusted"] =Ratings["rate"]-Ratings["mean_rate"]
    result = pd.DataFrame({"user":Ratings["user_id"],"anime":Ratings["subject_id"],"rating":Ratings["Ratings_adjusted"]})
    return result

# 目标用户与所有用户计算的cos相似度
def cosine_similarly(pivot_table,target_user_id):
    allusers = pivot_table.values 
    target_user = pivot_table.loc[target_user_id].values
    
    Users_normalization = allusers/np.linalg.norm(allusers,axis=1)[:, np.newaxis]
    tu_normalization = target_user/np.linalg.norm(target_user)
    cosinesimilarity= Users_normalization@tu_normalization
    cosinesimilarity[np.isnan(cosinesimilarity)] = -1
    return cosinesimilarity

# 针对特定用户返回的pivot_table
def Recommendation_table(pivot_table, cosinesimilarity,target_items_bool, sun=100):
    """
    sun:指定相似用户的数量
    target_items_bool:索引是与列名匹配的，使用该bool值的方法是用".loc"
    """
    similarusers = cosinesimilarity.argsort()[-sun:] # -1 应该为自己
    topcosine = cosinesimilarity[similarusers]

    recomendation_table = pivot_table.iloc[similarusers]    

    # I = recomendation_table.iloc[sun]
    # bool = I==0
    recomendation_table = recomendation_table.loc[:,target_items_bool]
    recomendation_table["cosine"] = topcosine
    
    return recomendation_table

def weight(n:int,option):
    if option==1:
        # 全年龄权重
        if n<=3:
            return 0
        elif 3<n<=10:
            return 0.5
        elif 10<n<=50:
            return 0.01*n+0.5
        elif n>50:
            return 1
    else:
        # R18权重
        if n<=1:
            return 0
        elif 1<n<=10:
            return 0.05*n+0.5
        elif n>10:
            return 1

def get_recomendation(recomendation_table,num, option = 1):
    recom_matrix = recomendation_table.to_numpy()
    cos = recom_matrix[...,-1]
    score = recom_matrix[...,0:-1]
    """
    全年龄：最多71个评分，平均5.9个
    R18:最多15个评分, 平均2.4个
    """
    prediction_score = score*(cos.reshape(-1,1))
    # prediction_score = prediction_score.sum(axis = 0)/cos.sum()
    prediction_score_sum = prediction_score.sum(axis = 0)
    
    for i in np.where(prediction_score_sum!=0)[0]:
        bool = np.where(prediction_score[:,i]!=0)[0]
        
        # 票数过少的作品不计分
        if option ==1:
            count_weight = 1 if bool.size >3 else 0
        else:
            count_weight = 1 if bool.size >1 else 0            
        
        prediction_score_sum[i] = prediction_score_sum[i]*count_weight # 不除以cos权重，因为中心化评分是有可能有负数的，未必人多就分高
        # prediction_score_sum[i] = prediction_score_sum[i]/cos[bool].sum()*count_weight
        
    ii = prediction_score_sum.argsort()[-num:].tolist()
    ii.reverse()
    # recomendation_table.iloc[:,ii].columns
    for i,id in enumerate(recomendation_table.iloc[:,ii].columns):
        print(f"推荐指数:{round(prediction_score_sum[ii[i]],2)}    https://bgm.tv/subject/{id}")
    print("subject id:")
    for id in recomendation_table.iloc[:,ii].columns:
        print(id)
    # for id in recomendation_table.iloc[:,ii].columns:
    #     print(f"[url]https://bgm.tv/subject/{id}[/url]")
        