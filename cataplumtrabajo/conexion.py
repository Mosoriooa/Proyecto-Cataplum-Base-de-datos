import cx_Oracle
from flask import Flask, request, render_template
from datetime import datetime

conn = 'USERDB/PASSWORD@localhost:1521/xe'

try:
    connection = cx_Oracle.connect(conn)
    print(connection.version)

except Exception as ex:
    print(ex)


app= Flask(__name__)

def conexionBD():
    connection = cx_Oracle.connect(conn)
    return connection


@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/clientes')
def mostrar_clientes():
    try:
        conexion_Oracle = conexionBD()
        cursor = conexion_Oracle.cursor()

        cursor.execute("SELECT * FROM CLIENTE")
        clientes = cursor.fetchall()

        cursor.close()
        conexion_Oracle.close()

        return render_template('clientes.html', clientes=clientes)
    except Exception as ex:
        return f'Error al obtener datos de la base de datos: {ex}'


@app.route('/eventos')
def mostrar_eventos():
    try:
        conexion_Oracle = conexionBD()
        cursor = conexion_Oracle.cursor()
        cursor2 = conexion_Oracle.cursor()
        cursor3 = conexion_Oracle.cursor()



        cursor.execute("SELECT e.ID AS id_evento, r.ID AS id_reserva, c.ID AS id_cliente, c.Nombres AS nombre_cliente, e.Direccion, e.FechaEvento, e.NroInvitados, e.Descripcion, e.ID_CUMPLEANIERO, e.ID_TEMATICA  FROM RESERVA r JOIN EVENTO e ON r.ID_EVENTO = e.ID JOIN CLIENTE c ON r.ID_CLIENTE = c.ID ORDER BY e.ID")
        cursor2.execute("SELECT * FROM CUMPLEANIERO ORDER BY ID")
        cursor3.execute("SELECT * FROM TEMATICA ORDER BY ID")


        eventos = cursor.fetchall()
        cumpleanieros = cursor2.fetchall()
        tematicas = cursor3.fetchall()


        cursor.close()
        cursor2.close()
        cursor3.close()


        conexion_Oracle.close()

        return render_template('eventos.html', eventos=eventos, cumpleanieros = cumpleanieros, tematicas = tematicas)
    except Exception as ex:
        return f'Error al obtener datos de la base de datos: {ex}'


@app.route('/eventosc')
def eventosc():
    return render_template('eventosc.html')


@app.route('/animadores')
def mostrar_animadores():
    try:
        conexion_Oracle = conexionBD()
        cursor = conexion_Oracle.cursor()

        cursor.execute("SELECT * FROM ANIMADOR ORDER BY ID")
        animadores = cursor.fetchall()

        cursor.close()
        conexion_Oracle.close()

        return render_template('animadores.html', animadores=animadores)
    except Exception as ex:
        return f'Error al obtener datos de la base de datos: {ex}'


@app.route('/paquetes')
def paquetes():
    return render_template('paquetes.html')

@app.route('/paquetesc')
def paquetesc():
    return render_template('paquetesc.html')


@app.route('/comentarios')
def mostrar_comentarios():
    try:
        conexion_Oracle = conexionBD()
        cursor = conexion_Oracle.cursor()

        cursor.execute("SELECT * FROM FEEDBACKCLIENTE")
        comentarios = cursor.fetchall()

        cursor.close()
        conexion_Oracle.close()

        return render_template('comentarios.html', comentarios=comentarios)
    except Exception as ex:
        return f'Error al obtener datos de la base de datos: {ex}'

@app.route('/comentariosc')
def comentariosc():
    return render_template('comentariosc.html')


