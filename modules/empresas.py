from pathlib import Path

import pandas as pd


class Empresas:

    def __init__(self, arquivo="empresas.xlsx"):

        self.arquivo = Path(arquivo)

    # ---------------------------------------------------------

    def listar(self):

        if not self.arquivo.exists():

            raise FileNotFoundError(
                f"Arquivo não encontrado: {self.arquivo}"
            )


        # Lê tudo como texto para não alterar CNPJ
        df = pd.read_excel(
            self.arquivo,
            dtype=str
        )


        colunas = [
            str(c).strip().lower()
            for c in df.columns
        ]


        if "empresa" not in colunas:

            raise Exception(
                "A coluna 'Empresa' não foi encontrada."
            )


        if "cnpj" not in colunas:

            raise Exception(
                "A coluna 'CNPJ' não foi encontrada."
            )


        coluna_empresa = df.columns[
            colunas.index("empresa")
        ]


        coluna_cnpj = df.columns[
            colunas.index("cnpj")
        ]


        empresas = []


        for _, linha in df.iterrows():


            empresa = str(
                linha[coluna_empresa]
            ).strip()


            cnpj = str(
                linha[coluna_cnpj]
            ).strip()


            # Remove máscara do CNPJ

            cnpj = (
                cnpj
                .replace(".", "")
                .replace("/", "")
                .replace("-", "")
                .replace(" ", "")
            )


            # Corrige valores vazios

            if empresa == "" or empresa.lower() == "nan":

                continue


            if cnpj == "" or cnpj.lower() == "nan":

                continue


            empresas.append(
                {
                    "empresa": empresa,
                    "cnpj": cnpj
                }
            )


        return empresas

    # ---------------------------------------------------------

    def quantidade(self):

        return len(
            self.listar()
        )