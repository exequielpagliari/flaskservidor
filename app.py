

from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Mariela@localhost:3308/plantapiloto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino la tabla
class Curso(db.Model):   # la clase Cursos hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(250))
    link=db.Column(db.String(250))
    imagen=db.Column(db.String(250))
    fechaInicio=db.Column(db.String(100))
    fechaFinalizacion=db.Column(db.String(100))
    estado=db.Column(db.String(100))
    def __init__(self,nombre, link, imagen, fechaInicio, fechaFinalizacion, estado):   #crea el  constructor de la clase
        self.nombre = nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.link = link
        self.imagen=imagen
        self.fechaInicio=fechaInicio
        self.fechaFinalizacion=fechaFinalizacion
        self.estado=estado

with app.app_context():
    db.create_all()  # aqui crea todas las tablas

#  ************************************************************
class CursoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','link','imagen', 'fechaInicio', 'fechaFinalizacion', 'estado')

curso_schema=CursoSchema()            # El objeto curso_schema es para traer un curso
cursos_schema=CursoSchema(many=True)  # El objeto cursos_schema es para traer multiples registros de cursos


# crea los endpoint o rutas (json)
@app.route('/cursos',methods=['GET'])
def get_Cursos():
    all_cursos=Curso.query.all()         # el metodo query.all() lo hereda de db.Model
    result=cursos_schema.dump(all_cursos)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla




@app.route('/cursos/<id>',methods=['GET'])
def get_curso(id):
    curso=Curso.query.get(id)
    return curso_schema.jsonify(curso)   # retorna el JSON de un curso recibido como parametro




@app.route('/cursos/<id>',methods=['DELETE'])
def delete_curso(id):
    curso=Curso.query.get(id)
    db.session.delete(curso)
    db.session.commit()
    return curso_schema.jsonify(curso)   # me devuelve un json con el registro eliminado


@app.route('/cursos', methods=['POST']) # crea ruta o endpoint
def create_curso():
    print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    link=request.json['link']
    imagen=request.json['imagen']
    fechaInicio=request.json['fechaInicio']
    fechaFinalizacion=request.json['fechaFinalizacion']
    estado=request.json['estado']
    new_curso=Curso(nombre,link, imagen, fechaInicio, fechaFinalizacion, estado)
    db.session.add(new_curso)
    db.session.commit()
    return curso_schema.jsonify(new_curso)



@app.route('/cursos/<id>' ,methods=['PUT'])
def update_curso(id):
    curso=Curso.query.get(id)
 
    nombre=request.json['nombre']
    link=request.json['link']
    imagen=request.json['imagen']
    fechaInicio=request.json['fechaInicio']
    fechaFinalizacion=request.json['fechaFinalizacion']
    estado=request.json['estado']

    curso.nombre=nombre
    curso.link=link
    curso.imagen=imagen
    curso.fechaInicio=fechaInicio
    curso.fechaFinalizacion=fechaFinalizacion
    curso.estado=estado

    db.session.commit()
    return curso_schema.jsonify(curso)
 
# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
