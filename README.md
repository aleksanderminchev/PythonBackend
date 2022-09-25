# PythonBackend
A webshop backend redesign  
## The webshop database is a mongoDB database  
This project uses django and djongo(mongoDb addapter)  
An email service is used to confirm the email.  
Uses pipenv for a python enviroment in folder backend.  
Basic CRUD functions are created for users,furniture and orders.  
Full integration with frontend has not been achieved.   
Example of API routes:  
  **GET orders** - retrives all objects with the same name in DB  
  **POST orders** - creates 1 object in the DB of the same type  
  **PUT orders**- **updates 1 object in the DB of the same type  
  **GET orders/<id>** - retrieves 1 object that matches the id   
  **DELETE orders/<id>** - deletes 1 object that matches the id  
  **POST login** - logs in the user and gives back a jwt token with all the data   
  **GET confirmation/<confirmationString>**- route used to confirm the email address of the user  
### You can replace orders with furniture/users  
Users password gets hashed.  
