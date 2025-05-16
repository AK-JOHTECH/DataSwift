import pyodbc
import os
import datetime
import re
    
def ceramic_info(part_number,rev):
    #********************************************************************************************
    #Description: This function fetches data based on input Part number and rev. from Access Database. 
    #             Input: Driver string from Connection_Check(), table_name, Column_name_1, and Column_name_2. 
    #             Output: .  
    #********************************************************************************************
    try:
        # Establish connection
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()

        # Search Parameters
        table_name = 'AMCDesignMaster'
        column_A = 'JDI_PART__'
        column_B = 'JDI_REV_'
        column_info = ['TCC','CERAMIC_TY','CERAMIC_LO']
        # Construct SQL query
        query = f"SELECT {', '.join(column_info)} FROM {table_name} WHERE [{column_A}] LIKE ? AND [{column_B}] LIKE ?"

        # Execute query
        parameters = (f"%{part_number}%", f"%{rev}%")
        cursor.execute(query, parameters)
        data = cursor.fetchone()

        # Convert to a list and handle None values
        # data = [0 if value is None else value for value in data]

        # Close cursor and connection
        cursor.close()
        conn.close()
        data = list(data)
        return data

    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return []


#=======================================================================================================
def edit_FT_database_table(criteria, newData,start_time,end_time):
    """
    Description: Edit values in specific rows of an Access database table based on provided criteria.
    Input:
        criteria: Tuple containing criteria for the row to be edited (Part_Number, Rev, MO_Number).
        newData: List containing new data to be updated in the matching row.
    Output: None
    """
    
    date = datetime.datetime.now()
    current_date = date.date()
    duration =str(int(end_time-start_time))
    Time = [str(current_date),duration]
    zeroVec = [0]*10
    index = 0
    d = []
    for i in newData:
        if i == []:
            d.append(zeroVec)
            index += 1
        else:
            d.append(newData[index])
            index += 1
    
    newData = []
    for i in d:
        for j in i:
            newData.append(str(float(j)))
    newData = tuple(newData) + tuple(ceramic_info(criteria[0],criteria[2])) + tuple(Time)

    print('len New Data',len(newData)) # This data length is 73
   
    try:
        # Establish connection
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()
        tableName = 'FT_DIM_DB'

        # Find the row to update
        sql_select = f"SELECT * FROM {tableName} WHERE Part_number=? AND MO=? AND Rev=?"
        cursor.execute(sql_select, criteria)
        row = cursor.fetchone()

        if row:
            # Update the row
            sql_update = f"UPDATE {tableName} SET "
            columns = [
                "OD_L_1", "OD_L_2", "OD_L_3", "OD_L_4", "OD_L_5", "OD_L_6", "OD_L_7", "OD_L_8", "OD_L_9", "OD_L_10",
                "Width_1", "Width_2", "Width_3", "Width_4", "Width_5", "Width_6", "Width_7", "Width_8", "Width_9", "Width_10",
                "Thickness_1", "Thickness_2", "Thickness_3", "Thickness_4", "Thickness_5", "Thickness_6", "Thickness_7", "Thickness_8", "Thickness_9", "Thickness_10",
                "ID1_1", "ID1_2", "ID1_3", "ID1_4", "ID1_5", "ID1_6", "ID1_7", "ID1_8", "ID1_9", "ID1_10",
                "ID2_1", "ID2_2", "ID2_3", "ID2_4", "ID2_5", "ID2_6", "ID2_7", "ID2_8", "ID2_9", "ID2_10",
                "ID3_1", "ID3_2", "ID3_3", "ID3_4", "ID3_5", "ID3_6", "ID3_7", "ID3_8", "ID3_9", "ID3_10",
                "Warpage_1", "Warpage_2", "Warpage_3", "Warpage_4", "Warpage_5", "Warpage_6", "Warpage_7", "Warpage_8", "Warpage_9", "Warpage_10",
                "TCC", "Powder_Name", "Powder_Lot","Date_MO","Duration"
            ]
            for index, column in enumerate(columns):
                sql_update += f"{column}=?"
                if index != len(columns) - 1:
                    sql_update += ", "
            sql_update += " WHERE Part_number=? AND MO=? AND Rev=?"

            # Execute UPDATE statement
            cursor.execute(sql_update, (*newData, *criteria))

            # Commit transaction
            conn.commit()

            print("Data updated successfully.")
        else:
            print("Row not found.")

        # Close connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error occurred while updating data: {e}")

