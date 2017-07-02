import pickle

DISASM_UNIT_PROPERTY_TYPE_NONE = 0
DISASM_UNIT_PROPERTY_INSTRUCTION = 1
DISASM_UNIT_PROPERTY_DATA = 2
# Special properties that saved accross range of addresses and not per address.
DISASM_UNIT_PROPERTY_ADDR_TYPE = 1000

ADDR_TYPE_NONE = 0 # Invalid
ADDR_TYPE_INSTRUCTION = 1 # Should have DISASM_UNIT_PROPERTY_INSTRUCTION
ADDR_TYPE_DATA = 2 # Should have DISASM_UNIT_PROPERTY_DATA
ADDR_TYPE_UNINITIALIZE_DATA = 3 # Should have DISASM_UNIT_PROPERTY_DATA
ADDR_TYPE_UNDEFINE = 4 # initial state of every address.

class DisasmUnit(Unit):
    def __init__(self, binary_unit_id, processor_unit_id):
        self.diffs = {} # address to dict of properties
        self.binary_unit_id = binary_unit_id
        self.processor_unit_id = processor_unit_id
        
        self.ranges = [] # Every byte is initially undefined.
        
    # return the dict of diffs-properties for address
    def get_properties(self, addr):
        pass
    
    # replace the dict of diffs-properties for address
    def set_properties(self, addr, properties):
        pass
    
    # add a property to scpecific address
    def add_property(self, addr, prop):
        pass
    
    # this routine decided if an address is instruction or data etc.
    def _get_addr_type(self, addr):
        pass
        
    def get_property(self, addr, property_type):
        if (property_type == DISASM_UNIT_PROPERTY_INSTRUCTION):
            instruction = self.processor_unit_id.get_instruction(addr, self.binary_unit_id)
            if instruction == None:
                return None
            if self.diffs.has_key(addr):
                props = self.diffs[addr]
                if props.has_key(DISASM_UNIT_PROPERTY_INSTRUCTION):
                    instruction.opcode = props[DISASM_UNIT_PROPERTY_INSTRUCTION].opcode
                    if props[DISASM_UNIT_PROPERTY_INSTRUCTION].__dict__.has_key("operands"):
                        for idx, operand in props[DISASM_UNIT_PROPERTY_INSTRUCTION].operands.items():
                            instruction.operands[idx] = operand 
        elif property_type == DISASM_UNIT_PROPERTY_DATA:
            # get the data:
            if self.diffs.has_key(addr):
                props = self.diffs[addr]
                if props.has_key(DISASM_UNIT_PROPERTY_DATA):
                    data = 
        elif property_type == DISASM_UNIT_PROPERTY_ADDR_TYPE:
            return self._get_addr_type(addr)
        
        else:
            raise "No such property!"
    
    @staticmethod
    def from_data(data):
        return pickle.loads(filename)
    
    def to_data(self):
        return pickle.dumps(self)
    
    
    
    
class DisasmUnitProperty(object):
    def __init__(self):
        self.property_type = DISASM_UNIT_PROPERTY_TYPE_NONE
        self.data = None
        
DATA_TYPE_NONE = 0        
DATA_TYPE_BYTE = 1
DATA_TYPE_WORD = 2
DATA_TYPE_DWORD = 3
DATA_TYPE_QWORD = 4
DATA_TYPE_STRING = 5
DATA_TYPE_UNDEFINE = 6

STRING_TYPE_ASCII = 0
STRING_TYPE_UNICODE = 1
class DisasmUnitPropertyData(DisasmUnitProperty):
    def __init__(self):
        self.data_type = DATA_TYPE_NONE
    
    def _del_members(self):
        self.read_size = None
        del self.read_size
        
        self.string_type = None
        del self.string_type
    
    def set_data_type_byte(self):
        self._del_members(self)
        self.data_type = DATA_TYPE_BYTE
        self.read_size = 1
    
    def set_data_type_word(self):
        self._del_members(self)
        self.data_type = DATA_TYPE_WORD
        self.read_size = 2
    
    def set_data_type_dword(self):
        self._del_members(self)
        self.data_type = DATA_TYPE_DWORD
        self.read_size = 4
    
    def set_data_type_qword(self):
        self._del_members(self)
        self.data_type = DATA_TYPE_QWORD
        self.read_size = 8
        
    def set_data_type_string(self, string_type):
        self._del_members(self)
        self.data_type = DATA_TYPE_STRING
        self.string_type = STRING_TYPE_ASCII
        
class DisasmUnitPropertyInstruction(DisasmUnitProperty):
    def __init__(self):
        pass
        
    def change_opcode(self, opcode):
        self.opcode = opcode
    
    def change_operand(self, operand_idx, operand)
        if not self.__dict__.has_key("operands"):
            self.operands = {}
        self.opreands[operand_idx] = operand
        

        
class Data(object):
    def __init__(self, data_type, string_type = None):
        self.data_type = data_type
        if data_type == DATA_TYPE_STRING
            self.string_type = STRING_TYPE_ASCII
        
    def 
        
class Instruction(object):
    def __init__(self, opcode, operands):
        self.opcode = opcode
        self.operands = operands
        pass
    
class Opcode(object):
    def __init__(self, opcode_id)
        self.id = opcode_id

class Operand(object):
    OPER_TYPE_NONE = 0
    OPER_TYPE_REGISTER = 1
    OPER_TYPE_IMMEDIATE = 2
    pass
        
class RegisterOperand(Operand):
    def __init__(self, reg_id):
        self.operand_type = OPER_TYPE_REGISTER
        self.id = reg_id

class ImmediateOperand(Operand):
    OPER_IMMED_TYPE_BIN = 0
    OPER_IMMED_TYPE_OCT = 1
    OPER_IMMED_TYPE_DEC = 2
    OPER_IMMED_TYPE_HEX = 3
    OPER_IMMED_TYPE_STACK = 4
    OPER_IMMED_TYPE_OFFSET = 5
    def __init__(self, immed_type):
        self.operand_type = OPER_TYPE_IMMEDIATE
        self.immed_type = immed_type
    """
    def set_immed_type(self, immed_type, data = None)
        self.immed_type = immed_type
        if immed_type == OPER_IMMED_TYPE_OFFSET:
            self.data = data
        else:
            del self.data
    """
    