import os.path
import sys
import argparse
import configparser
import json

import Exploit


class Opt:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('target', help='Processo bersaglio')
        parser.add_argument('target_address', help='Indirizzo in cui scrivere')
        parser.add_argument('target_value', help='Valore da scrivere')
        parser.add_argument('input_file', help='Posizione del file di input')
        parser.add_argument('--integer_value', help='Specifica che il valore da scrivere è espresso come intero', type=bool)
        parser.add_argument('--integer_address', help='Specifica che l\'indirizzo in cui scrivere è espresso come intero', type=bool)

        args = parser.parse_args()

        print(args.integer_value)

        if os.path.exists(args.target):
            self.target = args.target
        else:
            print("L'eseguibile fornito non è stato trovato")
            sys.exit(1)

        try:
            self.target_address = int(args.target_address, 10 if args.integer_address else 16)
        except ValueError:
            print("L'indirizzo fornito non non valido")
            sys.exit(1)

        try:
            self.target_value = int(args.target_value, 10 if args.integer_value else 16)
        except ValueError:
            print("Il valore fornito non può essere convertito in esadecimale")
            sys.exit(1)

        try:
            with open(args.input_file) as input_file:
                data = input_file.read()
                self.input_in_json = json.loads(data)
        except EnvironmentError:
            print("Il file di input fornito non è stato trovato")
            sys.exit(1)

        self.configs = dict()
        config = configparser.ConfigParser()
        try:
            if os.path.exists("./options.ini"):
                config.read("./options.ini")

                self.configs["bytes_to_write"] = config.getint("Options", "bytes_to_write")
                self.configs["wait_time"] = config.getint("Options", "wait_time")
                self.configs["print_log"] = config.getboolean("Options", "print_log")
                self.configs["log_dir"] = config.get("Options", "log_dir")
            else:
                print("Il file di configurazione fornito non è stato trovato")
                sys.exit(1)
        except ValueError:
            print("Uno o più valori forniti nel file di configurazione non è valido")
            sys.exit(1)

        print(self.input_in_json)
        print(self.configs)


if __name__ == "__main__":
    opts = Opt()

    exploit = Exploit.Exploit(target=opts.target, value=opts.target_value, target_address=opts.target_address,
                              input_in_json=opts.input_in_json, configs=opts.configs)