# part_info_vec = ['12C16-A','1234','NCC-12']
# drill_dim_output = [[1,2,3,4,5,6,7,8,9,10],[],[],[],[],[],[]]
# start_time = 0
# end_time = 10
# edit_FT_database_table(part_info_vec, drill_dim_output,start_time,end_time)
#======================================================================================================
def get_last_used_id(DB):
    try:
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()

        # Execute SQL query to get the maximum ID from the table
        if DB == 'Drill':
            cursor.execute("SELECT MAX(ID) FROM Drill_DIM_DB")
        elif DB == 'FT':
            cursor.execute("SELECT MAX(ID) FROM FT_DIM_DB")
        elif DB == 'login':
            cursor.execute("SELECT MAX(UserID) FROM Login")
        last_id = cursor.fetchone()[0]  # Fetch the max ID value
        conn.commit()
        cursor.close()
        conn.close()

        return last_id
    except Exception as e:
        print(f"Error occurred while retrieving last ID: {e}")
        return None

#=======================================================================================================
def write_to_drill_database(part_info_vec,drill_dim_output,start_time,end_time):
    """
    Description: Write information to an Access database table.
    Input:
        filePath: Path to the Access database file.
        tableName: Name of the table where data will be inserted.
        data: Tuple containing data to be inserted into the table.
    Output: None
    """
    # Get the last used ID from the database
    DB = 'Drill'
    last_id = get_last_used_id(DB)

    # Calculate new ID
    new_id = last_id + 1 if last_id else 1  # If no previous ID, start from 1

    date = datetime.datetime.now()
    current_date = str(date.date())

    duration = str(int(end_time - start_time))
    Time = [current_date,duration]
    zeroVec = [0]*10
    index = 0
    d = []
    for i in drill_dim_output:
        if i == []:
            d.append(zeroVec)
            index+=1
        else:
            d.append(drill_dim_output[index])
            index+=1
    
    data = []
    for i in d:
        for j in i:
            data.append(str(float(j)))

    data = (new_id,)+tuple(part_info_vec) + tuple(data) + tuple(ceramic_info(part_info_vec[0],part_info_vec[2])) + tuple(Time) # combine all the data into one vector
    try:
        # Establish connection
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()
        tableName = 'Drill_DIM_DB'

        # Construct SQL INSERT statement
        column_names = "ID,Part_number, MO, Rev, OD_L_1, OD_L_2, OD_L_3, OD_L_4, OD_L_5, OD_L_6, OD_L_7, OD_L_8, OD_L_9, OD_L_10, " \
                   "Width_1, Width_2, Width_3, Width_4, Width_5, Width_6, Width_7, Width_8, Width_9, Width_10, " \
                   "Thickness_w_1, Thickness_w_2, Thickness_w_3, Thickness_w_4, Thickness_w_5, Thickness_w_6, " \
                   "Thickness_w_7, Thickness_w_8, Thickness_w_9, Thickness_w_10, Thickness_wo_1, Thickness_wo_2, " \
                   "Thickness_wo_3, Thickness_wo_4, Thickness_wo_5, Thickness_wo_6, Thickness_wo_7, Thickness_wo_8, " \
                   "Thickness_wo_9, Thickness_wo_10, ID1_1, ID1_2, ID1_3, ID1_4, ID1_5, ID1_6, ID1_7, ID1_8, ID1_9, " \
                   "ID1_10, ID2_1, ID2_2, ID2_3, ID2_4, ID2_5, ID2_6, ID2_7, ID2_8, ID2_9, ID2_10, ID3_1, ID3_2, ID3_3, " \
                   "ID3_4, ID3_5, ID3_6, ID3_7, ID3_8, ID3_9, ID3_10, Warpage_1, Warpage_2, Warpage_3, Warpage_4, " \
                   "Warpage_5, Warpage_6, Warpage_7, Warpage_8, Warpage_9, Warpage_10, TCC, Powder_Name, Powder_Lot, " \
                   "Date_MO, Duration"
        
        # Construct SQL INSERT statement

        placeholders = ','.join(['?' for _ in range(len(column_names.split(',')))])  # Create placeholders like '?,?,?,...'
        sql_insert = f"INSERT INTO {tableName} ({column_names}) VALUES ({placeholders})"
        
        # Execute INSERT statement
        cursor.execute(sql_insert,data)

        # Commit transaction and close connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error occurred while inserting data: {e}")

