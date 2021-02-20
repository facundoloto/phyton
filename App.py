from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_mail import Mail,Message







app = Flask(__name__)

mysql = MySQL()

# Configuración del email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USE_TLS']= False
app.config['MAIL_USERNAME']='pythonacme01@gmail.com'
app.config['MAIL_PASSWORD']='01_python'



mail = Mail(app)  # 2. Instanciamos un objeto de tipo Mail



# Mysql Connection

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'acme'
mysql.init_app(app)


# settings
app.secret_key = "key"





# routes
@app.route('/')
def Index(): #esta fucniona sirve para cargar todos los datos de la tabla user y enviarselas al index.html
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)#renderiza html



@app.route('/add_contact', methods=['POST'])
def add_contact(): #agrega datos una table 
      
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contraseña = request.form['contraseña']
        conex = mysql.connection.cursor()
        conex.execute("SELECT Email FROM user")
        datos = conex.fetchall()
        mysql.connection.commit()
        conex.close()
        comparar=True
        for i in range(len(datos)):
         if  email in datos[i]:
               flash("email en uso")
               comparar=False
               break
         
           
         
         
              
        if    comparar:
               cur = mysql.connection.cursor()
               cur.execute("INSERT INTO user (Nombre,Apellido,Email,Contraseña) VALUES (%s,%s,%s,%s)", (nombre,apellido,email,contraseña))
               mysql.connection.commit()
               #enviamos un email de bienvenida al usuario
               msg = Message("Verificacion", sender="pythonacme01@gmail@gmail.com", recipients=[email])
               msg.body = 'ACME'
               msg.html = '<h1>ACME COMPANY</h1><p>Este es un email para darles la bienvenida a nuestra compania,abajo le dejamos los datos para que ingrese a la plataforma de la empresa.</p><p>Email: '+email+'</p><p>Contraseña: '+contraseña+'</p>'
               mail.send(msg)
               flash('usuario agregado')
               return redirect(url_for('Index'))
        else:
              return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contraseña = request.form['contraseña']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE user
            SET Nombre = %s,
                Apellido = %s,
                Email = %s,
                Contraseña=%s
            WHERE id ="""+id+"""
        """, (nombre,apellido,email,contraseña))
        flash('Usuario modificado')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM user WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario eliminado')
    return redirect(url_for('Index'))


# starting the app
if __name__ == "__main__":
    app.run(port=5500, debug=True)
