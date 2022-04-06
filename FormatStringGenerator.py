class DirectFmtGenerator:
    def __init__(self, direct_parameter_num, address):
        self.writers = list()

        self.direct_parameter_num = [0, direct_parameter_num]

        self.align_padding = ""

        self.address = address

    def generate_fmt_for_find_start(self):
        fmt = ""

        fmt += self.address

        for i in range(self.direct_parameter_num[0], self.direct_parameter_num[1] + 1):
            fmt += "%" + str(i) + "$p"

        return fmt

    def generate_fmt_for_find_end(self, param_len):
        fmt = ""

        for w in self.writers:
            fmt += w[0] + "x" * (2 + param_len) + w[1]

        return fmt + self.align_padding + self.address


    def generate_fmt_in_byte(self):
        writers = ""
        for w in self.writers:
            writers += w[0] + w[1]

        #return writers.encode() + self.align_padding.encode() + b"TESTTESTTEST" + self.address + b"ABCDEFGH"
        return writers.encode() + self.align_padding.encode() + self.address

    def increase_direct_parameter_num(self, num):
        self.direct_parameter_num[0] = self.direct_parameter_num[1] + 1
        self.direct_parameter_num[1] += self.direct_parameter_num[1] + num

    def set_direct_parameter_num(self, num):
        self.direct_parameter_num[1] = num

    def get_direct_parameter_num(self):
        return self.direct_parameter_num[0]

    def add_writer(self, writer):
        self.writers.append(writer)

    def set_align_padding(self, align_padding):
        self.align_padding = align_padding

    def set_address(self, address):
        self.address = address


fmt = ""
for i in range(67, 79):
    fmt += "%" + str(i) + "$p"

print(fmt)