#======================================================================================================= 
def edit_drill_database_table(criteria, newData,start_time,end_time):
    """
    Description: Edit values in specific rows of an Access database table based on provided criteria.
    Input:
        criteria: Tuple containing criteria for the row to be edited (Part_Number, Rev, MO_Number).
        newData: List containing new data to be updated in the matching row.
    Output: None
    """
    
    date = datetime.datetime.now()
    current_date = date.date()
    formatted_date = current_date.strftime("%m-%d-%Y")
    duration = str(int(end_time - start_time))
    Time = [str(formatted_date),duration]
    zeroVec = [0]*10
    index = 0
    d = []
    for i in newData:
        if i == []:
            d.append(zeroVec)
            index += 1
        else:
            d.append(newData[index])
            index += 1
    
    newData = []
    for i in d:
        for j in i:
            newData.append(str(float(j)))
    newData = tuple(newData) + tuple(ceramic_info(criteria[0],criteria[2])) + tuple(Time)

    # Check connection

    try:
        # Establish connection
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()
        tableName = 'Drill_DIM_DB'

        # Find the row to update
        sql_select = f"SELECT * FROM {tableName} WHERE Part_number=? AND MO=? AND Rev=?"
        cursor.execute(sql_select, criteria)
        row = cursor.fetchone()

        if row:
            # Update the row
            sql_update = f"UPDATE {tableName} SET "
            columns = ["OD_L_1", "OD_L_2", "OD_L_3", "OD_L_4", "OD_L_5", "OD_L_6", "OD_L_7", "OD_L_8", "OD_L_9", "OD_L_10",
                       "Width_1", "Width_2", "Width_3", "Width_4", "Width_5", "Width_6", "Width_7", "Width_8", "Width_9", "Width_10",
                       "Thickness_w_1", "Thickness_w_2", "Thickness_w_3", "Thickness_w_4", "Thickness_w_5", "Thickness_w_6", "Thickness_w_7", "Thickness_w_8", "Thickness_w_9", "Thickness_w_10",
                       "Thickness_wo_1", "Thickness_wo_2", "Thickness_wo_3", "Thickness_wo_4", "Thickness_wo_5", "Thickness_wo_6", "Thickness_wo_7", "Thickness_wo_8", "Thickness_wo_9", "Thickness_wo_10",
                       "ID1_1", "ID1_2", "ID1_3", "ID1_4", "ID1_5", "ID1_6", "ID1_7", "ID1_8", "ID1_9", "ID1_10",
                       "ID2_1", "ID2_2", "ID2_3", "ID2_4", "ID2_5", "ID2_6", "ID2_7", "ID2_8", "ID2_9", "ID2_10",
                       "ID3_1", "ID3_2", "ID3_3", "ID3_4", "ID3_5", "ID3_6", "ID3_7", "ID3_8", "ID3_9", "ID3_10",
                       "Warpage_1", "Warpage_2", "Warpage_3", "Warpage_4", "Warpage_5", "Warpage_6", "Warpage_7", "Warpage_8", "Warpage_9", "Warpage_10",
                       "TCC", "Powder_Name", "Powder_Lot", "Date_MO", "Duration"]
            for index, column in enumerate(columns):
                sql_update += f"{column}=?"
                if index != len(columns) - 1:
                    sql_update += ", "
            sql_update += " WHERE Part_number=? AND MO=? AND Rev=?"

            # Execute UPDATE statement
            cursor.execute(sql_update, (*newData, *criteria))

            # Commit transaction
            conn.commit()

            print("Data updated successfully.")
        else:
            print("Row not found.")

        # Close connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error occurred while updating data: {e}")


#=======================================================================================================

