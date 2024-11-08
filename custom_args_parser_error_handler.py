import argparse
import logging

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        logging.error(message)
        self.exit(2)
