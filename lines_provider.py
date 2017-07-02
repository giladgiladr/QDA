
# The term line-number is a running number starts with 0 that is the actual logical line number that
# the gui will present.
# The line_id term, is a LinesProvider implementation specific object that the LineProvider uses
# in order to manage the get_next and get_prev functions.
class LinesProvider(object):
    def __init__(self):
        raise "Abstract"

    # returns some number that correlated to the number of lines that we have.
    # Not have to be accurate.
    def get_num_of_lines(self):
        pass

    # returns line_id from line number where line number starts with 0.
    # Not have to be accurate.
    def get_line_from_line_number(self, line_number):
        pass

    # returns tuple of (line_id, "line")
    # If line_id is the first line, returns it.
    # If line_id is smaller the the first line, returns the first line.
    def get_previous_line(self, line_id):
        pass

    # returns tuple of (line_id, "line")
    # If line_id is the last line, returns it.
    # If line_id is bigger then the last line, returns the last line.
    def get_next_line(self, line_id):
        pass


class DisassembleLinesProvider(LinesProvider):
    BUFFER_SIZE = 0x1000
    def __init__(self, disassembler_iface):
        self.diface = disassembler_iface
        self.buffer = [] # every element is (addr, [text_lines])
        self.buffer_first_addr = 0
        self.buffer_size = -1
        self.buffer_valid = False
        self.minimum_addr = 0
        self.maximum_addr = 0x100000
    def get_num_of_lines(self):
        return self.maximum_addr - self.minimum_addr

    def get_line_from_line_number(self, line_number):
        line_id = (self.diface.get_closest_base_address(self.minimum_addr + line_number), 0)
        return line_id

    # fix the buffer.
    # The start address for fill up is cur_buf[0] address if cur_buf is not None. if is None, then "start_addr"
    # The start address for fill down is cur_buf[-1] address if cur_buf is not None. if is None, then "start_addr"
    def _create_buffer(self, up, down, cur_buf, start_addr):
        #for i in xrange(up):
        pass

    def get_prevoius_line(self, line_id):
        (addr, sub_addr, buffer_idx) = line_id
        # If the previous line is inside the buffer:
        if buffer_idx < self.buffer_size: # We in the buffer. In that case, the addr has entry in the buffer, and sub_addr could not be -1.
            if sub_addr > 0: # Get the prev sub_addr:
                ret_addr, text_lines = self.buffer[buffer_idx]
                assert ret_addr == addr
                ret_line_text = text_lines[sub_addr - 1]
                return (ret_addr, sub_addr - 1, buffer_idx), ret_line_text
            elif buffer_idx > 0: # Get the prev addr:
                ret_addr, text_lines = self.buffer[buffer_idx-1]
                ret_line_text = text_lines[-1]
                return (ret_addr, len(text_lines) - 1, buffer_idx - 1), ret_line_text
            else: # We at the start of the buffer and want the previous line. We need to shift the buffer:
                self._adjust_buffer()
        else: # We not in the buffer. In that case, sub_addr have to be -1 (last sub_line) or 0 (first sub_line).
            # create new buffer
            pass


        if sub_addr > 0: # That means that the buffer contains the previous.
            return self.buffer[addr - self.buffer_first_addr][sub_addr - 1]
        if self.buffer_first_addr <= line_num and self.buffer_first_addr + self.buffer_num_addrs > line_num:
            pass
        buf_line_num = line_num - DisassembleLinesProvider.BUFFER_SIZE/2
        buf_line_num = self.diface.get_closest_base_address(buf_line_num, search_up_first=True)

        return get_address_text(ret_line_num)

    def get_next_line(self, line_id):
        pass

#line_id here is a tuple of (address, address_text_line_num). because every address could have couple of lines.
class DisassembleLinesProvider2(LinesProvider):
    def __init__(self, d_iface):
        self.diface = d_iface
    # returns some number that correlated to the number of lines that we have.
    # Not have to be accurate.
    def get_num_of_lines(self):
        return self.diface.get_max_address() - self.diface.get_min_address()
    # returns line_id from line number where line number starts with 0.
    # Not have to be accurate.
    def get_line_from_line_number(self, line_number):
        addr = self.diface.get_min_address() + line_number
        addr = self.diface.get_closest_base_address(addr)
        return (addr, 0), self.diface.get_address_text(addr)[0]

    # returns tuple of (line_id, "line")
    # If line_id is the first line, returns it.
    # If line_id is smaller the the first line, returns the first line.
    def get_previous_line(self, line_id):
        addr, addr_line_num = line_id
        if (addr_line_num > 0):
            return ((addr, addr_line_num-1), self.diface.get_address_text(addr)[addr_line_num-1])
        else:
            prev_addr = self.diface.get_closest_base_address(addr-1, search_up_first = True)
            lines = self.diface.get_address_text(prev_addr)
            assert len(lines) >= 1
            return ((prev_addr, len(lines)-1), lines[-1])

    # returns tuple of (line_id, "line")
    # If line_id is the last line, returns it.
    # If line_id is bigger then the last line, returns the last line.
    def get_next_line(self, line_id):
        addr, addr_line_num = line_id
        lines = self.diface.get_address_text(addr)
        if addr_line_num+1 < len(lines):
            return ((addr, addr_line_num+1), lines[addr_line_num+1])
        else:
            next_addr = self.diface.get_closest_base_address(addr+1, search_up_first = False)
            lines = self.diface.get_address_text(next_addr)
            assert len(lines) >= 1
            return ((next_addr, 0), lines[0])

