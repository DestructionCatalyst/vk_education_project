from json import load


class ConfigReader:
    def __init__(self, path):
        with open('config.json') as f:
            self.config = load(f)

    def __getitem__(self, item):
        return self.config[item]

    def get(self, item):
        return self.config.get(item)
