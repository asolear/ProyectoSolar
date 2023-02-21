# from app_SAM import mas2sam

import os
import datetime
import io
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Table

from PyPDF2 import PdfFileWriter, PdfFileReader
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import magenta, red
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Image,
    BaseDocTemplate,
)
from reportlab.graphics.widgets import signsandsymbols

import toml
import numpy as np
import graphviz
import ast
import importlib
import requests
import itertools
import sys
import geopandas as gpd
from itertools import cycle
from PIL import Image
import utm
from shapely.geometry import (
    Point,
    LineString,
    MultiLineString,
    Polygon,
    mapping,
    MultiPolygon,
    MultiPoint,
    box,
    MultiPoint,
)
from shapely import affinity
from shapely.ops import (
    polygonize_full,
    orient,
    linemerge,
    nearest_points,
    transform,
    unary_union,
)
import yaml
from yaml.loader import SafeLoader
import math
import csv
from io import StringIO
from types import SimpleNamespace
# NREL
import PySAM.Pvwattsv8 as PV
import PySAM.Grid as GRID
import PySAM.Utilityrate5 as UR
import PySAM.Cashloan as CL

# variables glbales pero no estan ejecutada no tienen los outputs
pv = PV.default("PVWattsResidential")
grid = GRID.from_existing(pv, "PVWattsResidential")
ur = UR.from_existing(pv, "PVWattsResidential")
cl = CL.from_existing(pv, "PVWattsResidential")
#####################################


print(os.path.basename(__file__))

with open("modelo/mm.json", "r") as f:
    s = json.load(f)
s = SimpleNamespace(s=s)


# la tngo ue importara asi porque si no el lint la pone antes dela cdecalaracion de var globales de la funcion
app_SAM = importlib.import_module('app_SAM')
app_SAM.app()


# y simula sam
# pv,grid,ur,cl=mas2sam()
#####################################


# pd.set_option("display.max_rows", None)
#


meses = [
    "Ene",
    "Feb",
    "Mar",
    "Abr",
    "May",
    "Jun",
    "Jul",
    "Ago",
    "Sep",
    "Oct",
    "Nov",
    "Dic",
]
colores = [
    "blue",
    "orange",
    "red",
    "red",
    "purple",
    "brown",
    "pink",
    "gray",
    "olive",
    "cyan",
]

# Fade the cells


def tabla(df, titulo=''):

    if 1:
        fig, ax1 = plt.subplots()
        ccolors = ['lightgrey']*len(df.columns)
        t = ax1.table(cellText=df.values, colColours=ccolors,
                      colLabels=df.columns, cellLoc='left', loc='center')
        ax1.axis("off")
        # ax.set_title('$$')
    if 1:
        t.auto_set_font_size(False)
        t.set_fontsize(11)
        t.scale(1, 1)
        t.auto_set_column_width(col=list(range(len(df.columns))))
        t.colColours = ['grey']*len(df.columns)
        for cell in t.get_children():
            cell_text = cell.get_text().get_text()
            cell.set_edgecolor('lightgrey')
            if cell_text not in df.index \
                    and cell_text not in df.columns:
                cell.get_text().set_color('black')

            else:
                cell.get_text().set_weight('bold')
                cell.get_text().set_color('black')
    if 1:
        ax1.set_title(titulo, y=.62+len(df)*.02, pad=-14, fontweight="bold")
        imgdata = io.BytesIO()
        fig.savefig(imgdata, format="png", transparent=True)
        imgdata.seek(0)  # rewind the data

    plt.close()
    return imgdata


