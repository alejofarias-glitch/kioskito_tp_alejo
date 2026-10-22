import streamlit as st
from mi_negocio import *
import calculos
import pdf_presupuesto
NOMBRE_KIOSCO = "Kioskito"
LOGO = "logo.png"
EFECTIVO = "Efectivo"
TRANSFERENCIA = "Transferencia"
productos=["gaseosa", "alfajor", "pebete", "chicles", "agua"]
precios=[   2000,      1500,      2500,     500,       1100]
st.title("Kioskito")
nombre = st.text_input("Ingrese su nombre")
producto1 = st.selectbox("Producto N°1", productos)
cantidad1 = st.number_input("Ingrese la cantidad del primer producto", min_value=0, step=1)
producto2 = st.selectbox("Producto N°2", productos)
cantidad2 = st.number_input("Ingrese la cantidad del segundo producto", min_value=0, step=1)
producto3 = st.selectbox("Producto N°3", productos)
cantidad3 = st.number_input("Ingrese la cantidad del tercer producto", min_value=0, step=1)
pago = st.radio("Forma de pago", ["Efectivo", "Transferencia"])
numero = st.number_input("N° de presupuesto", min_value=1, step=1) 
fecha = st.date_input("Fecha")
pos1 = calculos.buscar_posicion(productos, producto1)
pos2 = calculos.buscar_posicion(productos, producto2)
pos3 = calculos.buscar_posicion(productos, producto3)
precio1 = precios[pos1]
precio2 = precios[pos2]
precio3 = precios[pos3]
subtotal1 = precio1*cantidad1
subtotal2 = precio2*cantidad2
subtotal3 = precio3*cantidad3
subtotal_final=subtotal1+subtotal2+subtotal3
descontado = calculos.aplicar_descuento(subtotal_final, pago)
if pago == EFECTIVO:
    descuento = subtotal_final * (10/100)
else:
    descuento = 0
iva = calculos.calcular_iva(descontado)
total = descontado+iva
archivo=pdf_presupuesto.armar_pdf(numero, fecha, nombre, producto1, producto2, producto3, cantidad1, cantidad2, cantidad3, precio1, precio2, precio3, subtotal1, subtotal2, subtotal3, subtotal_final, descuento, iva, total)
st.download_button("Descargar presupuesto (PDF)", archivo, file_name=f"presupuesto_{numero}.pdf", mime="application/pdf")
