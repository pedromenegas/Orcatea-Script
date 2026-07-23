from pathlib import Path


class Download:

    def __init__(self, page, empresa, cnpj, tipo, competencia, nome_empresa=""):

        self.page = page

        self.empresa = str(empresa)

        self.cnpj = str(cnpj)

        self.tipo = tipo

        self.nome_empresa = str(nome_empresa).strip()
        
        if self.nome_empresa and self.nome_empresa.lower() != "nan":
            nome_pasta = f"{self.empresa} - {self.nome_empresa}"
        else:
            nome_pasta = self.empresa

        self.pasta_destino = (
            Path(r"Z:\SAT\downloads")
            / nome_pasta
            / competencia
        )

    # -----------------------------------------------------

    def localizar_solicitacao(self, timeout=300):

        print("\nLocalizando solicitação...")

        tempo = 0

        while tempo < timeout:

            linhas = self.page.locator(
                "#Body_Main_ctl00_grpSolicitacoes_gridView tbody tr"
            )

            quantidade = linhas.count()

            for i in range(quantidade):

                linha = linhas.nth(i)

                texto = linha.inner_text()

                if self.cnpj not in texto:

                    continue

                if self.tipo == "NF-e":

                    if "NF-es" not in texto:

                        continue

                if self.tipo == "NFC-e":

                    if "NFC-es" not in texto:

                        continue

                print(
                    "Solicitação encontrada."
                )

                return linha

            self.page.wait_for_timeout(
                1000
            )

            tempo += 1

        return None

    # -----------------------------------------------------

    def aguardar_download_disponivel(self, linha, timeout=300):

        print(
            "\nVerificando disponibilidade do download..."
        )

        tempo = 0

        while tempo < timeout:

            botao_download = linha.locator(
                "a[title='Baixar o arquivo resultante']"
            )

            if botao_download.count() > 0:

                print(
                    "Botão de download encontrado."
                )

                return botao_download

            botao_processamento = linha.locator(
                "a[title='Acompanhar o processamento']"
            )

            if botao_processamento.count() > 0:

                print(
                    "Ainda processando..."
                )

                botao_processamento.click()

                self.page.wait_for_timeout(
                    5000
                )

            self.page.reload()

            self.page.wait_for_timeout(
                2000
            )

            nova_linha = self.localizar_solicitacao(
                timeout=5
            )

            if nova_linha:

                linha = nova_linha

            tempo += 5

        return None

    # -----------------------------------------------------

    def salvar_arquivo(self, download):

        self.pasta_destino.mkdir(
            parents=True,
            exist_ok=True
        )

        if self.tipo == "NF-e":

            nome = "NFE.xlsx"

        else:

            nome = "NFCE.xlsx"

        destino = (
            self.pasta_destino
            /
            nome
        )

        if destino.exists():

            destino.unlink()

        download.save_as(
            destino
        )

        print(
            f"Arquivo salvo em: {destino}"
        )

    # -----------------------------------------------------

    def baixar(self, botao):

        print(
            "\nIniciando download..."
        )

        with self.page.expect_download() as download_info:

            botao.click()

        download = download_info.value

        self.salvar_arquivo(
            download
        )

    # -----------------------------------------------------

    def executar(self):

        # ==========================================
        # NFC-e opcional
        # ==========================================

        if self.tipo == "NFC-e":

            linha = self.localizar_solicitacao(
                timeout=3
            )

            if linha is None:

                print(
                    "NFC-e não encontrada. Pulando."
                )

                return

        # ==========================================
        # NF-e obrigatória
        # ==========================================

        else:

            linha = self.localizar_solicitacao(
                timeout=300
            )

            if linha is None:

                raise Exception(
                    "NF-e não encontrada."
                )

        botao = self.aguardar_download_disponivel(
            linha
        )

        if botao is None:

            if self.tipo == "NFC-e":

                print(
                    "NFC-e não ficou disponível. Pulando."
                )

                return

            raise Exception(
                "NF-e não ficou disponível para download."
            )

        self.baixar(
            botao
        )

        print(
            "\nDownload concluído."
        )