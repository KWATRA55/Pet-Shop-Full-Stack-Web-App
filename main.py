
# username - admin
# password - admin123







from pandas._libs import missing
import streamlit as st
import pickle
import pandas as pd
import base64


# db management
import sqlite3
conn = sqlite3.connect("data.db")
c = conn.cursor()


con = sqlite3.connect("data1.db")
a = con.cursor()




def create_pettable():
    a.execute('CREATE TABLE IF NOT EXISTS pettable(pet_name TEXT, owner_name TEXT,  owner_res TEXT, pet_age REAL, pet_breed TEXT, pet_color TEXT, pet_weight REAL, pet_unique TEXT)')

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT, password TEXT)')
    
def create_missing():
    a.execute("CREATE TABLE IF NOT EXISTS missing( new_pet_name TEXT, new_owner_name TEXT, contact_owner TEXT, pet_features TEXT, last_seen TEXT)")


def add_userdata(username, password):
    c.execute('INSERT INTO usertable(username, password) VALUES (?,?)', (username, password))
    conn.commit()

def add_petdata(pet_name, owner_name, owner_res, pet_age, pet_breed, pet_color, pet_weight, pet_unique):
    a.execute('INSERT INTO pettable(pet_name, owner_name, owner_res, pet_age, pet_breed, pet_color, pet_weight, pet_unique) VALUES (?,?,?,?,?,?,?,?)', (pet_name, owner_name, owner_res, pet_age, pet_breed, pet_color, pet_weight, pet_unique))
    con.commit()


def add_missing( new_pet_name, new_owner_name, contact_owner , pet_features , last_seen ):
    a.execute("INSERT INTO missing( new_pet_name, new_owner_name, contact_owner , pet_features , last_seen ) VALUES (?,?,?,?,?)", ( new_pet_name, new_owner_name, contact_owner , pet_features , last_seen ))
    con.commit()


def login_user(username, password):
    c.execute('SELECT * FROM usertable WHERE username =? AND password =?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data

def view_all_pet():
    a.execute('SELECT * FROM pettable')
    data = a.fetchall()
    return data


def view_all_missing():
    a.execute('SELECT * FROM missing')
    data = a.fetchall()
    return data



missing_report = 1

def main():
    # simple login app

    st.title("Pet Shop Online Portal")

    menu = ("Home", "View All missing Pets","Add a missing Pet","Login")
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.markdown(""" 
        ## Add Your Pet Details """)

        # pet details
        pet_name = st.text_input("Pet's Name" )
        owner_name = st.text_input("Owner Name")
        owner_res = st.text_area("Owner's residence and contact info")
        pet_age = st.number_input("Pet's Age (In Months)", step=0.1 )
        breed = ("Dog-lebra", "Dog-pitbull", "Dog-other", "Bird", "Cat", "Rabbit", "Snake", "Hamster")
        pet_breed = st.selectbox("Pet's Breed", breed)
        pet_color = st.text_input("Pet's Color")
        pet_weight = st.number_input("Pet's Weight (In Kgs)", step=0.1)
        pet_unique = st.text_area("Pet's Unique Features")

        button = st.button("Submit")
        if button:
            create_pettable()
            add_petdata(pet_name, owner_name, owner_res, pet_age, pet_breed, pet_color, pet_weight, pet_unique)
            st.success("Thankyou, You have successfully entered all the details")





    elif choice == "Login":
        st.subheader("Login Alert : Only For Admin")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type= "password")
        if st.sidebar.checkbox("Login"):

            create_pettable()
            create_usertable()
            
            result = login_user(username, password)
            if result:

                st.success("Logged in as {}".format(username))

                # This is our dashboard
                task = st.selectbox("Task", ["View All", "Analytics", "Profile"])
                
                if task == "View All":
                    
                    st.write("Username :  " + username )
                    st.write("Password : " + password)

                    data = view_all_pet()
                    data = pd.DataFrame(data)
                    data.columns = ['pet_name', 'owner_name', 'owner_res', 'pet_age', 'pet_breed', 'pet_color', 'pet_weight', 'pet_unique']
                    data
            else:
                st.error("Invalid Username/Password")



    # add a missing pet
    elif choice == "Add a missing Pet":
        st.markdown(""" ## Add a missing Pet """)
        photo = st.file_uploader("Add a picture of the missing Pet", type= ["jpg", "jpeg", "png", "pdf"])
        new_pet_name = st.text_input("Add the Pet name")
        new_owner_name = st.text_input("Add the Owner name")
        contact_owner = st.text_input("Add your contact info")
        pet_features = st.text_input("Add your Pet features")
        last_seen = st.text_input("when's the last time you saw your pet?")

        submit = st.button("Submit")
        if submit:
            create_missing()


            add_missing( new_pet_name, new_owner_name, contact_owner , pet_features , last_seen )
            st.success("You have successfully added your pet to the missing column")



    # view all missing pets
    elif choice == "View All missing Pets":
        st.markdown(""" ## View All missing Pets """)
        data = view_all_missing()

        missing_report = 1
        for row in data:
            new_pet_name = row[0]
            new_owner_name = row[1]
            contact_owner  = row[2] 
            pet_features = row[3] 
            last_seen = row[4]
            

            

            st.write("missing report : {}".format(missing_report))
            
            st.write("Pet Name : {}".format(new_pet_name))
            st.write("Owner Name : {}".format(new_owner_name))
            st.write("Owner Details : {}".format(contact_owner))
            st.write("Pet Features : {}".format(pet_features))
            st.write("Last seen : {}".format(last_seen))
            st.write("____________________________________________________________________________________")
            missing_report = missing_report + 1


        



if __name__ == "__main__":
    main()