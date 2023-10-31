from flash import Flask, render_template
import util 

app = Flask(__name__)

username = 'oscar'
password = 'test'
host = '127.0.0.1'
port = '5432'
database = 'dvdrental'

@app.route('/api/update_basket_a')

def update_basket_a():
  cursor,connection = util.connect_tp_db(username,password,host,port,database)
  record = util.run_and_commit_sql(cursor, connection,"INSERT into basket_a (a, fruit_a) values (5, 'Cherry');")
  if record == -1:
    print('Something is wrong with the SQL command')
  else:
    print ('Success!')
    
util.disconnect_from_db(connection,cursor)

return render_template('update_basket_a.html',log_html = record)

@app.route('/api/unique')

def unique():
  cursor, connection = util.connect_to_db(username,password,host,port,database)
  
  record2 = util.run_and_fetch_sql(cursor,"select a,fruit_a,b,fruit_b from basket_a full join basket_b on fruit_a = fruit_b where a is null or b is null;")
  
if record2 == -1:
  print('Something is wrong with the SQL command')
else:
  col_names = [desc[0] for desc in cursor.description]
  log = record2[:5]
  util.disconnect_from_db(connection,cursor)
  
return render_template('unique.html',sql_table = log, table_title=col_names)

if __name__ == '__main__':
	
    app.debug = True

    ip = '127.0.0.1'
    app.run(host=ip)
