import os.path
import sys
import argparse
import configparser
import json
import math

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
                input_in_json = json.loads(data)

                # suddivido gli input in input da linea di comand e input da passare durante l'esecuzione. Gli input sono
                # rappresentati come dizionari, dove:
                # - "type" specifica se sono iput da passare da linea di comando o durante l'esecuzione
                # - "value" specifica il valore effettivo dell'input
                # - "marker", se non nullo, specifica quando l'input, da passare durante l'esecuzione, deve essere inviato al processo
                # - "free" specifica se il valore dell'input può essere modificato o meno
                #
                # Se l'input ha già un valore definito associato (specificato nel file json oppure settato al termine dei test
                # su quell'input), la relativa etichetta "free" sarà settata a False, altrimenti verrà associato un valore
                # temporaneo e l'etichettà free sara settata a True.
                # Solo gli input con "free" == False saranno testati come possibili input exploitabili
                self.command_line_input_list = list()
                self.during_execution_input_list = list()
                for input_elem in input_in_json["input"]:
                    if input_elem["value"] == "":
                        input_elem["value"] = "P" * 4
                        input_elem["free"] = True
                    else:
                        input_elem["free"] = False

                    if input_elem["type"] == "execution_input":
                        self.during_execution_input_list.append(input_elem)
                        if "marker" not in input_elem.keys() or "value" not in input_elem.keys():
                            print("Il file contenente gli input fornito non è strutturato correttamente")
                            exit(1)
                    elif input_elem["type"] == "command_line_input":
                        self.command_line_input_list.append(input_elem)
                        if "value" not in input_elem.keys():
                            print("Il file contenente gli input fornito non è strutturato correttamente")
                            exit(1)
        except EnvironmentError:
            print("Il file contenente gli input fornito non è stato trovato")
            sys.exit(1)
        except KeyError as e:
            print("Il file contenente gli input fornito non è strutturato correttamente")
            exit(1)

        self.configs = dict()
        config = configparser.ConfigParser()
        try:
            if os.path.exists("./options.ini"):
                config.read("./options.ini")

                self.configs["bytes_to_write"] = config.getint("Options", "bytes_to_write")
                if math.ceil(len(hex(self.target_value).replace("0x", "")) / 2) > self.configs["bytes_to_write"]:
                    print("Il valore da scrivere supera il numero di byte da scrivere settato nel file di configurazione")
                    exit(1)
                elif self.configs["bytes_to_write"] not in [1, 2, 4, 8]:
                    print("Il numero di byte da scrivere settato nel file di configurazione non rientra tra quelli previsti")
                    exit(1)
                self.configs["wait_time_marker"] = config.getint("Options", "wait_time_marker")
                if self.configs["wait_time_marker"] < 1 and self.configs["wait_time_marker"] != -1:
                    print("Uno o più valori forniti nel file di configurazione non sono validi")
                    exit(1)
                self.configs["wait_time_no_marker"] = config.getint("Options", "wait_time_no_marker")
                if self.configs["wait_time_no_marker"] < 1:
                    print("Uno o più valori forniti nel file di configurazione non sono validi")
                    exit(1)
                self.configs["input_len_control"] = config.getboolean("Options", "input_len_control")
                self.configs["log_dir"] = config.get("Options", "log_dir")
            else:
                print("Il file di configurazione fornito non è stato trovato")
                sys.exit(1)
        except ValueError:
            print("Uno o più valori forniti nel file di configurazione non sono validi")
            sys.exit(1)

if __name__ == "__main__":
    opts = Opt()

    exploit = exploit.Exploit(target=opts.target, value=opts.target_value, target_address=opts.target_address,
                              command_line_input_list=opts.command_line_input_list, during_execution_input_list=opts.during_execution_input_list, configs=opts.configs)
