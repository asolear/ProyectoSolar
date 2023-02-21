from app_utils import *

pdf_file = (
    os.path.dirname(__file__)
    + "/"
    + os.path.splitext(os.path.basename(__file__))[0]
    + ".pdf"
)

in_pdf_file = "./apps/A/flow_canvas.pdf"

# ###########
# ###########
# ###########
# ###########


def tipo_inst2columna(tipo="A", aislamiento="XLPE", fases="2x"):
    import csv

    data = list(
        csv.reader(
            StringIO(
                """A1,4,3,7,6
A2,3,2,6,5
B1,6,5,10,8
B2,5,4,8,7
C,8,6,11,9
E,9,7,12,10
F,10,8,13,11
"""
            )
        )
    )

    df = pd.DataFrame(data)
    df.set_index(0, inplace=True)
    df.index.rename("Tipo_instalacion", inplace=True)
    columns = pd.MultiIndex.from_tuples(
        [("PVC", "2x"), ("PVC", "3x"), ("XLPE", "2x"), ("XLPE", "3x")]
    )
    df.columns = columns
    col = df.loc[tipo, (aislamiento, fases)]
    # col = "444"
    return col


def Imax(secc="6", col="10"):
    import csv

    data = list(
        csv.reader(
            StringIO(
                """mm2,2,3,4,5,6,7,8,9,10,11,12,13
1.5,11,11.5,13,13.5,15,16,16.5,19,20,21,24,
2.5,15,16,17.5,18.5,21,22,23,26,26.5,29,33,
4,20,21,23,24,27,30,31,34,36,38,45,
6,25,27,30,32,36,37,40,44,46,49,57,
10,34,37,40,44,50,52,54,60,65,68,76,
16,45,49,54,59,66,70,73,81,87,91,105,
25,59,64,70,77,84,88,95,103,110,116,123,140
35,,77,86,96,104,110,119,127,137,144,154,174
50,,94,103,117,125,133,145,155,167,175,188,210
70,,,,149,160,171,185,199,214,224,244,269
95,,,,180,194,207,224,241,259,271,296,327
120,,,,208,225,240,260,280,301,314,348,380
150,,,,236,260,278,299,322,343,363,404,438
185,,,,268,297,317,341,368,391,415,464,500
240,,,,315,350,374,401,435,468,490,552,590
300,,,,361,401,430,461,500,538,563,638,678
400,,,,431,480,515,552,699,645,674,770,812
500,,,,493,551,592,633,687,741,774,889,931
630,,,,565,632,681,728,790,853,890,1028,1071
"""
            )
        )
    )
    df = pd.DataFrame(data=data[1:], columns=data[0])
    df.set_index("mm2", inplace=True)

    Imax = df.loc[secc, col]
    secc = df.index  # solo por sacar las seccines normalizadas
    return Imax, secc


def secciones_execute():
    # circuito = "LGA"
    # df = pd.DataFrame(ss.ii.Circuitos)
    df = pd.DataFrame.from_dict(
        {
            (i, j): ss.ii.Circuitos[i][j]
            for i in ss.ii.Circuitos.keys()
            for j in ss.ii.Circuitos[i].keys()
        },
        orient="index",
    )
    df = df[["value"]]
    df = df.reset_index()
    df = df.pivot(index="level_1", columns="level_0", values="value")

    for circuito in list(ss.ii.Circuitos.keys()):
        # https://industria.gob.es/Calidad-Industrial/seguridadindustrial/instalacionesindustriales/baja-tension/Documents/bt/guia_bt_anexo_2_sep03R1.pdf

        if 1 == 1:  # secion por caida de tension maxima ##############
            if df.loc["_F", circuito] == "2x":
                ff = 2
                fases = 1
            else:
                ff = 1
                fases = 3

            df.loc["e_V", circuito] = (
                float(df.loc["_e", circuito]) * float(df.loc["_U", circuito]) / 100
            )

            if df.loc["_I", circuito] == "FV":
                df.loc["FI", circuito] = 1.25  # GUÍA-BT-40 5. CABLES DE CONEXION
            else:
                df.loc["FI", circuito] = 1

            #  a tabla A de la guía BT-19

            df.loc["col", circuito] = tipo_inst2columna(
                df.loc["_TI", circuito],
                df.loc["_C", circuito],
                df.loc["_F", circuito],
            )
            if 1 == 1:
                df.loc["I", circuito] = round(
                    df.loc["FI", circuito]
                    * df.loc["_P_kW", circuito]
                    * 1000
                    / (np.sqrt(fases) * df.loc["_U", circuito] * 1),
                    1,
                )

            # seccion
            df.loc["Sc", circuito] = round(
                ff
                * np.sqrt(fases)
                * df.loc["I", circuito]
                * 1
                * df.loc["_L_m", circuito]
                / 48
                / float(df.loc["e_V", circuito]),
                2,
            )

            (
                aa,
                secciones_comerciales,
            ) = Imax()  # esta vez la llamo solopara coger las secciones

            # bins = secciones_comerciales.copy()
            bins = [float(i) for i in secciones_comerciales.copy().tolist()]
            bins.insert(0, 0)
            try:
                df.loc["S_V", circuito] = (
                    pd.cut(
                        x=[df.loc["Sc", circuito]],
                        bins=bins,
                        labels=list(map(str, secciones_comerciales)),
                        include_lowest=True,
                    )
                )[0]
            except:
                print("seccion comercial ha fallado")

            df.loc["I_z", circuito], secc = Imax(
                df.loc["S_V", circuito], df.loc["col", circuito]
            )
        ######################################
        ######################################
        ######################################
        # !!!!!!!!!!!!!!!!!  falta poner las condiciones y meter la tabla
        # factores de correccion  por temperatura, agrupamiento ...
        df.loc["Ft", circuito] = 0.77
        df.loc["Fa", circuito] = 0.9
        df.loc["Fr", circuito] = 1
        df.loc["Fs", circuito] = 0.9
        # df.loc["kr", circuito]= df.loc["Ft", circuito]*df.loc["Fa", circuito]*df.loc["Fr", circuito]*df.loc["Fs", circuito]
        df.loc["kr", circuito] = 1
        ######################################
        ######################################
        ######################################

        # if 1 == 11:  # secccion por intensidad maxima
        imax = 0.0
        indice_seccion = 0
        while float(imax) <= float(df.loc["I", circuito]):
            imax, secc = Imax(
                secciones_comerciales[indice_seccion], df.loc["col", circuito]
            )
            imax = float(imax) * df.loc["kr", circuito]

            indice_seccion += 1
        df.loc["S_I", circuito] = secciones_comerciales[indice_seccion]
        # para la seccion tomando la mas restricitva
        df.loc["S", circuito] = max(
            float(df.loc["S_I", circuito]), float(df.loc["S_V", circuito])
        )

        # Intnsidades d cortocircuito
        df.loc["Icc", circuito] =22

    return df


