import psycopg2

#connect to postgres database
try:
    connection = psycopg2.connect(
            host = "127.0.0.1",
            port = "5432",
            database = "digital_phone_book",
            user = "postgres",
            password = "r@hulp@ndey"
    )

    print("Database Connected")
except Exception as e:
    print("Error: ",e)
    print("Database Connection Failed")


connection.autocommit = True
cursor = connection.cursor()

# add data in database
def add(user_name):

    while True:
        permission = input("YOU WANT ADD CONTACT PRESS Y OTHERWISE N")

        if permission.upper() == 'Y':
            name = input("Enter name : ")
            number = input("Enter number : ")
    
            sql_query = f'''
                            INSERT INTO {user_name} VALUES('{name}','{number}');
                        '''
    
            cursor.execute(sql_query)
        else:
            break

# read all a data of user from database
def read(user_name):
    sql_query = f'''
                    SELECT * FROM {user_name};
                '''
        
    cursor.execute(sql_query)

    datas = cursor.fetchall()
    
    for data in datas:
        print(data[0],"------>>>",data[1])

# read any specfic data of user from database
def read_specfic(user_name,contact_name):
    sql_query = f'''
                    SELECT * FROM {user_name};
                '''
        
    cursor.execute(sql_query)

    datas = cursor.fetchall()

    for data in datas:
        if data[0] == contact_name:
            print(data[0],"------>>>>",data[1])
            break
    else:
        print("NOT FOUND")

# update data of user in database
def update(user_name,name,number):
    sql_query = f'''
                    UPDATE {user_name} SET phone_number='{number}' WHERE contact_person_name = '{name}';
                '''
    
    cursor.execute(sql_query)

# delete all data of user from database
def delete(user_name):
    sql_query = f'''
                    DELETE FROM {user_name};
                '''
    cursor.execute(sql_query)

# delete any specfic data of user from database
def delete_specfic(user_name,name):
    sql_query = f'''
                    DELETE FROM {user_name} WHERE contact_person_name = '{name}';
                '''
    cursor.execute(sql_query)

# perform add,read,update, and delete opertions
def digital_phone_book(user_name):
    print('''
            WELCOME TO DIGITAL PHONE BOOK
            PRESS A FOR ADD CONTACT
            PRESS R FOR READ CONTACT
            PRESS U FOR UPDATE CONTACT
            PREES D FOR DELETE CONTACT
        ''')
    
    operation = input("WHICH OPERTION YOU WANT TO PERFORM : ")

    if operation.upper() == 'A':
        add(user_name)
    elif operation.upper() == 'R':
        print('''
                PRESS 1 FOR READ ALL CONTACT
                PRESS 2 FOR READ SPECIFIC CONTACT
            ''')
        
        res = input("WHICH OPERATION YOU WANT TO PERFORM : ")

        if res == '1':
            read(user_name)
        elif res == '2':
            contact_name = input("Enter a name of person")
            read_specfic(user_name,contact_name)
        else:
            print("INVALID INPUT")

    elif operation.upper() == 'U':
        name = input("Enter a person who contact number you want to update name : ")
        number = input("Enter a update number : ")
        update(user_name,name,number)
    elif operation.upper() == 'D':
        print('''
                PRESS 1 FOR DELETE ALL CONTACT
                PRESS 2 FOR DELETE SPECIFIC CONTACT
            ''')
        
        res = input("WHICH OPERATION YOU WANT TO PERFORM : ")

        if res == '1':
            delete(user_name)
        elif res == '2':
            name = input("Enter person name you want to delete : ")
            delete_specfic(user_name,name)
        else:
            print("INVALID INPUT")

    else:
        print("INVALID INPUT")
    
# user details taken for user
def user_details():
    user_name = input("Name : ")
    user_password = input("Password : ")

    return user_name,user_password

# check whether user exists or not
def user_exists(user_info):

    sql_query = f'''
                    SELECT * FROM users;
                '''
    
    cursor.execute(sql_query)
    users = cursor.fetchall()

    print(users)

    for user in users:
        print("Run")
        if user[0] == user_info[0]:
            return True,user
    
    return False,""

# check whether user password is correct or not
def check_password(check_user_exists,user_info):
    if check_user_exists[1][1] == user_info[1]:
        return True
    else:
        return False

# create sperate table for each user to store data
def seperate_data_for_each_user(user_name):
    sql_query = f'''
                    CREATE TABLE {user_name}(contact_person_name text,phone_number text);
                '''
    
    cursor.execute(sql_query)

# user can register here and if user is already exists then user will login autocompletely
def registered(user_info):
    
    check_user_exists = user_exists(user_info)
    print(check_user_exists)

    if check_user_exists[0]:
        print("USER ALREADY EXISTS")

        check_user_password = check_password(check_user_exists,user_info)

        if check_user_password:
            digital_phone_book(user_info[0])
        else:
            print("WRONG PASSWORD")
        
    else:
        sql_query = f'''
                        INSERT INTO users(user_name,user_password) VALUES('{user_info[0]}','{user_info[1]}')
                    '''
        
        cursor.execute(sql_query)

        # create sperate table for each user to store data
        seperate_data_for_each_user(user_info[0])

        print("Successfully Register")
        digital_phone_book(user_info[0])

# register user can login here and if user not exists then user will register first
def login(user_info):

    check_user_exists = user_exists(user_info)
    print(check_user_exists)

    if check_user_exists[0]:
        
        check_user_password = check_password(check_user_exists,user_info)

        if check_user_password:
            digital_phone_book(user_info[0])
        else:
            print("WRONG PASSWORD")
    else:
        print("USER NOT REGISTER")
        print()
        print(input("PRESS ENTER FOR REGISTER"))
        # user details taken from user
        user_info = user_details()
        # user can register here and if user is already exists then user will login autocompletely
        registered(user_info)


def main():
    print("WELCOME TO DIGITAL PHONE BOOK")
    print('''
            PRESS R FOR REGISTER
            PRESS L FOR LOGIN
        ''')
    
    user_input = input("Register or Login ")

    if user_input.upper() == 'R':
        # user details taken from user
        user_info = user_details()
        # user can register here and if user is already exists then user will login autocompletely
        registered(user_info)
    elif user_input.upper() == 'L':
        # user details taken from user
        user_info = user_details()
        # user can register here and if user is already exists then user will login autocompletely
        login(user_info)
    else:
        print("INVALID INPUT")

main()