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
managed_base="/home/baicrom/workspace/github.com/Baicrom54/file_manager/managed_dir"
trash="/home/baicrom/workspace/github.com/Baicrom54/file_manager/trash"


def appender():
    stack=deque([])
    def append_stack(record_dict=None):
        nonlocal stack
        if record_dict:
            stack.appendleft(record_dict)
        return stack
    return append_stack

done_operations_app=appender()
undone_operations_app=appender()
history_app=appender()

def handle_commands(input):
    d_input=input.split(" ")
    command=d_input[0]
    done_stack=done_operations_app()
    undone_stack=undone_operations_app()
    match command:
        case "create":
            num_file_created=create(d_input)
            history_app(input) 
            s_input=input.split(" ")
            print(s_input)
            if num_file_created and s_input[-1]!=str(num_file_created):
                done_operations_app(input+ f" {num_file_created}")
            else:
                done_operations_app(input)         
        case "delete":
            delete(d_input)
            history_app(input) 
            done_operations_app(input)  

        case "move":
            move(d_input)
            history_app(input) 
            done_operations_app(input)  

        case "rename":
            rename(d_input)
            history_app(input) 
            done_operations_app(input)     
        case "copy":
            copy(d_input)
            history_app(input) 
            done_operations_app(input)  

        case "history":
            history_lst=list(history_app())
            history_s="\n".join(history_lst)
            print(history_lst)     
        case "undo":
            last_action=done_stack.popleft()
            undo(last_action)
            history_app().popleft
            undone_operations_app(last_action)
            history_app(input)
        case "redo":
            last_undone_action=undone_stack.popleft()
            redo(last_undone_action)
            history=history_app()
            history.popleft()
            history_app(input)

        case "quit":
            return 
        case _:
            raise Exception("invalid command")
    print(f"done stack:{done_stack}\n undone stack:{undone_stack}")


def create(d_input,valid_file_extension=valid_file_extension,managed_base=managed_base):
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
            raise Exception("path not found use -r flag to create it or insert an existing path before the folder to add")



        


def delete(d_input,managed_base=managed_base):
    os.chdir(managed_base)
    command=d_input[0]
    if d_input[1]=="-b":
        print("not implemented")
    else:
        rel_path=d_input[1]
        if os.path.exists(os.path.join(managed_base,rel_path)):
            shutil.move(rel_path,trash)

    
        
def rename(d_input,managed_base=managed_base):
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
        rel_path=d_input[1]
        prefix=rel_path.split("/")[:-1]
        prefix.append(d_input[2])
        new_name_path="/".join(prefix)
        if os.path.exists(rel_path):
            os.rename(rel_path,new_name_path)


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

def copy(d_input,managed_base=managed_base):
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
        rel_path=d_input[1]
        destination=d_input[2]
        if os.path.exists(rel_path) and os.path.exists(destination):
            if os.path.isfile(rel_path):
                shutil.copy(rel_path,destination)
            else:
                lst=rel_path.split("/")
                folder_to_create=destination+"/"+lst[-1]
                os.mkdir(os.path.join(managed_base,folder_to_create))


def move(d_input,managed_base=managed_base):
    os.chdir(managed_base)
    command=d_input[0]
    if d_input[1]=="-b":
        print("not implemented")
    else:
        rel_path=d_input[1]
        destination=d_input[2]
        if os.path.exists(rel_path) and os.path.exists(destination):
                shutil.move(rel_path,destination)

def redo(last_undone):
    handle_commands(last_undone)
    s_last_undone=last_undone.split(" ")
    num_created=s_last_undone[-1]
    if s_last_undone[0]=="create":
        os.chdir(trash)
        if s_last_undone[1]!="-r":
            os.remove(s_last_undone[1])
        else:
            folder_to_remove=s_last_undone[2].split("/")[-int(num_created)]
            shutil.rmtree(folder_to_remove)
    elif s_last_undone[0]=="copy":
        os.chdir(trash)
        if s_last_undone[1]!="-r":
            os.remove(s_last_undone[1])
        else:
            folder_to_remove=s_last_undone[2].split("/")[-1]
            shutil.rmtree(folder_to_remove)
    os.chdir(managed_base)

    

def undo(last_action):
    s_last_action=last_action.split(" ")
    if s_last_action[0]=="create":
        s_last_action[0]="delete"
        ns_last_action=[command for command in s_last_action if command!="-r"]
        if len(s_last_action)>len(ns_last_action):
            num_file_created=ns_last_action.pop()
            s_path_to_delete=ns_last_action[1].split("/")[:-(int(num_file_created)-1)]
            ns_last_action[1]="/".join(s_path_to_delete)
        delete(ns_last_action)
            
    elif s_last_action[0]=="delete":
        s_last_action[0]="move"
        s_path=s_last_action[1].split("/")
        s_last_action[1]=trash+"/"+s_path[-1]
        if len(s_path)!=1:
            s_last_action.append("/".join(s_path[:-1]))
        else:
            s_last_action.append(".")
        move(s_last_action)
    elif s_last_action[0]=="copy":
        s_last_action[0]="delete"
        ns_last_action=[command for command in s_last_action if command!="-r"]
        copied_folder=ns_last_action[1].split("/")[-1]
        ns_last_action[1]=ns_last_action[2]+"/"+copied_folder
        delete(ns_last_action)
    elif s_last_action[0]=="rename":
        if s_last_action[1]=="-r":
           f_old_name=s_last_action[2].split("/")
           new_name=s_last_action[3].split("/")
           if len(f_old_name)>len(new_name):
                prefix=f_old_name[:-(len(new_name))]
                undo_name=f_old_name[len(prefix)-1:]
                prefix.extend(new_name)
                s_last_action[2]="/".join(prefix)
                s_last_action[3]="/".join(undo_name)
                rename(s_last_action)
           elif len(f_old_name)<len(new_name):
                prefix=new_name[:-(len(f_old_name))]
                prefix.append(f_old_name[0])
                s_last_action[2]="/".join(new_name)
                s_last_action[3]="/".join(f_old_name)
                move_script=["move","/".join(prefix),"."]
                delete_script=["delete",prefix[0]]
                rename(s_last_action)
                move(move_script)
                delete(delete_script)
           else:
                s_last_action[2]="/".join(new_name)
                s_last_action[3]="/".join(f_old_name)
                rename(s_last_action)
        else:
            temp=s_last_action[1]
            prefix=temp.split("/")[:-1]
            f_name=temp.split("/")[-1]
            if len(prefix)==0:
                s_last_action[1]=s_last_action[2]
                s_last_action[2]=temp
            else:
                prefix.append(s_last_action[2])
                s_last_action[1]="/".join(prefix)
                s_last_action[2]=f_name
        rename(s_last_action)
    else:
        temp=s_last_action[1]
        s_temp=temp.split("/")
        s_last_action[1]=s_last_action[2] + "/" + s_temp[-1]
        s_last_action[2]="/".join(s_temp[:-1])
        move(s_last_action)
    return s_last_action

    
  