def write_to_FT_database(part_info_vec,FT_dim_output,start_time,end_time):
    """
    Description: Write information to an Access database table.
    Input:
        filePath: Path to the Access database file.
        tableName: Name of the table where data will be inserted.
        data: Tuple containing data to be inserted into the table.
    Output: None
    """
    DB = 'FT'
    last_id = get_last_used_id(DB)

    # Calculate new ID
    new_id = last_id + 1 if last_id else 1  # If no previous ID, start from 1

    date = datetime.datetime.now()
    current_date = str(date.date())
    duration = str(int(end_time - start_time))
    Time = [current_date,duration]
    zeroVec = [0]*10
    index = 0
    d = []
    for i in FT_dim_output:
        if i == []:
            d.append(zeroVec)
            index+=1
        else:
            d.append(FT_dim_output[index])
            index+=1
    
    data = []
    for i in d:
        for j in i:
            data.append(str(float(j)))
    
    data = (new_id,)+tuple(part_info_vec) + tuple(data) + tuple(ceramic_info(part_info_vec[0],part_info_vec[2])) + tuple(Time) # combine all the data into one vector
   
    try:
        # Establish connection
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()
        tableName = 'FT_DIM_DB'
        # Construct SQL INSERT statement
        # Create placeholders like '?,?,?,...'
        column_names = "ID,Part_number,MO,Rev, "\
                        "OD_L_1,OD_L_2,OD_L_3,OD_L_4,OD_L_5,OD_L_6,OD_L_7,OD_L_8,OD_L_9,OD_L_10,"\
                        "Width_1,Width_2,Width_3,Width_4,Width_5,Width_6,Width_7,Width_8,Width_9,Width_10,"\
                        "Thickness_1,Thickness_2,Thickness_3,Thickness_4,Thickness_5,Thickness_6,Thickness_7,Thickness_8,Thickness_9,Thickness_10,"\
                        "ID1_1,ID1_2,ID1_3,ID1_4,ID1_5,ID1_6,ID1_7,ID1_8,ID1_9,ID1_10,ID2_1,ID2_2,ID2_3,ID2_4,ID2_5,ID2_6,ID2_7,ID2_8,ID2_9,ID2_10,ID3_1,ID3_2,ID3_3,ID3_4,ID3_5,ID3_6,ID3_7,ID3_8,ID3_9,ID3_10,"\
                        "Warpage_1,Warpage_2,Warpage_3,Warpage_4,Warpage_5,Warpage_6,Warpage_7,Warpage_8,Warpage_9,Warpage_10,"\
                        "TCC,Powder_Name,Powder_Lot,Date_MO,Duration"
        
        placeholders = ','.join(['?' for _ in range(len(column_names.split(',')))]) 
        sql_insert = f"INSERT INTO {tableName} ({column_names}) VALUES ({placeholders})"

        # Execute INSERT statement
        cursor.execute(sql_insert, data)

        # Commit transaction and close connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error occurred while inserting data: {e}")  



# FT_dim_output = [['1.2430', '1.2420', '1.2415', '1.2410', '1.2410', '1.2430', '1.2430', '1.2425', '1.2410', '1.2430'],[], [], ['0.0005', '0.0005', '0.0005', '0.0005', '0.0005', '0.0005', '0.0005', '0.0005', '0.0005', '0.0005'], [], [], ['0.0000', '0.0010', '0.0010', '0.0000', '0.0010', '0.0000', '0.0000', '0.0010', '0.0000', '0.0000']]    
# part_info_vec = ['128C466-C-G','430855-01','NCC-20']
# write_to_FT_database(part_info_vec,FT_dim_output)
#=======================================================================================================
#=======================================================================================================
def FT_info_extract(part_number,rev):
    #********************************************************************************************
    #Description: This function fetches data based on input Part number and rev. from Access Database. 
    #             Input: Driver string from Connection_Check(), table_name, Column_name_1, and Column_name_2. 
    #             Output: .  
    #********************************************************************************************
    try:
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        # Establish connection
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()

        # Search Parameters
        table_name = 'AMCDesignMaster'
        column_A = 'JDI_PART__'
        column_B = 'JDI_REV_'
        column_info = ['JDI_PART__', 'JDI_REV_', 'FIN_DIM_MI', 'FIN_TOL_MA', 'FIN_DIM_M2', 'FIN_TOL_M2',
                       'FIN_DIM_M3', 'FIN_TOL_M3', 'FIN_DIM_M5', 'FIN_DIM_MA', 'FIN_DIM_M4', 'FIN_DIM_M6',
                       'FIN_DIM_M7', 'FIN_DIM_M8', '[MAX WARPAGE ALLOWED]']  # Adjusted column names
        # Construct SQL query
        query = f"SELECT {', '.join(column_info)} FROM {table_name} WHERE [{column_A}] LIKE ? AND [{column_B}] = ?"

        # Execute query
        parameters = (f"%{part_number}%", rev)
        cursor.execute(query, parameters)
        data = cursor.fetchone()

        # Convert to a list and handle None values
        # data = [0 if value is None else value for value in data]

        # Close cursor and connection
        cursor.close()
        conn.close()
        data = list(data)
        for i in range(len(data)):
            if data[i] == None:
                data[i] = 0
        return data

    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return []
#=====================================================================================================================
def convert_upper(input_str):
    #********************************************************************************************
    #Description: This function converts any lower case letters in a string to uppercase. 
    #             Input: any string. 
    #             Output: uppercase letter string.  
    #********************************************************************************************
    output_str = ""
    for char in input_str:
        if char.isalpha():  # Check if the character is a letter
            output_str += char.upper()  # Convert the letter to uppercase
        else:
            output_str += char  # Keep non-letter characters unchanged 
    return output_str
