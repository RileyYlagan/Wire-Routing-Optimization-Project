#function to confirm if a .csv file is a .csv file

def confirm_csv(input_cons_file):
    myFile = str(input_cons_file)
    if myFile.lower().endswith('.csv'):
        return True

#function to confirm if a .stl file is a .stl file

def confirm_stl(discret_out_file):
    myDomDisc = str(discret_out_file)
    if myDomDisc.lower().endswith('.stl'):
        return True
