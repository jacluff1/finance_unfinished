import pandas as pd
import numpy as np
import csv

class base_loan:

    # today, is the date in which the loan data was entered and optimized
    today   =   pd.to_datetime('today')

    # how many months have gone by since today
    months  =   0

    def UPDATE_LISTS(self,interest,principle,extra):
        # update instance interest, principle, extra, and presentValues lists
        self.interest.append(interest)
        self.principle.append(principle)
        self.extra.append(extra)
        self.presentValues.append(self.presentValue)

    def GET_MONTH(self):
        # get the month based on optimization date (today) and how many months have gone by
        date    =   self.today + pd.DateOffset(months=self.months)
        return date.strftime('%Y/%m')

    def GET_PAYOFF_RESULTS(self):
        # gater the date and the sum of each list: interest, principle, and extra
        results     =   dict(payoffDate=self.GET_MONTH(), months=self.months, interest=sum(self.interest), principle=sum(self.principle), extra=sum(self.extra))
        return results

    def MAKE_MINIMUM_PAYMENT(self):

        # calculate payment
        monthlyPayment      =   self.GET_MONTHLY_PAYMENT(self.presentValue)
        interest            =   self.presentValue * self.monthlyPercentageRate
        principle           =   monthlyPayment - interest

        # update present value
        self.presentValue   -=  principle

        # enter in payment information for the month
        self.UPDATE_LISTS(interest,principle,0)

        # increment month counter
        self.months +=  1

    def MAKE_EXTRA_PAYMENT(self,extra):
        # make an extra payment on principle, using this method lowers the present value by given extra amount and adjusts the latest entry in the princple, extra, and presentValues lists
        self.presentValue       -=  extra
        self.principle[-1]      +=  extra
        self.extra[-1]          +=  extra
        self.presentValues[-1]  -=  extra

    def PAYOFF_THROUGH_MINIMUM_PAYMENT(self):
        # pay off the loan by making minimum payment

        # break down payment
        interest            =   self.presentValue * self.monthlyPercentageRate
        principle           =   self.presentValue

        # set present value to 0
        self.presentValue   =   0

        # update lists
        self.UPDATE_LISTS(interest,principle,0)

        # increment month counter
        self.months         +=  1

        # add payoff results to loan
        self.payoff_results =   self.GET_PAYOFF_RESULTS()

        # return the last payment amount
        return interest + principle

    def PAYOFF_THROUGH_EXTRA_PAYMENT(self,extra):
        # pay off the loan by making an extra payment

        # get the difference between the extra available and the present value
        extra_left          =   extra - self.presentValue

        # make an extra payment equal to the present value
        self.MAKE_EXTRA_PAYMENT(self.presentValue)

        # add payoff results to loan
        self.payoff_results =   self.GET_PAYOFF_RESULTS()

        # return the left over extra
        return extra_left

class ammoritized_loan(base_loan):

    def __init__(self,name,presentValue,monthlyPayment,annualPercentageRate,nPeriods,nPeriodsRemaining):

        # record loan type
        self.type                   =   'ammoritized_loan'

        # loan name
        self.name                   =   name

        # present value
        self.presentValue           =   float(presentValue)

        # origina loan amount (at time of optimiztion)
        self.originalValue          =   float(presentValue)

        # monthly payment amount
        self.monthlyPayment         =   float(monthlyPayment)

        # annual percentage rate
        self.annualPercentageRate   =   float(annualPercentageRate)/100

        # monthly percentage rate
        self.monthlyPercentageRate  =   self.annualPercentageRate/12

        # number of periods (months)
        self.nPeriods               =   int(nPeriods)

        # number of periods remaining (months left)
        self.nPeriodsRemaining      =   int(nPeriodsRemaining)

        # list of interest paid over time
        self.interest               =   [0]

        # list of principle payments over time
        self.principle              =   [0]

        # list of extra payments made over time
        self.extra                  =   [0]

        # list of PV over time
        self.presentValues          =   [self.presentValue]

        # anticipated payoff date
        self.payoffDate             =   self.GET_PAYOFF_DATE()

    def GET_MONTHLY_PAYMENT(self,PV):
        # # calculate the recuring monthly payment for the ammoritized loan
        # return (self.MPA*self.MPR) / (1 - (1+self.MPR)**(-self.nPer) )
        return self.monthlyPayment

    def GET_PAYOFF_DATE(self):
        # get the loan payoff date

        # get payoff date by adding nPerR to today
        payoff  =   self.today + pd.DateOffset(months=self.nPeriodsRemaining)

        # return payoff date formated as "year/month"
        return  payoff.strftime('%Y/%m')

    def GET_TOTAL_REMAINING_PAYMENT(self):
        # get the anticipated total remaining payment
        return self.monthlyPayment * self.nPeriodsRemaining

