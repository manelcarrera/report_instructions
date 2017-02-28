#!/usr/bin/python

from common import ReportSection

class Screen:
	""" """

	@staticmethod
	def _print_rows( rows ):
		""" """

		widths = [max(map(len, col)) for col in zip(*rows)]
		for row in rows:
			print( "  ".join((val.rjust(width) for val, width in zip(row, widths))) )

	@staticmethod
	def print_section( section, rows ):
		""" """

		if section == ReportSection.Instructions:

			print( '\nINSTRUCTIONS:' )
			print( '-------------'  )

			rows.insert( 0, ( 'Entity', 'B/S', 'AgreedFX', 'Currency', 'Instruction', 'Settlement', 'Units', 'Price/unit', 'Real Settlement' ) )

		elif section == ReportSection.IncomingOutgoingsPerDay:

			print( '\nEVERYDAY TOTALS:'  )
			print( '----------------'  )

			rows.insert( 0, ( 'Date', 'Incomings', 'Outgoings' ) )

		else:
			print( '\nRANKING:' )
			print( '--------' )
			rows.insert( 0, ( '', 'Incomings', 'Outgoings' ) )
	
		Screen._print_rows( rows )

