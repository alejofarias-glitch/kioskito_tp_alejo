from fpdf import FPDF
import streamlit as st
from mi_negocio import *
from calculos import *
def renglon(pdf, texto, valor):
    # un renglon con el texto a la izquierda y el valor a la derecha
    pdf.cell(120, 9, texto)
    pdf.cell(0, 9, valor, align="R", new_x="LMARGIN", new_y="NEXT")
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
