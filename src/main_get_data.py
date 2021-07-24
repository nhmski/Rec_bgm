from multiprocessing import Pool
from joblib import Parallel, delayed
from utils import process_user


filename = "data/user_now.csv"
errorfile = "bgm_error.txt"

with open(filename, "a") as f:
    f.write("\t".join(['user_id', 'subject_id', 'status', 'rate']) + "\n")

with open(errorfile, "a") as f:
    f.write("ok\n")

# if __name__ =="__main__":   
#     with Pool(2) as p:
#         p.map(process_user, range(1, 1000))
process_user(572059)