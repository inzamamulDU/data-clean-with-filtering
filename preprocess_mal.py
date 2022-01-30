#!Inzamamul Alam

import pandas as pd

import sys

original_stdout = sys.stdout # Save a reference to the original standard output


def split(x):
    a = str(x).split(" ")[1]
    b = str(a).split(".")[:-4]
    b = ".".join(b)
    return b

def split_mal(x):
    a = str(x).split(" ")[0]
    return a


df_porn = pd.read_csv("porn.host.srv",skiprows= 10,header = None,error_bad_lines = True)
df_mal = pd.read_csv("malware_domains.txt",skiprows= 1,header = None,error_bad_lines = True)


df_porn =df_porn[~df_porn[0].str.contains('CNAME', na=False)]
df_porn =df_porn[~df_porn[0].str.contains('rpz-ip', na=False)]
df_porn.reset_index(inplace= True)
df_porn=df_porn[df_porn.index % 2 != 0]
df_porn[0]= df_porn[0].apply(split)
df_porn.drop(['index'],axis = 1,inplace = True)

df_mal[0]= df_mal[0].apply(split_mal)



df_1notin2 = df_mal[(df_mal[0].isin(df_porn[0]))].reset_index(drop=True)
df_1notin2.to_csv("/var/sftp/files/mal.txt",index = False, header = 0)

with open('/var/sftp/files/logs.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    
    
    print("malware :"+ str(df_1notin2.shape[0]) +" "+ "out of :"+ str(df_porn.shape[0]))


    sys.stdout = original_stdout # Reset the standard output to its original value

