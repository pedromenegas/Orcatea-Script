from pathlib import Path
from datetime import datetime

import pandas as pd


class Relatorio:

    def __init__(self):

        self.registros = []

        self.pasta = Path(
            r"Z:\SAT\relatorios"
        )


    # -----------------------------------------------------

    def adicionar(
        self,
        empresa,
        cnpj,
        nfe,
        nfce,
        status,
        observacao=""
    ):


        self.registros.append(
            {
                "Empresa": str(empresa),
                "CNPJ": str(cnpj),
                "NF-e": nfe,
                "NFC-e": nfce,
                "Status": status,
                "Observação": observacao,
                "Data/Hora": datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
            }
        )


    # -----------------------------------------------------

    def salvar(self):


        if not self.registros:

            print(
                "Nenhum registro para salvar."
            )

            return



        self.pasta.mkdir(
            parents=True,
            exist_ok=True
        )


        arquivo = (
            self.pasta
            /
            f"relatorio_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
        )


        df = pd.DataFrame(
            self.registros
        )


        df.to_excel(
            arquivo,
            index=False
        )


        print(
            "\nRelatório salvo em:"
        )

        print(
            arquivo
        )