import json
from pathlib import Path


class Login:

    def __init__(self, page):

        self.page = page

        base_dir = Path(__file__).resolve().parent.parent

        with open(base_dir / "config.json", "r", encoding="utf-8") as arquivo:
            self.config = json.load(arquivo)

    # ---------------------------------------------------------

    def executar(self):

        print("Abrindo portal...")

        self.page.goto(
            self.config["portal"]["url"],
            wait_until="domcontentloaded"
        )

        print("Preenchendo login...")

        usuario = self.page.locator("input[type='text']").first

        usuario.wait_for(state="visible")

        usuario.fill(
            self.config["login"]["usuario"]
        )

        senha = self.page.locator("input[type='password']").first

        senha.wait_for(state="visible")

        senha.fill(
            self.config["login"]["senha"]
        )

        print("Entrando...")

        clicou = False

        seletores = [
            "input[type='submit']",
            "button[type='submit']",
            "button:has-text('Entrar')",
            "input[value='Entrar']",
            "text=Entrar"
        ]

        for seletor in seletores:

            try:

                botao = self.page.locator(seletor).first

                botao.wait_for(state="visible", timeout=2000)

                botao.click()

                clicou = True

                break

            except Exception:
                pass

        if not clicou:

            raise Exception("Não foi possível localizar o botão Entrar.")

        print("Aguardando tela inicial...")

        self.page.wait_for_load_state("domcontentloaded")

        aplicativo = self.page.locator(
            "#Body_Main_ctl11_ctl07_rptAppList_ctl03_0"
        )

        aplicativo.wait_for(timeout=15000)

        print("Abrindo NFe / NFCe - Consulta...")

        with self.page.context.expect_page(timeout=15000) as nova_pagina:

            aplicativo.click(force=True)

        self.page = nova_pagina.value

        self.page.wait_for_load_state("domcontentloaded")

        print("URL aberta:")
        print(self.page.url)

        # ---------------------------------------------------------
        # Aguarda a validação manual do CAPTCHA
        # (executado apenas na primeira abertura da tela)
        # ---------------------------------------------------------

        print("\nAguardando 10 segundos para validação do CAPTCHA...")

        self.page.wait_for_timeout(10000)

        print("Tela de consulta aberta.")

        return self.page