#=====================================================================================================================
def entry_check(part_info_vec):
    #********************************************************************************************
    #Description: This function checks data based on input Part number and rev. using Access Database. 
    #             Input: part_info_vec --> part#, mo#, rev from GUI.py. 
    #             Output: Returns True if part number and rev matches else false.  
    #********************************************************************************************
    part_number = convert_upper(part_info_vec[0])
    rev = convert_upper(part_info_vec[2])
    try:
        data = drill_info_extract(part_number,rev)
    except IndexError as e:
        print('Index Error:',e)
        return False
    except Exception as e:
        print('Random Error:',e)
        return False
    if data[0] == part_number and data[1] == rev:
        return True
    else:
        return False
#=====================================================================================================================
def entry_check_drill(part_info_vec):
    #********************************************************************************************
    #Description: This function checks data based on input Part number and rev. using Access Database. 
    #             Input: part_info_vec --> part#, mo#, rev from GUI.py. 
    #             Output: Returns True if part number and rev matches else false.  
    #********************************************************************************************
    part_number = part_info_vec[0]
    MO = part_info_vec[1]
    rev = part_info_vec[2]
    try:
        data = read_drill_database(part_info_vec)
    except IndexError as e:
        print('Index Error:',e)
        return False
    except Exception as e:
        print('Random Error:',e)
        return False
    if data[0] == part_number and data[1] == MO and data[2] == rev:
        return True
    else:
        return False
#=====================================================================================================================
def entry_check_FT(part_info_vec):
    #********************************************************************************************
    #Description: This function checks data based on input Part number and rev. using Access Database. 
    #             Input: part_info_vec --> part#, mo#, rev from GUI.py. 
    #             Output: Returns True if part number and rev matches else false.  
    #********************************************************************************************
    part_number = convert_upper(part_info_vec[0])
    MO = part_info_vec[1]
    rev = convert_upper(part_info_vec[2])
    try:
        data = read_FT_database(part_info_vec)
    except IndexError as e:
        print('Index Error:',e)
        return False
    except Exception as e:
        print('Random Error:',e)
        return False
    if data[0] == part_number and data[1] == MO and data[2] == rev:
        return True
    else:
        return False


#=====================================================================================================================
def login_check(username,password):
    #********************************************************************************************
    #Description: This function checks data based on input Part number and rev. using Access Database. 
    #             Input: part_info_vec --> part#, mo#, rev from GUI.py. 
    #             Output: Returns True if part number and rev matches else false.  
    #********************************************************************************************
   
    # Connection string to the database
   
    # Make dielectic lot as user input,
    # Search Parameters
    try:
            driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
            # Establish connection
            conn = pyodbc.connect(driver=driver)
            cursor = conn.cursor()
            table_name = 'login'
            column_A = 'Username'
            column_B = 'Password'
            column_info = ['Access']
            # Use case-sensitive collation for comparison
            case_sensitive_collation = 'Latin1_General_BIN'
            query = f"""
            SELECT {', '.join(column_info)}
            FROM {table_name}
            WHERE [{column_A}] COLLATE {case_sensitive_collation} = ?
            AND [{column_B}] COLLATE {case_sensitive_collation} = ?
            """
            # Use the 'AND' operator to combine the conditions in the WHERE clause
            parameters = (username, password)
            cursor.execute(query, parameters)
            data = cursor.fetchall()
            
            if not data:
                return []

            # Convert to a list and handle None values
            data = list(data[0])
            data = [0 if value is None else value for value in data]

            # Close the cursor and connection
            cursor.close()
            conn.close()
            
            return data
    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return []


def drill_info_extract(part_number,rev):
    #********************************************************************************************
    #Description: This function fetches data based on input Part number and rev. from Access Database. 
    #             Input: Driver string from Connection_Check(), table_name, Column_name_1, and Column_name_2. 
    #             Output: .  
    #********************************************************************************************
    try:
        # Establish connection
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()

        # Search Parameters
        table_name = 'AMCDesignMaster'
        column_A = 'JDI_PART__'
        column_B = 'JDI_REV_'
        column_info = ['JDI_PART__','JDI_REV_','[Green Dim:OD/L(nom)]','[Green Dim:W(nom)]','[Green Dim: T(min)]','[Green Tol: T(max)]','[Green Dim ID1(min)]','[Green TOL:ID1(max)]','[Green Dim:ID2(min)]','[Green Dim:ID2(max)]','[Green Dim:ID3(min)]','[Green TOL:ID3(max)]','[MAX WARPAGE ALLOWED]']
        # Construct SQL query
        query = f"SELECT {', '.join(column_info)} FROM {table_name} WHERE [{column_A}] LIKE ? AND [{column_B}] = ?"

        # Execute queryS
        parameters = (f"%{part_number}%", rev)
        cursor.execute(query, parameters)
        data = cursor.fetchone()

        # Convert to a list and handle None values
         # Check if data is None and handle accordingly
        if data is None:
            return []

        # Close cursor and connection
        cursor.close()
        conn.close()
        data = list(data)
        for i in range(len(data)):
            if data[i] == None:
                data[i] = 0
        return data

    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return []


