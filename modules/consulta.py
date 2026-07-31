from modules.datas import obter_periodo_mes_anterior
from modules.captcha import CaptchaSolver


class Consulta:

    def __init__(self, page, empresa, cnpj):

        self.page = page

        self.empresa = str(empresa)

        self.cnpj = str(cnpj)

        # Instância do resolvedor de CAPTCHA
        self.captcha_solver = CaptchaSolver()

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

        # CAPTCHA
        self.imagem_captcha = (
            "#Body_Main_Main_sepConsultaNfpe_ctl17 img"
        )

        self.campo_captcha = (
            "input[name='ctl00$ctl00$ctl00$Body$Main$Main$sepConsultaNfpe$ctl23']"
        )

        self.btn_recarregar_captcha = (
            "#Body_Main_Main_sepConsultaNfpe_ctl23_btn0"
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

    def resolver_e_submeter_com_validacao(self, tentativas_max=20):

        for tentativa in range(1, tentativas_max + 1):

            print(
                f"\n[CAPTCHA] Tentativa {tentativa} de {tentativas_max}..."
            )

            try:

                element_captcha = self.page.locator(
                    self.imagem_captcha
                ).first

                element_captcha.wait_for(
                    state="visible",
                    timeout=7000
                )

                # Pequeno tempo para garantir que a imagem do CAPTCHA estabilizou
                self.page.wait_for_timeout(500)

                image_bytes = element_captcha.screenshot()

                texto_resolvido = self.captcha_solver.resolver_bytes(
                    image_bytes
                )

                print(
                    f"[CAPTCHA] Texto obtido pelo OCR: '{texto_resolvido}'"
                )

                # Aceita códigos com números e letras de tamanho consistente (ex: entre 4 e 9 caracteres)
                if 4 <= len(texto_resolvido) <= 9:

                    self.digitar(
                        self.campo_captcha,
                        texto_resolvido
                    )

                    print(
                        "[CAPTCHA] Preenchido. Clicando em Exportar..."
                    )

                    # Clica no botão exportar
                    botao = self.page.locator(self.botao_exportar)
                    botao.wait_for(state="visible")
                    botao.click()

                    self.page.wait_for_timeout(3500)

                    # VERIFICAÇÃO: Se o campo do captcha ainda estiver visível,
                    # significa que o SAT recusou (código incorreto)
                    captcha_ainda_visivel = self.page.locator(
                        self.campo_captcha
                    ).is_visible()

                    if not captcha_ainda_visivel:

                        print(
                            "✅ [CAPTCHA VALIDADO] Exportação iniciada com sucesso!"
                        )

                        return True

                    print(
                        "❌ [CAPTCHA Incorreto] SAT rejeitou a tentativa. Solicitando nova imagem..."
                    )
                else:

                    print(
                        f"[CAPTCHA] Leitura incompleta ({len(texto_resolvido)} chars). Ignorando envio..."
                    )

            except Exception as err:

                print(
                    f"[CAPTCHA Warning] Erro no ciclo: {err}"
                )

            # Clica no botão de recarregar CAPTCHA para a próxima tentativa
            try:

                btn_refresh = self.page.locator(
                    self.btn_recarregar_captcha
                ).first

                if btn_refresh.is_visible():

                    btn_refresh.click()

                    # Espera a nova imagem carregar no DOM
                    self.page.wait_for_timeout(2000)

            except Exception:

                pass

        raise Exception(
            f"Não foi possível validar o CAPTCHA após {tentativas_max} tentativas."
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

        # Executa as tentativas de validação do relatório
        self.resolver_e_submeter_com_validacao(tentativas_max=20)

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