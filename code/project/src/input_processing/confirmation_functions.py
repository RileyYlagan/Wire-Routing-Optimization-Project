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

#function to confirm if a .xlsx file is a .xlsx file
    
def confirm_xlsx(input_const_file):
    myCons = str(input_const_file)
    if myCons.lower().endswith('.xlsx'):
        return True
    
#function confirms if constraints are in a readable format
# a .txt file may be added !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def confirm_const(input_const_file):
    myConst = str(input_const_file)
    if myConst.lower().endswith('.xlsx') or myConst.lower().endswith('.csv'):
        return True