# ###########
# ###########
# ###########
# ###########


def app():
    if 1 == 1:
        # print(df)
        packet = io.BytesIO()
        can = Canvas(packet)
        pagina = 0
        out_pdf_file = pdf_file
        existing_pdf = PdfFileReader(open(in_pdf_file, "rb"))
        output = PdfFileWriter()
        st.write(str(len(existing_pdf.pages)) + " paginas")
    # ###########
    # ###########
    # ###########
    # ###########

    if 1 == 1:
        print("proyecto.secciones")
    if 1 == 1:
        instalacion = ss.ii.proyecto["general"]["tipo_instalacion"]

        imagen = "apps/A/figs/asistidas.png"

        can.drawImage(
            imagen,
            77,
            400,
            mask="auto",
            width=500,
            height=300,
        )
    if 1 == 1:
        # df=pd.DataFrame(ss.ii.circuitos)
        dff = secciones_execute().T
        # print(dff)
        df = dff.loc[:, :"col"]
        df = round(df, 1)
        columnas = df.columns.tolist()
        columnas.insert(0, "i")
        df["i"] = df.index
        df = df[columnas]
        cd = df.values.tolist()
        cd.insert(0, (df.columns.tolist()))
        # cd.insert(
        #     0,
        #     [
        #         "Id.",
        #         "Tramo",
        #         "Aislam. (***)",
        #         "Cond. (*)",
        #         "L (m)",
        #         "P (kW)",
        #         "Inst. (**)",
        #         "U (V)",
        #         "e (%)",
        #     ],
        # )
        tbl = Table(cd)
        tbl.setStyle(tblstyle)
        tbl.wrapOn(can, 0, 0)
        tbl.drawOn(can, 100, 222)

    if 1 == 1:
        dff = secciones_execute().T
        df = dff.loc[:, "col":]
        df = round(df, 1)
        columnas = df.columns.tolist()
        columnas.insert(0, "i")
        df["i"] = df.index
        df = df[columnas]
        cd = df.values.tolist()
        cd.insert(0, (df.columns.tolist()))
        # cd.insert(
        #     0,
        #     [
        #         "Id.",
        #         "S.calc. (mm2)",
        #         "S (mm2)",
        #         "I max (A)*",
        #         "I prevista (**)",
        #     ],
        # )
        tbl = Table(cd)
        tbl.setStyle(tblstyle)
        tbl.wrapOn(can, 0, 0)
        tbl.drawOn(can, 100, 0)

    if 1 == 1:
        while pagina < 1:
            can.showPage()
            pagina += 1

    if 1 == 1:
        definiciones = [
            ["fasdf", "fasfd"],
            ["fasdf", "fasfd"],
            ["fasdf", "fasfd"],
            ["fasdf", "fasfd"],
        ]

        cd = definiciones
        cd.insert(0, ['variable','Definicion'])
        # cd.insert(
        #     0,
        #     [
        #         "Id.",
        #         "S.calc. (mm2)",
        #         "S (mm2)",
        #         "I max (A)*",
        #         "I prevista (**)",
        #     ],
        # )
        tbl = Table(cd)
        tbl.setStyle(tblstyle)
        tbl.wrapOn(can, 0, 0)
        tbl.drawOn(can, 0, 666)

    if 1 == 1:
        while pagina < 2:
            can.showPage()
            pagina += 1

    # ###########
    # ###########
    # ###########
    # ###########
    if 1 == 1:
        while pagina < len(existing_pdf.pages):
            can.showPage()
            pagina += 1

        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.getPage(i)
            page.merge_page(new_pdf.getPage(i))
            output.addPage(page)
        outputStream = open(out_pdf_file, "wb")
        output.write(outputStream)
        outputStream.close()
