import pandas as pd
import shutil
import sys

original_stdout = sys.stdout # Save a reference to the original standard output

shutil.copy2('/var/named/porn.host.srv', '/tmp/toyo/spamhouse-data-clean/porn.host.srv') 
shutil.copy2('/var/named/botnetcc.host.dtq', '/tmp/toyo/spamhouse-data-clean/botnetcc.host.dtq')
shutil.copy2('/var/named/botnet.host.dtq', '/tmp/toyo/spamhouse-data-clean/botnet.host.dtq')



df_porn = pd.read_csv("porn.host.srv",skiprows= 10,header = None,error_bad_lines = True)
df_botnetcc = pd.read_csv("botnetcc.host.dtq",skiprows= 10,header = None,error_bad_lines = True)
df_botnet = pd.read_csv("botnet.host.dtq",skiprows= 10,header = None,error_bad_lines = True)



df_porn =df_porn[~df_porn[0].str.contains('CNAME', na=False)]
df_botnetcc =df_botnetcc[~df_botnetcc[0].str.contains('CNAME', na=False)]
df_botnet =df_botnet[~df_botnet[0].str.contains('CNAME', na=False)]



df_porn =df_porn[~df_porn[0].str.contains('rpz-ip', na=False)]
df_botnetcc =df_botnetcc[~df_botnetcc[0].str.contains('rpz-ip', na=False)]
df_botnet =df_botnet[~df_botnet[0].str.contains('rpz-ip', na=False)]



df_porn.reset_index(inplace= True)
df_botnetcc.reset_index(inplace= True)
df_botnet.reset_index(inplace= True)



df_porn=df_porn[df_porn.index % 2 != 0]
df_botnetcc=df_botnetcc[df_botnetcc.index % 2 != 0]
df_botnet=df_botnet[df_botnet.index % 2 != 0]




def split(x):
    a = str(x).split(" ")[1]
    b = str(a).split(".")[:-4]
    b = ".".join(b)
    return b



df_porn[0]= df_porn[0].apply(split)
df_botnetcc[0]= df_botnetcc[0].apply(split)
df_botnet[0]= df_botnet[0].apply(split)



df_porn.drop(['index'],axis = 1,inplace = True)
df_botnetcc.drop(['index'],axis = 1,inplace = True)
df_botnet.drop(['index'],axis = 1,inplace = True)



df_1notin2 = df_botnetcc[(df_botnetcc[0].isin(df_porn[0]))].reset_index(drop=True)
df_1notin2.to_csv("/var/sftp/files/botnetcc_match.txt",index = False, header = 0)

#print (df_1notin2.shape[0] +"out of :"+ df_porn.shape[0])




df_3notin2 = df_botnet[(df_botnet[0].isin(df_porn[0]))].reset_index(drop=True)
df_3notin2.to_csv("/var/sftp/files/botnet_match.txt",index = False, header = 0)

with open('/var/sftp/files/logs.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    print("botnetcc :"+ str(df_1notin2.shape[0]) +" "+ "out of :"+ str(df_porn.shape[0]))
    print("botnet :"+ str(df_3notin2.shape[0]) +" "+ "out of :" + str(df_porn.shape[0]))
    sys.stdout = original_stdout # Reset the standard output to its original value



