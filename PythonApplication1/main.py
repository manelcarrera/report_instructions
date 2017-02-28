#!/usr/bin/python

# Environment Python 3.6 / Visual Studio 2015

import datetime
from enum import Enum
import sys, getopt

from report_creator import ReportCreator
from instructions import Instruction
from instructions_generator import InstructionsGenerator
from common import Weekday, ReportSection

from screen import Screen

def usage():
	"""Usage."""

	msg="""usage: main start_date stop_date [number_of_instructions]

	start_date				Earliest possible instruction date
							Format: %Y-%m-%d

	end_date				Latest possible instruction date
							Format: %Y-%m-%d

	number_of_instructions	Number of instructions to generate
							If no value is provided, default value is 10.
	"""
	print( msg )


def main( argv ):
	""""Main application.

	Generates a list of random instructions.

	With this sample instructiones creates a report that shows:

		Amount in USD settled incoming everyday
		Amount in USD settled outgoing everyday

		Ranking of entities based on incoming and outgoing amount.

	Positional arguments:

		start_date				Earliest possible instruction date
								Format: %Y-%m-%d

		end_date				Latest possible instruction date
								Format: %Y-%m-%d

	Optional arguments:

		number_of_instructions	if argument is provided:
									instructions to be generated
								otherwise (no value is provided): 
									10 instructions will be generated
	"""

	#################### (0) Arguments management #####################

	try:                                
		opts, args = getopt.getopt(argv, "h", ["help"])
	except getopt.GetoptError:          
		usage()                         
		sys.exit(2)                     
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage() 
			sys.exit()

	if len( argv ) < 2:
		usage()                         
		sys.exit(2)                     

	try:
		start_date, end_date = datetime.datetime.strptime( argv[ 0 ], '%Y-%m-%d'), datetime.datetime.strptime( argv[ 1 ], '%Y-%m-%d')
	except Exception as exception:
		print( exception )

	if start_date > end_date:
		tmp_date	= start_date
		start_date	= end_date
		end_date	= tmp_date 

	if len( argv ) >= 3:
		nInstructions  = int( argv[ 2 ] )
	else:
		nInstructions = 5

	#################### (1) Generate random instructions #####################

	instructions = InstructionsGenerator.generate_instructions( start_date, end_date, nInstructions )
	
	rows=[]

	for instruction in instructions:
		rows.append( instruction.get_row() )

	Screen.print_section( ReportSection.Instructions, rows )

	c = ReportCreator( instructions )

	#################### (2.1) Report: Incomings / Outgoings (per day) #####################

	rows=[]
	d =  start_date
	delta = datetime.timedelta( days = 1 )
	while d <= ( end_date + datetime.timedelta( 2 ) ):

		week_day = d.weekday()

		if( week_day != Weekday.Saturday ):
			incomings, outgoings = c.get_amounts_per_day( d )
			rows.append( ( d.strftime('%Y-%m-%d'), '%.2f' % incomings, '%.2f' % outgoings ) )

		d += delta

	Screen.print_section( ReportSection.IncomingOutgoingsPerDay, rows )

	#################### (2.2) Report: Ranking (The whole instructions) #####################

	ranking_incomings, ranking_outgoings = c.get_ranking()

	len_incomings = len( ranking_incomings )
	len_outgoings = len( ranking_outgoings )
	
	diff = abs( len_incomings - len_outgoings )
	max_elems = max( len_incomings, len_outgoings )

	if len_incomings < len_outgoings:
		for i in range( diff ):
			ranking_incomings.append('')
	else:
		for i in range( diff ):
			ranking_outgoings.append('')

	rows=[]
	for i in range( max_elems ):
		rows.append( ( str( i + 1 ), ranking_incomings[ i ], ranking_outgoings[ i ] ) )

	Screen.print_section( ReportSection.Ranking, rows )



if __name__ == "__main__":

	try:
		main( sys.argv[1:] )

	except Exception as exception:
		print( exception )
