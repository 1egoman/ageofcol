
class wallet(object):
  def __init__(self):
    self.amount = 0.00 # we want a floating point number here
    self.capacity = 0.00 # also a floating point number


class economy:
  currencyname = "Coins"

def pay(wallet, amt):   # pay a user 'amt' money

  # if wallet is acctully a wallet...
  if True:#type(wallet) == wallet:
    if float(wallet.amount)+float(amt) < 0: return False
    # Increment amount of money in wallet
    wallet.amount += float(amt)

    # Make sure the wallet isn't 'overstuffed' or 'overfilled'
    if wallet.amount > wallet.capacity: 
      wallet.amount = wallet.capacity
      return False
    return True
  else:
    return False