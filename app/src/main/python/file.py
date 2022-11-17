from os.path import dirname, join
from com.chaquo.python import Python

def main():
     files_dir = str(Python.getPlatform().getApplication().getFilesDir())
     filename = join(dirname(files_dir),"newfile.txt")

     with open(filename, 'w', encoding = 'utf8', errors = "ignore") as f:
        f.write("This is file")
        f.close()

     with open(filename, 'r', encoding = 'utf8', errors = "ignore") as f:
        data = f.read()

     return ""+data