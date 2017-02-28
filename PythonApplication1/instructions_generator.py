#!/usr/bin/python

from instructions import Instruction
from common import Weekday, Currency

import datetime
import random

class InstructionsGenerator():
	"""Support class to generate random instructions.
	"""

	@staticmethod
	def generate_instructions( start_date, end_date, number_of_instructions = 100 ):
		"""Returns a list of random instructions

		Parameteres:

			start_date				Earliest possible instruction date
			end_date				Latest possible instruction date
			number_of_instructions	Number of instructions to generate
									If no value is provided, function generates 10 instructions

		Possible values for instructions fields:

			entity					Whatever value defined in a list of 9 entities
			buy_sell_flag			Whatever value defined in the enum 'instructions.Instruction.Type'
			agreed_fx				Whatever value in between 0.01 and 1.00
			currency				Whatever value defined in the enum 'common.Currency'
			instruction_date		Whatever date
			settlement_date			Whatever date equal or more recent than 'instruction_date' 
			units					Whatever value in between 100 and 1000
			price_per_unit			Whatever value in between 10.XX and 200.XX
			real_settlement_date	if 'settlement_date' is a working day:
										'settlement_date'
									otherwise 
										first working day after 'settlement_date'
									A work week starts Monday and ends Friday, unless the currency of the trade is AED or SAR, where the work week starts Sunday and ends Thursday
		"""

		entities	= [ 'ent_1', 'ent_2', 'ent_3', 'ent_4', 'ent_5', 'ent_6', 'ent_7', 'ent_8', 'ent_9'  ]

		days = (end_date - start_date).days

		instructions=[]

		for i in range( number_of_instructions ):

			entity					= random.choice( entities )
			buy_sell_flag			= random.choice( [ e.value for e in Instruction.Type ] )
			agreed_fx				= 0.01 + random.random()											
			currency				= random.choice( [ e.value for e in Currency ] )
			instruction_date		= start_date + datetime.timedelta( random.randint( 0, days ) )
			settlement_date			= instruction_date + datetime.timedelta( random.randint( 1, 2 ) )	#FIXME: settlement_date > 2016
			units					= random.randint( 100, 1000 )										
			price_per_unit			= random.randint( 10, 200 ) + random.random()						


			instructions.append( Instruction(	entity,
												buy_sell_flag,
												agreed_fx, 
												currency,
												instruction_date,
												settlement_date, 
												units, 
												price_per_unit ) )	

		return instructions