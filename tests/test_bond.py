import unittest
from app.Bond import Bond

class TestBondCalculations(unittest.TestCase):

    def test_price(self):
        '''
        Test the price of a bond with the following parameters:
        - Face value = $1,000
        - Coupon rate = 6% (annual)
        - Maturity = 5 years
        - Coupon frequency = 2 (semi-annual)
        - Yield (ytm) = 3% (annual)
        Example is the first question taken from: https://spu.edu/ddowning/ECN3321/bondprac.pdf
        '''
        face_value = 1000
        coupon_rate = 0.06
        maturity = 5
        coupon_frequency = 2
        yield_rate = 0.03

        bond = Bond(face_value, coupon_rate, maturity, coupon_frequency)
        computed_price = bond.price(yield_rate)
        expected_price = 1138.33

        self.assertAlmostEqual(computed_price, expected_price, places=2, msg=f'Computed price {computed_price} is not clode to expected price of {expected_price}')

    def test_modified_duration(self):
        '''
        Tests the Modified Duration for a 4-year, 8% annual coupon bond with 5% annual yield.
        Question 7.1 from: https://people.tamu.edu/~kahlig/HOMEWORK/325/ch11-duration-immun.pdf
        '''
        face_value = 1000.0
        coupon_rate = 0.08
        maturity = 4.0
        coupon_frequency= 1
        yield_rate = 0.05

        bond = Bond(face_value, coupon_rate, maturity, coupon_frequency)
        computed_mod_duration = bond.modified_duration(yield_rate)
        expected_mod_duration = 3.428

        self.assertAlmostEqual(computed_mod_duration, expected_mod_duration, places=2, msg=f'Computed modified duration {computed_mod_duration} is not close to expected {expected_mod_duration}')

    def test_compute_ytm(self):
        '''
        Test the Yield to Maturity for the following bond:
          - Market Price = $1,100
          - Face Value = $950
          - Annual coupon rate = 5%
          - Maturity = 5 years
          - Coupon frequency = 1 (annual)
        '''
        face_value = 950.0
        coupon_rate = 0.05
        maturity = 5
        coupon_frequency = 1
        market_price = 1100.0
        expected_ytm = 0.0168

        bond = Bond(face_value, coupon_rate, maturity, coupon_frequency)
        computed_ytm = bond.compute_ytm(market_price)

        self.assertAlmostEqual(computed_ytm, expected_ytm, places=3, msg=f'Computed YTM {computed_ytm:.4%} is not close to expected {expected_ytm:.4%}')

if __name__ == '__main__':
    unittest.main()

    
