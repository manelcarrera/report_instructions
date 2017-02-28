import unittest

from instructions import Instruction

from common import Currency, Weekday

import datetime

class Test_Instructions( unittest.TestCase ):
	""" Tests 'Instruction' class

	Just implemented one unittest:

		Test to push an settlement in a holidays day to next working day
	"""
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass

	def test_set_real_settlement_date(self):
		""" Tests the correct value assignment to the field 'real_settlement_date'
		A work week: 
			starts Monday and ends Friday, 
		unless the currency of the trade is AED or SAR:
			where the work week starts Sunday and ends Thursday. 
		
		No other holidays to be taken into account.
		
		Atrade can only be settled on a working day.
		"""

		i = Instruction(	'ent_1', 
							Instruction.Type.Sell, 
							agreed_fx=0.01, 
							currency=Currency.AED, 
							instruction_date = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d'),
							settlement_date = datetime.datetime.strptime('2017-01-05', '%Y-%m-%d'), # Weekday.Thursday
							units=100,
							price_per_unit=10,
						    real_settlement_date=None )

		self.assertEqual( i.real_settlement_date, i.settlement_date )

		
		i = Instruction(	'ent_1', 
							Instruction.Type.Sell, 
							agreed_fx=0.01, 
							currency=Currency.AED, 
							instruction_date = datetime.datetime.strptime('2017-01-01','%Y-%m-%d' ),
							settlement_date = datetime.datetime.strptime('2017-01-06','%Y-%m-%d' ), # Weekday.Friday
							units=100,
							price_per_unit=10,
						    real_settlement_date=None )
		
		self.assertEqual( i.real_settlement_date, datetime.datetime.strptime('2017-01-08','%Y-%m-%d' )  )


if __name__ == '__main__':
    unittest.main()