class rolling_loan(base_loan):

    def __init__(self,name,presentValue,annualPercentageRate,minimumPaymentPercentage,financeFee,sigfig,paymentFloor):

        # record type of loan
        self.type                       =   "rolling_loan"

        # loan name
        self.name                       =   name

        # current loan balance
        self.presentValue               =   float(presentValue)

        # original loan balance
        self.originalValue              =   self.presentValue

        # annual percentage rate
        self.annualPercentageRate       =   float(annualPercentageRate)/100

        # monthly percentage rate
        self.monthlyPercentageRate      =   self.annualPercentageRate/12

        # minimum payment percentage
        self.minimumPaymentPercentage   =   float(minimumPaymentPercentage)/100

        # finance fee
        self.financeFee                 =   float(financeFee)

        # significant figures of MPA
        self.sigfig                     =   int(sigfig)

        # threshold payment for low balance
        self.paymentFloor               =   float(paymentFloor)

        # current monthly payment amount
        self.monthlyPayment             =   self.GET_MONTHLY_PAYMENT(self.presentValue)

        # list of interest paid over time
        self.interest                   =   [0]

        # list of principle payments over time
        self.principle                  =   [0]

        # list of extra payments made over time
        self.extra                      =   [0]

        # list of present values over time
        self.presentValues              =   [self.presentValue]

        # get number of periods remaining and payoff date
        self.GET_PAYOFF_DATE()

    def GET_MONTHLY_PAYMENT(self,PV):
        # calculate minimum payment
        if PV > self.paymentFloor:
            M   =   round(PV*self.minimumPaymentPercentage + self.financeFee, self.sigfig)
            return M
        else:
            return PV*(1 + self.monthlyPercentageRate) + self.financeFee

    def GET_PAYOFF_DATE(self):
        # get anticipated payoff date

        # get number of periods remaining
        n                       =   0
        balance                 =   self.presentValue
        while balance > 0:
            n           +=  1
            payment     =   self.GET_MONTHLY_PAYMENT(balance)
            interest    =   balance * self.monthlyPercentageRate
            principle   =   payment - interest
            balance     -=  principle

        # add nPeriodsRemaining
        self.nPeriodsRemaining  =   n

        # get payoff date by adding nPerR to today
        payoff                  =   self.today + pd.DateOffset(months=n)

        # return payoff date formated as "year/month"
        return payoff.strftime('%Y/%m')

    def GET_TOTAL_REMAINING_PAYMENT(self):
        # get the anticipated total remaining payment
        total   =   0
        balance =   self.presentValue
        while balance > 0:
            payment     =   self.GET_MONTHLY_PAYMENT(balance)
            interest    =   balance * self.monthlyPercentageRate
            principle   =   payment - interest
            balance     -=  principle
            total       +=  payment
        return total

