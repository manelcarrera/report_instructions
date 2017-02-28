#!/usr/bin/python

from common import Currency, Weekday

from enum import Enum
import datetime

class Instruction:
	"""instructions sent by various clients to JP Morgan to execute in the international market

	Attributes:

		entity					A financial entity whose shares are to be bought or sold
		buy_sell_flag			If the instruction is to by or sell
									B – Buy – outgoing
									S – Sell – incoming
		agreed_fx				Is the foreign exchange rate with respect to USD that was agreed
		currency				Currency of the instruction 
		instruction_date		Date on which the instruction was sent to JP Morgan by various clients
		settlement_date			The date on which the client wished for the instruction to be settled with respect to Instruction Date
		units					Number of shares to be bought or sold
		price_per_unit			Price per unit to buy or sell
		real_settlement_date	Real date of settlement having in account that settlement orders in the we pass to next first working day

	"""

	class Type( Enum ):
		Buy		= 'B'
		Sell	= 'S'

		def __eq__( self, y ):
			"""'__eq__' funcion override"""
			return self.value == y

	@staticmethod
	def get_real_settlement_date( settlement_date, currency ):
		"""Returns a valid settlement date

		if 'settlement_date' is a working day:
			returns 'settlement_date'
		otherwise:
			returns first working day after 'settlement_date'
		
		A work week starts Monday and ends Friday, unless the currency of the trade is AED or SAR, where the work week starts Sunday and ends Thursday.
		"""

		days_to_add = 0
		week_day = settlement_date.weekday()

		if currency in ( Currency.AED, Currency.SAR ):
			if week_day in ( Weekday.Friday, Weekday.Saturday ):
				days_to_add = 6 - week_day
		else:
			if week_day in ( Weekday.Saturday, Weekday.Sunday ):
				days_to_add = 7 - week_day

		return settlement_date + datetime.timedelta( days_to_add )


	def set_real_settlement_date( fn ):
		"""Decorates Instruction creator to auto calculate 'real_settlement_date' parameter

		if 'settlement_date' is a working day:
			returns 'settlement_date'
		otherwise:
			returns first working day after 'settlement_date'
		
		A work week starts Monday and ends Friday, unless the currency of the trade is AED or SAR, where the work week starts Sunday and ends Thursday.
		"""

		def inner( self, entity, buy_sell_flag, agreed_fx, currency, instruction_date, settlement_date, units, price_per_unit, real_settlement_date = None ):
		#def inner( *args, **kwargs ):

			#fn( *args, **kwargs )
			real_settlement_date = Instruction.get_real_settlement_date( settlement_date, currency )
			fn( self, entity, buy_sell_flag, agreed_fx, currency, instruction_date, settlement_date, units, price_per_unit, real_settlement_date )
			#currency		= args[ 4 ]
			#settlement_date = args[ 6 ]
			
			#args[ 0 ].real_settlement_date = Instruction.get_real_settlement_date( settlement_date, currency )

		return inner


	@set_real_settlement_date
	def __init__( self, entity, buy_sell_flag, agreed_fx, currency, instruction_date, settlement_date, units, price_per_unit, real_settlement_date = None ):
		"""Constructor.
		
		All the fields of the instruction must be provided.

		Even the real settlement date calculated as follows:

			If an instructed settlement date falls on a weekend, then the settlement date should be changed to the next working day

		Attributes types adnd allowed values:

			buy_sell_flag			must be a valid value contained in the enum 'Type' 
			currency				must be a valid value contained in the enum 'Currency' 
			instruction_date		'datetime.date' object
			settlement_date			'datetime.date' object
			real_settlement_date	'datetime.date' object
			agreed_fx				real
			'price_per_unit			real
			units					must be a positive integer

		Assertions:

			Two assrtions added to ensure some fields integrity.

				buy_sell_flag
				currency
		"""

		assert buy_sell_flag in [ e.value for e in Instruction.Type ]
		assert currency in [ e.value for e in Currency ]

		self.entity 				= entity
		self.buy_sell_flag			= buy_sell_flag
		self.agreed_fx				= agreed_fx
		self.currency 				= currency
		self.instruction_date		= instruction_date
		self.settlement_date 		= settlement_date
		self.units 					= units
		self.price_per_unit			= price_per_unit
		self.real_settlement_date 	= real_settlement_date

	@property
	def entity( self ):
		return self.entity
	def entity( self, value ):
		self.entity = value

	@property
	def buy_sell_flag( self ):
		return self.buy_sell_flag
	def buy_sell_flag( self, value ):
		self.buy_sell_flag + value

	@property
	def agreed_fx( self ):
		return self.agreed_fx
	def agreed_fx( self, value ):
		self.agreed_fx = value
	
	@property
	def currency( self ):
		return self.currency
	def currency( self, value ):
		self.currency = value
	
	@property
	def instruction_date( self ):
		return self.instruction_date
	def instruction_date( self, value ):
		self.instruction_date = value

	@property
	def settlement_date( self ):
		return self.settlement_date
	#@set_real_settlement_date
	def settlement_date( self, valeue ):
		self.settlement_date = value

	@property
	def units( self ):
		return self.units
	def units( self, valeue ):
		self.units = value

	@property
	def price_per_unit( self ):
		return self.price_per_unit
	def price_per_unit( self, value ):
		self.price_per_unit = value

	@property
	def real_settlement_date( self ):
		return self.real_settlement_date
	def real_settlement_date( self, valeue ):
		self.real_settlement_date = value

	def __str__( self ):
		"""'__str__' funcion override"""
		return '%s | %s | %.2f | %s | %s | %s | %s | %.2f | %s' % (	self.entity, 
																	self.buy_sell_flag, 

																	self.agreed_fx, 
															
																	self.currency,
																	self.instruction_date,
																	self.settlement_date,
																	self.units,
															
																	self.price_per_unit,
														   
																	self.real_settlement_date )

	def get_row( self ):
		return  (	self.entity, 
					self.buy_sell_flag, 

					'%.2f' % self.agreed_fx, 
															
					self.currency,
					self.instruction_date.strftime('%Y-%m-%d'),
					self.settlement_date.strftime('%Y-%m-%d'),
					str(self.units),
															
					'%.2f' % self.price_per_unit,
														   
					self.real_settlement_date.strftime('%Y-%m-%d') )


