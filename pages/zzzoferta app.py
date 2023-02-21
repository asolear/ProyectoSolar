from app_utils import *


def app():
    ###############################################################
    mmpdf = io.BytesIO()
    c = Canvas(mmpdf)

    print(os.path.basename(__file__))
    ###############################################################

    tblstyle = TableStyle(
        [
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("FONTNAME", (0, 0), (-1, -1), "Times-Italic"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-BoldOblique"),
            ("TEXTCOLOR", (0, 0), (-1, -1), "grey"),
            ("TEXTCOLOR", (0, 0), (-1, 0), "black"),
            ("BOX", (0, 0), (-1, -1), 1, colors.grey),
            # ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]
    )
    letra_pequena = TableStyle(
        [
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("FONTNAME", (0, 0), (-1, -1), "Times-Italic"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-BoldOblique"),
            ("TEXTCOLOR", (0, 0), (-1, -1), "grey"),
            ("TEXTCOLOR", (0, 0), (-1, 0), "black"),
        ]
    )
    letra_grande = TableStyle(
        [
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("FONTNAME", (0, 0), (-1, -1), "Times-Italic"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-BoldOblique"),
            ("TEXTCOLOR", (0, 0), (-1, -1), "grey"),
            ("TEXTCOLOR", (0, 0), (-1, 0), "black"),
        ]
    )
    ff = -300
    tt = 0
    vencimiento = datetime.datetime.now() + datetime.timedelta(days=-14)
    enlaceqr = [
        "https://asolear.es/proyecto?ref="
        + s.s["GEN"]["Ubicacion"]["Parcela"]

        + "&nv="
        + str(s.s["GEN"]["Ubicacion"]["_Nvecinos"])
        + "&a="
        + vencimiento.strftime("%Y")
        + "&m="
        + vencimiento.strftime("%m")
        + "&d="
        + vencimiento.strftime("%d")
    ]

    def G_CODIGO_QR(x, y):

        # este dato lo manda al JS que cuenta los mese de 0 a 11 por eso resto 15

        c.drawImage(
            ImageReader(fqrcode_logo(enlaceqr[0])),
            x,
            y,
            mask="auto",
            width=77,
            height=77,
        )

    G_CODIGO_QR(500, 760)

    def T_EMPRESA(x, y):

        c.drawImage("assets/img/asolear.png", x, y,
                    width=50, height=50, mask="auto")

        data = [
            ["ASOLEAR"],
            [s.s["_ADMIN"]["empresa"]["d1"]],
            [s.s["_ADMIN"]["empresa"]["d2"]],

            [],
        ]

        table = Table(data, rowHeights=(12))
        table.setStyle(letra_grande)
        table.wrapOn(c, 1, 1)
        table.drawOn(c, x + 60, y - 10)

    T_EMPRESA(44, 760)

    def T_DESTINATARIO(x, y):

        # c.drawImage("assets/img/asolear.png", x, y, width=50, height=50, mask="auto")

        data = [
            ["Sr. <propietario> "],
            ["Moby Dick 30"],
            ["29004 Málaga"],
            ["Tel.: 600 366 211 • www.asolear.es "],
            [],
        ]

        table = Table(data, rowHeights=(12))
        table.setStyle(letra_grande)
        table.wrapOn(c, 1, 1)
        table.drawOn(c, x + 60, y - 10)

    T_DESTINATARIO(288, 666)

    def T_OFERTA(x, y):

        c.setFillColor("grey", alpha=1)
        c.setFont("Helvetica", 17)
        c.drawString(x, y + 40, "Oferta " +
                     s.s["GEN"]["Ubicacion"]["Parcela"]
                     )

        data = [
            ["Fecha de oferta:", "Fecha de vencimiento"],
            [
                (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime(
                    " %d / %m / %Y "
                ),
                (datetime.datetime.now() + datetime.timedelta(days=+16)).strftime(
                    " %d / %m / %Y "
                ),
            ],
            ['Oferta no vinculante supeditada a la visita tecnica.']
        ]

        table = Table(data, rowHeights=(12))
        table.setStyle(letra_grande)
        table.wrapOn(c, 1, 1)
        table.drawOn(c, x, y)

        c.setFillColor("grey", alpha=1)
        c.setFont("Helvetica", 17)
        data = [
            [
                "Descripción                                                              ",
                "Cantidad",
                "Precio",
                "Importe",
            ],
            [],
            # [str(s.FV.Ubicacion._kwp)],
            [
                "           Instalacion fotovoltaica de autoproduccion colectiva en red  \ninterior con excedentes y compensacion simplificada. (kWp / Viv.)",
                str(s.s["GEN"]["Ubicacion"]["_kwp"])+" / " + \
                str(s.s["GEN"]["Ubicacion"]["_Nvecinos"]),
                str(s.s['FV']['Costes']['_coste_unitario']),
                "€  "+str(cl.SystemCosts.total_installed_cost),
            ],
            [],
            ["      Subtotal", "", "", "€ " + \
                str(cl.SystemCosts.total_installed_cost)],
            ["      IVA (21 %)", "", "", "€ " + \
             str(round(cl.SystemCosts.total_installed_cost*0.21, 2))],
            ["      TOTAL", "", "", "€ " + \
                str(round(cl.SystemCosts.total_installed_cost*1.21, 2))],
        ]

        table = Table(data, rowHeights=(14))
        table.setStyle(tblstyle)
        table.wrapOn(c, 1, 1)
        table.drawOn(c, x, y - 122)

        c.setFillColor("black", alpha=1)
        c.setFont("Helvetica", 8)
        c.drawString(
            x,
            y - 133,
            "           Por favor utilice el codigo QR para asociarse a la instalacion. Debe haber al menos " +
            str(np.ceil(s.s["GEN"]["Ubicacion"]["_Nvecinos"]/3))+" asociados.",
        )

    T_OFERTA(44, 577 + tt)
    c.setStrokeColor("grey", alpha=.51)
    c.rect(44, 5, 522, 380,  fill=0)
    # c.roundRect(44, 5, 522, 380, 4, stroke=1, fill=0)
    c.setFillColor("black", alpha=1)

    def T_ESTUDIO(x, y):

        # c.drawImage("assets/img/asolear.png", x, y, width=50, height=50, mask="auto")

        data = [
            ["RESUMEN DEL ESTUDIO TECNICO-ECONOMICO POR ASOCIADO"],
            [],
            [],
            [],
        ]

        table = Table(data, rowHeights=(12))
        table.setStyle(letra_pequena)
        table.wrapOn(c, 1, 1)
        table.drawOn(c, x, y)

    T_ESTUDIO(44, 333)

    def T_INSTALACION(x, y):
        c.drawImage(
            ImageReader(tabla(T_INSTALACION_JUSTIFICACION(),
                        'Datos de la instalación')),
            x,
            y,
            mask="auto",
            width=222,
            height=222,
        )

    T_INSTALACION(22, 210)

    def T_CONSUMOS(x, y):
        c.drawImage(
            ImageReader(tabla(T_CONSUMOS_JUSTIFICACION(),
                        'Energía consumida anual estimada')),
            x,
            y,
            mask="auto",
            width=222,
            height=222,
        )

    T_CONSUMOS(22, 133)

    def T_GENERADA(x, y):

        c.drawImage(
            ImageReader(
                tabla(T_GENERADA_JUSTIFICACION(), 'Energía generada anual estimada')),
            x,
            y,
            mask="auto",
            width=222,
            height=222,
        )

    T_GENERADA(22, 55)

    def T_FINANCIERA(x, y):

        c.drawImage(
            ImageReader(
                tabla(T_FINANCIERA_JUSTIFICACION(), 'Valores economicos estimados')),
            x,
            y,
            mask="auto",
            width=222,
            height=222,
        )

    T_FINANCIERA(22, -40)

    def G_CUBIERTA(x, y):
        c.drawImage(
            ImageReader(plano_cubierta_paneles()),
            x,
            y,
            mask="auto",
            width=333,
            height=333,
        )

    G_CUBIERTA(133, 266 + ff)

    def G_E_ANUAL(x, y):
        c.drawImage(
            ImageReader(fig_diagrama_energia_anual()),
            x,
            y,
            mask="auto",
            width=155,
            height=133,
        )

    G_E_ANUAL(222, 515 + ff)

    def G_E_DIARIO(x, y):
        c.drawImage(
            ImageReader(fig_diagrama_energia_horaria_barras()),
            x,
            y,
            mask="auto",
            width=200,
            height=100,
        )

    G_E_DIARIO(377, 560 + ff)

    def G_E_ANUAL_LIN(x, y):
        c.drawImage(
            ImageReader(fig_diagrama_energia_mensual_barras()),
            x,
            y,
            mask="auto",
            width=200,
            height=100,
        )

    G_E_ANUAL_LIN(377, 440 + ff)

    def G_AMORTIZACION(x, y):
        c.drawImage(
            ImageReader(fig_flujo_caja_simplificado()),
            x,
            y,
            mask="auto",
            width=200,
            height=100,
        )

    G_AMORTIZACION(377, 322 + ff)

    def T_CONDICIONES(x, y):

        c.drawImage("assets/img/454px-Escudo_Ingeniería_Tecnica_Industrial.svg.png", x+5, y+6,
                    width=22, height=22, mask="auto")
        data = [
            [
                " © PROYECTO.SOLAR • Tel.: 600 366 211 • www.proyecto.solar ",
            ],
            [
                "Prohibido el uso por terceros. Contiene información sometida a derecho profesional "
            ],
        ]

        table = Table(data, rowHeights=(8))
        table.setStyle(letra_pequena)
        table.wrapOn(c, 1, 1)
        table.drawOn(c, x+22, y)

    T_CONDICIONES(44, 0)

    def TXTs():
        c.setFillColor("grey", alpha=1)
        c.setFont("Helvetica", 7)
        c.rotate(90)
        c.drawString(
            580,
            -590,
            enlaceqr[0],
        )
        c.drawString(
            222,
            -11,
            "ASOLEAR" + s.s["_ADMIN"]["empresa"]["d1"] +
            s.s["_ADMIN"]["empresa"]["d2"],
        )

    TXTs()

    ###############################################################
    ppdf(os.path.abspath(__file__)[:-3], c, mmpdf, 0)
    ###############################################################


# str(np * s.s["GEN"]["panel"]["Pmp"][0])+
#                 " / " +
#                 str(s.s["GEN"]["Ubicacion"]["_Nvecinos"])+
#                 " $ kWp$"
