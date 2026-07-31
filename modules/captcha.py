import io
import re
import cv2
import easyocr
import numpy as np
from PIL import Image


class CaptchaSolver:

    def __init__(self):
        print("[EasyOCR] Carregando modelo de Inteligência Artificial...")
        self.reader = easyocr.Reader(['en'], gpu=False)

    # ---------------------------------------------------------

    def resolver_bytes(self, image_bytes: bytes) -> str:

        if not image_bytes:
            return ""

        try:
            # 1. Carrega a imagem enviada pelo Playwright
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img_np = np.array(image)

            # 2. Apenas aumenta a imagem (Zoom 2.5x) para dar mais definição sem alterar cores/fundo
            altura, largura = img_np.shape[:2]
            img_ampliada = cv2.resize(
                img_np,
                (int(largura * 2.5), int(altura * 2.5)),
                interpolation=cv2.INTER_CUBIC
            )

            # 3. Leitura direta pelo EasyOCR com parâmetros ajustados
            resultados = self.reader.readtext(
                img_ampliada,
                detail=0,
                allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                text_threshold=0.3, # Reduz a exigência para detectar caracteres finos
                low_text=0.2       # Ajuda a capturar traços fracos de números
            )

            if not resultados:
                return ""

            texto_bruto = "".join(resultados)

            # Limpa espaços e caracteres indesejados
            texto_limpo = re.sub(r'[^A-Z0-9]', '', texto_bruto.upper())

            return texto_limpo

        except Exception as e:
            print(f"[CAPTCHA Error] Falha ao processar com EasyOCR: {e}")
            return ""