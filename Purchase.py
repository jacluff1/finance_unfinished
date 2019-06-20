
XLE_kwargs = {
    'name'          : 'XLE',
    'purchase_price': 30328,
    'APR'           : 0.0389,
    'term'          : 6,
    'downpayment'   : 1250 + 500 + 200,
    'tax_rate'      : 0.083,
    'doc_fee'       : 489,
    'plates'        : 544.22,
    'tire_tax'      : 5
}

XSE_kwargs = {
    'name'          : 'XSE',
    'purchase_price': 36000,
    'APR'           : 0.0389,
    'term'          : 6,
    'downpayment'   : 1250 + 500 + 200,
    'tax_rate'      : 0.083
}

House_kwargs = {
    'name'          : 'House',
    'purchase_price': 370e3,
    'APR'           : 0.0422,
    'term'          : 30,
    'downpayment'   : .2,
    'tax_rate'      : 0,
    'closing_cost_rate'    : 0.02,
    'realtor_rate'  : 0
}

class Base:

    def __init__(self, **kwargs):
        self._set_options(**kwargs)
        self.tax = self.purchase_price * self.tax_rate

    def _set_options(self, **kwargs):
        for key,value in kwargs.items():
            setattr(self, key, value)

    def find_monthly_payment(self):
        MPR = self.APR / 12
        n_per = self.term * 12
        D = (1 + MPR)**n_per
        return round(self.balance0 * MPR * D / (D - 1), 2)

    def print_self(self):
        d = vars(self)
        print(f"\nBelongs to {self.name}:")
        for key,value in d.items():
            print(f"{key} \t {value}")

class Car(Base):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.balance0 = self.purchase_price + self.tax + self.doc_fee + self.plates + self.tire_tax - self.downpayment
        self.payment = self.find_monthly_payment()
        self.print_self()

class House(Base):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.closing_cost = self.purchase_price * self.closing_cost_rate
        self.realtor_fee = self.purchase_price * self.realtor_rate
        cost = self.purchase_price + self.tax + self.closing_cost + self.realtor_fee
        self.downpayment = cost * self.downpayment
        self.balance0 = cost - self.downpayment
        self.payment = self.find_monthly_payment()
        self.print_self()
