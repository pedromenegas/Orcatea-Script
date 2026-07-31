from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import sys


class Navegador:

    def __init__(self):

        if getattr(sys, "frozen", False):
            # Executando como .exe
            self.base_dir = Path(sys.executable).parent
        else:
            # Executando pelo Python
            self.base_dir = Path(__file__).resolve().parent.parent

        with open(self.base_dir / "config.json", "r", encoding="utf-8") as arquivo:
            self.config = json.load(arquivo)

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def iniciar(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.connect_over_cdp(
            "http://127.0.0.1:9222"
        )

        if not self.browser.contexts:
            raise Exception(
                "Nenhum contexto encontrado. Verifique se o Chrome foi iniciado com --remote-debugging-port=9222."
            )

        self.context = self.browser.contexts[0]

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

        self.page.set_default_timeout(
            self.config["navegador"]["timeout"]
        )

        return self.page

    def fechar(self):

        if self.playwright:
            self.playwright.stop()