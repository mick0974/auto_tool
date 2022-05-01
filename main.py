import os.path
import sys
import argparse
import configparser
import json

import exploit


class Opt:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('target', help='Processo bersaglio')
        parser.add_argument('target_address', help='Indirizzo in cui scrivere')
        parser.add_argument('target_value', help='Valore da scrivere')
        parser.add_argument('input_file', help='Posizione del file di input')

        args = parser.parse_args()

        if os.path.exists(args.target):
            self.target = args.target
        else:
            print("L'eseguibile fornito non è stato trovato")
            sys.exit(1)

        try:
            self.target_address = int(args.target_address, 16 if "0x" in args.target_address else 10)
            print("indirizzo")
            print(self.target_address)
        except ValueError:
            print("L'indirizzo fornito non è valido")
            sys.exit(1)

        try:
            self.target_value = int(args.target_value, 16 if "0x" in args.target_value else 10)
        except ValueError:
            print("Il valore fornito non può essere convertito in esadecimale")
            sys.exit(1)

        try:
            with open(args.input_file) as input_file:
                data = input_file.read()
                self.input_in_json = json.loads(data)
        except EnvironmentError:
            print("Il file contenente gli input fornito non è stato trovato")
            sys.exit(1)

        self.configs = dict()
        config = configparser.ConfigParser()
        try:
            if os.path.exists("./options.ini"):
                config.read("./options.ini")

                self.configs["bytes_to_write"] = config.getint("Options", "bytes_to_write")
                self.configs["wait_time_marker"] = config.getint("Options", "wait_time_marker")
                self.configs["wait_time_no_marker"] = config.getint("Options", "wait_time_no_marker")
                if self.configs["wait_time_no_marker"] < 1:
                    raise ValueError
                self.configs["input_len_control"] = config.getboolean("Options", "input_len_control")
                self.configs["log_dir"] = config.get("Options", "log_dir")
            else:
                print("Il file di configurazione fornito non è stato trovato")
                sys.exit(1)
        except ValueError:
            print("Uno o più valori forniti nel file di configurazione non sono validi")
            sys.exit(1)

        print(self.input_in_json)
        print(self.configs)


if __name__ == "__main__":
    opts = Opt()

    exploit = exploit.Exploit(target=opts.target, value=opts.target_value, target_address=opts.target_address,
                              input_in_json=opts.input_in_json, configs=opts.configs)
