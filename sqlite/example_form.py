import streamlit as st
import pandas as pd
import sqlite3

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

# Función principal de la aplicación
def main():
    crear_tabla()  # Asegurar que la tabla existe antes de cualquier operación

    st.title('Aplicación de Usuarios')

    menu = ['Registro', 'Ver Usuarios']
    eleccion = st.sidebar.selectbox('Menú', menu)

    if eleccion == 'Registro':
        st.subheader('Formulario de Registro')

        nombre = st.text_input('Nombre')
        email = st.text_input('Email')
        contraseña = st.text_input('Contraseña', type='password')

        if st.button('Registrarse'):
            agregar_usuario(nombre, email, contraseña)
            st.success('¡Registro exitoso!')
    elif eleccion == 'Ver Usuarios':
        st.subheader('Lista de Usuarios Registrados')
        usuarios = obtener_usuarios()
        df_usuarios = pd.DataFrame(usuarios, columns=['Nombre', 'Email'])
        st.dataframe(df_usuarios)

if __name__ == '__main__':
    main()
