from app.Bond import Bond

def main():
    '''
    This script creates a bond and then reprices it under different yield scenarios.
    For each scenario, it calculates and displays:
        - Bond Price
        - Macaulay Duration
        - Modified Duration
        - Convexity
    '''
    bond = Bond(face_value=1000, coupon_rate=0.06, maturity=5, coupon_frequency=2)

    base_yield = 0.03
    yield_shocks = [-0.01, -0.005, 0, 0.005, 0.01]

    print('Repricing the vond for different yield scenarios:\n')
    print(f'Base yield = {base_yield}\n')
    print("   Shock      Yield      Price      Macaulay Dur.  Modified Dur.  Convexity")
    print("   -----      -----      -----      -------------  -------------  ---------")
    for shock in yield_shocks:
        new_yield = base_yield + shock
        price = bond.price(new_yield)
        macaulay_dur = bond.macaulay_duration(new_yield)
        modified_dur = bond.modified_duration(new_yield)
        convex = bond.convexity(new_yield)

        print(f' {shock:+7.1%}   {new_yield:7.2%}   ${price:10.2f}'
        f'       {macaulay_dur:6.3f}'
        f'          {modified_dur:6.3f}'
        f'        {convex:8.4f}')

if __name__ == '__main__':
    main()