def verified_Drill_dimension_info(part_info_vec):
    #********************************************************************************************
    #Description: This function fetches data based on input Part number and rev. from Access Database. 
    #             Input: part_info_vec -> part number,MO#,Rev. 
    #             Output: frame_ID, new_data (all the min and max values),mod_part_info_vec (upper)  
    #********************************************************************************************
    part_number = convert_upper(part_info_vec[0])
    rev = convert_upper(part_info_vec[2])
    data = drill_info_extract(part_number,rev)

    OD_L_min = format(data[2]-(1/1000),'.3f')
    OD_L_max = format(data[2]+(1/1000),'.3f')
    wid_min = format(data[3]-(1/1000),'.3f')
    wid_max = format(data[3]+(1/1000),'.3f')
    Thick_min = format(data[4],'.3f')
    Thick_max = format(data[5],'.3f')
    Thick_no_top_min = format(data[4]-(10/1000),'.3f')
    Thick_no_top_max = format(data[5]-(10/1000),'.3f')
    ID1_min = format(data[6],'.3f')
    ID1_max = format(data[7],'.3f')
    ID2_min = format(data[8],'.3f') 
    ID2_max = format(data[9],'.3f')
    ID3_min = format(data[10],'.3f') 
    ID3_max = format(data[11],'.3f')
    warpage = format(data[12],'.3f')

    frame_ID = []
    if data[3] == 0:
        frame_ID.extend(['OD','Thickness\nWith Top Layer','Thickness\nWithout Top Layer','ID A'])
    elif data[3] != 0:
        frame_ID.extend(['Length','Width','Thickness\nWith Top Layer','Thickness\nWithout Top Layer','ID A'])

    if data[8] != 0 and data[9] != 0:
        frame_ID.extend(['ID B'])
    if data[10] != 0 and data[11] != 0:
        frame_ID.extend(['ID C'])

    if data[12] != 0:
        frame_ID.extend(['Warpage'])

    frame_ID.append('Review')

    new_data = [data[0],data[1],OD_L_min, OD_L_max, wid_min, wid_max, Thick_min, Thick_max,Thick_no_top_min,Thick_no_top_max, ID1_min, ID1_max, ID2_min, ID2_max, ID3_min, ID3_max, warpage]
    mod_part_info_vec = [part_number,part_info_vec[1],rev]
    return frame_ID, new_data,mod_part_info_vec




def verified_Fired_dimension_info(part_info_vec):
    #********************************************************************************************
    #Description: This function fetches data based on input Part number and rev. from Access Database. 
    #             Input: part_info_vec -> part number,MO#,Rev. 
    #             Output: frame_ID, new_data (all the min and max values),mod_part_info_vec (upper)  
    #********************************************************************************************
    part_number = convert_upper(part_info_vec[0])
    rev = convert_upper(part_info_vec[2])
    data = FT_info_extract(part_number,rev)

    OD_L_min = format(data[2],'.3f')
    OD_L_max = format(data[3],'.3f')
    wid_min = format(data[4],'.3f')
    wid_max = format(data[5],'.3f')
    Thick_min = format(data[6],'.3f')
    Thick_max = format(data[7],'.3f')
    ID1_min = format(data[8],'.3f')
    ID1_max = format(data[9],'.3f')
    ID2_min = format(data[10],'.3f') 
    ID2_max = format(data[11],'.3f')
    ID3_min = format(data[12],'.3f') 
    ID3_max = format(data[13],'.3f')
    warpage = format(data[14],'.3f')

    frame_ID = []
    if data[4] == 0 and data[5] == 0:
        frame_ID.extend(['OD','Thickness','ID A'])
    elif data[4] != 0 and data[5] != 0:
        frame_ID.extend(['Length','Width','Thickness','ID A'])

    if data[10] != 0 and data[11] != 0:
        frame_ID.extend(['ID B'])
    if data[12] != 0 and data[13] != 0:
        frame_ID.extend(['ID C'])

    if data[14] != 0:
        frame_ID.extend(['Warpage'])

    frame_ID.append('Review')
    new_data = [data[0],data[1],OD_L_min, OD_L_max, wid_min, wid_max, Thick_min, Thick_max, ID1_min, ID1_max, ID2_min, ID2_max, ID3_min, ID3_max, warpage]
    mod_part_info_vec = [part_number,part_info_vec[1],rev]
    return frame_ID, new_data,mod_part_info_vec



    
