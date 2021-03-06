from myhdl import *


class Instruction:

    def __init__(self, opcode='0', type_inst='R', imm='0', func7='0', rs2='0', rs1='0', func3='0', rd='0'):
        self.opcode = opcode
        self.type_inst = type_inst
        self.imm = imm
        self.func7 = func7
        self.rs2 = rs2
        self.rs1 = rs1
        self.func3 = func3
        self.rd = rd
        self.type_inst = type_inst.capitalize()

    """
        We need to get the following :
            Opcode
            Rs1
            Rs2
            Rd
            func7
            func3
            imm ... etc
        then pass the arguments to the decode function based on Opcode, func3 , func7
    """

    def decode(self, pass_Bits):
        data_holder = intbv(pass_Bits)
        # ============================== Opcodes ============================== #
        #                R           I      I(LOAD)     I(JALR)   I(sys calls)
        opcode_key = [0b0110011, 0b0010011, 0b0000011, 0b1100111, 0b1110011,
                      0b0100011, 0b1100011, 0b0110111, 0b0010111, 0b1101111]
        #                S          B         U(LUI)    U(AUIPC)   J(JAL)

        for i in range(len(opcode_key)):
            if data_holder[7:0] == opcode_key[i]:
                if i == 0:  # R-Type
                    self.rd = data_holder[12:7]
                    self.func3 = data_holder[15:12]
                    self.rs1 = data_holder[20:15]
                    self.rs2 = data_holder[25:20]
                    self.func7 = data_holder[32:25]
                    self.opcode = opcode_key[0]
                    self.type_inst = 'R'

                elif i == 1:  # I-Type
                    self.rd = data_holder[12:7]
                    self.func3 = data_holder[15:12]
                    self.func7 = data_holder[32:25]
                    self.rs1 = data_holder[20:15]
                    self.imm = data_holder[32:20]
                    self.opcode = opcode_key[1]
                    self.type_inst = 'I'

                elif i == 2:  # Load instructions
                    self.rd = data_holder[12:7]
                    self.func3 = data_holder[15:12]
                    self.rs1 = data_holder[20:15]
                    self.imm = data_holder[32:20]
                    self.opcode = opcode_key[2]
                    self.type_inst = 'I(LOAD)'

                elif i == 3:  # Jump instructions (JALR)
                    self.rd = data_holder[12:7]
                    self.func3 = data_holder[15:12]
                    self.rs1 = data_holder[20:15]
                    self.imm = data_holder[32:20]
                    self.opcode = opcode_key[3]
                    self.type_inst = 'I(JALR)'

                elif i == 4:  # System calls
                    self.rd = data_holder[12:7]
                    self.func3 = data_holder[15:12]
                    self.rs1 = data_holder[20:15]
                    self.imm = data_holder[32:20]
                    self.opcode = opcode_key[4]
                    self.type_inst = 'I(sys calls)'

                elif i == 5:  # S-Type
                    self.rs1 = data_holder[20:15]
                    self.rs2 = data_holder[25:20]
                    self.func3 = data_holder[15:12]
                    imm_p = str(bin(data_holder[32:25], 7)) + str(bin(data_holder[12:7], 5))
                    temp = int(imm_p, 2)
                    temp1 = intbv(temp).signed()
                    self.imm = intbv(temp1)
                    self.opcode = opcode_key[5]
                    self.type_inst = 'S'

                elif i == 6:  # B-Type
                    self.func3 = data_holder[15:12]
                    self.rs1 = data_holder[20:15]
                    self.rs2 = data_holder[25:20]
                    self.opcode = opcode_key[6]
                    imm_p = str(bin(data_holder[31], 1)) + str(bin(data_holder[7], 1)) + str(bin(data_holder[31:25], 6)) \
                            + str(bin(data_holder[12:8], 4))
                    temp = intbv(imm_p)[12:].signed()
                    self.imm = temp
                    self.type_inst = 'B'

                elif i == 7:  # U-Type(Load Up)
                    self.rd = data_holder[12:7]
                    self.imm = data_holder[32:12]
                    self.opcode = opcode_key[7]
                    self.type_inst = 'U(LUI)'

                elif i == 8:  # U-Type(AUIPC)
                    self.rd = data_holder[12:7]
                    self.imm = data_holder[32:12]
                    self.opcode = opcode_key[8]
                    self.type_inst = 'U(AUIPC)'

                elif i == 9:  # J-Type
                    imm_p = str(bin(data_holder[31], 1)) + str(bin(data_holder[20:12], 8)) + str(
                        bin(data_holder[20], 1)) \
                            + str(bin(data_holder[31:21], 10))
                    temp = int(imm_p, 2)
                    temp1 = intbv(temp)[12:].signed()
                    self.imm = temp1
                    self.rd = data_holder[12:7]
                    self.opcode = opcode_key[9]
                    self.type_inst = 'J'