# consumo
def T_CONSUMOS_JUSTIFICACION():
    datos = {"Lat": str(round(s.s["GEN"]["Ubicacion"]["_lat"], 3))+"$a=2/4$",
             "Lng": str(round(s.s["GEN"]["Ubicacion"]["_lng"], 3))+" °",
             "Inc": str(round(pv.SystemDesign.tilt, 3))+" °",
             "Azm": str(round(pv.SystemDesign.azimuth-180, 1))+" °",
             "Pot": str(s.s["GEN"]["Ubicacion"]["_kwp"])+" kWp",
             }
    datos = [
        ('Vivienda', '$kWh/kW_c$', 872),
        ('Vehículo eléctrico', 'kWh/ud', 1630),
        ('ACS con Bomba de calor ', 'kWh/viv', 4000),
        ('AA con bomba de calor ', 'kWh/ud ', 180),
        (' Energía consumida.', '', 0),
    ]
    columns = ['Consumo anual ('+s.s["FV"]["consumo"]
               ["perfil"]+')', 'Unidad', 'kWh/Q']
    df = pd.DataFrame(datos, columns=columns)
    df['Q'] = [
        s.s['FV']['consumo']['kWcontratad'],
        s.s['FV']['consumo']['cantidad_ve'],
        s.s['FV']['consumo']['ACS_bomba_calor'],
        s.s['FV']['consumo']['AA_bomba_calor'],
        0
    ]
    df['kwh'] = df['kWh/Q']*df['Q']
    if 0:  # no en el resumen
        df['(*)Con valores medios'] = [
            'Informe SPAHOUSEC I, IDAE',
            '0,163 kWh/km * 10000 km/a',
            '$12000 kWh_{calor}/año;SPF=3,0$',
            '1 kW * 90 días * 2 horas/dia',
        ]
    df.iloc[-1:, -1:] = df['kwh'].sum()
    df.iloc[-1:, 1:-1] = ''
    s.s['FV']['consumo']['_consumo_anual'] = df['kwh'].sum()/2
    s.s['FV']['consumo']['_df'] = df.to_dict(orient='records')
    return df


def T_GENERADA_JUSTIFICACION():
    datos = [
        ("Ubicación. Lat, Lng [°]", str(round(s.s["GEN"]["Ubicacion"]["_lat"], 3))+', '+str(
            round(s.s["GEN"]["Ubicacion"]["_lng"], 3))),
        ("Inclinacion, Azimut [°]", str(round(pv.SystemDesign.tilt, 3)) + ', ' +
         str(round(pv.SystemDesign.azimuth-180, 1))),
        ("FV instalada [kWp]", round(pv.SystemDesign.system_capacity, 1)),
        ("Perdidas del sistema [%]", round(pv.SystemDesign.losses, 1)),
        ("Energía generada [kWh]",
         round(pv.Outputs.annual_energy, 1)),
    ]
    columns = ['', ' ']
    df = pd.DataFrame(datos, columns=columns)
    s.s['_TABLAS']['Generacion']['_df'] = df.to_dict(orient='records')
    return df


def T_FINANCIERA_JUSTIFICACION():

    datos = [("Coste del proyecto [Є]", cl.SystemCosts.total_installed_cost),
             ('Vida de la instalacion [años]',
              cl.FinancialParameters.analysis_period),
             ('Precio Demanda estim. [Є/kWh]',
              s.s["FV"]["Economico"]["Precio_demanda"]),
             ('Precio Excedente estim. [Є/kWh]',
              s.s["FV"]["Economico"]["Precio_excedente"]),
             ('Subvencion NG estimada [Є]', round(
                 600*pv.SystemDesign.system_capacity, 1)),
             ('LCOE [Є/KWh]', round(cl.Outputs.lcoe_real/100, 6)),
             ('Periodo de retorno [años]', round(cl.Outputs.payback, 1)),
             ('VAN [Є]', round(cl.Outputs.npv, 1)),
             ]

    columns = [' ', '  ']
    df = pd.DataFrame(datos, columns=columns)
    s.s['_TABLAS']['Economico']['_df'] = df.to_dict(orient='records')
    return df


def T_INSTALACION_JUSTIFICACION():
    datos = [

        ('a', "Ubicación.", "Malaga"),
        ('b', "$N^o$ Consumidores asociados", str(
            s.s["GEN"]["Ubicacion"]["_Nvecinos"])),
        ('c', "Energía consumida anual [kWh]",
         round(ur.Outputs.year1_electric_load, 1)),
        ('d', "Energía generada anual [kWh]",
         round(pv.Outputs.annual_energy, 1)),
        ('e', "Potencia instalada [kWp]", round(
            pv.SystemDesign.system_capacity, 1)),
        ('f', "Horas equivalentes [h]", round(
            pv.Outputs.annual_energy/pv.SystemDesign.system_capacity, 1)),
        ('', "Econsumida / Egenerada * 100  [%]",
         round(ur.Outputs.year1_electric_load/pv.Outputs.annual_energy*100, 1)),
    ]

    columns = ['', ' ', '  ']
    df = pd.DataFrame(datos, columns=columns)
    s.s['_TABLAS']['Instalacion']['_df'] = df.to_dict(orient='records')
    return df


