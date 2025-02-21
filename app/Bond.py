import numpy as np
from scipy.optimize import root_scalar

class Bond:
    '''
    A Class representing a vanilla coupon-bearing bond.

    Attributes:
        face_value (float): The par value of the bond.
        coupon_rate (float): The annual coupon rate(as a decimal).
        maturity (float): The time to maturity in years.
        coupon_frequency (int): Number of coupon payments per year.
    '''

    def __init__(self, face_value: float, coupon_rate: float, maturity: float, coupon_frequency:int=1):
        if coupon_frequency <=0:
            raise ValueError('Coupon frequency must be a positive integer.')
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.maturity = maturity
        self.coupon_frequency = coupon_frequency
        self.periods = int(maturity * coupon_frequency)
        self.coupon = self.face_value * self.coupon_rate / self.coupon_frequency

    def cash_flows(self) -> np.ndarray:
        '''
        Returns the array of cash flows for each period.
        '''
        flows = np.full(self.periods, self.coupon)
        flows[-1] += self.face_value
        return flows
    
    def time_periods(self) -> np.ndarray:
        '''
        Returns the array of time (in years) corresponding to each cash flow.
        '''
        return np.arange(1, self.periods + 1) / self.coupon_frequency
    
    def price(self, yield_rate: float) -> float:
        '''
        Computes the price of the bond given a yield rate.
        
        Args: 
            yield_rate (float): Annual yield rate as a decimal. Annualized rate used to discount future cash flows back to the present. This rate reflects the return investors require in the current market environment.
        
        Returns:
            float: Present value (price) of the bond.
        
        '''
        t = self.time_periods()
        cf = self.cash_flows()
        discount_factors = 1 / (1 + yield_rate / self.coupon_frequency) ** (self.coupon_frequency * t)
        return np.sum(cf * discount_factors)

    def macaulay_duration(self, yield_rate: float) -> float:
        '''
        Calculates the Macaulay Duration of the bond.
        
        Args:
            yield_rate (float): Annual yield rate as a decimal
        
        Returns:
            float: Macaulay Duration in years.
        '''
        t = self.time_periods()
        cf = self.cash_flows()
        discount_factors = 1 / (1 + yield_rate / self.coupon_frequency) ** (self.coupon_frequency * t)
        pv = np.sum(cf * discount_factors)
        weighted_times = t * cf * discount_factors
        return np.sum(weighted_times) / pv
    
    def modified_duration(self, yield_rate: float) -> float:
        '''
        Calculates Modified Duration of the bond.

        Args:
            yield_rate (float): Annual yield rate as a decimal

        Returns:
            float: Modified Duration in years.
        '''
        macaulay = self.macaulay_duration(yield_rate)
        return macaulay / (1 + yield_rate / self.coupon_frequency)
    
    def convexity(self, yield_rate: float) -> float:
        '''
        Calculates the convexity of the bond using a discrete cash flow approach.
        
        Args:
            yield_rate (float): Annual yield rate as a decimal.

        Returns:
            float: Convexity measure.
        '''
        periods = np.arange(1, self.periods + 1)
        cf = self.cash_flows()
        y = yield_rate
        price_adjusted = np.sum([cf[i - 1] / (1 + y / self.coupon_frequency) ** i for i in periods])
        convexity_sum = np.sum([periods[i - 1] * (periods[i - 1] + 1) * cf[i - 1] / (1 + y / self.coupon_frequency) ** (i + 2) for i in periods])
        return convexity_sum / (price_adjusted * self.coupon_frequency ** 2)
    
    def compute_ytm(self, market_price: float, guess: float=0.05, tol: float=1e-6, max_iter: int=100) -> float:
        '''
        Computes the Yield to Maturity (YTM) given the market price of the bond.
        Uses a numerical root-finding algorithm (Brent's method).

        Args:
            market_price (float): Observed market price of the bond.
            guess (float, optional): Initial guess for the yield. Defaults to 0.05
            tol (float, optional): Tolerance for convergence. Defaults to 1e-6.
            max_iter (int, optional): Maximum iterations. Defaults to 100.

        Returns:
            float: Yield to Maturity as annual rate.

        Raises:
            ValueError: If the numerical solver does not converge.
        '''
        def f(y):
            return self.price(y) - market_price
        sol = root_scalar(f, bracket=[0.0001, 1.0], method='brentq', xtol=tol, maxiter=max_iter)
        if sol.converged:
            return sol.root
        else:
            raise ValueError('YTM calculation did not converge.')
        