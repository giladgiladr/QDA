import os
import sys
import struct
import socket



# An abstract class of log records.
# Every log record should implement this interface.
#
# Log record contains common header, and per-log-record user data.
# This class implements the header, and define the interface for implementing the data.
class LogRecord(object):
    HEADER_SIZE = 0x28
    def __init__(self, log_size = LogRecord.HEADER_SIZE, type = RECORD_TYPE_NONE, message_id = 0, timestamp = 0, flags = None):
        assert log_size >= LogRecord.HEADER_SIZE
        self.log_size = log_size
        self.message_id = message_id
        self.type = type
        self.timestamp = timestamp
        self.flags = None
        
  # Log records API:
    
    # Creates and returns log record from the data.
    @staticmethod
    def from_data(self, data):
        size, type = struct.unpack("<QQ", data[:0x10])
        assert len(data) == size
        log_record = LogTypes.create_object(type)
        log_record.decode(data)
        return log_record
        
    # serialize the current log message to a buffer.
    def encode(self):
        data = self._encode_data()
        self.log_size = LogRecord.HEADER_SIZE + len(data)
        header = struct.pack("<QQQQQ", self.log_size, self.message_id, self.type, self.timestamp, self.flags)
        return header + data
        
    # deserialize log-message from buffer.
    def decode(self, data):
        assert len(data) > LogRecord.HEADER_SIZE
        self.log_size, self.type, self.message_id, self.timestamp, self.flags = struct.unpack("<QQQQQ", data[0:LogRecord.HEADER_SIZE])
        assert len(data) == self.log_size
        data = data[LogRecord.HEADER_SIZE:]
        self._decode_data(data)
    
    # returns new LogRecord object that represent the opposite action of the current log-message.
    def reverse(self):
        return self._reverse()
        
    # returns printable string of the log message.
    def dump(self):
        ret = ""
        ret += "TODO: CLASS NAME(0x%x): id=0x%x, ts=0x%x, data_size=0x%x flags=%d\n"%(self.type, self.id, self.timestamp, self.data_size, self.flags)
        data_dump = self._dump_data().replace("\n","\n\t")
        return ret + data_dump
        
  # Per-inheriting class methods that should be implements by inheriting classes.
    
    # This method gets raw-data of the log record and deserialize it.
    def _decode_data(self, data):
        raise "Should be implement by intheriting classes!"
    
    # This method produce buffer that contains the user-data.
    def _encode_data(self):
        raise "Should be implement by intheriting classes!"
    
    # Returns printable string that desribes the log message.
    def _dump_data(self):
        raise "Should be implement by intheriting classes!"
    
    # The method should create a log-message that describes the opposite action of the current log message.
    # The method responsible to create a new object and to return it.
    def _reverse(self):
        raise "Should be implement by intheriting classes!"

# define log container:
class LogsContainer(LogRecord):
    def __init__(self, records = []):
        LogRecord.__init__(type = RECORD_TYPE_CONTAINER)
        self.records = records
        
    def _decode_data(data):
        self.records = []
        while len(data) > 0:
            size = struct.unpack("<Q", data[:8])
            assert len(data) >= size
            rec_data = data[:size]
            data = data[size:]
            self.records.append(LogRecord.from_data(data))
        
    def _encode_data(self):
        ret = ""
        for i in self.records:
            ret += i.encode()
        return ret
    
    def _dump_data(self):
        return "\n".join([i.dump().replace("\n","\n") for i in self.records])
        
    def _reverse(self):
        reverse_records = [record.reverse() for record in self.records][::-1]
        return LogsContainer(reverse_records)
    
# Log types:
RECORD_TYPE_NONE = 0
RECORD_TYPE_CONTAINER = 1

# singelton that create logs-object from types
class LogTypes(object):
    log_types = LogTypes()
    def __init__(self):
        self.types = {RECORD_TYPE_NONE:None,
                      RECORD_TYPE_CONTAINER:LogsContainer}
    
    @staticmethod
    def register_type(_class, type):
        assert not LogTypes.log_types.has_key(type)
        LogTypes.log_types[type] = _class
    
    @staticmethod
    def create_object(type):
        return LogTypes.log_types[type]()
            
     
# This class manages the log
# It use the log file that store the logs, and another
# index file for fast access to log-records.
class LogManager(object):
    LOG_FILE_NAME = "log.bin"
    LOG_INDEX_FILE_NAME = "log.idx"
    def __init__(self, log_folder):
        log_path = 
        if QFS.exists(log_path):
            mode = "r+b"
        else:
            mode = "wb"
        self.log_file = QFS.open(os.path.join(log_folder, LOG_FILE_NAME), mode)
        self.log_idx = QFS.open(os.path.join(log_folder, LOG_INDEX_FILE_NAME), mode)
        
        self.log_file.seek(0,2) # seek to the end
        self.log_size = self.log_file.tell()
        self.log_idx.seek(0,2) # seek to the end
        
    def write_record(self, log_record):
        log_data = log_record.encode()
        self.log_file.write(log_data)
        self.log_idx.write(struct.pack("<I", self.log_size))
        self.log_size += len(log_data)
        return
        
    def read_record(self, idx):
        self.log_idx.seek(idx*4)
        offset = struct.unpack("<I", self.log_idx.read(4))[0]
        self.log_file.seek(offset)
        rec_size = struct.unpack("<Q", self.log_file.read(8))
        self.log_file.seek(offset)
        log_record_data = self.log_file.read(rec_size)
        assert len(log_record_data) == rec_size
        return LogRecord.from_data(log_record_data)
    
    def read_records(self, start, count):
        ret = []
        for i in xrange(count):
            ret += self.read_record(start + i)
        return ret
    
    def delete_last_record(self):
        self.log_idx.seek(-4,2)
        self.log_idx.truncate(self.log_idx.tell())
        offset = struct.unpack("<I", self.log_idx.read(4))
        self.log_file.truncate(offset)
        self.log_idx.flush()
        self.log_file.flush()