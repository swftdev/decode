from dataclasses import dataclass
from enum import IntEnum, auto

class W(IntEnum):
    BYTE = auto()
    WORD = auto()

class Operator(IntEnum):
    MOV_RMTFR = auto() # Register/memory to/from register
    MOV_ITRM = auto()  # Immediate to register/memory
    MOV_ITR = auto()   # Immediate to register
    MOV_MTA = auto()   # Memory to accumulator
    MOV_ATM = auto()   # Accumulator to memory
    MOV_RMTSR = auto() # Register/memory to segment register
    MOV_SRTRM = auto() # Segment register to register/memory

op_to_byte_count = {
    Operator.MOV_RMTFR: 4
}

class Fields():
    w: W
    d: None
    mod: None
    reg: None
    r_m: None

class Instruction:
    op: Operator
    fields: Fields
    data: list[str]
    
    #[s:inclusive : stop:exclusive]

# w: b, index

op_to_fields = {
    Operator.MOV_RMTFR: [(W, 0, 7)]
}

# def W_FLAG(b, i):
#     match b[i]:
        
def decode(ba, idx):
    instruction =  Instruction()
    b = ba[idx]
    if (b & 0b11111100 == 0b10001000): instruction.op = Operator.MOV_RMTFR
    if (b & 0b11111110 == 0b11000110): instruction.op = Operator.MOV_ITRM
    if (b & 0b11110000 == 0b10110000): instruction.op = Operator.MOV_ITR
    if (b & 0b11111110 == 0b10100000): instruction.op = Operator.MOV_MTA
    if (b & 0b11111110 == 0b10100010): instruction.op = Operator.MOV_ATM
    if (b == 0b10001110): instruction.op = Operator.MOV_RMTSR
    if (b == 0b10001100): instruction.op = Operator.MOV_RMTSR

    # Extract W
    total_read_len = op_to_byte_count[instruction.op]

    instruction.data = ba[idx: idx + total_read_len]

    # fields = op_to_fields[instruction.op]
    # for f, *rest in fields:
    #     match f:
    #         case W:
    #             (byteIndex, bitIndex) = rest
    #             byte = ba[idx + byteIndex]
    #             bit = byte[7]
    #             if bit: 
    #                 instruction.fields.w = W.BYTE
    #             else:
    #                 instruction.fields.w = W.WORD

    return instruction







if __name__ == '__main__':
    ba = [0b10001000, 0b00000000, 0b00000000, 0b00000000, 
          0b10001000, 0b00000000, 0b00000000, 0b00000000]
    len_ba = len(ba)

    instuctions = []
    idx = 0
    while(len_ba > 0):
        instruction = decode(ba, idx)
        instuctions.append(instruction)

        # advance = op_to_byte_count[instruction.op] - 1
        # idx += advance

    print(instuctions)


# Look through the byte and find the op
# the op will tell me what else I need to do with the first byte
# additional work based off the op