class loans:

    def __init__(self,monthlyExtraAvailable):

        # today
        self._today                 =   pd.to_datetime('today')

        # monthly extra available
        self.monthlyExtraAvailable  =   monthlyExtraAvailable

        # get basic pre-optimized results
        self._ADD_BASIC_RESULTS()

        # total number of permutations of loan payoff order
        self._nTrials               =   np.math.factorial(self._nLoans)

        # total debt allocation
        self.totalDebtAllocation    =   self.basic_results['monthlyPayment'] + monthlyExtraAvailable

    def GET_BASIC_LOAN_LIST(self):

        # create empty list to hold loan instances
        loan_list               =   []

        # import csvs
        data1                   =   pd.read_csv("input/RollingLoans.csv")
        data2                   =   pd.read_csv("input/AmmoritizedLoans.csv")

        # get number of rows in data
        nRows1                  =   data1.shape[0]
        nRows2                  =   data2.shape[0]

        # go through each loan in data, create loan instance and add to loan dictionary
        for row in range(nRows1):
            inst    =   rolling_loan(*data1.loc[row])
            loan_list.append(inst)
        for row in range(nRows2):
            inst    =   ammoritized_loan(*data2.loc[row])
            loan_list.append(inst)

        # # add loan_list to instance
        # self.basic_loan_list    =   np.array(loan_list, dtype='O')
        return np.array(loan_list, dtype='O')

    def _ADD_BASIC_RESULTS(self):
        # get pre-optimized anticipated values for: total interest paid, total debt amount,total amount to be paid, total MMP (minimum monthly payment), and total payoff date

        # set initial values
        total_I             =   0
        total_debt          =   0
        total_pay           =   0
        total_MPA           =   0
        total_months        =   0
        total_POD           =   self._today.strftime('%Y/%m')

        # get the loan_list
        loan_list           =   self.GET_BASIC_LOAN_LIST()

        # loop through all loans and update values
        for i,loan in enumerate(loan_list):
            total_debt  +=  loan.presentValue
            total_pay   +=  loan.GET_TOTAL_REMAINING_PAYMENT()
            total_MPA   +=  loan.monthlyPayment
            POD         =   loan.GET_PAYOFF_DATE()
            if POD > total_POD: total_POD = POD
            if loan.nPeriodsRemaining > total_months: total_months = loan.nPeriodsRemaining
        total_I     =   total_pay - total_debt

        # gather results into a dictionary and add it to instance
        results             =   dict(interest=total_I, debt=total_debt, total=total_pay, monthlyPayment=total_MPA, months=total_months, payoffDate=total_POD)
        self.basic_results  =   results
        self._nLoans         =   len(loan_list)

    def _FILTER_PAID_OFF_LOANS(self,loan_list):
        # create a mask that filters out loans that are paid off and return the filtered list
        mask    =   []
        for loan in loan_list:
            if loan.presentValue > 0:
                mask.append(True)
            else:
                mask.append(False)
        return loan_list[mask]

    def _PAY_MONTH(self,loan_list):
        # pay each loan one month forward while making extra payments to highest priority loan.

        # track the total monthly payments for each loan
        total_MPA   =   0

        # filter out paid off loans from loan list
        loan_listF  =   self._FILTER_PAID_OFF_LOANS(loan_list)

        # make minimum payments to each non paid off loan
        for loan in loan_listF:
            # get loan's monthly payment amount
            MPA     =   loan.GET_MONTHLY_PAYMENT(loan.presentValue)
            # if monthly payment amount is greater than or equal to present value, add the last payment value returned from "PAYOFF_THROUGH_MINIMUM_PAYMENT" to total_MPA
            if MPA >= loan.presentValue:
                last_payment    =   loan.PAYOFF_THROUGH_MINIMUM_PAYMENT()
                total_MPA       +=  last_payment
            # if monthly payment amount is less than remaining balance, "MAKE_MINIMUM_PAYMENT" and add MPA to total_MPA
            if MPA < loan.presentValue:
                loan.MAKE_MINIMUM_PAYMENT()
                total_MPA       +=  MPA

        # get the amount available for extra payments (difference between the total debt allocation and the total monthly payments)
        extra       =   self.totalDebtAllocation - total_MPA

        # filter out paid off loans from loan list
        loan_listF  =   self._FILTER_PAID_OFF_LOANS(loan_list)

        # go through each un paid off loan
        for loan in loan_listF:
            # if the present value of the loan is greater than or equal to the extra amount available, make an extra payment on the loan and break the loop
            if loan.presentValue >= extra:
                loan.MAKE_EXTRA_PAYMENT(extra)
                extra   =   0
                break
            # if present value is less than the extra amount available, pay off the loan through extra payment and update the extra amount
            else:
                extra   =   loan.PAYOFF_THROUGH_EXTRA_PAYMENT(extra)

        # return the extra amount (if greater than 0, then all loans are paid off)
        return extra

    def _RUN_PERMUTATION(self,loan_list):
        # run through the selected loan_list and PAY_MONTH untill all the loans are paid off. collect the final pay off date, the total interest paid, and the amount left over in the final month

        # 'extra' is the amount of money available to pay directly to the princple for all the loans, the extra will be applied to highest priority loans until all loans are paid off. 'extra_left' is the amount left over in the month after making extra principle paymnets, this number will be zero every month untill all loans are paid off.
        extra_left      =   0
        while extra_left == 0:
            extra_left  =   self._PAY_MONTH(loan_list)

        # collect the final pay off date and the total interest paid from each loan
        POD             =   []
        I               =   []
        for loan in loan_list:
            results =   loan.payoff_results
            POD.append(results['payoffDate'])
            I.append(results['interest'])

        # collect results
        total_results   =   dict(payoffDate=max(POD), interest=sum(I), extra_left=extra_left)

        # return results and loan list
        return total_results, loan_list

    def _WRITE_TO_CSV(self,loan_list,filename):
        # collect data and optimized results and write them to csv file.

        # inititate arrays for: name, how many months payments were made, payoff date, original value, interest paid, extra paid
        names           =   np.empty(self._nLoans, dtype='O')
        M               =   np.zeros(self._nLoans)
        POD             =   np.empty_like(names)
        OV              =   np.zeros_like(M)
        I               =   np.zeros_like(M)
        E               =   np.zeros_like(M)

        # fill arrays with final values
        for i,loan in enumerate(loan_list):
            results     =   loan.payoff_results
            names[i]    =   loan.name
            M[i]        =   results['months']
            POD[i]      =   results['payoffDate']
            OV[i]       =   loan.originalValue
            I[i]        =   results['interest']
            E[i]        =   results['extra']

        # put the results into a dictionary, then into a DataFrame
        results         =   dict(names=names, months=M, payoffDate=POD, originalValue=OV, interest=I, extra=E)
        results         =   pd.DataFrame(results)

        # calculate for group: months ellapsed, pay off date, original value, interest paid, total paid, extra left over from last month payment
        results['total']    =   OV + I
        totals              =   dict(months=np.max(M), payoffDate=np.max(POD), debt=np.sum(OV), interest=np.sum(I), total=np.sum(results['total']), extra=np.sum(E))

        # load basic results
        basic_results       =   self.basic_results

        # find the difference
        difference          =   dict(months=basic_results['months']-totals['months'], interest=basic_results['interest']-totals['interest'], extra=0-totals['extra'], total=basic_results['total']-totals['total'])

        # write results to csv
        filename            =   "output/%s.csv" % filename
        results.to_csv(filename)

        # open up csv file for further editing (closes after 'with')
        with open(r"%s" % filename,'a') as f:
            writer  =   csv.writer(f)
            writer.writerow("")
            writer.writerow(["", "optimized results", totals['months'], np.max(POD), totals['debt'], totals['interest'], totals['extra'], totals['total']])
            writer.writerow(["", "basic results", basic_results['months'], basic_results['payoffDate'], "", basic_results['interest'], 0, basic_results['total']])
            writer.writerow(["", "save", difference['months'], "", "", difference['interest'], "", difference['total']])

    def OPTIMIZE_LOANS_FULL(self):

        # get the basic results for pay of date (POD) and total interest paid and set them as the initial values for the time optimized and interest optimized values.
        time_opt        =   self.basic_results['payoffDate']
        interest_opt    =   self.basic_results['interest']

        # generate permutations. For each permutation: make a copy of the loan list, pay through each month until all loans are paid off, record how many months it took to pay off all loans and record the total amount of interest paid. keep track of permutation with the quickest payoff and permutation with lowest total interest paid.

        def _heap_perm_(n, A):
            # https://stackoverflow.com/a/29044942
            if n == 1: yield A
            else:
                for i in range(n-1):
                    for hp in _heap_perm_(n-1, A): yield hp
                    j = 0 if (n % 2) == 1 else i
                    A[j],A[n-1] = A[n-1],A[j]
                for hp in _heap_perm_(n-1, A): yield hp

        # https://stackoverflow.com/questions/29042819/heaps-algorithm-permutation-generator
        A       =   np.arange(self._nLoans)
        Alist   = [el for el in A]
        for i,hp in enumerate(_heap_perm_(self._nLoans, Alist)):

            nTrial              =   i+1
            print("\nstarting trial %s out of %s..." % (nTrial,self._nTrials))

            # make a copy of the the basic loan list and filter it with permutation mask 'hp'
            loan_list           =   self.GET_BASIC_LOAN_LIST()[hp]

            # run the re-ordered loan list and get the results
            results, loan_list  =   self._RUN_PERMUTATION(loan_list)

            # compare the permutation's results with the current optimized results. If permuation's results are better, then save them as new results.
            if results['payoffDate'] < time_opt:
                time_opt                    =   results['payoffDate']
                self.time_opt_results       =   results
                self.time_opt_loan_list     =   loan_list
                print("trial %s has superior time results." % i)
            if results['interest'] < interest_opt:
                interest_opt                =   results['interest']
                self.interest_opt_results   =   results
                self.interest_opt_loan_list =   loan_list
                print("trial %s has superior interest results." % i)

            print("completed trial %s of %s. %s percent complete." % (nTrial,self._nTrials,(100*nTrial/self._nTrials)) )

        # record optimized results
        self._WRITE_TO_CSV(self.time_opt_loan_list,"TimeOptimizedResults_full")
        self._WRITE_TO_CSV(self.interest_opt_loan_list,"InterestOptimizedResults_full")

    def OPTIMIZE_LOANS_WEIGHTED(self,x=.5):
        # orders the loans based on the lowest present value. The rolling loans recieve a weighting factor to give them a higher priority.

        # get copy of basic loan list
        loan_list                   =   self.GET_BASIC_LOAN_LIST()

        # make an empty array to hold loan present values weighted against loan type
        weights                     =   np.zeros(self._nLoans)
        for i,loan in enumerate(loan_list):
            if loan.type == 'ammoritized_loan':
                weights[i]  =   loan.originalValue
            else:
                weights[i]  =   x*loan.originalValue

        # create a mask that sorts weights by value
        mask                        =   weights.argsort()

        # run the re-ordered loan list and get the results
        results, loan_list          =   self._RUN_PERMUTATION(loan_list[mask])

        # record results
        self.quick_opt_results      =   results
        self.quick_opt_loan_list    =   loan_list

        # record optimized results
        self._WRITE_TO_CSV(self.quick_opt_loan_list,"optimizedResults_weighted")

    def OPTIMIZE_LOANS_GUESS(self):
        # the rolling loans are at the top; the ammoritized loans beneath them. Each type is then ordered based on lowest present value.

        # get copy of basic loan list
        loan_list                   =   self.GET_BASIC_LOAN_LIST()

        # separate rolling and ammoritized loans
        rolling                     =   []
        rolling1                    =   []
        ammoritized                 =   []
        ammoritized1                =   []
        for loan in loan_list:
            if loan.type == "ammoritized_loan":
                ammoritized.append(loan)
                ammoritized1.append(loan.originalValue)
            else:
                rolling.append(loan)
                rolling1.append(loan.originalValue)

        # order each type by lowest present value
        mask1                       =   np.array(rolling1).argsort()
        mask2                       =   np.array(ammoritized1).argsort() + mask1.shape[0]
        mask                        =   np.hstack((mask1,mask2))

        # import pdb; pdb.set_trace()

        # run the re-ordered loan list and get the results
        results, loan_list          =   self._RUN_PERMUTATION(loan_list[mask])

        # record results
        self.guess_opt_results      =   results
        self.guess_opt_loan_list    =   loan_list

        # record optimized results
        self._WRITE_TO_CSV(self.guess_opt_loan_list,"optimizedResults_guess")