def ppdf(ppath, can, mmpdf, pagina):
    in_pdf_file = ppath + "_.pdf"
    out_pdf_file = ppath + ".pdf"
    existing_pdf = PdfFileReader(open(in_pdf_file, "rb"))
    output = PdfFileWriter()
    while pagina < len(existing_pdf.pages):
        can.showPage()
        pagina += 1

    can.save()
    mmpdf.seek(0)
    new_pdf = PdfFileReader(mmpdf)
    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.getPage(i)
        page.merge_page(new_pdf.getPage(i))
        output.addPage(page)
    outputStream = open(out_pdf_file, "wb")
    output.write(outputStream)
    outputStream.close()


def fqrcode_logo(texto):
    import qrcode
    from io import BytesIO
    from reportlab.lib.utils import ImageReader
    from PIL import Image

    # taking image which user wants
    # in the QR code center
    Logo_link = "assets/img/logo.png"

    logo = Image.open(Logo_link)

    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = basewidth / float(logo.size[0])
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    # taking url or text
    url = texto

    # addingg URL or text to QRcode
    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = "Green"
    QRcolor = "Blue"
    QRcolor = "Black"

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert("RGB")

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    buffered = BytesIO()
    QRimg.save(buffered, format="PNG")
    figura = ImageReader(buffered)
    buffered.seek(0)  # rewind the data
    return figura


