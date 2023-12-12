""" Small code to read an output file from CMGTools and write a .tex with a yield table """
import os
import sys
import re 
inpath = sys.argv[1]
import re
from make_latex_table import dict_to_latex_table


def process_line(line):
    # Skip lines starting with # or -
    if line.startswith("#") or line.startswith("-"):
        return None, None

    # Extract relevant information using regular expressions
    match = re.match(r'(\w+)\s+([\d.]+)\s+\+/-\s+([\d.]+)\s+\(stat\)\s+\+\/-\s+([\d.]+)\s+\(syst\)\s+=\s+\+/-\s+([\d.]+)\s+\(all\)', line)
    if match:
        process_name, value, stat, syst, total = match.groups()
        return "$%3.2f \pm %3.2f$"%(float(value), float(total)), process_name
        #{
            #'entry': float(value),
            #'Statistical': float(stat),
            #'Systematic': float(syst),
            #'Total': float(total)
        #}, process_name
    else:
        return None, None

def read_table(file_path):
    processes = {
        "Process" : [],
        "Inclusive" : [],
    }
    with open(file_path, 'r') as file:
        for line in file:
            data, process_name = process_line(line.strip())
            if data:
                processes["Process"].append(process_name)
                processes["Inclusive"].append(data)
    return processes

if __name__ == "__main__":
    process_data = read_table(inpath)
    caption="""Expected (pre-fit) yields (by flavor channel) for the relevant processes in the signal 
    region of the analysis. All analysis uncertainties but the $(\mu_r, \mu_F)$ and PDFs are included."""
    
    print(process_data)
    table = dict_to_latex_table(process_data, caption, "yields_prefit2022PostEE")
    print(table)
    
    
    
    

    
