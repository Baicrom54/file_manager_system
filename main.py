from simplest_commands import *
from history_workflow_ops import *
import os

def main():
    managed_base=None
    trash=None
    while not managed_base or not trash:
        managed_base=input("Insert path to manage: ")
        trash=input("Insert trash directory: ")
        if not os.path.exists(managed_base):
            managed_base=None
        if not os.path.exists(trash):
            trash=None
    print("Starting proccess completed")
    user_input=input().strip()
    while user_input!="quit":
        try:
            handle_commands(user_input,managed_base,trash)
        except Exception as e:
            print(f"Error:{e}")
        user_input=input().strip()

    


if __name__=="__main__":
    main()