def email_attachs(email, usuario, clave, files):
    # Import modules
    import smtplib
    import ssl

    # email.mime subclasses
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Add new subclass for adding attachments
    ##############################################################
    from email.mime.application import MIMEApplication

    ##############################################################
    # The pandas library is only for generating the current date, which is not necessary for sending emails
    import pandas as pd

    # Define the HTML document
    html = f"""
        <html>
            <body>
                <h2> Hola {usuario}, esta es tu clave</h2>
                <h1> {clave}</h1>
                <p>gracias por elegirnos</p>
            </body>
        </html>
        """
    ss
    # Define a function to attach files as MIMEApplication to the email
    ##############################################################

    def attach_file_to_email(email_message, filename):
        # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
        with open(filename, "rb") as f:
            file_attachment = MIMEApplication(f.read())
        # Add header/name to the attachments
        file_attachment.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        # Attach the file to the message
        email_message.attach(file_attachment)

    ##############################################################

    # Set up the email addresses and password. Please replace below with your email address and password
    email_from = "admin@asolear.es"
    password = "cscnrfff"
    email_to = email

    # Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime("%Y-%m-%d")

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message["From"] = email_from
    email_message["To"] = email_to
    email_message["Subject"] = f"Report email - {date_str}"

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))

    # Attach more (documents)
    for file in files:
        ##############################################################
        attach_file_to_email(email_message, file)
    # attach_file_to_email(email_message, "solar_edge.pdf")
    # attach_file_to_email(email_message, "01_disenio_generador_fv.pdf")
    ##############################################################
    # Convert it as a array
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("imap.privateemail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)


def plano_cubierta_paneles():

    if 1:
        gg = gpd.read_file(
            "modelo/mm.geojson"
        )  # !!!!! ojo que todos los numeros pasan a str
        # gg=gpd.GeoDataFrame(s.s['geojson'])
        # print(gg.head(3))
        # plot
        fig, ax = plt.subplots(figsize=(9, 9))
        legend = []
        # construccion por plantas
    if 1:
        # gg[(gg['cc']=='CUBIERTA')&(gg['ee']==0)].plot(column='ee',ax=ax,cmap='Reds', alpha=0.5395)

        legend.append("PANEL_FV")
        gg[(gg["cc"] == "PANEL_FV")].boundary.plot(
            ax=ax, color="b", linestyle="-", linewidth=1, aspect=1
        )

        # legend.append("PANEL_FV±4")
        gg[
            (gg["cc"] == "PANEL_FV") & ((gg["-4"] == "1") | (gg["4"] == "1"))
        ].boundary.plot(ax=ax, color="lightblue", linestyle="-", linewidth=1, aspect=1)

        # legend.append("PANEL_FV±3")
        gg[
            (gg["cc"] == "PANEL_FV") & ((gg["-3"] == "1") | (gg["3"] == "1"))
        ].boundary.plot(ax=ax, color="cyan", linestyle="-", linewidth=1, aspect=1)

    if 1:

        # zonas vrdes , piscina ..
        zonas = ["PI", "P", "ZD", "J"]
        color = ["aqua", "seagreen", "lime", "red"]
        c2z = dict(zip(zonas, color))
        for zona, color in c2z.items():
            if not gg[gg["ee"] == zona].empty:
                # legend.append(zona)
                gg[(gg["ee"] == zona)].boundary.plot(
                    ax=ax, color=color, alpha=1, aspect=1
                )

    if 1:
        # legend.append("PANEL_FV_SOMBRA")
        gg[(gg["cc"] == "PANEL_FV_SOMBRA")].plot(
            ax=ax, color="whitesmoke", linestyle="-.", alpha=1, aspect=1
        )

        legend.append("SOMBRA SI±2")
        gg[
            (gg["cc"] == "SOMBRA")
            & ((gg["cc"] == "fv") | (gg["azimut"] == "2") | (gg["azimut"] == "-2"))
        ].plot(ax=ax, color="whitesmoke", linestyle="-.", aspect=1)

        # legend.append("SOMBRA")
        gg[(gg["cc"] == "SOMBRA") & (gg["azimut"] == "0")].plot(
            ax=ax, color="gainsboro", linestyle="-.", aspect=1
        )

        # legend.append("CUBIERTA")
        gg[(gg["cc"] == "CUBIERTA")].boundary.plot(
            ax=ax, color="brown", alpha=0.9395, aspect=1
        )

        # legend.append("CUBIERTA")
        gg[(gg["cc"] == "fv")].boundary.plot(
            ax=ax, color="white", alpha=0.9395, aspect=1
        )

    for index, row in gg[(gg["cc"] == "fv")].iterrows():
        ax.text(
            row.geometry.centroid.x,
            row.geometry.centroid.y,
            str(index),
            color="r",
            weight="bold",
            fontsize=16,
            alpha=0.98,
        )

    # titulo
    if 1:
        np = gg[(gg["cc"] == "PANEL_FV")].ee.count()
        # data = {
        #     # "$N^o$ Paneles Solares ": [np, ""],
        #     # "Superficie": [
        #     #     round(gg[(gg["cc"] == "CUBIERTA")].geometry.area.sum(), 1),
        #     #     "$m^2$",
        #     # ],
        #     "Potencia": [
        #         np * s.s["GEN"]["panel"]["Pmp"][0],
        #         "$kWp$",
        #     ],
        # }
        # df = pd.DataFrame(data=data).T
        # df = df.set_axis(
        #     ["CUBIERTA ", s.s["GEN"]["Ubicacion"]["Parcela"]
        # )
        # ax.set_title("Cubierta"
        #              )
        # ax.legend(legend)
    ax.axis("off")
    if 0:

        # Hide the right and top spines
        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        ax.set_xlabel("$UTM_x$")
        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")
        ax.set_ylabel("$UTM_y$")

    if 1:
        plt.axis("off")
        imgdata = io.BytesIO()
        fig.savefig(imgdata, format="png", transparent=True)
        imgdata.seek(0)  # rewind the data

    plt.close()
    return imgdata


def fig_flujo_caja():
    fig, ax = plt.subplots(figsize=(10, 5))
    df = pd.DataFrame()
    # df['cf_operating_expenses']=['cl']['Outputs']cf_operating_expenses
    df["coste"] = cl.Outputs.cf_debt_balance
    df["coste"] = df["coste"] * 0
    df["Ayuda"] = df["coste"] * 0
    df["Prestamo"] = df["coste"] * 0
    df.at[0, "coste"] = -cl.SystemCosts.total_installed_cost
    df.at[0, "Ayuda"] = cl.Outputs.cbi_total
    df.at[0, "Prestamo"] = cl.Outputs.loan_amount
    df["cf_energy_value"] = cl.Outputs.cf_energy_value
    df["cf_energy_value"] = cl.Outputs.cf_energy_value
    df["cf_fed_tax_savings"] = cl.Outputs.cf_fed_tax_savings
    df = -df
    df["cf_debt_payment_interest"] = cl.Outputs.cf_debt_payment_interest
    df["cf_debt_payment_principal"] = cl.Outputs.cf_debt_payment_principal
    df["cf_om_capacity_expense"] = cl.Outputs.cf_om_capacity_expense
    df["cf_insurance_expense"] = cl.Outputs.cf_insurance_expense
    df = -df
    # df = df.iloc[1:, :]
    df.plot(kind="bar", stacked=True, ax=ax, alpha=0.5)
    df = pd.DataFrame()
    df["cf"] = cl.Outputs.cf_after_tax_cash_flow
    # df["cf_cumulative_payback_without_expenses"] = cl.Outputs.cf_cumulative_payback_without_expenses
    # df["cf_cumulative_payback_with_expenses"] = cl.Outputs.cf_cumulative_payback_with_expenses
    # df["cf_discounted_cumulative_payback"] = cl.Outputs.cf_discounted_cumulative_payback
    #
    df.plot(kind="line", ax=ax, alpha=0.8)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="y")
    ax.set_title("fig_flujo_caja")
    ax.legend(loc="lower right")

    ###################
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="png", transparent=True)
    imgdata.seek(0)  # rewind the data
    plt.close()
    return imgdata


