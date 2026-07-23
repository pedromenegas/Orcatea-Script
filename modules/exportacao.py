class Exportacao:

    def __init__(self, page):

        self.page = page

        self.url = (
            "https://sat.sef.sc.gov.br/tax.NET/"
            "Sat.Compartilhado.GerenciadorDeExportacao.Web/"
            "ManutencaoDeSolicitacoesDeExportacao.aspx"
        )

        self.tabela = (
            "#Body_Main_ctl00_grpSolicitacoes_gridView"
        )

    # ---------------------------------------------------------

    def abrir(self):

        print(
            "\nAbrindo Manutenção das Solicitações de Exportação..."
        )

        self.page.goto(
            self.url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print(
            "Aguardando carregamento da tabela..."
        )

        self.page.wait_for_timeout(
            2000
        )

        self.page.locator(
            self.tabela
        ).wait_for(
            state="visible",
            timeout=15000
        )

        print(
            "Tela de solicitações aberta."
        )