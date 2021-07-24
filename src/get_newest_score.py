import pandas as pd
from utils import process_user

def update_score(uid):
    print(f"Updating the latest score about user_{uid}")
    filename = "data/user_now.csv"
    errorfile = "bgm_error.txt"

    with open(filename, "w") as f:
        f.write("\t".join(['user_id', 'subject_id', 'status', 'rate']) + "\n")

    with open(errorfile, "a") as f:
        f.write("ok\n")

    process_user(uid)
    
def update_dateset(df,uid, update_df=0):
    update_score(uid)
    ud_df = pd.read_csv('data/user_now.csv',sep=r"\t", engine='python')
    df_remove_user = df[df["user_id"]!=uid]

    bgm_anime_cleaned = pd.concat([df_remove_user,ud_df])
    if update_df:
        bgm_anime_cleaned.to_csv("data/bgm_anime_cleaned.csv",index=None)
    print("update completed ")
    return bgm_anime_cleaned    
    

    