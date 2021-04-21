import os
import random
def fn():       # 1.Get file names from directory
	os.system("mkdir images && cd images")
    file_list=os.listdir(r"~/YOUR-PATH-HERE")
    # Change here the size of the paper and the printer name.
    # Find printer name on OSX under Printers & Scanners/Options & Supplies
    os.system("lpr -o media=Custom.80x200mm -P HP_DeskJet_2700_series " + random.choice(file_list))


 #2.To rename files
fn()

