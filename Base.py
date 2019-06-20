import pandas as pd
from pprint import pprint
import pickle
# import pdb

class Base:

    def __init__(self, **kwargs):

        self.update_options(**kwargs)

    def update_options(self, **kwargs):
        print("\nsaving attributes")
        for key,attr in kwargs.items():
            setattr(self, key, attr)
            print(f"attribute saved: \t {key}")

        if hasattr(self, 'csv_'):
            print("\nloading csvs...")
            for attr,csvfile in self.csv_.items():
                try:
                    # pdb.set_trace()
                    setattr(self, attr, pd.read_csv(csvfile))
                    print(f"loaded csv: \t {csvfile}")
                except:
                    print(f"couldn't load {csvfile}")
                    continue

    def save_csv(self, key):
        print(f"\nsaving {key} to {self.csv_[key]}...")
        getattr(self, key).to_csv( self.csv_[key], index=False )

    def get_index_map(self, key_list, **kwargs):

        # kwargs
        df = kwargs['df'] if 'df' in kwargs else self.plan_
        column = kwargs['column'] if 'column' in kwargs else 'name'

        # index map
        idx_map = {}
        for key in key_list:
            idx = df[df[column] == key].index.item()
            idx_map[key] = idx
        return idx_map

    def print_self(self):
        d = vars(self)
        print(f"\nBelongs to {self.name_}:")
        for key,value in d.items():
            print(f"{value} \t {key}")