@app.route('/agregarCliente', methods=['GET', 'POST'])
def agregarCliente():
    print("Route reached")
    if request.method == 'POST':
        print("POST request received")
        try:
            id_cliente = request.form['id']
            id_tipo_cliente = request.form['idtipocliente']
            nombres = request.form['nombres']
            ap_paterno = request.form['apPaterno']
            ap_materno = request.form['apMaterno']
            dni = request.form['dni']
            celular = request.form['celular']
            ruc = request.form['ruc']

            conexion_Oracle = conexionBD()
            cursor = conexion_Oracle.cursor()

            cursor.execute("INSERT INTO Cliente (ID, ID_TIPO_CLIENTE, Nombres, ApellidoPaterno, ApellidoMaterno, Celular, DNI, RUC) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", (id_cliente, id_tipo_cliente, nombres, ap_paterno, ap_materno, celular, dni, ruc))
            connection.commit()
            cursor.close()
            connection.close()

            return render_template('agregarCliente.html')
        except Exception as ex:
            return f'Error al registrar cliente: {ex}'
    else:
        return render_template('agregarCliente.html')

@app.route('/agregarAnimador', methods=['GET', 'POST'])
def agregarAnimador():
    if request.method == 'POST':
        print("POST request received")
        try:
            id_animador = request.form['id']
            dni = request.form['dni']
            nombres = request.form['nombres']
            apPaterno = request.form['apPaterno']
            apMaterno = request.form['apMaterno']
            celular = request.form['celular']
            disponibilidad = None  

            conexion_Oracle = conexionBD()
            cursor = conexion_Oracle.cursor()

            cursor.execute("INSERT INTO ANIMADOR (ID, DNI, Nombres, ApellidoPaterno, ApellidoMaterno, Celular, Disponibilidad) VALUES (:1, :2, :3, :4, :5, :6, :7)", (id_animador, dni, nombres, apPaterno, apMaterno, celular, disponibilidad))

            conexion_Oracle.commit()
            cursor.close()
            conexion_Oracle.close()

            return render_template('agregarAnimador.html')

        except Exception as ex:
            return f'Error al guardar animador: {ex}'
    else:
        return render_template('agregarAnimador.html')
    
@app.route('/agregarEvento', methods=['GET', 'POST'])
def agregarEvento():
    if request.method == 'POST':
        print("POST request received")
        try:
            idCliente = request.form['idCliente']
            dirr = request.form['direccion']
            fecha_input = request.form['fechaEvento']
            numInvitados = request.form['numInvitados']
            descripcion = request.form['descripcion']
            idTematica = request.form['idTematica']
            nombres = request.form['nombres']
            edad  = request.form['edad']

            fecha_validada = datetime.strptime(fecha_input, '%Y-%m-%d')

            conexion_Oracle = conexionBD()
            cursor = conexion_Oracle.cursor()
            cursor2 = conexion_Oracle.cursor()
            cursor3 = conexion_Oracle.cursor()

            # Call the INSERTAR_CUMPLEANIERO procedure
            p_id_cumpleaniero = cursor2.var(cx_Oracle.NUMBER)
            cursor2.callproc("INSERTAR_CUMPLEANIERO", [edad, nombres, p_id_cumpleaniero])

            # Retrieve the OUT parameter value
            idCumpleañero = p_id_cumpleaniero.getvalue()

            
            p_id_evento = cursor.var(cx_Oracle.NUMBER)
            cursor.callproc("INSERTAR_EVENTO", [dirr, fecha_validada, numInvitados, descripcion, idCumpleañero, idTematica, p_id_evento])
            
            # Retrieve the OUT parameter value
            id_evento = p_id_evento.getvalue()
            print(id_evento)


            cursor3.callproc("INSERTAR_RESERVA", [idCliente, id_evento])

            conexion_Oracle.commit()
            cursor.close()
            cursor2.close()
            cursor3.close()
            conexion_Oracle.close()

            return render_template('agregarEvento.html')

        except Exception as ex:
            return f'Error al guardar Evento: {ex}'
    else:
        return render_template('agregarEvento.html')


if __name__ == '__main__':
    app.run(debug=True)