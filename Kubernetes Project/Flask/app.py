from flask import Flask, jsonify, render_template
import mysql.connector
import os
import base64


app = Flask(__name__)

encoded_password = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_PASSWORD'] = base64.b64decode(encoded_password).decode('utf-8')
app.config['DB_HOST'] = os.environ.get('DB_HOST')
app.config['DATABASE'] = os.environ.get('DATABASE')


@app.route("/")
def test_db_connection():
    try:
        # Connect to the database
        cnx = mysql.connector.connect(
            user='root',
            password=app.config['MYSQL_PASSWORD'],
            host=app.config['DB_HOST'],
            database=app.config['DATABASE']
        )
        cursor = cnx.cursor()

        cursor.execute('SELECT 1;')

        while cursor.nextset():
             pass
        
        # If no exceptions were thrown, the connection was successful
        return render_template('success.html')#"Database connection successful"
   
    except mysql.connector.Error as e:
        return render_template('error.html')
    #finally:
        # Close the database connection
     #   cursor.close()
     #   cnx.close()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=9999)
