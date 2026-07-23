from modules.datas import obter_periodo_mes_anterior


class Consulta:

    def __init__(self, page, empresa, cnpj):

        self.page = page

        self.empresa = str(empresa)

        self.cnpj = str(cnpj)

        # Guarda o período utilizado na exportação
        self.data_inicio = None
        self.data_fim = None

        # URL da consulta
        self.url_consulta = (
            "https://sat.sef.sc.gov.br/"
            "tax.NET/Sat.NFe.Web/Consultas/ConsultaOnlineCC.aspx"
        )

        # Tipo documento (Select2)
        self.tipo_documento = (
            "#s2id_Body_Main_Main_sepConsultaNfpe_selTipoDocumento"
        )

        # Emitente
        self.campo_cnpj = (
            "#Body_Main_Main_sepConsultaNfpe_ctl10_idnEmitente_MaskedField"
        )

        # Datas
        self.data_inicial = (
            "#Body_Main_Main_sepConsultaNfpe_datDataInicial"
        )

        self.data_final = (
            "#Body_Main_Main_sepConsultaNfpe_datDataFinal"
        )

        # Botão Exportar
        self.botao_exportar = (
            "#Body_Main_Main_sepConsultaNfpe_btnExportar"
        )

    # ---------------------------------------------------------

    def abrir_consulta(self):

        print("\nVoltando para tela de consulta...")

        self.page.goto(
            self.url_consulta,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print(
            "Aguardando estabilização da tela..."
        )

        self.page.wait_for_timeout(
            2000
        )

        print(
            "Tela de consulta aberta novamente."
        )

    # ---------------------------------------------------------

    def selecionar_tipo(self, tipo):

        print(f"\nSelecionando {tipo}...")

        self.page.locator(
            self.tipo_documento
        ).click()

        self.page.wait_for_timeout(
            500
        )

        opcao = self.page.locator(
            ".select2-result-label",
            has_text=tipo
        ).first

        opcao.wait_for(
            state="visible"
        )

        opcao.click()

        self.page.wait_for_timeout(
            1000
        )

    # ---------------------------------------------------------

    def digitar(self, seletor, valor):

        campo = self.page.locator(
            seletor
        )

        campo.wait_for(
            state="visible"
        )

        campo.click()

        campo.press(
            "Control+A"
        )

        campo.press(
            "Delete"
        )

        campo.fill(
            str(valor)
        )

        campo.press(
            "Tab"
        )

        self.page.wait_for_timeout(
            300
        )

    # ---------------------------------------------------------

    def preencher_cnpj(self):

        print(
            f"Empresa: {self.empresa}"
        )

        print(
            f"CNPJ: {self.cnpj}"
        )

        self.digitar(
            self.campo_cnpj,
            self.cnpj
        )

    # ---------------------------------------------------------

    def preencher_datas(self):

        print(
            "Preenchendo datas..."
        )

        data_inicio, data_fim = obter_periodo_mes_anterior()

        # Guarda a competência utilizada
        self.data_inicio = data_inicio
        self.data_fim = data_fim

        self.digitar(
            self.data_inicial,
            data_inicio
        )

        self.digitar(
            self.data_final,
            data_fim
        )

    # ---------------------------------------------------------

    def exportar(self):

        print(
            "Exportando..."
        )

        botao = self.page.locator(
            self.botao_exportar
        )

        botao.wait_for(
            state="visible"
        )

        botao.click()

        print(
            "Solicitação enviada."
        )

        self.page.wait_for_timeout(
            3000
        )

    # ---------------------------------------------------------

    def consultar_tipo(self, tipo):

        print("\n===================================")

        print(
            f"Empresa : {self.empresa}"
        )

        print(
            f"CNPJ    : {self.cnpj}"
        )

        print(
            f"Tipo    : {tipo}"
        )

        print(
            "==================================="
        )

        self.selecionar_tipo(
            tipo
        )

        self.preencher_cnpj()

        self.preencher_datas()

        self.exportar()

    # ---------------------------------------------------------

    def executar(self):

        self.consultar_tipo(
            "NF-e"
        )

        self.abrir_consulta()

        self.consultar_tipo(
            "NFC-e"
        )

        print(
            "\nConsultas concluídas."
        )