def fig_diagrama_energia_anual():

    Aut = sum(ur.Outputs.year1_hourly_system_to_load)
    Exc = sum(ur.Outputs.year1_hourly_e_togrid)
    Dem = sum(ur.Outputs.year1_hourly_e_fromgrid)
    Dem = sum(ur.Outputs.year1_hourly_e_fromgrid)
    cons = round(ur.Outputs.year1_electric_load, 1)
    gen = round(pv.Outputs.annual_energy, 1)
    dae = Dem+Aut+Exc
    ww = 30  # factor de grosor de los edges

    dot = graphviz.Digraph(
        "Flujo de Carga",
        comment="Inversores",
        graph_attr={
            "label": "",
            "bgcolor": "transparent",
            # "splines": "curved" ,
            # "nodesep": "1",
        }
    )
    fv = "🌞 FV\n" + "Generacion\n" + str(gen)+' kWh'
    viv = "🏠 VIVIENDA\n" + "Consumo\n" + \
        str(round(cons, 1))+' kWh'
    rd = "⚡ RED  \nDISTR."
    bat = "      🔋  BATERIA      \n "
    if s.s["GEN"]["BAT"]["kwh"] >0:
        bat_style = 'solid'
    else:
        bat_style = 'invis'
    dot.node(
        bat,
        color="black",
        shape="cylinder",
        fontcolor="black",
        style=bat_style
    )
    dot.node(
        fv,
        color="blue",
        shape="box",
        fontcolor="blue",
    )

    dot.node(
        viv,
        color="brown",
        shape="house",
        fontcolor="brown",
    )


    dot.node(
        rd,
        color="black",
        # shape="cds",
        shape="underline",
        fontcolor="black",
    )

    dot.edge(
        fv,
        bat,
        style='invis',
    )
    dot.edge(
        fv,
        rd,
        style='invis',
    )


    dot.edge(
        fv,
        viv,
        xlabel="AUTOCON.:\n"+str(round(Aut/gen*100))+' % Gen.\n' + str(round(Aut/cons*100))+' % Cons.\n' +
        str(round(Aut, 1))+' kWh',
        # arrowhead="none",
        color="blue",
        fontcolor="black",
        style='dashed',
        penwidth=str(Aut/dae*ww),
    )


    dot.edge(
        fv,
        rd,
        xlabel="EXCEDENTE:\n"+str(round(Exc/gen*100))+' % Gen.\n' +
        str(round(Exc, 1))+' kWh',
        # arrowhead="none",
        color="red",
        fontcolor="black",
        style='dotted',
        penwidth=str(Exc/dae*ww),
    )

    dot.edge(
        rd,
        viv,
        xlabel="DEMANDA:\n"+str(round(Dem/cons*100))+' % Cons.\n' +
        str(round(Dem, 1))+' kWh',
        # arrowhead="none",
        color="grey",
        fontcolor="black",
        style="bold",
        penwidth=str(Dem/dae*ww),
    )
    if 1:
        dot.edge(
            rd,
            bat,
            xlabel="",
            # arrowhead="none",
            color="black",
            fontcolor="black",
            style=bat_style,
            penwidth="1",
        )
        dot.edge(
            fv,
            bat,
            xlabel='',
            # arrowhead="none",
            color="black",
            fontcolor="black",
            style=bat_style,
            penwidth="1",
        )
        dot.edge(
            bat,
            viv,
            xlabel='',
            # arrowhead="none",
            color="black",
            fontcolor="black",
            style=bat_style,
            penwidth="1",
        )

    # st.graphviz_chart(dot)
    # dot.view()
    dot.format = "png"
    return dot.render()


