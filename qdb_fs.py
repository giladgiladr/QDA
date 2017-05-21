import struct
import os
import sys


# this file implements the QDB file-system.
# for now, it will be a real file system.

# abstract class for file-system interface.
class GenericFileSystem(object):
    
    # returns file-like object that supports the file-methods "seek", "read", "write", "close", "tell", "truncate", "flush"
    @staticmethod
    def open(self, path, mode):
        raise "Abstract class!"
    @staticmethod    
    def close(self, file_obj):
        raise "Abstract class!"
    @staticmethod
    def mkdir(self, path):
        raise "Abstract class!"

    @staticmethod
    def exists(self, path):
        raise "Abstract class!"
        
class RealFileSystem(GenericFileSystem):
    def __init__(self, path):
        self.path = path
    @staticmethod
    def open(self, path, mode):
        return open(os.path.join(self.path, path), mode)
    @staticmethod
    def close(self, file_obj):
        file_obj.close()
    @staticmethod
    def mkdir(self, path):
        os.makedirs(path)
    @staticmethod
    def exists(self, path):
        return os.path.exists(os.path.join(self.path, path))
        
# Choose here the file-system
QFS = RealFileSystem



