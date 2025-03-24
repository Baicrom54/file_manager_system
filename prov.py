def delete(d_input,managed_base=managed_base):
    if d_input[1]=="-b":
        print("not implemented")
    elif d_input[1]=="-r":
        rel_path=d_input[2]
        path=os.path.join(managed_base,rel_path)
        if os.path.exists(path):
            os.chdir(managed_base)
            shutil.rmtree(rel_path)
        else:
            raise Exception("Path not found")
    else:
        rel_path=d_input[1]
        path=os.path.join(managed_base,rel_path)
        if os.path.exists(path):
            if os.path.isfile(os.path.join(managed_base,rel_path)):
                os.remove(os.path.join(managed_base,rel_path))
            else:
                os.rmdir(os.path.join(managed_base,rel_path))
        else:
            raise Exception("Path not found")