def read_drill_database(part_info_vec):
    """++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    Description: Write information to an Access database table.
    Input:
        filePath: Path to the Access database file.
        tableName: Name of the table where data will be inserted.
        data: Tuple containing data to be inserted into the table.
    Output: None
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
   
    # Connection string to the database
    driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
    # Establish connection
    conn = pyodbc.connect(driver=driver)
    cursor = conn.cursor()
    # Make dielectic lot as user input,
    # Search Parameters
    table_name = 'Drill_DIM_DB'
    column_A = 'Part_number'
    column_B = 'Rev'
    column_C = 'MO'
    column_info = ["Part_number","MO","Rev","OD_L_1","OD_L_2","OD_L_3","OD_L_4","OD_L_5","OD_L_6","OD_L_7","OD_L_8","OD_L_9","OD_L_10","Width_1","Width_2","Width_3","Width_4","Width_5","Width_6","Width_7","Width_8","Width_9","Width_10","Thickness_w_1","Thickness_w_2","Thickness_w_3","Thickness_w_4","Thickness_w_5","Thickness_w_6","Thickness_w_7","Thickness_w_8","Thickness_w_9","Thickness_w_10","Thickness_wo_1","Thickness_wo_2","Thickness_wo_3","Thickness_wo_4","Thickness_wo_5","Thickness_wo_6","Thickness_wo_7","Thickness_wo_8","Thickness_wo_9","Thickness_wo_10","ID1_1","ID1_2","ID1_3","ID1_4","ID1_5","ID1_6","ID1_7","ID1_8","ID1_9","ID1_10","ID2_1","ID2_2","ID2_3","ID2_4","ID2_5","ID2_6","ID2_7","ID2_8","ID2_9","ID2_10","ID3_1","ID3_2","ID3_3","ID3_4","ID3_5","ID3_6","ID3_7","ID3_8","ID3_9","ID3_10","Warpage_1","Warpage_2","Warpage_3","Warpage_4","Warpage_5","Warpage_6","Warpage_7","Warpage_8","Warpage_9","Warpage_10","Date_MO","Duration"]
    # Use the 'AND' operator to combine the conditions in the WHERE clause
    query = f"SELECT {', '.join(column_info)} FROM {table_name} WHERE [{column_A}] LIKE ? AND [{column_B}] LIKE ? AND [{column_C}] LIKE ?"
    # Use the 'AND' operator to combine the conditions in the WHERE clause
    parameters = (f"%{part_info_vec[0]}%", f"%{part_info_vec[2]}%",f"%{part_info_vec[1]}%")
    cursor.execute(query, parameters)
    data = cursor.fetchall()
     # Convert to a list
    data = list(data[0])
    for i in range(len(data)):
        if data[i] == None:
            data[i] = 0
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return data


def read_FT_database(part_info_vec):
    """
    Description: Write information to an Access database table.
    Input:
        filePath: Path to the Access database file.
        tableName: Name of the table where data will be inserted.
        data: Tuple containing data to be inserted into the table.
    Output: None
    """
    driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
    # Establish connection
    conn = pyodbc.connect(driver=driver)
    cursor = conn.cursor()
    # Make dielectic lot as user input,
    # Search Parameters
    table_name = 'FT_DIM_DB'
    column_A = 'Part_number'
    column_B = 'Rev'
    column_C = 'MO'
    column_info = ["Part_number",	"MO",	"Rev",	"OD_L_1",	"OD_L_2",	"OD_L_3",	"OD_L_4",	"OD_L_5",	"OD_L_6",	"OD_L_7",	"OD_L_8",	"OD_L_9",	"OD_L_10",	"Width_1",	"Width_2",	"Width_3",	"Width_4",	"Width_5",	"Width_6",	"Width_7",	"Width_8",	"Width_9",	"Width_10",	"Thickness_1",	"Thickness_2",	"Thickness_3",	"Thickness_4",	"Thickness_5",	"Thickness_6",	"Thickness_7",	"Thickness_8",	"Thickness_9",	"Thickness_10",	"ID1_1",	"ID1_2",	"ID1_3",	"ID1_4",	"ID1_5",	"ID1_6",	"ID1_7",	"ID1_8",	"ID1_9",	"ID1_10",	"ID2_1",	"ID2_2",	"ID2_3",	"ID2_4",	"ID2_5",	"ID2_6",	"ID2_7",	"ID2_8",	"ID2_9",	"ID2_10",	"ID3_1",	"ID3_2",	"ID3_3",	"ID3_4",	"ID3_5",	"ID3_6",	"ID3_7",	"ID3_8",	"ID3_9",	"ID3_10",	"Warpage_1",	"Warpage_2",	"Warpage_3",	"Warpage_4",	"Warpage_5",	"Warpage_6",	"Warpage_7",	"Warpage_8",	"Warpage_9",	"Warpage_10","Date_MO","Duration"]
    # Use the 'AND' operator to combine the conditions in the WHERE clause
    query = f"SELECT {', '.join(column_info)} FROM {table_name} WHERE [{column_A}] LIKE ? AND [{column_B}] LIKE ? AND [{column_C}] LIKE ?"
    # Use the 'AND' operator to combine the conditions in the WHERE clause
    parameters = (f"%{part_info_vec[0]}%", f"%{part_info_vec[2]}%",f"%{part_info_vec[1]}%")
    cursor.execute(query, parameters)
    data = cursor.fetchall()
     # Convert to a list
    data = list(data[0])
    for i in range(len(data)):
        if data[i] == None:
            data[i] = 0
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return data

# part_info_vec = ['12C16-A','1234','NCC-12']
# VALE = read_FT_database(part_info_vec)
# print(VALE)


def passivation_check(part_info_vec):
    part_number = part_info_vec[0]
    rev = part_info_vec[2]
    try:
        # Establish connection
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()

        # Search Parameters
        table_name = 'AMCDesignMaster'
        column_A = 'JDI_PART__'
        column_B = 'JDI_REV_'
        column_info = ["PASS_REQ_D"]
        # Construct SQL query
        query = f"SELECT {', '.join(column_info)} FROM {table_name} WHERE [{column_A}] LIKE ? AND [{column_B}] LIKE ?"

        # Execute query
        parameters = (f"%{part_number}%", f"%{rev}%")
        cursor.execute(query, parameters)
        data = cursor.fetchone()

        # Convert to a list and handle None values
        # data = [0 if value is None else value for value in data]

        # Close cursor and connection
        cursor.close()
        conn.close()
        data = list(data)
        if data[0] == 'YES':
            return True
        else: 
            return False

    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return []

def sign_up(username_get,password_get,access_type_new):
    DB = 'login'
    last_id = get_last_used_id(DB)

    # Calculate new ID
    new_id = last_id + 1 if last_id else 1  # If no previous ID, start from 1
    data = [username_get,password_get,access_type_new]
    data = (new_id,)+tuple(data)
    print(data)
    try:
        # Establish connection
        driver = 'SQL Server;SERVER=jdi-mssql.jdimain.com;UID=amcdesignmaster;PWD=7Z4Pq5=*B~3UXWC8;APP=Microsoft Office;DATABASE=AMCDesignMaster'
        conn = pyodbc.connect(driver=driver)
        cursor = conn.cursor()
        tableName = 'Login'
        # Construct SQL INSERT statement
        # Create placeholders like '?,?,?,...'
        column_names = "UserID,Username,Password,Access"
        
        placeholders = ','.join(['?' for _ in range(len(column_names.split(',')))]) 
        sql_insert = f"INSERT INTO {tableName} ({column_names}) VALUES ({placeholders})"

        # Execute INSERT statement
        cursor.execute(sql_insert, data)

        # Commit transaction and close connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error occurred while inserting data: {e}")  

# part_info_vec = ['12C16-A','123','NCC-12']s
# data = read_FT_database(part_info_vec)
# print(data)
# # part_info_vec = ['12C16-A','1232-21','NCC-1']
# part_info_vec = ['12C16-A','NCC-1','1232-21']
# data = read_drill_database(part_info_vec)
# print(data)
#======================================================================================================= 
# part_info_vec = ['12c16-a','12342','ncc-10']
# condition = entry_check(part_info_vec)
# print(condition)

# # Example usage:
# filePath = r'C:\Users\akohli\Music\Firetest Database\Firetest_Database.accdb'
# tableName = 'Warpage'
# data = ('12C165-A', 'NCC-11', '230123-00')  # Replace 'Value1', 'Value2', 'Value3' with actual data
# write_to_access_database_table(filePath, tableName, data)
# part_info_vec = ['12C16-A','1234','NCC-12']
# VALE = entry_check_FT(part_info_vec)
# print(VALE)