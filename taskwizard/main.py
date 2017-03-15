"""Task Wizard.

Usage:
  taskwizard create <name> [<folder>]
  taskwizard stubs [options]
  taskwizard prepare [options]
  taskwizard evaluate [options] [-t <test scenario>] [-s <test seed>] [-p <phase>] [-l <language>]... [<file>...]
  taskwizard summary [options] [-t <test scenario>] [-s <test seed>] [-p <phase>]
  taskwizard (-h | --help)

Commands:

  create  Creates a new task definition folder
  stubs  Creates the stubs of files that should be written for this problem
  prepare  Prepares this problem for evaluation
  evaluate  Evaluate this problem on some submissions
  summary  Summarize the result of an evaluation

Global options:

  -h --help  Show this screen

  -d --definition-dir=<dir>  Task definition directory [default: .]
  -i --input-dir=<dir>  Input directory [default: .task/]
  -o --output-dir=<dir>  Output directory [default: .task/]

Test options:

  -t --test-scenario=<scenario>  The test scenario to consider.
  -s --test-seed=<seed>  The test seed to consider. Use dash to specify a range (example '-s 1-5').
  -p --test-phase=<phase>  The test phase to consider.

  If any option is omitted, then all the possibilities are considered
  for that option.
  Moreover, if a phase is specified but it is not defined in a scenario,
  then nothing is evaluated for that scenario.
  Example:
      taskwizard evaluate -p generate_input
  evaluates the phase 'generate_input' for every test scenario
  which defines a phase called 'generate_input',
  and for every test seed allowed for that scenario.

Command evaluate options:

  <file>  Submission file. Use the syntax <slot>=<file> to specify a slot.
  -l --language=<language>  Programming language. Use the syntax -l <slot>=<language> to specify a slot.

"""

import docopt


def main():
    args = docopt.docopt(__doc__)

    raise NotImplementedError