def fig_diagrama_energia_mensual():

    from matplotlib.offsetbox import TextArea, OffsetImage, AnnotationBbox

    df = pd.DataFrame()
    df["Autoconsumo"] = ur.Outputs.year1_hourly_system_to_load
    df["Demanda"] = ur.Outputs.year1_hourly_e_fromgrid
    df["Excedente"] = ur.Outputs.year1_hourly_e_togrid
    df["Excedente"] = -df["Excedente"]
    df["Generacion"] = pv.Outputs.gen
    df["Sin FV"] = ur.Load.load
    df["Con FV"] = df["Sin FV"] - df["Autoconsumo"]
    df["Consumo"] = ur.Load.load

    df["fecha_hora"] = pd.date_range("2021-01-01", periods=365 * 24, freq="H")
    df = df.set_index("fecha_hora")
    df0 = df.copy()

    # para el acumulado anual

    # fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(5, 2.5))

    ###########################
    # para el acumulado por horas
    df = df0.copy()
    df = df.groupby(df.index.month).mean()
    df

    styles = ["ks--", "ko-", "k|-", "kx-", "k*-"]
    linewidths = [4, 4, 0.51, 0.51, 0.51]
    for col, style, lw in zip(df.columns, styles, linewidths):
        df[col].plot(style=style, lw=lw, ax=ax)

    ax.set_title("Energia mensual")
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    # df.loc['2021-01-01':'2021-01-01'].plot(xlabel='mes' , ylabel='kw',kind='bar',ax=ax)
    ax.yaxis.grid()
    ax.legend()
    ax.set_xlabel("mes")
    ax.set_ylabel("kWh")
    ###################
    # plt.close()
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="png", transparent=True)
    imgdata.seek(0)  # rewind the data
    plt.close()
    return imgdata


