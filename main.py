from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path

from modules.navegador import Navegador
from modules.login import Login
from modules.empresas import Empresas
from modules.consulta import Consulta
from modules.exportacao import Exportacao
from modules.download import Download
from modules.relatorio import Relatorio


def main():

    navegador = Navegador()

    page = None

    relatorio = Relatorio()

    try:

        print("=" * 60)
        print("SAT RPA")
        print("=" * 60)

        # -------------------------------------------------
        # Conecta ao Chrome
        # -------------------------------------------------

        page = navegador.iniciar()

        # -------------------------------------------------
        # Login
        # -------------------------------------------------

        print("\nRealizando login...")

        page = Login(page).executar()

        # -------------------------------------------------
        # Empresas
        # -------------------------------------------------

        empresas = Empresas().listar()

        print(
            f"\nEmpresas encontradas: {len(empresas)}"
        )

        # -------------------------------------------------
        # Processamento
        # -------------------------------------------------

        for empresa in empresas:

            numero_empresa = empresa["empresa"]

            nome_empresa = empresa.get("nome", "")

            cnpj = empresa["cnpj"]

            nfe_status = "ERRO"
            nfce_status = "Não executado"
            status_final = "Revisar"
            observacao = ""

            print("\n" + "=" * 60)
            print(f"Empresa: {numero_empresa} - {nome_empresa}")
            print(f"CNPJ    : {cnpj}")
            print("=" * 60)

            consulta = Consulta(
                page,
                numero_empresa,
                cnpj
            )

            # ==========================================
            # NF-e
            # ==========================================

            try:

                print("\nExportando NF-e...")

                # Competência = mês anterior
                competencia = (
                    datetime.today().replace(day=1)
                    - relativedelta(months=1)
                ).strftime("%Y-%m")

                if nome_empresa and nome_empresa.lower() != "nan":
                    nome_pasta = f"{numero_empresa} - {nome_empresa}"
                else:
                    nome_pasta = str(numero_empresa)

                pasta_competencia = (
                    Path(r"Z:\SAT\downloads")
                    / nome_pasta
                    / competencia
                )

                # Se já existe o arquivo OK, pula a empresa
                if (pasta_competencia / "OK").exists():

                    print(
                        f"\nEmpresa {numero_empresa} já possui OK para {competencia}. Pulando..."
                    )

                    continue

                consulta.consultar_tipo(
                    "NF-e"
                )

                Exportacao(page).abrir()

                Download(
                    page,
                    numero_empresa,
                    cnpj,
                    "NF-e",
                    competencia,
                    nome_empresa
                ).executar()

                nfe_status = "OK"

                print(
                    "\nNF-e concluída."
                )

            except Exception as erro:

                observacao = f"Erro NF-e: {erro}"

                print(
                    observacao
                )

                relatorio.adicionar(
                    numero_empresa,
                    nome_empresa,
                    cnpj,
                    nfe_status,
                    nfce_status,
                    status_final,
                    observacao
                )

                continue
        
            # -------------------------------------------------
            # Volta para consulta
            # -------------------------------------------------

            consulta.abrir_consulta()

            page.wait_for_timeout(
                2000
            )

            # ==========================================
            # NFC-e
            # ==========================================

            try:

                print("\nExportando NFC-e...")

                consulta.consultar_tipo(
                    "NFC-e"
                )

                Exportacao(page).abrir()

                Download(
                    page,
                    numero_empresa,
                    cnpj,
                    "NFC-e",
                    competencia,
                    nome_empresa
                ).executar()

                nfce_status = "OK"

                print(
                    "\nNFC-e concluída."
                )

            except Exception as erro:

                nfce_status = "Sem NFC-e"

                print(
                    f"\nNFC-e não disponível: {erro}"
                )

            # -------------------------------------------------
            # Empresa concluída
            # -------------------------------------------------

            status_final = "Concluído"

            pasta_competencia.mkdir(
                parents=True,
                exist_ok=True
            )

            (pasta_competencia / "OK").touch()

            # -------------------------------------------------
            # Salva relatório
            # -------------------------------------------------

            relatorio.adicionar(
                numero_empresa,
                nome_empresa,
                cnpj,
                nfe_status,
                nfce_status,
                status_final,
                observacao
            )

            # -------------------------------------------------
            # Volta para próxima empresa
            # -------------------------------------------------

            consulta.abrir_consulta()

            page.wait_for_timeout(
                2000
            )

        print(
            "\nTodas as empresas foram processadas."
        )

    except Exception as erro:

        print(
            "\nERRO ENCONTRADO"
        )

        print(
            erro
        )

        if page:

            try:

                page.screenshot(
                    path="screenshots/erro.png",
                    full_page=True
                )

                print(
                    "\nScreenshot salva em screenshots/erro.png"
                )

            except Exception:

                pass

    finally:

        relatorio.salvar()

        input(
            "\nPressione ENTER para encerrar..."
        )

        navegador.fechar()


if __name__ == "__main__":

    main()