class DisassemblerInterface(object):
    def __init__(self):
        pass

    # The function returns the closest address that is exists and its not in middle of data / opcode.
    def get_closest_base_address(self, addr, search_up_first = False):
        raise

    # returns list of lines. raise if address is not valid.
    def get_address_text(self, addr):
        raise

    def get_min_address(self):
        raise

    def get_max_address(self):
        raise

import md5
import random
import struct
class MockDisassemblerInterface(object):
    opcodes = [("MOV", 2), ("LEA", 2), ("SUB", 2), ("JMP", -1),("JNE", -1), ("ADD", 2), ("INT", -1), ("PASTEN", 0), ("MOVE", 2), ("HLT",0), ("SYSCALL", 1) , ("PUSH",1), ("POP",1) ,("PUSHA",0) ,("POPA",0), ("NOP",0)]
    operands = ["RAX", "RDX", "RCX", "RBX", "RBP", "RSP", "REX", "RFX", "R8", "R9", "R10", "R11", "R12", "R13", "ROT", "R14"]
    comments = [x.replace("\n","").replace("\r","").strip() for x in open("MockTextFile.txt","rb").read().split(".")]

    datas = ["db","dh","dd","dq"]

    def __init__(self):
        pass

    # The function returns the closest address that is exists and its not in middle of data / opcode.
    def get_closest_base_address(self, addr, search_up_first = False):
        orig_addr = addr
        if md5.md5(str(addr)).digest()[15] < 0x60:
            return addr
        found = True
        if search_up_first:
            while ord(md5.md5(str(addr)).digest()[15]) >= 0x60:
                addr-=1
                if addr <= self.get_min_address():
                    found = False
                    break
            if found:
                return addr
            addr = orig_addr
            while ord(md5.md5(str(addr)).digest()[15]) >= 0x60:
                addr += 1
                if addr >= self.get_max_address():
                    return None
            return addr

        else:
            while ord(md5.md5(str(addr)).digest()[15]) >= 0x60:
                addr+=1
                if addr >= self.get_max_address():
                    found = False
                    break

            if found:
                return addr
            addr = orig_addr
            while ord(md5.md5(str(addr)).digest()[15]) >= 0x60:
                addr -= 1
                if addr >= self.get_max_address():
                    return None
            return addr


    # returns list of lines. raise if address is not valid.
    def get_address_text(self, addr):
        lines = []
        hash = md5.md5(str(addr)).digest()
        assert ord(hash[15]) < 0x60 # start of opcode / data.
        addr_len = 1
        while ord(md5.md5(str(addr + addr_len)).digest()[15]) >= 0x60:
            addr_len += 1
        assert len(hash) == 16
        is_data = True in [(ord( md5.md5(str(addr - i)).digest()[0]) < 0x4) for i in xrange(0x10)]
        if is_data:

            lines.append(".data:0x%08X "%addr + " ".join(map(lambda x:x.encode("hex").upper(), hash[1:1 + addr_len])).ljust(42) +\
                         "%s"%MockDisassemblerInterface.datas[ord(hash[14])%1] +\
                         " " +\
                         ", ".join(map(lambda x:"%d"%(ord(x)), hash[1:1 + addr_len])))
            #addr_len *= (2 ** (ord(hash[14]) % 4))
        else: # code:

            lines.append(".text:0x%08X " %addr + " ".join(map(lambda x: x.encode("hex").upper(), hash[1:1 + addr_len])).ljust(42) +\
                         "%s"%MockDisassemblerInterface.opcodes[ord(hash[14])%16][0].ljust(8) + \
                         ", ".join([MockDisassemblerInterface.operands[ord(hash[i+2])%len(MockDisassemblerInterface.operands)] \
                                    for i in xrange(MockDisassemblerInterface.opcodes[ord(hash[14])%16][1])]))
        num_of_lines = 1 + (ord(hash[0]) % 9) - 6


        #print num_of_lines, ord(hash[0])%8
        if num_of_lines < 0:
            num_of_lines = 0
        else:
            if num_of_lines > 1:
                num_of_lines *= 2
            comment_offset = 67
           # print struct.unpack("<I", hash[10:14])[0], struct.unpack("<I", hash[10:14])[0]%len(MockDisassemblerInterface.comments)
            lines[0] = lines[0].ljust(comment_offset) + " ; " + MockDisassemblerInterface.comments[(struct.unpack("<I", hash[10:14])[0])%len(MockDisassemblerInterface.comments)]
            cur = hash[10:14]
            for i in xrange(num_of_lines-1):
                cur = md5.md5(str(cur)).digest()[0:4]
            #    print struct.unpack("<I", hash[10:14])[0], struct.unpack("<I", cur)[0] % len(MockDisassemblerInterface.comments)
                lines.append(lines[0][:16].ljust(comment_offset) + " ; " + MockDisassemblerInterface.comments[struct.unpack("<I", cur)[0]%len(MockDisassemblerInterface.comments)])
        return lines

    def get_min_address(self):
        return 0

    def get_max_address(self):
        return 0xfffffff

if __name__ == '__main__':
    a = MockDisassemblerInterface()
    i = a.get_min_address() - 1
    while True:
        #print i
        i = a.get_closest_base_address(i+1, False)
        #print i
        lines = a.get_address_text(i)
        for j in lines:
            print j
        raw_input()
