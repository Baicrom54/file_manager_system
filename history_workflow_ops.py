from collections import deque
from simplest_commands import *

def appender():
    stack=deque([])
    def append_stack(record_dict=None):
        nonlocal stack
        if record_dict:
            stack.append(record_dict)
        return stack
    return append_stack


done_operations_app=appender()
undone_operations_app=appender()
history_app=appender()

def handle_commands(input,managed_base,trash):
    d_input=input.split(" ")
    command=d_input[0]
    done_stack=done_operations_app()
    undone_stack=undone_operations_app()
    match command:
        case "create":
            num_file_created=create(d_input,managed_base,trash)
            history_app(input) 
            s_input=input.split(" ")
            if num_file_created and s_input[-1]!=str(num_file_created):
                done_operations_app(input+ f" {num_file_created}")
            else:
                done_operations_app(input)         
        case "delete":
            delete(d_input,managed_base,trash)
            history_app(input) 
            done_operations_app(input)  

        case "move":
            move(d_input,managed_base,trash)
            history_app(input) 
            done_operations_app(input)  

        case "rename":
            rename(d_input,managed_base,trash)
            history_app(input) 
            done_operations_app(input)     
        case "copy":
            copy(d_input,managed_base,trash)
            history_app(input) 
            done_operations_app(input)  

        case "history":
            history_lst=list(history_app())
            for index,action in enumerate(history_lst,start=1):
                print(f"{index}.{action}")    
        case "undo":
            try:
                last_action=done_stack.popleft()
                undo(last_action,managed_base,trash)
                history_app().popleft
                undone_operations_app(last_action)
                history_app(input)
            except IndexError:
                raise Exception("no actions to undo")
        case "redo":
            try:
                last_undone_action=undone_stack.popleft()
                redo(last_undone_action,managed_base,trash)
                history=history_app()
                history.popleft()
                history_app(input)
            except IndexError:
                raise Exception("no action to redo")

        case "quit":
            return 
        case "set_managed_dir":
            old_managed_base=managed_base
            managed_base=d_input[1]
            done_operations_app(input + f" {old_managed_base}" )
            history_app(input)
        case "set_trash_dir":
            old_trash=trash
            trash=d_input[1]
            done_operations_app(input + f" {old_trash}")
            history_app(input)
        case _:
            raise Exception("invalid command")
    print(f"done stack:{done_stack}\n undone stack:{undone_stack}\n")




def redo(last_undone,managed_base,trash):
    handle_commands(last_undone,managed_base,trash)
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

    

def undo(last_action,managed_base,trash):
    s_last_action=last_action.split(" ")
    if s_last_action[0]=="create":
        s_last_action[0]="delete"
        ns_last_action=[command for command in s_last_action if command!="-r"]
        if len(s_last_action)>len(ns_last_action):
            num_file_created=ns_last_action.pop()
            s_path_to_delete=ns_last_action[1].split("/")[:-(int(num_file_created)-1)]
            ns_last_action[1]="/".join(s_path_to_delete)
        delete(ns_last_action,managed_base,trash)
            
    elif s_last_action[0]=="delete":
        s_last_action[0]="move"
        s_path=s_last_action[1].split("/")
        s_last_action[1]=trash+"/"+s_path[-1]
        if len(s_path)!=1:
            s_last_action.append("/".join(s_path[:-1]))
        else:
            s_last_action.append(".")
        move(s_last_action,managed_base,trash)
    elif s_last_action[0]=="copy":
        s_last_action[0]="delete"
        ns_last_action=[command for command in s_last_action if command!="-r"]
        copied_folder=ns_last_action[1].split("/")[-1]
        ns_last_action[1]=ns_last_action[2]+"/"+copied_folder
        delete(ns_last_action,managed_base,trash)
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
                rename(s_last_action,managed_base,trash)
           elif len(f_old_name)<len(new_name):
                prefix=new_name[:-(len(f_old_name))]
                prefix.append(f_old_name[0])
                s_last_action[2]="/".join(new_name)
                s_last_action[3]="/".join(f_old_name)
                move_script=["move","/".join(prefix),"."]
                delete_script=["delete",prefix[0]]
                rename(s_last_action,managed_base,trash)
                move(move_script,managed_base,trash)
                delete(delete_script,managed_base,trash)
           else:
                s_last_action[2]="/".join(new_name)
                s_last_action[3]="/".join(f_old_name)
                rename(s_last_action,managed_base,trash)
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
        rename(s_last_action,managed_base,trash)

    elif s_last_action[0]=="set_managed_dir":
        s_last_action[1]=s_last_action[2]
        s_last_action.popleft()
        handle_commands(" ".join(s_last_action),managed_base,trash)
        history=history_app()
        history.popleft()
    elif s_last_action[0]=="set_trash_dir":
        s_last_action[1]=s_last_action[2]
        s_last_action.pop()
        handle_commands(" ".join(s_last_action),managed_base,trash)
        history=history_app()
        history.popleft()

    else:
        temp=s_last_action[1]
        s_temp=temp.split("/")
        s_last_action[1]=s_last_action[2] + "/" + s_temp[-1]
        s_last_action[2]="/".join(s_temp[:-1])
        move(s_last_action,managed_base,trash)
    return s_last_action









                    

                


