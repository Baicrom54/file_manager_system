from commands import *
def main():
    user_input=None
    while user_input!="quit":
        user_input=input().strip()
        handle_commands(user_input)

    


if __name__=="__main__":
    main()