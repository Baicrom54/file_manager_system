import unittest
from commands import create,delete,rename,rename_helper,call_history
import os
import shutil
managed_base="/home/baicrom/workspace/github.com/Baicrom54/file_manager/managed_dir"
trash="/home/baicrom/workspace/github.com/Baicrom54/file_manager/trash"
flags=os.O_RDWR | os.O_CREAT

class Test_Get_Command(unittest.TestCase):
    def test_single_file(self):
        create(["create","bho.py"])
        self.assertEqual(os.path.exists(os.path.join(managed_base,"bho.py")),True)
        os.remove(os.path.join(managed_base,"bho.py"))

    def test_one_directory_file(self):
        create(["create","-r","mrc/bho.py"])
        self.assertEqual(os.path.exists(os.path.join(managed_base,"mrc/bho.py")),True)
        os.chdir(managed_base)
        shutil.rmtree("mrc")

    def test_multiple_directory_file(self):
        create(["create","-r","src/zio_pera/bho.py"])
        self.assertEqual(os.path.exists(os.path.join(managed_base,"src/zio_pera/bho.py")),True)
        os.chdir(managed_base)
        shutil.rmtree("src")

class Test_Rename_Command(unittest.TestCase):
    def test_rename_nr(self):
        os.chdir(managed_base)
        fd=os.open("bho.py",flags)
        os.close(fd)
        rename(["rename","bho.py","maybe.py"])
        self.assertEqual(os.path.exists(os.path.join(managed_base,"maybe.py")),True)
        os.remove("maybe.py")
    def test_rename_r_equal_lenght(self):
        os.chdir(managed_base)
        os.mkdir("src")
        os.mkdir("src/zio_pera")
        fd=os.open("src/zio_pera/bho.py",flags)
        os.close(fd)
        rename(["rename","-r","src/zio_pera/bho.py", "rcc/zio_mela/maybe.py"])
        self.assertEqual(os.path.exists(os.path.join(managed_base,"rcc/zio_mela/maybe.py")),True)
        shutil.rmtree("rcc")
    
    def test_rename_r_with_buffer(self):
        os.chdir(managed_base)
        os.mkdir("rcc")
        os.mkdir("rcc/zio_mela")
        fd=os.open("rcc/zio_mela/maybe.py",flags)
        os.close(fd)
        rename(["rename","-r","rcc/zio_mela/maybe.py","buffer0/buffer1/lcc/zio_ban/puf.py"])
        self.assertEqual(os.path.exists(os.path.join(managed_base,"buffer0/buffer1/lcc/zio_ban/puf.py")),True)
        shutil.rmtree("buffer0")

class Test_Delete_Command(unittest.TestCase):
    def test_delete_file(self):
        os.chdir(managed_base)
        fd=os.open("maybe.py",flags)
        os.close(fd)
        delete(["delete","maybe.py"])
        self.assertEqual(os.path.exists(os.path.join(trash,"maybe.py")),True)
        shutil.rmtree(trash)
        os.mkdir(trash)
    def test_delete_recursively(self):
        os.chdir(managed_base)
        os.mkdir("mrc")
        fd=os.open("mrc/bho.py",flags)
        os.close(fd)
        delete(["delete","mrc"])
        self.assertEqual(os.path.exists(os.path.join(trash,"mrc")),True)
        shutil.rmtree(trash)
        os.mkdir(trash)


class Test_History_Commands(unittest.TestCase):
    def test_history:
        create(["create","-r","mrc/bho.py"])
        create(["create","-r","src/zio_pera/bho.py"])
        rename(["rename","-r","src/zio_pera/bho.py", "rcc/zio_mela/maybe.py"])












