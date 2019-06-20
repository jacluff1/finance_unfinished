import pandas as pd

bills = {
    'BANK OF AMERICA ONLINE PMT': 'BoA - card',
    'BK OF AMER VISA'       : 'BoA - card',
    'CARDMEMBER'            : 'DF-card',
    'CARRINGTON'            : 'Carrington',
    'CENTURYLINK'           : 'CenturyLink',
    'CITY OF MESA CHECKPYMT': 'Mesa Utilities',
    'NAVI ED SERV PP STUDNTLOAN ACH TRANSACTION JAC'    : 'student loans - Jacob',
    'NAVI ED SERV PP STUDNTLOAN ACH TRANSACTION CLUFF'  : 'student loans - Amber',
    'NAVI ED SERV WEB STUDNTLOAN ACH TRANSACTION AM'    : 'student loans - Amber',
    'PLANET FIT'            : 'Planet Fitness',
    'SOLARCITY'             : 'Solar City',
    'SOLAR CITY'            : 'Solar City',
    'SRP SUREPAY'           : 'SRP',
    'T-MOBILE'              : 'Tmobile',
    'TRANSFER TO 2102'      : 'Prius V',
}

entertainment = {
    'AMC ONLINE'            : 'AMC',
    'ATOM TICKETS'          : 'Atom Tickets',
    'BLACKROCKCO'           : 'Blackrock Coffee',
    'DAIRY QUEEN'           : 'Dairy Queen',
    'EDIBLE ARRANGEMENTS'   : 'Edible Arrangements',
    'JAMBA JUICE'           : 'Jamba Juice',
    'JARRODS COFFEE TEA'    : 'Jarrods Coffee & Tea',
    'SPOTIFY'               : 'Spotify',
    'NETFLIX.COM'           : 'Netflix',
    'REDBOX'                : 'Redbox',
    'PLAYSTATION NETWORK'   : 'Playstation',
    'PLAYSTATIONNETWORK'    : 'Playstation',
    'TOTAL WINE'            : 'Total Wine',
    'TICKETMASTER'          : 'Ticketmaster',
    'WORLD MARK THE CLUB'   : 'World Mark'
}

fees = {
    'ASU STUDENT AR ASU PAYMNT' : "ASU-Payment",
    'AZ MOTOR VEHICLE'      : 'MVD',
    'AZ VEHICLE EMISSION'   : 'emissions',
    'ETS GRE EXAM'          : 'GRE',
    'PAID NSF FEE'          : 'Overdraft'
}

foodAndGrocery = {
    'ARBYS'                 : 'Arbys',
    'BACKYARD TACO'         : 'Backyard Taco',
    'BANNER DESERT BISTR'   : 'Banner Desert Bistro',
    'CHICK-FIL-A'           : 'Chick-Fil-A',
    'CHIPOTLE'              : 'Chipotle',
    'COSTCO'                : 'Costco',
    'CULINARY DROPOUT'      : 'Culinary Dropout',
    "DENNY'S"               : 'Dennys',
    'EL POLLO LOCO'         : 'El Pollo Loco',
    'FOOD CITY'             : 'Food City',
    'FRYS-MKTPLACE'         : 'Frys',
    'GENOS GIANT SLICE'     : 'Genos Pizza',
    'GO PUFF'               : 'Go Puff',
    'IN N OUT BURGER'       : 'In-N-Out',
    'LITTLE CAESARS'        : 'Little Caesars',
    'JIMMY JOHNS'           : 'Jimmy Johns',
    'MSB MESA UNIFIED'      : 'school lunches',
    'PANDA EXPRESS'         : 'Panda Express',
    'PRIME NOW'             : 'Prime Now',
    'PUBLIX'                : 'Publix',
    'RAISING CANES'         : 'Raising Canes',
    'SCHLOTZSKY'            : "Schlotzsky's",
    'SMART AND FINAL'       : 'Smart & Final',
    'SQ *'                  : 'SQ',
    'SUBWAY'                : 'Subway',
    'TACO BELL'             : 'Taco Bell',
    'TACO NAZO'             : 'Taco Nazo',
    'TACO PRADO'            : 'Taco Prado',
    'TARGET'                : 'Target',
    'WINCO FOODS'           : 'Winco',
    'WAL-MART'              : 'Wal-Mart',
    'WM SUPERCENTER'        : 'Wal-Mart'
}

