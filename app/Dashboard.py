import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io


def show_dash():

    st.title('Análisis de becas')

    # Cargar el archivo CSV y ordenar por "ID"
    df = pd.read_csv("app/final_df.csv").iloc[:, 1:].sort_values(by="ID", ascending=True)

    st.sidebar.subheader('Filtros')


    # Usar st.form para agrupar filtros y botón de submit
    with st.sidebar.form(key='filters_form'):
        # Multiselect para 'Tipo de Beca' (default: sin selección)
        scholarship_type_filter = st.multiselect(
            'Tipo de Beca', 
            options=df['Scholarship_Type'].unique(),
            default=[]  # Sin selección por defecto
        )

        # Multiselect para 'Becas disponibles' (default: sin selección)
        available_scholarships_filter = st.multiselect(
            'Becas disponibles', 
            options=df['Number_of_Scholarships'].unique(),
            default=[]  # Sin selección por defecto
        )

        # Multiselect para 'Experiencia de estudio' (default: sin selección)
        study_experience_filter = st.multiselect(
            'Experiencia de Estudio', 
            options=df['study_experience_required'].drop_duplicates(),
            default=[]  # Sin selección por defecto
        )

        # Multiselect para 'Pais' (default: sin selección)
        country_experience_filter = st.multiselect(
            'Pais', 
            options=df['country'].drop_duplicates(),
            default=[]  # Sin selección por defecto
        )

        # Botón para aplicar los filtros
        submit_button = st.form_submit_button(label='Aplicar Filtros')

    # Si el botón es presionado, aplicar los filtros
    if submit_button:
        # Aplicar filtros solo si hay selección en los multiselect
        if scholarship_type_filter:
            df = df[df['Scholarship_Type'].isin(scholarship_type_filter)]
        if available_scholarships_filter:
            df = df[df['Number_of_Scholarships'].isin(available_scholarships_filter)]
        if study_experience_filter:
            df = df[df['study_experience_required'].isin(study_experience_filter)]
        if country_experience_filter:
            df = df[df['country'].isin(country_experience_filter)]

    # Contar el número de filas en el DataFrame
    rows_num = len(df)
    st.write(f"""
                Hay una cantidad de **{rows_num}** becas que cumplen con los criterios seleccionados.
                """)

    st.subheader("Gráficas de resumen")

    # Gráficos de barras: Scholarship_Type, study_experience_required, country

    # Gráfico 1: Scholarship_Type ordenado en orden descendente
    scholarship_type_counts = df['Scholarship_Type'].value_counts().sort_values(ascending=True)
    fig_scholarship_type = px.bar(
        y=scholarship_type_counts.index, 
        x=scholarship_type_counts.values, 
        title="Cantidad de Becas por Tipo",
        labels={'x': 'Cantidad', 'y': 'Tipo de Beca'},
        text=scholarship_type_counts.values  # Añadir etiquetas a las barras
    )
    fig_scholarship_type.update_traces(textposition='auto')  # Ajustar la posición de las etiquetas

    # Gráfico 2: Study Experience Required en orden descendente
    study_experience_counts = df['study_experience_required'].value_counts().sort_values(ascending=True)
    fig_study_experience = px.bar(
        y=study_experience_counts.index, 
        x=study_experience_counts.values, 
        title="Experiencia de Estudio Requerida",
        labels={'x': 'Cantidad', 'y': 'Experiencia Requerida'},
        text=study_experience_counts.values  # Añadir etiquetas a las barras
    )
    fig_study_experience.update_traces(textposition='auto')  # Ajustar la posición de las etiquetas

    # Gráfico 3: Country en orden descendente
    country_counts = df['country'].value_counts().sort_values(ascending=False)
    fig_country = px.bar(
        x=country_counts.index, 
        y=country_counts.values, 
        title="Cantidad de Becas por País",
        labels={'x': 'País', 'y': 'Cantidad'},
        text=country_counts.values  # Añadir etiquetas a las barras
    )
    fig_country.update_traces(textposition='auto')  # Ajustar la posición de las etiquetas

    # Gráfico 4: Cantidad de becas por deadline (gráfico de línea)
    df_deadline_counts = df['deadline_date'].value_counts().sort_index()  # Agrupar por fecha
    fig_deadline = px.line(
        x=df_deadline_counts.index, 
        y=df_deadline_counts.values, 
        title="Cantidad de Becas por Fecha Límite (Deadline)",
        labels={'x': 'Fecha Límite', 'y': 'Cantidad de Becas'},
        markers=True  # Añadir puntos a la línea
    )
    fig_deadline.update_traces(mode="lines+markers")

    # Gráfico 3: Country en orden descendente
    Number_of_Scholarships = df['Number_of_Scholarships'].value_counts().sort_values(ascending=False)
    fig_schol_num = px.bar(
        x=Number_of_Scholarships.index, 
        y=Number_of_Scholarships.values, 
        title="Cantidad de Becas Disponibles",
        labels={'x': 'Becas disponibles', 'y': 'Cantidad'},
        text=Number_of_Scholarships.values  # Añadir etiquetas a las barras
    )
    fig_schol_num.update_traces(textposition='auto')  # Ajustar la posición de las etiquetas

    # Grafico 4
        # Contar becas por país
    country_counts = df['country'].value_counts()

    # Mapa Coroplético de becas por país (Filled Map)
    fig_map = px.choropleth(
        df, 
        locations='country',  # Columna que contiene los nombres de los países
        locationmode='country names',  # Indicamos que la columna contiene nombres de países
        color=df['country'].map(country_counts),  # Mapear el conteo de becas a los países
        hover_name='country',  # Mostrar el nombre del país en el hover
        title="Cantidad de Becas por País",
        #color_continuous_scale=px.colors.sequential.Plasma,  # Escala de colores
        labels={'color': 'Cantidad de Becas'}
    )

    # Crear dos columnas en la primera fila
    col1, col2 = st.columns([1, 1])

    # Agregar gráficos en las columnas
    with col1:
        st.plotly_chart(fig_scholarship_type, use_container_width=True)
        st.write("Muestra la cantidad de becas por tipo de beca. Las becas pueden ser por merito o por necesidad.")
        st.plotly_chart(fig_study_experience, use_container_width=True)
        
    with col2:
        st.plotly_chart(fig_schol_num, use_container_width=True)
        st.write("Muestra la cantidad de becas por cantidad de becas disponibles por beca. Las becas pueden ser multiples o solo una.")
        st.plotly_chart(fig_deadline, use_container_width=True)  # Añadir gráfico de deadline
    

    col11, col22 = st.columns([1, 1])

    with col11:
        # Mostrar el mapa interactivo en Streamlit
        st.plotly_chart(fig_map)
        
    with col22:
        st.plotly_chart(fig_country)



    st.subheader("Lista de Becas")
    
    # Mostrar el DataFrame en la aplicación
    st.dataframe(df)

    # Botón para descargar el archivo Excel
    st.subheader('Descargar los datos en Excel')
    to_excel(df)
    

def to_excel(df):
    """
    Función que convierte el DataFrame en un archivo Excel y permite la descarga.
    """
    output = io.BytesIO()
    # Escribir el DataFrame a un archivo Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:  # Usar 'openpyxl' como motor
        df.to_excel(writer, index=False, sheet_name='Becas')
    output.seek(0)  # Volver al inicio del archivo generado

    # Crear el botón para descargar el archivo
    st.download_button(
        label="Descargar datos en formato Excel",
        data=output,
        file_name="becas_seleccionadas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

