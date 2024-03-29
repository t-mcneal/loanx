import math


class MonthlyPaymentCalc:

    @staticmethod
    def calculate(loan: float, intRate: float, years: int) -> float:
        """Returns a loan's monthly payment amount.

        After calculating the monthly payment, the dollar amount can
        equal long floating point values (i.e. 105.12893837). This method
        rounds to two decimal places to present the number as a normal 
        dollar amount. The rounding needs to be very accurate and 
        consider financial portions that are less than 1 cent. 

        Args:
            loan: laon amount
            intRate: interest rate
            years: years to repay loan
        """
        if loan <= 0:
            raise ValueError("A loan amount must be greater than 0.")
        elif intRate <= 0:
            raise ValueError("A loan's interest rate must be greater than 0.")
        elif years <= 0:
            raise ValueError("A loan's repayment period must be greater than 0 years.")
        j = intRate / 12
        n = years * 12
        monPay = loan * (j / (1 - (1 + j)**-n))
        strMonPay = str(monPay)
        if '.' in strMonPay:
            numList = strMonPay.split('.')
            r = numList[1]
            if len(r) > 2:
                r = int(r[:2]) + 1
            elif len(r) == 1:
                r = int(r + '0')
            else:
                r = int(r[:2])
            return math.floor(monPay) + (r / 100)
        return monPay
