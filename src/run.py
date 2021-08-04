import pandas as pd
from data_clean import split
from recommendation import centralization_adjust,cosine_similarly,Recommendation_table,get_recomendation
from get_newest_score import update_dateset

def main(target_user_id,num = 10,option=1):
    """
    arg:
        target_user_id：受推荐用户的bangumi user id.
        num:推荐的动漫个数
        option：
            1：只推荐全年龄作品
            -1：只推荐R18作品
            0：两者都推荐        
        
    """
    print("reading data")
    df = pd.read_csv('data/bgm_anime_cleaned.csv', engine='python')
    dataset = update_dateset(df,target_user_id)
    dfs = split(dataset) 

    def recomend(df,op):
        pivot_table = df.pivot_table(index="user",columns="anime",values="rating").fillna(0)
        cosinesimilarly = cosine_similarly(pivot_table,target_user_id)

        bool = pivot_table.loc[target_user_id]==0
        recomendation_table = Recommendation_table(pivot_table,cosinesimilarly,bool)
        
        get_recomendation(recomendation_table, num,op)

    if option == 1:
        print("全年龄作品推荐")
        df = centralization_adjust(dfs[1])
        recomend(df,1)
    elif option == -1:
        print("R18作品推荐")
        df = centralization_adjust(dfs[0])
        recomend(df,0)
    elif option == 0:
        print("全年龄作品推荐")
        df = centralization_adjust(dfs[1])
        recomend(df,1)

        print("R18作品推荐")
        df = centralization_adjust(dfs[0])
        recomend(df,0)
