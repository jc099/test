from flask import Flask
from flask import render_template,request,redirect,url_for, flash
from flaskext.mysql import MySQL
from flask import jsonify

app= Flask(__name__)
app.secret_key="develoteca"

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sist_inscrip'

mysql.init_app(app)

@app.route('/')
def index():

    return render_template('inscripcion/index.html')

@app.route('/confirm')
def confirm():

    return render_template('inscripcion/confirm.html')

@app.route('/logueo')
def logueo():

    return render_template('inscripcion/logueo.html')

@app.route('/log', methods=['POST'])
def log():

    _dni=request.form['txtDni']

    conn= mysql.connect()  
    cursor= conn.cursor()
    cursor.execute("SELECT COUNT(dni) FROM `participante` WHERE dni LIKE %s;", _dni)
    dnirep=cursor.fetchall()
    conn.commit()

    print(dnirep)
    if dnirep == ((1,),):
        flash("ATENCION!!!: El numero de documento ingresado se encuentra registrado", 'alert-warning')
        return redirect(url_for('confirm')) 
      
    return render_template('inscripcion/preinscripcion.html')

@app.route('/preinscripcion')
def preinscripcion():

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM provincia ORDER BY nombre")
    prov=cursor.fetchall()
    cursor.execute("SELECT * FROM distancia ORDER BY distancia")
    distancia=cursor.fetchall()
    cursor.execute("SELECT * FROM talle ORDER BY talle")
    talle=cursor.fetchall()
    cursor.execute("SELECT * FROM categoria ORDER BY categoria")
    categoria=cursor.fetchall()
    conn.commit()
    return render_template('inscripcion/preinscripcion.html', provs=prov, distancias=distancia, talles=talle, categorias=categoria)

@app.route('/store', methods=['POST'])
def storage():

    conn= mysql.connect()

    _nombre=request.form['txtNombre']
    _dni=request.form['txtDni']
    _fechanac=request.form['txtFecnac']
    _correo=request.form['txtCorreo']
    _ciu=request.form['localidad']
    _direccion=request.form['txtDireccion']
    _celular=request.form['txtCelular']
    _celular2=request.form['txtCelular2']
    _categoria=request.form['categoria']
    _distancia=request.form['distancia']
    _talle=request.form['talle']


    if _dni == ((1,),):
        flash("ATENCION!!!: El numero de documento ingresado se encuentra registrado, REPITA el procedimiento", 'alert-warning')
        return redirect(url_for('Confirm'))

    if _nombre =='' or _dni =='' or _ciu =='' or _fechanac =='' or _correo =='' or _celular =='' or _direccion =='' or _categoria ==''or _distancia =='' or _talle =='':
        flash("ATENCION!!!: Debe llenar todos los campos requeridos", 'alert-warning')
        return redirect(url_for('confirm'))
   
    if _nombre !='' or _dni !='':
        sql ="INSERT INTO `participante` (`idparticipante`, `apenom`, `dni`, `fecnac`, `mail`, `idciudad`, `direccion`, `celular`, `celular2`, `idcategoria`, `iddistancia`, `idtalle`)  VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        datos=(_nombre,_dni,_fechanac,_correo,_ciu,_direccion,_celular,_celular2,_categoria,_distancia,_talle)
        print(datos)
        cursor= conn.cursor()
        cursor.execute(sql,datos)
        conn.commit()

    flash("Los Datos Han Sido Cargado Satisfactoriamente", 'alert-success')
    return redirect(url_for('confirm'))

@app.route("/ciudad",methods=["POST","GET"])
def ciudad():  
    
    conn= mysql.connect()
    cursor=conn.cursor()
    if request.method == 'POST':
        p_id = request.form['prov_id']
        result = cursor.execute("SELECT * FROM localidad WHERE provincia_id = %s ORDER BY nombre ASC;", [p_id] )
        ciu = cursor.fetchall()
        OutputArray = []
        for row in ciu:
            outputObj ={
                'id': row[0],
                'name': row[2]}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)


@app.route('/listado')
def listado():
  
    conn= mysql.connect()
    cursor= conn.cursor() 
    cursor.execute("SELECT * FROM participante inner join categoria inner join distancia inner join localidad inner join provincia WHERE localidad.id= participante.idciudad and provincia.id=localidad.provincia_id and participante.idcategoria=categoria.idcategoria and participante.iddistancia=distancia.iddistancia")
    participante=cursor
    conn.commit()
    return render_template('inscripcion/listado.html', participantes=participante)

@app.route('/5kmjrs1819')
def kmjrs1819():
        
    sql="SELECT * FROM participante inner join categoria inner join distancia inner join localidad inner join provincia WHERE participante.iddistancia LIKE 4 and participante.idcategoria LIKE 9 and localidad.id= participante.idciudad and provincia.id=localidad.provincia_id and participante.idcategoria=categoria.idcategoria and participante.iddistancia=distancia.iddistancia ;"
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql)
    participante= cursor.fetchall()
    print(participante)
    conn.commit()
    return render_template('inscripcion/5kmjrs1819.html', participantes=participante)

@app.route('/busqueda')
def busqueda():

    return render_template('inscripcion/busqueda.html')

if __name__== '__main__':
    app.run(debug=True)