def fig_diagrama_energia_mensual_barras():

    from matplotlib.offsetbox import TextArea, OffsetImage, AnnotationBbox

    color = ["b", "dimgray",  "r"]
    df = pd.DataFrame()
    df["Autoconsumo"] = ur.Outputs.year1_hourly_system_to_load
    df["Demanda"] = ur.Outputs.year1_hourly_e_fromgrid
    df["Excedente"] = ur.Outputs.year1_hourly_e_togrid
    df["Excedente"] = -df["Excedente"]
    df["Generacion"] = pv.Outputs.gen
    df["Sin FV"] = ur.Load.load
    df["Con FV"] = df["Sin FV"] - df["Autoconsumo"]
    df["Consumo"] = ur.Load.load

    df["fecha_hora"] = pd.date_range("2021-01-01", periods=365 * 24, freq="H")
    df = df.set_index("fecha_hora")
    df0 = df.copy()

    # para el acumulado anual

    # fig, ax = plt.subplots()
    fig, ax = plt.subplots(figsize=(5, 2.5))

    ###########################
    # para el acumulado por horas
    df = df0.copy()
    df = df.groupby(df.index.month).sum()

    #
    # df[df.columns.to_list()[0:3]].plot(
    #     xlabel="hora",
    #     ylabel="kWh",
    #     kind="bar",
    #     color=color[0:3],
    #     width=1,
    #     stacked=True,
    #     alpha=0.9,
    #     ax=ax,
    # )
    df[["Autoconsumo", "Demanda", "Excedente"]].plot(
        xlabel="hora",
        ylabel="kWh",
        kind="line",
        color=color,
        linewidth=4,
        style=["--", "-", ":"],
        alpha=0.9,
        ax=ax,
    )

    for container, hatch in zip(ax.containers, ("|", "x", ".")):
        for patch in container.patches:
            patch.set_hatch(hatch)

    ax.set_title("Consumo mensual")
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    # df.loc['2021-01-01':'2021-01-01'].plot(xlabel='mes' , ylabel='kw',kind='bar',ax=ax)
    ax.yaxis.grid()
    plt.axhline(y=0, color='k', linestyle='-.')

    fig.autofmt_xdate()
    ax.set_xlabel('mes')

    ###################
    # plt.close()
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="png", transparent=True)
    imgdata.seek(0)  # rewind the data
    plt.close()
    return imgdata


def fig_diagrama_energia_horaria_barras():

    from matplotlib.offsetbox import TextArea, OffsetImage, AnnotationBbox

    color = ["b", "dimgray",  "r"]
    df = pd.DataFrame()
    # df["Autoconsumo"] = s.s["ur"]["Outputs"]["year1_hourly_system_to_load"]
    df["Autoconsumo"] = ur.Outputs.year1_hourly_system_to_load
    df["Demanda"] = ur.Outputs.year1_hourly_e_fromgrid
    df["Excedente"] = ur.Outputs.year1_hourly_e_togrid
    df["Excedente"] = -df["Excedente"]
    df["Generacion"] = pv.Outputs.gen
    df["Sin FV"] = ur.Load.load
    df["Con FV"] = df["Sin FV"] - df["Autoconsumo"]
    df["Consumo"] = ur.Load.load

    df["fecha_hora"] = pd.date_range("2021-01-01", periods=365 * 24, freq="H")
    df = df.set_index("fecha_hora")
    df0 = df.copy()

    # para el acumulado anual

    fig, ax = plt.subplots(figsize=(5, 2.5))

    ###########################
    # para el acumulado por horas
    df = df0.copy()
    df = df.groupby(df.index.hour).mean()
    df
    #
    # df[df.columns.to_list()[0:3]].plot(
    #     xlabel="hora",
    #     ylabel="kWh",
    #     kind="bar",
    #     color=color[0:3],
    #     width=1,
    #     stacked=True,
    #     alpha=0.9,
    #     ax=ax,
    # )
    df[["Autoconsumo", "Demanda", "Excedente"]].plot(
        xlabel="hora",
        ylabel="kWh",
        kind="line",
        color=color,
        linewidth=4,
        style=["--", "-", ":"],
        alpha=0.9,
        ax=ax,
    )

    # )
    df[["Consumo", "Generacion"]].plot(
        xlabel="hora",
        ylabel="kWh",
        kind="line",
        color=["black", "blue"],
        linewidth=1,
        style=["-", "--"],
        alpha=0.9,
        ax=ax,
    )

    for container, hatch in zip(ax.containers, ("|", "x", ".")):
        for patch in container.patches:
            patch.set_hatch(hatch)
    plt.axhline(y=0, color='k', linestyle='-.')

    ax.set_title("Consumo horario medio anual")
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    # df.loc['2021-01-01':'2021-01-01'].plot(xlabel='mes' , ylabel='kw',kind='bar',ax=ax)
    ax.legend(["Autoconsumo", "Demanda", "Excedente"])
    ax.yaxis.grid()
    fig.autofmt_xdate()

    ###################
    # plt.close()
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="png", transparent=True)
    imgdata.seek(0)  # rewind the data
    plt.close()
    return imgdata


