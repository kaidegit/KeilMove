import os
import fnmatch
import re

# find sdk
sdk_root = input("请输入SDK根目录：\r\n例如C:\\Users\\<user>\\Documents\\DevPkgs\\nRF5_SDK_17.1.0_ddde560\\\n")
if not sdk_root.endswith("\\"):
    sdk_root += "\\"
    
# find uvprojx
uvprojx_files = []
for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*.uvprojx'):
        uvprojx_files.append(os.path.join(root, filename))
        
if len(uvprojx_files) == 0:
    print("未找到uvprojx文件")
    exit(1)
elif len(uvprojx_files) > 1:
    print("找到多个uvprojx文件")
    exit(1)
else:
    print("find", uvprojx_files[0])

old_sdk_path = ''
find_key = 'components\libraries'
with open(uvprojx_files[0]) as f:
    for line in f:
        line = line.strip()
        # print(line)
        if line.startswith('<FilePath>') \
            and '</FilePath>' in line: 
            # print(line)
            if find_key in line:
                start = line.find('<FilePath>')
                end = line.find('</FilePath>')
                line = line[start + len('<FilePath>'):end]
                old_sdk_path = line[:line.find(find_key)]
                print('find old sdk path:', old_sdk_path)
                break
    if old_sdk_path == '':
        print('未找到旧SDK路径')
        exit(1)
        
# replace
with open(uvprojx_files[0], 'r') as file:
    file_content = file.read()

# 替换字符串
modified_content = file_content.replace(old_sdk_path, sdk_root)

with open(uvprojx_files[0], 'w') as file:
    file.write(modified_content)

print('替换完成')