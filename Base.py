import pickle

class Base:

    def __init__(self, **kwargs):

        self.update_options(**kwargs)

    def update_options(self, **kwargs):
        for key,attr in kwargs.items(): setattr(self, key, attr)
