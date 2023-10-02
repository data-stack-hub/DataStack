'''
user authantication functionality in the app
- two type of framework 1. sessionbased 2. token based  ---will go with session based 
- we need a database to store username and password
    the database shoule be seperate for each app. it make sense if the database can be created on the same folder where the user scraip is and same as entry script name.

    this will create a db file and admin user as default
    imprort datastack as ds
    ds.set_oonfig(
        {
            "auth":True,
            "db_location":"firebase.app.com" //default: .
            "admin_user_id":"vishal_vora",
            "admin_password":"123test"
        }
    )
- once the user get authanticated the data the auth related information can be stored to session
- the function can be protected using decorator

    @auh
    def get_information():
        return information

- current user related information
    ds.get_current_user()
    responde:
        {
            "user_name":'vishal vora'
            "user_id":123,
            "role":"admin",
        }

- show user related information
    def some_function():
        if ds.get_current_user()['roll'] == 'admin'
            ds.write('you are a admin')
        else:
            ds.write('you are not an admin')
'''