def fig_flujo_caja_simplificado():
    color = ["k", "b", "r"]

    fig, ax = plt.subplots(figsize=(5, 2.5))

    df = pd.DataFrame()
    df["SIN Subv."] = cl.Outputs.cf_cumulative_payback_with_expenses
    pb_sin = cl.Outputs.payback
    #######################################################
    cl.PaymentIncentives.ibi_sta_amount = 600*pv.SystemDesign.system_capacity
    cl.execute(0)
    #######################################################
    df["CON Subv."] = cl.Outputs.cf_cumulative_payback_with_expenses
    pb_con = cl.Outputs.payback
    #######################################################
    cl.PaymentIncentives.ibi_sta_amount = 0
    cl.execute(0)
    #######################################################
    color = ['b', 'r']
    style = ["-", "--"]
    x = [pb_sin, pb_con]

    df.plot(kind="line", ax=ax, alpha=1, color=color, style=style)
    plt.axhline(y=0, color='k', linestyle='-.')

    for i in [0, 1]:

        # plt.axvline(x=x[i], color=color[i], linestyle='-.')

        ax.annotate(
            str(round(x[i], 1))+' años '+df.columns[i],
            xy=(x[i], 0),
            color=color[i],
            xycoords='data',
            xytext=(-20, 40+i*20),
            textcoords='offset points',
            arrowprops=dict(arrowstyle="->",
                            color=color[i],
                            linestyle=style[i],
                            connectionstyle="arc3,rad=.98"))

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="y")
    ax.set_title("Amortización")
    ax.legend(loc='lower right').remove()
    fig.autofmt_xdate()
    ###################
    imgdata = io.BytesIO()
    fig.savefig(imgdata, transparent=True)
    imgdata.seek(0)  # rewind the data
    plt.close()
    return imgdata


def fig_factura():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    df = pd.DataFrame()
    df["year1_monthly_utility_bill_wo_sys"] = s.s["ur"]["Outputs"][
        "year1_monthly_utility_bill_wo_sys"
    ]
    df["year1_monthly_utility_bill_w_sys"] = s.s["ur"]["Outputs"][
        "year1_monthly_utility_bill_w_sys"
    ]

    ax.set_title("Factura mensual con y sin sistema")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    df.plot(xlabel="mes", ylabel="$/mo", kind="bar", ax=ax)
    ###################
    for bar in ax.patches:
        # The text annotation for each bar should be its height.
        bar_value = round(bar.get_height(), 2)
        # Format the text with commas to separate thousands. You can do
        # any type of formatting here though.
        text = f"{bar_value:,}"
        # This will give the middle of each bar on the x-axis.
        text_x = bar.get_x() + bar.get_width() / 2
        # get_y() is where the bar starts so we add the height to it.
        text_y = bar.get_y() + bar_value
        # If we want the text to be the same color as the bar, we can
        # get the color like so:
        bar_color = bar.get_facecolor()
        # If you want a consistent color, you can just set it as a constant, e.r. #222222
        ax.text(text_x, text_y, text, ha="center",
                va="bottom", color=bar_color, size=8)
    #
    ax.legend(["CON FV", "SIN FV"])

    imgdata = io.BytesIO()
    fig.savefig(imgdata, transparent=True)
    imgdata.seek(0)  # rewind the data
    plt.close()
    return imgdata


def df2tabla(
    df=pd.DataFrame({"lab": ["A", "B", "C"], "valfasdfasdfasd": [10, 30, 20]})
):
    # df=df.T
    # fig, ax = plt.subplots(**kwargs)
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.set_title("tabla_sam_summary", y=-0.15)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ccolors = ["lightgrey"] * len(df.columns)
    t = ax.table(
        cellText=df.values,
        colColours=ccolors,
        colLabels=df.columns,
        cellLoc="left",
        loc="center",
    )
    ax.axis("off")
    t.auto_set_font_size(False)
    t.set_fontsize(12)
    t.scale(1, 2)
    t.auto_set_column_width(col=list(range(len(df.columns))))
    imgdata = io.BytesIO()
    fig.savefig(imgdata, format="png")
    imgdata.seek(0)  # rewind the data
    #
    plt.close()
    return imgdata
