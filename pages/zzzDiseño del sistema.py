from app_utils import *
import itertools


def app():
    ###############################################################
    mmpdf = io.BytesIO()
    can = Canvas(mmpdf)
    ###############################################################

    def df2tabla(df):
        fig, ax = plt.subplots(figsize=(6, 6))
        # ax.set_title("tttittttuuuulllooo", y=0.21015)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ccolors = ["lightgrey"] * len(df.columns)
        rcolors = ["lightgrey"] * df.shape[0]
        t = ax.table(
            cellText=df.values,
            rowLabels=df.index,
            colLabels=df.columns,
            colColours=ccolors,
            rowColours=rcolors,
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
        return imgdata

    def curva_IV(df):  # curva IV de los paneles e inversor
        from scipy import interpolate

        # df.set_index(0)
        df = df.squeeze()
        # st.stop()
        fig, ax = plt.subplots(figsize=(16, 4))
        plt.grid()
        plt.title(
            str(df["Ramas_Paralelo"])
            + " paneles "
            # + s.s['sys']['panel']["Name"]
            + " conectados al "
            + "\n"
            + " MPPT "
            + str(1)
            + " del inversor "
            # + s.s['sys']['inversor']["Name"]
        )
        plt.xlabel("Voltaje (V)")
        plt.ylabel("Intensidad (A)")

        ymax = max(
            df["Idcmax"] * 1.1,
            df["Isc_s"] * df["Ramas_Paralelo"] * 1.1,
        )
        xmax = max(
            df["Vdcmax"] * 1.2,
            df["Voc_s"] * df["Ramas_Paralelo"] * 1.1,
        )
        ax.set_xlim(0, xmax)
        ax.set_ylim(0, ymax)
        #
        plt.axhline(
            y=df["Imp_s"] * df["Ramas_Paralelo"],
            color="y",
            linestyle=":",
            linewidth="3",
            label="IMPP * NP = {} A".format(
                round(df["Imp_s"] * df["Ramas_Paralelo"], 2)
            ),
        )
        plt.axvline(
            x=df["Vmp_s"] * df["Ramas_Paralelo"],
            color="c",
            linestyle=":",
            linewidth="3",
            label="VMPP * NS= {} V".format(
                round(df["Vmp_s"] * df["Ramas_Paralelo"], 2)
            ),
        )
        plt.axvspan(
            0,
            df["Mppt_low"],
            alpha=0.2,
            hatch="///",
            color="black",
            label="VI_MIN = {} V".format(df["Mppt_low"]),
        )
        plt.axvspan(
            df["Mppt_high"],
            xmax,
            hatch="///",
            alpha=0.2,
            color="orange",
            label="Mppt_high = {} V".format(df["Mppt_high"]),
        )
        plt.axvspan(
            df["Vdcmax"],
            xmax,
            hatch="\\",
            alpha=0.2,
            color="black",
            label="Vdcmax = {} V".format(df["Vdcmax"]),
        )
        plt.axhspan(
            df["Idcmax"],
            ymax,
            hatch="\\",
            alpha=0.2,
            color="grey",
            label="Idcmax = {} A".format(df["Idcmax"]),
        )
        TT = [0, 25, 70]
        cc = ["b", "g", "r"]
        i = 1
        for i in range(len(TT)):
            VCAx = (
                df["Voc_s"]
                * (1 + (TT[i] - 25) * (df["Boc"] / 100))
                * df["Ramas_Paralelo"]
            )
            VMPPx = (
                df["Vmp_s"]
                * (1 + (TT[i] - 25) * (df["Boc"] / 100))
                * df["Ramas_Paralelo"]
            )
            ICCx = (
                df["Isc_s"]
                * (1 + (TT[i] - 25) * (df["Asc"] / 100))
                * df["Ramas_Paralelo"]
            )
            IMPPx = (
                df["Imp_s"]
                * (1 + (TT[i] - 25) * (df["Asc"] / 100))
                * df["Ramas_Paralelo"]
            )
            x = np.array([0, VMPPx * 0.9, VMPPx, VCAx])
            y = np.array([ICCx, ICCx * 0.97, IMPPx, 0])
            x2 = np.linspace(x[0], x[-1], 100)
            y2 = interpolate.pchip_interpolate(x, y, x2)
            plt.plot(
                x2,
                y2,
                "--",
                color=cc[i],
                linewidth="3",
                label="f(I,V) {} °C, 1000 W/m$^2$".format(TT[i]),
            )
            plt.plot(
                x[[0, 2, 3]],
                y[[0, 2, 3]],
                "o",
                color=cc[i],
                ms=10,
            )
        plt.legend()
        if 1:  # al pdf
            mmfig = io.BytesIO()
            fig.savefig(mmfig, format="png");plt.close()
            
            mmfig.seek(0)  # rewind the data
        return mmfig

    def curva_sombras(array):  # histograma produccion
        def cielo(str_sombras=[20, 0, 50, 0, 40]):
            fhh = pd.read_json(
                json.dumps(
                    s.s["PVGIS_printhorizon"]["outputs"]["horizon_profile"], indent=2
                ),
                orient="records",
            )
            fhh.set_index("A", inplace=True)
            Xresampled = fhh.index
            sombras = str_sombras
            df_sombras = pd.DataFrame([sombras]).T.rename(columns={0: "e"})
            df_sombras["a"] = np.arange(-180, 180, 360 / len(sombras))
            df_sombras = df_sombras.set_index("a")
            df_sombras_resampled = (
                df_sombras.reindex(df_sombras.index.union(Xresampled))
                .interpolate("values")
                .loc[Xresampled]
            )
            df = pd.DataFrame(
                [fhh["H_hor"].tolist(), df_sombras_resampled["e"].tolist()]
            ).T
            df.index = fhh.index
            horizonte = df[[0, 1]].max(axis=1)
            # ss.ii.horizonte = ",".join(horizonte.astype(str).to_list())
            #
            fsi = pd.read_json(
                json.dumps(
                    s.s["PVGIS_printhorizon"]["outputs"]["winter_solstice"], indent=2
                ),
                orient="records",
            )
            fsv = pd.read_json(
                json.dumps(
                    s.s["PVGIS_printhorizon"]["outputs"]["summer_solstice"], indent=2
                ),
                orient="records",
            )
            fsi.set_index("A_sun(w)", inplace=True)
            fsv.set_index("A_sun(s)", inplace=True)
            #
            return fsi, fsv, fhh, df_sombras_resampled, horizonte

        # str_sombras = s.s["FV"]["superficie"]["Sombras"][0]
        str_sombras = array["Sombras"]
        # st.stop()
        fig, ax = plt.subplots(figsize=(16, 4))
        fsi, fsv, fhh, df_sombras_resampled, horizonte = cielo(str_sombras)
        titulo = "Trayectorias del sol y Sombras"
        fsv.plot(kind="area", stacked=False, color="yellow", ax=ax)
        fsi.plot(kind="area", stacked=False, color="white", alpha=1, ax=ax)
        fhh.plot(kind="area", stacked=False, color="green", ax=ax, alpha=1)
        df_sombras_resampled["e"].plot(
            kind="area",
            stacked=False,
            ax=ax,
            alpha=1,
            grid=True,
            color="grey",
            xlabel=r"$E \leftarrow Azimut (\alpha ^o) \rightarrow O$",
        )
        horizonte.plot(kind="line", stacked=False, color="black", ax=ax, alpha=1)
        #
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.yaxis.grid()
        ax.legend("")
        ax.set_title("Horizonte y obstaculos")
        ax.set_ylabel("$Elevacion [^o]$")
        ax.set_xlabel("$ESTE  \\leftarrow Azimut [^o] \\rightarrow OESTE $")
        if 1:
            mmfig = io.BytesIO()
            fig.savefig(mmfig, format="png");plt.close()
            
            mmfig.seek(0)  # rewind the data
        return mmfig

    def curva_produccion_array(indice):
        fig, ax = plt.subplots(figsize=(16, 4))
        df = pd.read_json(
            json.dumps(
                s.s["FV"]["__pvgis"]["pvcalc"][indice]["outputs"]["monthly"][
                    "fixed"
                ],
                indent=2,
            ),
            orient="records",
        )
        df["mes"] = meses
        df = df.set_index("mes")
        df["E_m"].plot(kind="bar", ax=ax)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.yaxis.grid()
        ax.legend(frameon=False)
        ax.set_ylabel("Energía FV [kWh]")
        ax.set_title("Producción de energía array de paneles")
        if 1:
            mmfig = io.BytesIO()
            fig.savefig(mmfig, format="png");plt.close()
            
            mmfig.seek(0)  # rewind the data
        return mmfig

    def diagrama_bloques_inversores():  # digrama de bloques

        dot = graphviz.Digraph(
            "Inversores",
            comment="Inversores",
            graph_attr={
                "label": "Generador FV",
                "splines": "ortho",
                "nodesep": "1i",
            },
            node_attr={"shape": "box"},
        )
        for i_circuito_inversores, circuito_inversores in enumerate(
            s.s["FV"]["__diseno_sistema"]["Array"]
        ):

            dot.node(
                "B\n" + str(i_circuito_inversores),
                "B\n" + str(i_circuito_inversores),
                color="black",
                shape="box",
                fontcolor="black",
            )
            dot.node(
                "CGPM",
                "CGPM",
                color="black",
                shape="box",
                fontcolor="black",
            )
            dot.edge(
                "B\n" + str(i_circuito_inversores),
                "CGPM",
                xlabel="C" + str(i_circuito_inversores),
                # arrowhead="none",
                color="black",
                fontcolor="black",
                style="bold",
            )

            for i_inversor, inversor in enumerate(circuito_inversores):
                dot.edge(
                    "I\n" + str(i_circuito_inversores) + str(i_inversor),
                    "B\n" + str(i_circuito_inversores),
                    xlabel="C" + str(i_circuito_inversores) + str(i_inversor),
                    arrowhead="none",
                    color="black",
                    fontcolor="black",
                )

                for i_string, string in enumerate(inversor):
                    # if string != 0:
                    if 1:

                        txt = str(i_circuito_inversores) + str(i_inversor) + str(i_string)
                        dot.node(
                            "FV\n" + txt + "1",
                            "FV\n" + txt + "1",
                            color="black",
                            shape="box",
                            fontcolor="black",
                        )
                        dot.node(
                            "I\n" + str(i_circuito_inversores) + str(i_inversor),
                            "I\n" + str(i_circuito_inversores) + str(i_inversor),
                            color="black",
                            shape="box",
                            fontcolor="black",
                        )

                        dot.edge(
                            "FV\n" + txt + "1",
                            "I\n" + str(i_circuito_inversores) + str(i_inversor),
                            xlabel="C" + txt,
                            arrowhead="none",
                            color="black",
                            fontcolor="black",
                        )
                        if (
                            s.s["FV"]["__mppt"]["Paneles_Serie"][string] > 1
                        ):  # microinversor con 1 panel
                            dot.node(
                                "FV\n"
                                + txt
                                + str(s.s["FV"]["__mppt"]["Paneles_Serie"][string]),
                                "FV\n"
                                + txt
                                + str(s.s["FV"]["__mppt"]["Paneles_Serie"][string]),
                                color="black",
                                shape="box",
                                fontcolor="black",
                            )

                            dot.edge(
                                "FV\n"
                                + txt
                                + str(s.s["FV"]["__mppt"]["Paneles_Serie"][string]),
                                "FV\n" + txt + "1",
                                xlabel="C" + txt,
                                arrowhead="none",
                                color="black",
                                fontcolor="black",
                                style="dashed",
                            )

        dot.format = "png"
        return dot.render()

    def tabla_inversores():
        sistema_tabla = []
        for i_circuito_inversores, circuito_inversores in enumerate(
            s.s["FV"]["__diseno_sistema"]["Array"]
        ):
            for i_inversor, inversor in enumerate(circuito_inversores):
                for i_string, string in enumerate(inversor):

                    # para crear la tabla, ademas del digrama de bloques
                    array_gen = pd.DataFrame(
                        s.s["FV"]["__pvgis"]["pvcalc"][string]["outputs"]["monthly"][
                            "fixed"
                        ]
                    )["E_m"].values.tolist()

                    array_gen.insert(0, i_string)
                    array_gen.insert(0, i_inversor)
                    array_gen.insert(0, i_circuito_inversores)

                    # print(array_gen)
                    sistema_tabla.append(array_gen)

        columns = meses.copy()
        columns.insert(0, "string")
        columns.insert(0, "inversor")
        columns.insert(0, "circuito")
        df = pd.DataFrame(sistema_tabla, columns=columns)
        df = df.set_index(columns[:3])
        return df

    def curva_produccion_sistema(df):
        fig, ax = plt.subplots(figsize=(16, 4))

        df.T.plot(kind="bar", stacked=True, ax=ax)

        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.yaxis.grid()
        ax.legend(frameon=False)
        ax.set_ylabel("Energía FV [kWh]")
        ax.set_title("Producción de energía por inversor")
        if 1:
            mmfig = io.BytesIO()
            fig.savefig(mmfig, format="png");plt.close()
            
            mmfig.seek(0)  # rewind the data
        return mmfig

    def pagina_0(can):
        if 1:
            def linea(df):
                df["idss"] = [
                    str(a) for a in ([[str(x) for x in tup] for tup in df.index])
                ]
                df["Línea_string"] = df["idss"].apply(eval).apply("".join)
                df = df.drop(columns=["idss"])
                df["Línea_string"] = "C" + df["Línea_string"]
                df = df.reset_index(drop=True)
                df = df.set_index("Línea_string")
                # df['kk']=df['idss']
                return df

            def circuito_cgmp(df):

                df = df.reset_index()
                df["Línea_string"] = "C" + df["circuito"].apply(str)
                df = df.set_index("Línea_string")
                # df['kk']=df['idss']
                return df

            df = tabla_inversores().groupby(level=[0, 1, 2]).sum()
            df['ii']=df.index
            print((df))
            print(linea(df))
            df = tabla_inversores().groupby(level=[0, 1]).sum()
            df['ii']=df.index
            print((df))
            # print(linea(df))

            df = tabla_inversores().groupby(level=[0]).sum()
            df['ii']=df.index
            print((df))
            # print(circuito_cgmp(df))
            # st.stop()

            # print(tabla_inversores())
            can.drawImage(
                ImageReader(
                    curva_produccion_sistema(
                        tabla_inversores().groupby(level=[0, 1]).sum()
                    )
                ),
                10,
                22,
                mask="auto",
                width=600,
                height=155,
            )

        if 1:

            axm = 35 * len(
                list(
                    itertools.chain(
                        *list(
                            itertools.chain(
                                *s.s["FV"]["__diseno_sistema"]["Array"]
                            )
                        )
                    )
                )
            )
            maximoXpagina = 15
            can.drawImage(
                ImageReader(diagrama_bloques_inversores()),
                (300 - axm / 2) if axm < maximoXpagina * axm else 11,
                222,
                mask="auto",
                width=axm if axm < maximoXpagina * axm else maximoXpagina * axm,
                height=40 * 4,
            )

    def pagina_i(can):

        for indice in range(
            len(pd.DataFrame(s.s["FV"]["superficie"]).index)
        ):  # para cada una de las entradas MPPT

            can.showPage()  ######################   siguiente pagina    ##########################

            can.drawImage(
                ImageReader(
                    df2tabla(
                        pd.concat(
                            [
                                pd.DataFrame.from_dict(
                                    data=s.s["FV"]["superficie"], orient="index"
                                )
                                .iloc[:, indice]
                                .to_frame()
                                .drop("Sombras"),
                                pd.DataFrame.from_dict(
                                    data=s.s["FV"]["__mppt"], orient="index"
                                )
                                .iloc[:, indice]
                                .to_frame(),
                            ]
                        )
                    )
                ),
                400,
                550,
                mask="auto",
                width=200,
                height=200,
            )

            can.drawImage(
                ImageReader(
                    df2tabla(
                        pd.DataFrame.from_dict(
                            data=s.s["GEN"]["panel"], orient="index"
                        )
                        .iloc[:, indice]
                        .to_frame()
                    )
                ),
                0,
                550,
                mask="auto",
                width=200,
                height=200,
            )

            can.drawImage(
                ImageReader(
                    df2tabla(
                        pd.DataFrame.from_dict(
                            data=s.s["GEN"]["inversor"], orient="index"
                        )
                        .iloc[:, indice]
                        .to_frame()
                    )
                ),
                180,
                550,
                mask="auto",
                width=200,
                height=200,
            )

            can.drawImage(
                ImageReader(
                    curva_IV(
                        pd.concat(
                            [
                                pd.DataFrame.from_dict(
                                    data=s.s["FV"]["superficie"], orient="index"
                                )
                                .iloc[:, indice]
                                .to_frame()
                                .drop("Sombras"),
                                pd.DataFrame.from_dict(
                                    data=s.s["FV"]["__mppt"], orient="index"
                                )
                                .iloc[:, indice]
                                .to_frame(),
                                pd.DataFrame.from_dict(
                                    data=s.s["GEN"]["inversor"], orient="index"
                                )
                                .iloc[:, indice]
                                .to_frame(),
                                pd.DataFrame.from_dict(
                                    data=s.s["GEN"]["panel"], orient="index"
                                )
                                .iloc[:, indice]
                                .to_frame(),
                            ]
                        )
                    )
                ),
                10,
                400,
                mask="auto",
                width=600,
                height=155,
            )
            can.drawImage(
                ImageReader(curva_produccion_array(indice)),
                10,
                10,
                mask="auto",
                width=600,
                height=155,
            )
            can.drawImage(
                ImageReader(
                    curva_sombras(pd.DataFrame(s.s["FV"]["superficie"]).iloc[indice])
                ),
                10,
                222,
                mask="auto",
                width=600,
                height=155,
            )

    def pagina_n(can):
        can.showPage()  ######################   siguiente pagina    ##########################
        can.drawImage(
            ImageReader(
                fqrcode_logo(
                    "https://asolear.es/#contacto?doc=" + os.path.relpath(__file__)
                )
            ),
            544,
            11,
            mask="auto",
            width=44,
            height=44,
        )

    # systema2df()

    pagina_0(can)
    pagina_i(can)
    pagina_n(can)
    # pppppppppppppppppppppppppppp            pagina ultima           ppppppppppppppppppppppppppppppppppppppppppppppppppp

    ###############################################################
    ppdf(os.path.abspath(__file__)[:-3], can, mmpdf, 0)
    ###############################################################
