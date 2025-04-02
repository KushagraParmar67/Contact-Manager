import pandas as p, re

class Contact_Manager:
    def __init__(self,file="LogiQlink_Task_Data.csv",):
        self.file = file
        self.data_set = self.load_csv()
    
    def validator(self, data, data_type="Email"):
        pattern_of_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        pattern_of_phone = r'^\d{10}$'
        if data_type == "Email":
            if re.match(pattern_of_email, data):
                return True
            return False
        else:
            if re.match(pattern_of_phone, data):
                return True
            return False
            
    def message(self, msg):
        print(f"--------- {msg} ---------")

    def load_csv(self):
        try:
            data_set = p.read_csv(self.file)
            return data_set
        except FileNotFoundError:
            print(f"{self.file} File Not Found")    

    def display_all_contacts(self):
        print(self.data_set)
        self.message("Data Displayed.")

    def search_contacts(self, by_name=None):
        if by_name == " " or by_name=="":
            self.message("Please Provide a Name.")
        else:
            new_data_set = self.data_set[self.data_set["Name"].str.startswith(by_name)]
            print(new_data_set)

    def add_contact(self, data):
        new_row = p.DataFrame([data])
        if self.validator(data=str(data['Phone_Number']), data_type="Phone_Number"):
            if self.validator(data=data['Email']):    
                self.data_set = p.concat([self.data_set, new_row], ignore_index=True)
                self.data_set.to_csv('LogiQlink_Task_Data.csv', index=False)
                self.message("Data Uploaded Successfully.")
            else:
                self.message("Please Provide valid Email.")
        else:
            self.message("Please Provide valid Phone Number.")
    
    def delete_contacts(self, by_Id=None):
        if by_Id == None:
            self.message("Please Provide a Name.")
        else:
            if by_Id in self.data_set['Contact_Id'].values:
                self.data_set = self.data_set[self.data_set['Contact_Id'] != by_Id]
                self.data_set.to_csv(self.file, index=False)
                self.message(f"Deleted contact with Contact_Id: {by_Id}")
            else:
                self.message(f"Not found contact with Contact_Id: {by_Id}")

manager = Contact_Manager()
while True:
    try:
        choice = int(input("Welcome to Contact Manager. \n Enter 1 for View All Contacts. \n Enter 2 for Search in Contacts. \n Enter 3 for Add the Contact. \n Enter 4 for Delete the Contact. \n Enter 5 for Exit. \n Your Choice: "))
        match choice:
            case 1:
                manager.display_all_contacts()
            case 2:
                query = input("Enter Name of the contacts: ") 
                manager.search_contacts(by_name=query)
            case 3:
                data = {"Contact_Id":int(input("Enter Contact_Id: ")), "Name": input("Enter Name: "), "Phone_Number": int(input("Enter Phone Number: ")), "Email": input("Enter Email: ")}
                manager.add_contact(data)
            case 4:
                Id = int(input("Enter Contact_Id you want to Delete: "))
                manager.delete_contacts(by_Id=Id)
            case 5:
                exit()
            case _:
                raise ValueError()
    except TypeError:
        manager.message("Please Provide value with valid data type")
    except ValueError:
        manager.message("--------Please Enter Number Between 1 to 5.--------")