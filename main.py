from datetime import datetime

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

            cnpj = empresa["cnpj"]

            nfe_status = "ERRO"

            nfce_status = "Não executado"

            status_final = "Revisar"

            observacao = ""

            print("\n" + "=" * 60)
            print(f"Empresa: {numero_empresa}")
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

                consulta.consultar_tipo(
                    "NF-e"
                )

                competencia = datetime.strptime(
                    consulta.data_inicio,
                    "%d/%m/%Y"
                ).strftime("%Y-%m")

                Exportacao(page).abrir()

                Download(
                    page,
                    numero_empresa,
                    cnpj,
                    "NF-e",
                    competencia
                ).executar()

                nfe_status = "OK"

                print(
                    "\nNF-e concluída."
                )

            except Exception as erro:

                observacao = (
                    f"Erro NF-e: {erro}"
                )

                print(
                    observacao
                )

                relatorio.adicionar(
                    numero_empresa,
                    cnpj,
                    nfe_status,
                    nfce_status,
                    status_final,
                    observacao
                )

                continue

            # Volta para consulta

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
                    competencia
                ).executar()

                nfce_status = "OK"

                status_final = "Concluído"

                print(
                    "\nNFC-e concluída."
                )

            except Exception as erro:

                nfce_status = "Sem NFC-e"

                status_final = "Concluído"

                observacao = str(
                    erro
                )

                print(
                    f"NFC-e não disponível: {erro}"
                )

            # Salva resultado da empresa

            relatorio.adicionar(
                numero_empresa,
                cnpj,
                nfe_status,
                nfce_status,
                status_final,
                observacao
            )

            # Volta para próxima empresa

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

        # Salva relatório mesmo com erro

        relatorio.salvar()

        input(
            "\nPressione ENTER para encerrar..."
        )

        navegador.fechar()


if __name__ == "__main__":

    main()