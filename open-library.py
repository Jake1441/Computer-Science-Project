import sys
try:
    import process_data as proc_data
    import viaf_xml_parser as vxml_parse
    import read_marc21_countrycodes as output_graph
except ModuleNotFoundError:
    print("Unable to continue, are the python programs in their respective place?")
    print("Please refer to the documentation.")
    sys.exit()
"""
    Loads the programs in order required for the program to successfully execute
    each python package.
    
    Author: Jacob Reid
    Date: 26/05/2023
    Compatibilities:
    This program is recommended to run on Python 3.10.x
    Some packages may fail if they are run on older versions or run with unpredictable
    results. 

    The packages required will be provided in a requirements.txt
"""


# TODO: 1. import my program packages into a single python program
# TODO: 2. rename main in all my program packages to ensure they are different.
# TODO: 3. sort through the project read and put graphs at the start
# TODO: 4.make sure python -m pip install is called than just pip install
# TODO: 5.update report to include changes about the new python code to call the other codes
# TODO: 6.update video to include a small aside about the new python code to call my other programs
# TODO: 7. upload all the updated files.

def program_step(m_step, last_step):
    """
        Simple function to print to the user what is going on
        assumes its last step was the position it was in so adds one.
    """
    last_step += 1
    prompt_message = f"Currently at step {last_step} of {m_step}"
    wait_message = 'This process may not provide feedback and can take a while to complete, please wait...'
    print(prompt_message, '\n', wait_message)
    return last_step


def run_program():
    """Runs the program"""
    max_steps = 3
    c_step = 0
    c_step = program_step(max_steps, c_step)
    proc_data.jre141_proc_data()
    c_step = program_step(max_steps, c_step)
    vxml_parse.jre141_run_xml_parse
    c_step = program_step(max_steps, c_step)
    output_graph.jre141_output_g()
    print("Program reported finished last step OK!, Exiting...")


run_program()
