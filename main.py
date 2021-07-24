import pandas as pd
import numpy as np

from src.data_clean import split
from src.recommendation import centralization_adjust,cosine_similarly,Recommendation_table,get_recomendation

def main(target_user_id,num = 10,option=1):
    dataset = pd.read_csv('data/bgm_anime_cleaned.csv', engine='python')
    # df = centralization_adjust(dataset.iloc[:,1:5])
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
        print("R18作品推荐")
        df = centralization_adjust(dfs[0])
        recomend(df,0)

        print("全年龄作品推荐")
        num = 55
        df = centralization_adjust(dfs[1])
        recomend(df,1)
            
    
    
if __name__ == "__main__":
    main(target_user_id = 572059, option=1, num = 25)