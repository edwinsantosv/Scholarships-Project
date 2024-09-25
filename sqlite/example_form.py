import streamlit as st
import pandas as pd
import sqlite3
import random

# Conexión a la base de datos SQLite
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()

# Función para crear la tabla de usuarios si no existe
def crear_tabla():
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (nombre TEXT, email TEXT, contraseña TEXT)''')

# Función para agregar un nuevo usuario a la base de datos
def agregar_usuario(nombre, email, contraseña):
    c.execute('INSERT INTO usuarios (nombre, email, contraseña) VALUES (?, ?, ?)',
              (nombre, email, contraseña))
    conn.commit()

# Función para obtener todos los usuarios de la base de datos
def obtener_usuarios():
    c.execute('SELECT nombre, email FROM usuarios')
    datos = c.fetchall()
    return datos

# Función para generar una pregunta CAPTCHA simple
def generar_captcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operador = random.choice(['+', '-'])
    if operador == '+':
        respuesta = num1 + num2
    else:
        respuesta = num1 - num2
    pregunta = f'¿Cuánto es {num1} {operador} {num2}?'
    return pregunta, respuesta

# Función principal de la aplicación
def main():
    crear_tabla()  # Asegurar que la tabla existe antes de cualquier operación

    st.title('Aplicación de Usuarios')

    menu = ['Registro', 'Ver Usuarios']
    eleccion = st.sidebar.selectbox('Menú', menu)

    if eleccion == 'Registro':
        st.subheader('Formulario de Registro')

        with st.form(key='form_registro'):
            # Usar st.session_state para mantener y reiniciar los valores de los campos
            nombre = st.text_input('Nombre', value=st.session_state.get('nombre', ''))
            email = st.text_input('Email', value=st.session_state.get('email', ''))
            contraseña = st.text_input('Contraseña', type='password', value=st.session_state.get('contraseña', ''))

            # Guardar los valores actuales en st.session_state
            st.session_state['nombre'] = nombre
            st.session_state['email'] = email
            st.session_state['contraseña'] = contraseña

            # Generar y mostrar la pregunta CAPTCHA
            if 'pregunta_captcha' not in st.session_state:
                pregunta_captcha, respuesta_captcha = generar_captcha()
                st.session_state['pregunta_captcha'] = pregunta_captcha
                st.session_state['respuesta_captcha'] = respuesta_captcha
            else:
                pregunta_captcha = st.session_state['pregunta_captcha']
                respuesta_captcha = st.session_state['respuesta_captcha']

            respuesta_usuario = st.text_input(f'CAPTCHA: {pregunta_captcha}')

            submit_button = st.form_submit_button('Registrarse')

            if submit_button:
                if respuesta_usuario:
                    try:
                        if int(respuesta_usuario) == respuesta_captcha:
                            # Validar que los campos no estén vacíos
                            if not nombre or not email or not contraseña:
                                st.error('Por favor, completa todos los campos.')
                            else:
                                # Aquí puedes agregar encriptación de contraseña si lo deseas
                                agregar_usuario(nombre, email, contraseña)
                                st.success('¡Registro exitoso!')
                                st.balloons()
                                # Reiniciar el formulario y el CAPTCHA
                                del st.session_state['pregunta_captcha']
                                del st.session_state['respuesta_captcha']
                                del st.session_state['nombre']
                                del st.session_state['email']
                                del st.session_state['contraseña']
                                st.experimental_rerun()
                        else:
                            st.error('Respuesta incorrecta al CAPTCHA. Inténtalo de nuevo.')
                            # Generar un nuevo CAPTCHA
                            del st.session_state['pregunta_captcha']
                            del st.session_state['respuesta_captcha']
                    except ValueError:
                        st.error('Por favor, ingresa un número válido en el CAPTCHA.')
                else:
                    st.error('Por favor, completa el CAPTCHA.')

    elif eleccion == 'Ver Usuarios':
        st.subheader('Lista de Usuarios Registrados')
        usuarios = obtener_usuarios()
        df_usuarios = pd.DataFrame(usuarios, columns=['Nombre', 'Email'])
        st.dataframe(df_usuarios)

if __name__ == '__main__':
    main()
