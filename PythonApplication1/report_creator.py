#!/usr/bin/python

import datetime
import operator

from instructions import Instruction

class ReportCreator:

	def __init__( self, instructions ):
		"""Support calculations class to generate a rapport from a list of instructions.
		Takes an instruction list as a paramater and saves it as a property.
		Public methods in the class will use the saved instruction list.

		Attributes:

			Instructions	List of instructions taken as the base to generate the rapports. 
		"""
		self.instructions = instructions

	def get_amounts_per_day( self, date = None ):
		"""Calculates the total incoming and outgoings for a given date.
		Uses the instructions list member as a base to perform the calculations.
		"""

		incomings=0
		outgoings=0

		for instruction in self.instructions:
			if instruction.real_settlement_date == date:

				amount_in_usd = instruction.price_per_unit * instruction.units * instruction.agreed_fx

				if instruction.buy_sell_flag == Instruction.Type.Sell:
					incomings =+ amount_in_usd
				else: #Instruction.Type.Buy
					outgoings =+ amount_in_usd

		return ( incomings, outgoings )


	def get_ranking( self ):
		"""Returns two entities ordered lists for the total of incomings and outgoings 
		Uses the instructions list member as a base to perform the calculations.

		It uses a map to calculate the acumulates of incomings and outgoings.

		From these maps two sorted tuplas of objects are generated.
		"""

		incomings={}
		outgoings={}

		for instruction in self.instructions:

			amount_in_usd = instruction.price_per_unit * instruction.units * instruction.agreed_fx
			if instruction.buy_sell_flag == Instruction.Type.Sell:
				if instruction.entity in incomings:
					incomings[ instruction.entity ] += amount_in_usd
				else:
					incomings[ instruction.entity ] = amount_in_usd
			else: #Instruction.Type.Buy
				if instruction.entity in outgoings:
					outgoings[ instruction.entity ] += amount_in_usd
				else:
					outgoings[ instruction.entity ] = amount_in_usd

		sorted_icomings		= sorted( incomings.items(), key = operator.itemgetter( 1 ), reverse = True  )	#tupla (entity,amount_settled)
		sorted_outgoings	= sorted( outgoings.items(), key = operator.itemgetter( 1 ), reverse = True )	#tupla (entity,amount_settled)

		ranking_incomings=[]
		for entity in sorted_icomings:
			ranking_incomings.append( entity[ 0 ] )
		
		ranking_outgoings=[]
		for entity in sorted_outgoings:
			ranking_outgoings.append( entity[ 0 ] )

		return ( ranking_incomings, ranking_outgoings )
	
	@property
	def instructions( self ):
		return self.instructions
	def instructions( self, value ):
		self.instructions = value