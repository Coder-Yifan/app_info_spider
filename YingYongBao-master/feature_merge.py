import pandas as pd
import numpy as np
import os
feature_file_path = "C:/File/data/feature_importance_test/feature_data/"
file_list = os.listdir(feature_file_path)
# 离散型数据拼接
data_con = pd.DataFrame()
flag = 0
for iterion, file_name in enumerate(file_list[:-1]):
    # if "标签" in file_name.split("_")[-1] :
    file_path = feature_file_path + file_name
    #print(file_path)
    data_l = pd.read_excel(file_path)

    # print(data_l.columns)
    for column in data_l.columns:
        #print(type(column))
        if "-" in column:
            #             print("yse",column)
            #             print(column.split("-")[0])
            data_l.rename(columns={column: column.split("-")[0]}, inplace=True)
    # print(data_l.columns)
    # data_l.columns = ['name','mobile','idcard','applyDate','返回结果状态码','测试结果']
    if flag == 0:
        flag = 1
        data_con = data_l.loc[:, ['idcard', 'name', 'mobile', 'applyDate']]
    #     print(data_con.columns)
    #     print("========================================")
    column_name = file_name.split("_")[-1].split(".")[0]
    if column_name[-2:] == "标签":
        column_name = column_name[:-2]
    result = data_l['测试结果']
    for i, info in enumerate(result):
        if type(info) != str:
            continue
        info = eval(info)
        # print(data_con.head())
        # print(info.keys())
        if "data" in info.keys():
            data_l.loc[i, column_name] = info['data']['result']
        else:
            continue

    # data_l = data_l.loc[:,['mobile',column_name]]
    # data_l = data_l.loc[:, ['idcard', 'name', 'mobile', column_name]]
    # data_l = data_l.loc['['idcard', 'name', 'mobile']']
    data_con = pd.merge(data_con, data_l[['idcard', 'name', 'mobile', column_name]], on=['idcard', 'name', 'mobile'])
#     print(data_con.head())
#     print("=============================================")
data_l = pd.read_excel(feature_file_path+file_list[-1])
data_l.columns = ['name','idcard','mobile','applyDate','旅游达人','作为乘车人GDC列车购票总次数',
                 '线下（窗口、自动售票机、电话、代售点）购票比例','GDC列车车费消费总金额',
                 '总旅行时长 单位:分钟','高端商旅','交易未支付总张数','购乘意险数量','作为乘车人购票总次数',
                 '车费消费总金额']
for i ,col in enumerate(data_l.columns):
    if i < 4:
        continue
    result = data_l[col]
    for i,info in enumerate(result):
        if type(info)!=str:
            continue
        info = eval(info)
        #print(data_con.head())
        if "data" in info.keys():
            data_l.loc[i,col] = info['data']['result']
        else :
            data_l.loc[i,col] = None
data = pd.merge(data_con,data_l,on=['idcard','name','applyDate','mobile'],how='inner')
# for each in data.select_dtypes(exclude=np.number).columns:
#     data[each] = data[each].map(lambda x: x.rstrip())
for each in ['name','idcard','mobile']:
    data[each] = data[each].map(lambda x: x.rstrip())
label = pd.read_excel("C:/File/data/feature_importance_test/截至20190715全量贷款用户.xlsx")
del label['apply_date']
info_data = pd.merge(label,data,left_on=['id_no(md5)','phone(md5)'],right_on=['idcard','mobile'],how="inner")
info_data.to_excel(feature_file_path+"data.xlsx")
info_data.to_csv(feature_file_path+"data.csv")
