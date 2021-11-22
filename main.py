"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
import csv_handler
import scraper_

if __name__ == '__main__':
    print("### extract PHASE ###")
    gather_coingecko("bitcoin", 01-01-2021)
    print("### LOAD PHASE ###")
    print("### transform PHASE ###")