health = {
    'WALGREENS'             : 'Walgreens',
    'AZ DEPT HLTH SVCS'     : 'Arizona Dept Health Services'
}

income = {
    'ARIZONA STATE'         : 'ASU',
    'ARIZ STATE UNIV STUDNT AID'    : 'ASU-Student Aid',
    'CASH DEPOSIT'          : 'Private Clients',
    'CASH WITHDRAWAL'       : 'Cash Withdrawal',
    'CASH AND CHECK DEPOSIT': 'Envy',
    'DEPOSIT'               : 'Private Clients',
    'DEPOSIT CHECK'         : 'Envy',
    'FCNH'                  : 'Cortiva',
    'STACY CAMPBELL PAYROLL': 'Stacy Campbell',
    'STRIPE TRANSFER X'     : 'Lyft',
    'TECHFIELD'             : 'Techfield'
}

insurance = {
    'AHCCCSPREMBILL'        : 'AHCCCS - Kids Care',
    'PRIMERICA'             : 'Primerica',
    'SAFECO INSURANCE'      : 'Safeco'
}

investments = {
    'VANGUARD EDI PYMNTS'   : 'Vanguard Investments',
    'VGI-TGTRET2045 INVESTMENT' : 'Vanguard Investments'
}

shopping = {
    'AMAZON.COM'            : 'Amazon',
    'AMZN'                  : 'Amazon',
    'BLACK MARKET MINERA'   : 'Black Market Minera',
    'COSMOPROF'             : 'Cosmoprof',
    'CARTERS'               : 'Carters',
    'THE HOME DEPOT'        : 'Home Depot',
    'JOANN'                 : 'Joanns',
    'JOURNEYS KIDZ'         : 'Journeys Kidz',
    'KOHLS'                 : 'Kohls',
    'OFFICE MAX'            : 'Office Max',
    'PARTY CITY'            : 'Party City',
    'VISTAPRINT'            : 'Vistaprint'
}

transportation = {
    'ARCO'                  : 'Arco',
    'AUTO AIR & VACUUM'     : 'carwash',
    'CIRCLE K'              : 'Circle K',
    'EARNHARDT TOYOTA'      : 'Earnhardt',
    'LYFT'                  : 'Lyft',
    'RACEWAY CARWASH'       : 'carwash',
    'QT'                    : 'Quicktrip',
    'QUIKTRIP'              : 'Quicktrip',
    'SKYHARBORPARKINGTER'   : 'airport',
    'SHELL OIL'             : 'Shell',
    'SHELL SERVICE'         : 'Shell',
    'UBER'                  : 'Uber',
}

#===============================================================================
# rename and categorize
#===============================================================================

categories = {
    'bills'             : bills,
    'fun'               : entertainment,
    'food & grocery'    : foodAndGrocery,
    'health'            : health,
    'income'            : income,
    'insurance'         : insurance,
    'investments'       : investments,
    'shopping'          : shopping,
    'transportation'    : transportation
}

if __name__ == '__main__':
    DF = pd.DataFrame(columns=['search_key', 'new_description', 'category'])
    for cat,dic in categories.items():
        df = pd.DataFrame(columns=['search_key', 'new_description', 'category'])
        df.search_key = dic.keys()
        df.new_description = dic.values()
        df.category = cat
        DF = DF.append(df, ignore_index=True)
    DF.sort_values('new_description', inplace=True)
    # DF.sort_values('category', inplace=True)
    DF.to_csv("AccountDataMap.csv", index=False)
