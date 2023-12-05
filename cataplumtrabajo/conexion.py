import cx_Oracle
from flask import Flask, request, render_template

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


'''
@app.route('/eventos')
def eventos():
    return render_template('eventos.html')
'''

@app.route('/eventos')
def mostrar_eventos():
    try:
        conexion_Oracle = conexionBD()
        cursor = conexion_Oracle.cursor()

        cursor.execute("SELECT * FROM EVENTO")
        eventos = cursor.fetchall()

        cursor.close()
        conexion_Oracle.close()

        return render_template('eventos.html', eventos=eventos)
    except Exception as ex:
        return f'Error al obtener datos de la base de datos: {ex}'

@app.route('/agregarEvento')
def agregarEvento():
    return render_template('agregarEvento.html')

@app.route('/eventosc')
def eventosc():
    return render_template('eventosc.html')

'''
@app.route('/animadores')
def animadores():
    return render_template('animadores.html')
'''

@app.route('/animadores')
def mostrar_animadores():
    try:
        conexion_Oracle = conexionBD()
        cursor = conexion_Oracle.cursor()

        cursor.execute("SELECT * FROM ANIMADOR")
        animadores = cursor.fetchall()

        cursor.close()
        conexion_Oracle.close()

        return render_template('animadores.html', animadores=animadores)
    except Exception as ex:
        return f'Error al obtener datos de la base de datos: {ex}'

@app.route('/agregarAnimadores')
def agregarAnimadores():
    return render_template('agregarAnimadores.html')

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


'''@app.route('/agregarCliente')
def agregarCliente():
    return render_template('agregarCliente.html')'''

@app.route('/agregarCliente', methods=['GET', 'POST'])
def agregarCliente():
    print("Route reached")
    if request.method == 'POST':
        print("POST request received")
        try:
            tipo_cliente = request.form['tipoCliente']
            

            if tipo_cliente == '1':
                id_cliente = request.form['id']
                nombres = request.form['nombres']
                ap_paterno = request.form['apPaterno']
                ap_materno = request.form['apMaterno']
                dni = request.form['dni']
                celular = request.form['celular']

                conexion_Oracle = conexionBD()
                cursor = conexion_Oracle.cursor()

                cursor.execute("INSERT INTO Cliente (ID, ID_TIPO_CLIENTE, Nombres, ApellidoPaterno, ApellidoMaterno, Celular, DNI, RUC) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)",
                                                                                                                                                (id_cliente, 1, nombres, ap_paterno, ap_materno, celular, dni, None))
                connection.commit()
                cursor.close()
                connection.close()
                

            elif tipo_cliente == '2':
                id_empresa = request.form['id']
                nombres = request.form['nombres']
                celular_empresa = request.form['celular']
                ruc = request.form['ruc']
                
                cursor = connection.cursor()
                
                
                cursor.execute("INSERT INTO Cliente (ID, ID_TIPO_CLIENTE, Nombres, ApellidoPaterno, ApellidoMaterno, Celular, DNI, RUC) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)",
                               (id_empresa, 2, nombres, None, None, celular_empresa, None, ruc))

                connection.commit()
                cursor.close()
                connection.close()


            # Add any additional logic or validation as needed

            return render_template('agregarCliente.html')
        except Exception as ex:
            return f'Error al registrar cliente: {ex}'
    else:
        return render_template('agregarCliente.html')









if __name__ == '__main__':
    app.run(debug=True)
