from pathlib import Path
import sys

import pandas as pd


class Empresas:

    def __init__(self, arquivo="empresas.xlsx"):

        candidatos = []

        # Primeiro tenta a pasta do projeto/.exe
        if getattr(sys, "frozen", False):
            candidatos.append(Path(sys.executable).parent / arquivo)
        else:
            candidatos.append(Path(__file__).resolve().parent.parent / arquivo)

        # Depois tenta as unidades de rede
        candidatos.extend([
            Path(r"Z:\sat\SAT_RPA") / arquivo,
            Path(r"D:\sat\SAT_RPA") / arquivo,
        ])

        for caminho in candidatos:
            if caminho.exists():
                self.arquivo = caminho
                break
        else:
            raise FileNotFoundError(
                "Arquivo não encontrado:\n"
                + "\n".join(str(c) for c in candidatos)
            )

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

        if "nome" not in colunas:

            raise Exception(
                "A coluna 'Nome' não foi encontrada."
            )

        coluna_empresa = df.columns[
            colunas.index("empresa")
        ]

        coluna_cnpj = df.columns[
            colunas.index("cnpj")
        ]

        coluna_nome = df.columns[
            colunas.index("nome")
        ]

        empresas = []

        for _, linha in df.iterrows():

            empresa = str(
                linha[coluna_empresa]
            ).strip()

            cnpj = str(
                linha[coluna_cnpj]
            ).strip()

            nome = str(
                linha[coluna_nome]
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
                    "cnpj": cnpj,
                    "nome": nome
                }
            )

        return empresas

    # ---------------------------------------------------------

    def quantidade(self):

        return len(
            self.listar()
        )