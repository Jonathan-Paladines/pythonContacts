#Activa entorno virtual
#en el cmd, accder a la ruta: C:\Users\USER\Desktop\Entornos\39\env39\Scripts
#activar entorno.
#Regresar a la ruta del proyecto: C:\Users\USER\Desktop\Python\pythonContacts
#y seguir programando...

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL Coneccion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontactos'
mysql = MySQL(app)

#Setings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', contactos=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES(%s, %s, %s)' , 
                    (fullname,phone,email))
        mysql.connection.commit()
        flash('Contacto agregado Satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    dataEdit = cur.fetchall()
    return render_template('edit_contacto.html', contacto = dataEdit[0])


@app.route('/update/<id>',  methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname=request.form['fullname']
        phone=request.form['phone']
        email=request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts 
        SET fullname= %s,
            phone = %s,
            email = %s
        WHERE id = %s
        """, (fullname,phone, email, id))
        mysql.connection.commit()
        flash('Contacto actualizado correctamente')
        return redirect(url_for('Index'))




@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Eliminado Correctamente')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=3000, debug = True)