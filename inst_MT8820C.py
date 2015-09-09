import visa

rm = visa.ResourceManager()

rm.get_instrument("GPIB::1")
