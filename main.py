from flash import Flask, render_template
import util 

#create an application instance 
#all requests it receives from clients to this object for handling
#we are instantiating a Flask object by passing __name__ argument to the Flask constructor. 
# The Flask constructor has one required argument which is the name of the application package.
#Most of the time __name__ is the correct value. The name of the application package is used
#by Flask to find static assets, templates and so on.
app = Flask(__name__)

#evil global variables
#can be placed in a config file
#here is a possible tutorial how you can do this
username = 'oscar'
password = 'test'
host = '127.0.0.1'
port = '5432'
database = 'dvdrental'

#route is used to map a URL with a Python function
#complete address: ip:port/
#127.0.0.1:5000/api/
# in this case it is for the update the basket_a
@app.route('/api/update_basket_a')
#this is how to define the function of update_basket_a

def update_basket_a():
#TODO: connect to DB
  cursor,connection = util.connect_tp_db(username,password,host,port,database)
#TODO: Insert a new row into basket_a
#use function in util.py
  record = util.run_and_commit_sql(cursor, connection,"INSERT into basket_a (a, fruit_a) values (5, 'Cherry');")
#It will on the browser either message depending if the row was inserted into the basket_a
  if record == -1:
    print('Something is wrong with the SQL command')
  else:
    print ('Success!')

#TODO: Disconnect from database
util.disconnect_from_db(connection,cursor)

#Using render_template function, Flask will search 
#the file named update_basket_a.html under templates folder
return render_template('update_basket_a.html',log_html = record)

#route is used to map a URL with a Python function
#complete address: ip:port/
#127.0.0.1:5000/api/
# in this case it is for the unique
@app.route('/api/unique')
#this is how you define the function in Python 
def unique():
#connect to DB
  cursor, connection = util.connect_to_db(username,password,host,port,database)
#execute SQL commands
  record2 = util.run_and_fetch_sql(cursor,"select a,fruit_a,b,fruit_b from basket_a full join basket_b on fruit_a = fruit_b where a is null or b is null;")
if record2 == -1:
  print('404 page was not found')
else:
#this will return all column names of the select result table
  col_names = [desc[0] for desc in cursor.description]
#only use up to the first five rows
  log = record2[:5]
#disconnect from database
  util.disconnect_from_db(connection,cursor)
#using render_template function, Flask will search 
#the file named unique.html under templates folder 
return render_template('unique.html',sql_table = log, table_title=col_names)

if __name__ == '__main__':
# set debug mode
    app.debug = True
#your local machine ip
    ip = '127.0.0.1'
    app.run(host=ip)
