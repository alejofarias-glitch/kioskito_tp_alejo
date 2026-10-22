from fpdf import FPDF
import streamlit as st
from mi_negocio import *
 
NOMBRE_KIOSCO = "Kioskito"
LOGO = "logo.png"
EFECTIVO = "Efectivo"
TRANSFERENCIA = "Transferencia"

def buscar_posicion(lista, nombre):
    for i in range(len(lista)):
        if lista[i] == nombre:
            return i
    return -1
#------------------------------------------------------------------
def aplicar_descuento(monto, forma_pago):
    # 10% de descuento solo en efectivo
    if forma_pago == EFECTIVO:
        return round(monto - monto * 10 / 100, 2)
    return monto
#---------------------------------------------------------------------
def calcular_iva(monto):
    return round(monto * 21 / 100, 2)
#---------------------------------------------------------------------
def renglon(pdf, texto, valor):
    # un renglon con el texto a la izquierda y el valor a la derecha
    pdf.cell(120, 9, texto)
    pdf.cell(0, 9, valor, align="R", new_x="LMARGIN", new_y="NEXT")
#-----------------------------------------------------------------------
def armar_pdf(numero, fecha, cliente, productoa, productob, productoc, cantidada, cantidadb, cantidadc, precioa, preciob, precioc,
              subtotala, subtotalb, subtotalc, subtotalf, descuento, iva, total):
    pdf = FPDF()                      # pdf es el documento
    pdf.add_page()
 
    # encabezado: logo + nombre + numero y fecha
    pdf.image(LOGO, x=10, y=10, w=28)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, NOMBRE_KIOSCO, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Presupuesto N° {numero}", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Fecha: {fecha}", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
 
    # datos del pedido
    pdf.set_font("Helvetica", "", 12)
    renglon(pdf, "Cliente", cliente)
    renglon(pdf, f"{cantidada} x {productoa}", f"${precioa:.2f} c/u")
    renglon(pdf, f"{cantidadb} x {productob}", f"${preciob:.2f} c/u")
    renglon(pdf, f"{cantidadc} x {productoc}", f"${precioc:.2f} c/u")
    pdf.ln(4)
 
    # resumen
    renglon(pdf, "Subtotal N°1", f"${subtotala:.2f}")
    renglon(pdf, "Subtotal N°2", f"${subtotalb:.2f}")
    renglon(pdf, "Subtotal N°3", f"${subtotalc:.2f}")
    renglon(pdf, "Subtotal final", f"${subtotalf:.2f}")
    renglon(pdf, "Descuento", f"-${descuento}")
    renglon(pdf, "IVA 21%", f"${iva:.2f}")
    pdf.set_font("Helvetica", "B", 14)
    renglon(pdf, "TOTAL", f"${total:.2f}")
 
    # pie
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, "Presupuesto válido por 7 días.", new_x="LMARGIN", new_y="NEXT")
 
    return bytes(pdf.output())
#-------------------------------------------------------------------------
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
pos1 = buscar_posicion(productos, producto1)
pos2 = buscar_posicion(productos, producto2)
pos3 = buscar_posicion(productos, producto3)
precio1 = precios[pos1]
precio2 = precios[pos2]
precio3 = precios[pos3]
subtotal1 = precio1*cantidad1
subtotal2 = precio2*cantidad2
subtotal3 = precio3*cantidad3
subtotal_final=subtotal1+subtotal2+subtotal3
descontado = aplicar_descuento(subtotal_final, pago)
if pago == EFECTIVO:
    descuento = subtotal_final * (10/100)
else:
    descuento = 0
iva = calcular_iva(descontado)
total = descontado+iva
archivo=armar_pdf(numero, fecha, nombre, producto1, producto2, producto3, cantidad1, cantidad2, cantidad3, precio1, precio2, precio3, subtotal1, subtotal2, subtotal3, subtotal_final, descuento, iva, total)
st.download_button("Descargar presupuesto (PDF)", archivo, file_name=f"presupuesto_{numero}.pdf", mime="application/pdf")