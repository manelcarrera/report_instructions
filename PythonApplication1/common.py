#!/usr/bin/python

from enum import Enum

class Weekday( Enum ):
	"""Days of the week"""
	Monday		= 0
	Tuesday		= 1
	Wednesday	= 2
	Thursday	= 3
	Friday		= 4
	Saturday	= 5
	Sunday		= 6
		
	def __eq__( self, y ):
		return self.value == y

class Currency( Enum ):
	"""List of valid currencies"""
	SGP	= 'SGP'
	AED = 'AED'
	SAR = 'SAR'
	EUR = 'EUR'
	USD = 'USD'
	GBP = 'GBP'
	CAD = 'CAD'
	AUD = 'AUD'
	CHF = 'CHF'

	def __eq__( self, y ):
		return self.value == y

class ReportSection( Enum ):
	"""Sections of the report"""

	Instructions			= 0
	IncomingOutgoingsPerDay = 1
	Ranking					= 2
		
	def __eq__( self, y ):
		return self.value == y
