import os
from os.path import join
from os import listdir
from os import makedirs
import re
import pypinyin
import  shutil
import json

old_dataset="PRfaces2021"
new_dataset="DataSet-PRface2021"
name_sheet=dict()

for id_dir_item in sorted(listdir(old_dataset)):
    print(id_dir_item)

    #提取姓名，学号
    name_str=''.join(re.findall('[\u4e00-\u9fa5]',id_dir_item))
    number_str=''.join(re.findall(r"\d+",id_dir_item))

    #获取英文名 #pypinyin
    name_list=pypinyin.lazy_pinyin(name_str)
    last_name = name_list[0]
    first_name=''.join(name_list[1:])

    #首字母大写
    last_name=last_name.title()
    first_name=first_name.title()
    #姓名拼接
    english_name="".join(first_name)+"_"+last_name
    print("Chinese name: ",name_str)
    print("English Name:",english_name)
    print("id:",number_str)
    #保存姓名学号键值对
    name_sheet[english_name]=dict()
    name_sheet[english_name]['id']=number_str
    name_sheet[english_name]['name']=name_str

    #新的文件名
    flag=False
    id_dir_new_name=english_name
    print("new name:",id_dir_new_name)
    imgs_item=listdir(join(old_dataset,id_dir_item))
    print(imgs_item)
    print(join(old_dataset,id_dir_item,imgs_item[0]))
    print(os.path.isdir(join(old_dataset,id_dir_item,imgs_item[0])))
    if  os.path.isdir(join(old_dataset,id_dir_item,imgs_item[0])):
        flag=True
        imgs_item=listdir(join(old_dataset,id_dir_item,imgs_item[0]))
    index=1
    for  img_i in imgs_item:
        #对不同的文件夹进行处理
        if flag:
            old_img_name = join(old_dataset, id_dir_item,
                                listdir(join(old_dataset, id_dir_item))[0], img_i)
        else:
            old_img_name=join(old_dataset,id_dir_item,img_i)
        new_img_name=join(new_dataset,id_dir_new_name,english_name+"_000"+str(index)+img_i[-4:])
        if not os.path.exists(join(new_dataset,id_dir_new_name)):
            makedirs(join(new_dataset,id_dir_new_name))
        shutil.copy(old_img_name,new_img_name)
        index+=1


with open("name_sheet.json",'w') as f:
    json.dump(name_sheet,f)

