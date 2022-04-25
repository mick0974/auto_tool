import os


class Logger:
    def __init__(self, opts, configs):
        """Create a summary writer logging to log_dir."""
        if not os.path.exists(configs["log_dir"]):
            os.makedirs(configs["log_dir"])

        self.log_file = os.path.join(configs["log_dir"], 'log.txt')

    def write(self, txt):
        with open(self.log_file, 'a') as opt_file:
            opt_file.write(txt)

