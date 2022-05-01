import os


class Logger:
    def __init__(self, target, configs):
        if not os.path.exists(configs["log_dir"]):
            os.makedirs(configs["log_dir"])
        if os.path.exists(os.path.join(configs["log_dir"], 'log_' + os.path.basename(target) + '.txt')):
            os.remove(os.path.join(configs["log_dir"], 'log_' + os.path.basename(target) + '.txt'))

        self.log_file = os.path.join(configs["log_dir"], 'log_' + os.path.basename(target) + '.txt')

    def write(self, txt):
        with open(self.log_file, 'a') as opt_file:
            opt_file.write(txt)
