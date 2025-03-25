import re
import os 
import shutil
from collections import deque


valid_file_extension=[
        "txt", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
        "jpg", "jpeg", "png", "gif", "bmp", "tiff", "svg",
        "mp3", "wav", "ogg", "flac",
        "mp4", "avi", "mkv", "mov",
        "zip", "rar", "tar", "gz", "7z",
        "html", "css", "js", "py", "java", "c", "cpp", "cs", "rb", "php",
        "xml", "json", "yml", "ini", "cfg",
        "exe", "dll", "bin", "iso",
        "log", "md", "rtf"
    ]





def create(d_input,managed_base,trash,valid_file_extension=valid_file_extension):
    command=d_input[0]
    flags=os.O_RDWR | os.O_CREAT
    if d_input[1]=="-b":
        print("not implemented")
    elif d_input[1]=="-r":
        rel_path=d_input[2]
        os.chdir(managed_base)
        s_rel_path=rel_path.split("/")
        i=0
        while os.path.exists(s_rel_path[i]) and i<len(s_rel_path):
            i+=1
        num_to_create=len(s_rel_path)-i
        s_path=rel_path.split("/")
        m=re.match(r"\w+\.(\w+)$",s_path[-1])
        if m:
            p_ext=m.group(1)
            if p_ext in valid_file_extension:
                pre_path="/".join(s_path[:-1])
                os.makedirs(os.path.join(managed_base,pre_path),exist_ok=True)
                fd=os.open(os.path.join(managed_base,rel_path),flags)
                os.close(fd)
                return num_to_create
        os.makedirs(os.path.join(managed_base,rel_path),exist_ok=True)
        return num_to_create
    else:
        rel_path=d_input[1]
        s_path=rel_path.split("/")
        m=re.match(r"\w+\.(\w+)$",s_path[-1])
        existing_path="/".join(s_path[:-1])
        if os.path.exists(os.path.join(managed_base,existing_path)):
            if m:
                p_ext=m.group(1)
                if p_ext in valid_file_extension:
                    fd=os.open(os.path.join(managed_base,rel_path),flags)
                    os.close(fd)
                    return 
            os.mkdir(os.path.join(managed_base,rel_path))
            return 
        else:
            raise Exception("path not found use -r flag to create a path recursively")



        


def delete(d_input,managed_base,trash):
    os.chdir(managed_base)
    command=d_input[0]
    if d_input[1]=="-b":
        print("not implemented")
    else:
        rel_path=d_input[1]
        if os.path.exists(os.path.join(managed_base,rel_path)):
            shutil.move(rel_path,trash)
        else:
            raise Exception("Path to remove does not exist")

    
        
def rename(d_input,managed_base,trash):
    command=d_input[0]
    os.chdir(managed_base)
    if d_input[1]=="-b":
        print("not implemented yet")
    elif d_input[1]=="-r":
        rel_path=d_input[2]
        s_old_name=rel_path.split("/")
        new_name_path=d_input[3]
        s_new_name=d_input[3].split("/")
        if os.path.exists(rel_path):
            rename_helper(s_old_name,s_new_name)
        else:
            raise Exception("path to rename does not exist")
    else:
        rel_path=d_input[1]
        prefix=rel_path.split("/")[:-1]
        prefix.append(d_input[2])
        new_name_path="/".join(prefix)
        if os.path.exists(rel_path):
            os.rename(rel_path,new_name_path)
        raise Exception("path to rename does not exist")


def rename_helper(p_old_name,p_new_name):
    stack_new_name=list(reversed(p_new_name))
    full_new_name="/".join(p_new_name)
    p_new_name=[]
    stack_old_name=list(reversed(p_old_name))
    while len(p_old_name)!=0 and len(stack_new_name)!=0:
        last_name=stack_new_name.pop(0)
        prefix="/".join(p_old_name[:-1])
        old_name="/".join(p_old_name)
        n_name=prefix+"/" +last_name if prefix!="" else last_name
        if os.path.exists(old_name):
            os.rename(old_name,n_name)
        p_old_name.pop()
        p_new_name.append(last_name)
    if len(stack_new_name)>0:
        os.renames("/".join(reversed(p_new_name)),full_new_name)

def copy(d_input,managed_base,trash):
    os.chdir(managed_base)
    command=d_input[0]
    if d_input[1]=="-b":
        print("not implemented yet")
    elif d_input[1]=="-r":
        rel_path=d_input[2]
        last_folder=rel_path.split("/")[-1]
        destination=d_input[3]+"/"+last_folder
        if os.path.exists(rel_path) and os.path.exists(d_input[3]):
            shutil.copytree(rel_path,destination,dirs_exist_ok=True)
        else:
            if not os.path.exists(rel_path):
                raise Exception("path to copy does not exist")
            if not os.path.exist(d_input[3]):
                raise Exception("destination path does not exist")
    else:
        rel_path=d_input[1]
        destination=d_input[2]
        if os.path.exists(rel_path) and os.path.exists(destination):
            if os.path.isfile(rel_path):
                shutil.copy(rel_path,destination)
            else:
                lst=rel_path.split("/")
                folder_to_create=destination+"/"+lst[-1]
                os.mkdir(os.path.join(managed_base,folder_to_create))
        else:
            if not os.path.exists(rel_path):
                raise Exception("path to copy does not exist")
            if not os.path.exist(d_input[3]):
                raise Exception("destination path does not exist")


def move(d_input,managed_base,trash):
    os.chdir(managed_base)
    command=d_input[0]
    if d_input[1]=="-b":
        print("not implemented")
    else:
        rel_path=d_input[1]
        destination=d_input[2]
        if os.path.exists(rel_path) and os.path.exists(destination):
                shutil.move(rel_path,destination)
        else:
            if not os.path.exists(rel_path):
                raise Exception("path to move does not exist")
            if not os.path.exist(destination):
                raise Exception("destination path does not exist")



    
  










