import streamlit as st
import pandas as pd
import io

conversion_rate = 3.85

def read_file(file):
    lines = file.read().decode("utf-8").splitlines()
    data = []
    for line in lines:
        parts = line.split(",")
        producto = parts[0].strip()
        precio_usd = float(parts[1].strip())
        data.append([producto, precio_usd])
    df = pd.DataFrame(data, columns=["Producto", "Precio en USD"])
    return df

def convert_prices(data, rate):
    data["Precio en Soles"] = data["Precio en USD"] * rate
    return data

def save_converted_prices(data):
    output = io.StringIO()
    for index, row in data.iterrows():
        output.write(f"{row['Producto']}, {row['Precio en Soles']:.2f}\n")
    return output.getvalue().encode('utf-8')

def main():
    st.title("Conversión de Precios de USD a Soles")

    uploaded_file = st.file_uploader("Sube tu archivo de precios en USD (TXT)", type=["txt"])

    if uploaded_file is not None:
        data = read_file(uploaded_file)
        st.write("Datos cargados:")
        st.dataframe(data)

        converted_data = convert_prices(data, conversion_rate)
        st.write("Precios convertidos a Soles:")
        st.dataframe(converted_data)

        save_button = st.button("Guardar precios convertidos en archivo")

        if save_button:
            output = save_converted_prices(converted_data)
            st.download_button(label="Descargar precios convertidos",
                               data=output,
                               file_name="precios_convertidos.txt",
                               mime="text/plain")
            st.success("Archivo guardado con éxito como 'precios_convertidos.txt'.")

if __name__ == "__main__":
    main()
