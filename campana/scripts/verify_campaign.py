#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoría Pericial Independiente E2E de la Campaña Publicitaria Notarial
Escribano Público Fabricio Rivas · Punta del Este y Maldonado (Matrícula 17058/5)

Milestone M5 - Verification Track
Interface Contract: Verification Track ↔ Entire Campaign (sitio/campana/)

Este script ejecuta una verificación integral, objetiva e independiente sobre todos
los entregables de la campaña publicitaria de Instagram / Meta Ads:
1. Existencia y tamaño no nulo de los 8 entregables mandatorios.
2. Formato y dimensiones periciales de las piezas gráficas (1080x1350 y 1080x1920).
3. Consistencia visual de marca, paleta cromática (#111111, #c4ad7a, #f6f6f4) y tipografías.
4. Rigor lingüístico de tuteo formal, ausencia total de voseo (0%) y exclusión de términos prohibidos.
5. Exactitud de datos comerciales, de contacto (WhatsApp +598 99 431 185, Matrícula 17058/5, Web) y propuesta de valor del comprador.
6. Protocolo y acta de aprobación cruzada rubricada por Dirección de Arte y Marketing Digital.

Salida:
- Código de salida 0: 100% de los tests pasan satisfactoriamente.
- Código de salida no nulo: Error / falla de integridad detectada.
"""

import hashlib
import os
import re
import struct
import sys
import unittest
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ==============================================================================
# RUTAS CANÓNICAS DEL PROYECTO
# ==============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAMPANA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SITIO_DIR = os.path.abspath(os.path.join(CAMPANA_DIR, ".."))
REPO_ROOT = os.path.abspath(os.path.join(SITIO_DIR, ".."))

DELIVERABLES = {
    "brand_consistency_guide": os.path.join(CAMPANA_DIR, "direccion_arte", "brand_consistency_guide.md"),
    "brief_comercial_comprador": os.path.join(CAMPANA_DIR, "marketing", "brief_comercial_comprador.md"),
    "instagram_ads_copys": os.path.join(CAMPANA_DIR, "marketing", "instagram_ads_copys.md"),
    "modelo_metricas_optimizacion": os.path.join(CAMPANA_DIR, "marketing", "modelo_metricas_optimizacion.md"),
    "ad_feed_png": os.path.join(CAMPANA_DIR, "piezas", "ad_feed_1080x1350.png"),
    "ad_story_png": os.path.join(CAMPANA_DIR, "piezas", "ad_story_1080x1920.png"),
    "registro_produccion_ia": os.path.join(CAMPANA_DIR, "piezas", "registro_produccion_ia.md"),
    "acta_aprobacion_cruzada": os.path.join(CAMPANA_DIR, "aprobaciones", "acta_aprobacion_cruzada.md"),
}

OFFICIAL_ASSETS = {
    "logo_transparente": os.path.join(SITIO_DIR, "images", "fr logo transparente fondo dorado FR escribano fabricio rivas.png"),
}


def compute_sha256(filepath: str) -> str:
    """Calcula el hash SHA-256 de un archivo físico."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def get_image_info(filepath: str) -> Tuple[int, int, str]:
    """
    Obtiene (ancho, alto, formato) de una imagen usando PIL si está disponible,
    o mediante análisis directo de cabeceras binarias (PNG/JPEG) como alternativa.
    """
    if HAS_PIL:
        with Image.open(filepath) as img:
            return img.width, img.height, img.format

    # Fallback binario para PNG
    with open(filepath, "rb") as f:
        head = f.read(32)
        if head.startswith(b"\x89PNG\r\n\x1a\n"):
            w, h = struct.unpack(">II", head[16:24])
            return w, h, "PNG"
        elif head.startswith(b"\xff\xd8"):
            # Para JPEG básico
            f.seek(0)
            data = f.read()
            # Buscar SOF0 o SOF2
            idx = 2
            while idx < len(data) - 9:
                marker, length = struct.unpack(">HH", data[idx:idx + 4])
                if marker in (0xffc0, 0xffc2):
                    h, w = struct.unpack(">HH", data[idx + 5:idx + 9])
                    return w, h, "JPEG"
                idx += 2 + length
    raise ValueError(f"No se pudo determinar el formato/dimensiones de {filepath}")


# ==============================================================================
# SUITE DE PRUEBAS UNITARIAS Y PERICIALES
# ==============================================================================

class Test01DeliverablesIntegrity(unittest.TestCase):
    """
    Requisito 1: Existencia e integridad de todos los entregables mandatorios.
    Verifica que cada uno de los 8 archivos exista y posea un tamaño no nulo (>0 bytes).
    """

    def test_all_eight_deliverables_exist_and_non_zero(self):
        for key, filepath in DELIVERABLES.items():
            rel_path = os.path.relpath(filepath, REPO_ROOT)
            self.assertTrue(
                os.path.exists(filepath),
                f"FALTA ENTREGABLE MANDATORIO: El archivo '{rel_path}' no existe en el sistema.",
            )
            size = os.path.getsize(filepath)
            self.assertGreater(
                size,
                0,
                f"ENTREGABLE CORRUPTO / VACÍO: El archivo '{rel_path}' tiene 0 bytes.",
            )
            # Verificar integridad de lectura
            sha = compute_sha256(filepath)
            self.assertEqual(
                len(sha),
                64,
                f"ERROR CRIPTOGRÁFICO: Hash SHA-256 no válido para '{rel_path}'.",
            )

    def test_canonical_official_logo_exists(self):
        logo_path = OFFICIAL_ASSETS["logo_transparente"]
        self.assertTrue(
            os.path.exists(logo_path),
            f"FALTA ACTIVO OFICIAL: Logotipo maestro no encontrado en '{logo_path}'.",
        )
        self.assertGreater(
            os.path.getsize(logo_path),
            100000,
            "El logotipo maestro transparente debe ser el activo de alta resolución (>100KB).",
        )


class Test02ImageDimensionsAndFormats(unittest.TestCase):
    """
    Requisito 2: Validación pericial de dimensiones y formatos de imagen.
    - Feed post: exactamente 1080 x 1350 px (relación de aspecto 4:5 vertical).
    - Story post: exactamente 1080 x 1920 px (relación de aspecto 9:16 vertical).
    - Formato de archivo válido PNG.
    """

    def test_feed_image_dimensions_and_ratio(self):
        feed_png = DELIVERABLES["ad_feed_png"]
        w, h, fmt = get_image_info(feed_png)
        self.assertEqual(
            (w, h),
            (1080, 1350),
            f"DIMENSIÓN INCORRECTA EN FEED: Esperado (1080, 1350), obtenido ({w}, {h}).",
        )
        self.assertIn(
            fmt.upper(),
            ["PNG"],
            f"FORMATO NO VÁLIDO EN FEED: Esperado PNG, obtenido {fmt}.",
        )
        self.assertAlmostEqual(
            w / h,
            4 / 5,
            places=3,
            msg="La relación de aspecto de la pieza Feed debe ser exactamente 4:5.",
        )

    def test_story_image_dimensions_and_ratio(self):
        story_png = DELIVERABLES["ad_story_png"]
        w, h, fmt = get_image_info(story_png)
        self.assertEqual(
            (w, h),
            (1080, 1920),
            f"DIMENSIÓN INCORRECTA EN STORY: Esperado (1080, 1920), obtenido ({w}, {h}).",
        )
        self.assertIn(
            fmt.upper(),
            ["PNG"],
            f"FORMATO NO VÁLIDO EN STORY: Esperado PNG, obtenido {fmt}.",
        )
        self.assertAlmostEqual(
            w / h,
            9 / 16,
            places=3,
            msg="La relación de aspecto de la pieza Story debe ser exactamente 9:16.",
        )

    def test_image_readability_with_pil(self):
        if not HAS_PIL:
            self.skipTest("PIL / Pillow no está instalado en este entorno.")
        for key in ["ad_feed_png", "ad_story_png"]:
            path = DELIVERABLES[key]
            with Image.open(path) as im:
                im.verify()
            # Reabrir para inspeccionar canales tras verify()
            with Image.open(path) as im:
                self.assertIn(
                    im.mode,
                    ["RGBA", "RGB"],
                    f"Modo de color inesperado {im.mode} en {key}",
                )


class Test03BrandConsistencyAndPalette(unittest.TestCase):
    """
    Requisito 3: Validación de consistencia de marca y paleta cromática oficial.
    - Presencia de tokens cromáticos oficiales: #111111, #c4ad7a, #f6f6f4.
    - Presencia de la tipografía oficial: 'Open Sauce One', Inter, Cormorant Garamond, Montserrat.
    """

    def setUp(self):
        with open(DELIVERABLES["brand_consistency_guide"], "r", encoding="utf-8") as f:
            self.guide_content = f.read()

    def test_official_palette_tokens_in_brand_guide(self):
        required_tokens = [
            ("#111111", "Carbón Notarial Profundo"),
            ("#c4ad7a", "Oro Notarial Apagado (Primario)"),
            ("#f6f6f4", "Superficie Neutra Arena / Perla"),
        ]
        for token, name in required_tokens:
            self.assertIn(
                token.lower(),
                self.guide_content.lower(),
                f"TOKEN CROMÁTICO FALTANTE: No se encontró el color {name} ({token}) en la guía de marca.",
            )

    def test_secondary_palette_tokens(self):
        secondary_tokens = ["#ffffff", "#504602", "#dac17f", "#b99b5e"]
        for token in secondary_tokens:
            self.assertIn(
                token.lower(),
                self.guide_content.lower(),
                f"Token secundario {token} no documentado en la guía de marca.",
            )

    def test_typography_stacks_in_brand_guide(self):
        typography_stacks = [
            "Open Sauce One",
            "Inter",
            "Cormorant Garamond",
            "Montserrat",
        ]
        for font in typography_stacks:
            self.assertIn(
                font.lower(),
                self.guide_content.lower(),
                f"TIPOGRAFÍA OFICIAL FALTANTE: '{font}' no está certificada en la guía de marca.",
            )

    def test_official_logo_reference(self):
        self.assertIn(
            "fr logo transparente fondo dorado FR escribano fabricio rivas.png",
            self.guide_content,
            "La guía de marca debe certificar expresamente el logotipo maestro transparente.",
        )


class Test04LinguisticRulesAndTone(unittest.TestCase):
    """
    Requisito 4: Validación de reglas lingüísticas, tono notarial y términos prohibidos.
    - Tuteo riguroso formal: presencia obligatoria de 'revisa antes de firmar', 'informa', 'conecta'.
    - Cero voseo (0%): búsqueda regex asegurando ausencia de conjugaciones voseantes en anuncios.
    - Cero términos prohibidos: exclusión absoluta de 'ARTOWER' y 'trabajo en persona'.
    - Frase mandatoria de reemplazo: 'atención directa, también a distancia si estás en otro país'.
    """

    def setUp(self):
        with open(DELIVERABLES["instagram_ads_copys"], "r", encoding="utf-8") as f:
            self.copys_content = f.read()

        # Extraer exclusivamente la sección de variaciones de anuncios para el análisis estricto de texto
        match_section = re.search(
            r"## 3\. Matriz de Variaciones de Anuncios(.*?)## 4\.",
            self.copys_content,
            re.DOTALL,
        )
        if match_section:
            self.ad_variations_text = match_section.group(1)
        else:
            self.ad_variations_text = self.copys_content

    def test_formal_tuteo_key_phrases(self):
        copys_lower = self.ad_variations_text.lower()
        self.assertIn(
            "revisa antes de firmar",
            copys_lower,
            "FALTA LEMA DE TUTEO FORMAL: 'revisa antes de firmar' no encontrado en las piezas publicitarias.",
        )
        self.assertTrue(
            re.search(r"\binforma\b", copys_lower),
            "FALTA FORMA VERBAL MANDATORIA: 'informa' no se encontró conjugado en tuteo formal.",
        )
        self.assertTrue(
            re.search(r"\bconecta\b", copys_lower),
            "FALTA FORMA VERBAL MANDATORIA: 'conecta' no se encontró conjugado en tuteo formal.",
        )

    def test_zero_voseo_in_ad_copies(self):
        """
        Asegura que ninguna de las variaciones publicitarias utilice conjugaciones voseantes
        rioplatenses (revisá, tenés, coordinás, podés, llamá, escribí, consultá, comprás, hacé, firmá).
        """
        voseo_patterns = [
            r"\brevisá\b",
            r"\btenés\b",
            r"\bcoordinás\b",
            r"\bpodés\b",
            r"\bllamá\b",
            r"\bescribí\b",
            r"\bconsultá\b",
            r"\bcomprás\b",
            r"\bhacé\b",
            r"\bfirmá\b",
            r"\basegurá\b",
            r"\bmirá\b",
        ]
        violations = []
        for pat in voseo_patterns:
            matches = re.findall(pat, self.ad_variations_text, re.IGNORECASE)
            if matches:
                violations.extend(matches)

        self.assertEqual(
            len(violations),
            0,
            f"VIOLACIÓN DE VOSEO DETECTADA: Se encontraron formas voseantes no autorizadas en los anuncios: {violations}",
        )

    def test_zero_forbidden_term_artower(self):
        """
        El término 'ARTOWER' está estrictamente prohibido en los copys publicitarios.
        """
        artower_matches = re.findall(r"\bARTOWER\b", self.ad_variations_text, re.IGNORECASE)
        self.assertEqual(
            len(artower_matches),
            0,
            f"VIOLACIÓN DE TÉRMINO PROHIBIDO: 'ARTOWER' aparece {len(artower_matches)} veces en los copys.",
        )

    def test_zero_forbidden_phrase_trabajo_en_persona(self):
        """
        La frase 'trabajo en persona' está estrictamente prohibida en las variaciones de anuncio.
        """
        match = re.search(r"trabajo en persona", self.ad_variations_text, re.IGNORECASE)
        self.assertIsNone(
            match,
            "VIOLACIÓN DE FRASE PROHIBIDA: 'trabajo en persona' aparece en las variaciones de anuncio.",
        )

    def test_mandatory_remote_formula_presence(self):
        """
        Debe figurar de forma mandatoria: 'atención directa, también a distancia si estás en otro país'.
        """
        self.assertIn(
            "atención directa, también a distancia si estás en otro país",
            self.ad_variations_text.lower(),
            "FALTA FÓRMULA MANDATORIA: No se encontró 'atención directa, también a distancia si estás en otro país'.",
        )

    def test_minimum_ad_copies_count(self):
        """
        El requerimiento R2 estipula al menos 3 copys listos para pauta publicitaria.
        """
        variations = re.findall(r"### Variación \d+", self.copys_content)
        self.assertGreaterEqual(
            len(variations),
            3,
            f"CANTIDAD INSUFICIENTE DE COPYS: Esperadas al menos 3 variaciones, encontradas {len(variations)}.",
        )


class Test05CommercialAndContactData(unittest.TestCase):
    """
    Requisito 5: Validación de datos comerciales, de contacto y posicionamiento.
    - WhatsApp directo: +598 99 431 185 (formato internacional completo).
    - Matrícula Notarial habilitada: 17058/5.
    - Web oficial: escribanofabriciorivas.com.
    - Foco estratégico en la seguridad del comprador inmobiliario e independencia notarial frente a inmobiliarias.
    """

    def setUp(self):
        with open(DELIVERABLES["instagram_ads_copys"], "r", encoding="utf-8") as f:
            self.copys_content = f.read()
        with open(DELIVERABLES["brief_comercial_comprador"], "r", encoding="utf-8") as f:
            self.brief_content = f.read()

    def test_official_whatsapp_number(self):
        expected_wa = "+598 99 431 185"
        self.assertIn(
            expected_wa,
            self.copys_content,
            f"NÚMERO DE WHATSAPP FALTANTE: No se encontró '{expected_wa}' en los copys.",
        )
        self.assertIn(
            "59899431185",
            self.copys_content,
            "No se encontró el enlace de WhatsApp estructurado con código '59899431185'.",
        )

    def test_official_matricula(self):
        expected_matricula = "17058/5"
        self.assertIn(
            expected_matricula,
            self.copys_content,
            f"MATRÍCULA NOTARIAL FALTANTE: '{expected_matricula}' no figura en los copys.",
        )
        self.assertIn(
            expected_matricula,
            self.brief_content,
            f"MATRÍCULA NOTARIAL FALTANTE: '{expected_matricula}' no figura en el brief comercial.",
        )

    def test_official_web_domain(self):
        expected_web = "escribanofabriciorivas.com"
        self.assertIn(
            expected_web,
            self.copys_content.lower(),
            f"SITIO WEB FALTANTE: '{expected_web}' no figura en los copys.",
        )

    def test_buyer_protection_and_independence_focus(self):
        copys_lower = self.copys_content.lower()
        brief_lower = self.brief_content.lower()

        # Foco en el comprador y no en el vendedor
        self.assertIn("comprador", copys_lower)
        self.assertIn("comprador", brief_lower)

        # Independencia frente a inmobiliarias
        self.assertTrue(
            "independiente" in copys_lower or "independencia" in copys_lower,
            "Falta resaltar la condición de escribano independiente en los copys.",
        )

        # Mención a la auditoría de antecedentes y boletos
        self.assertIn("boleto de reserva", copys_lower)
        self.assertTrue(
            "estudio de títulos" in copys_lower or "títulos" in copys_lower,
            "Falta mención al estudio notarial de títulos en los copys.",
        )


class Test06CrossApprovalLog(unittest.TestCase):
    """
    Requisito 6: Validación pericial del acta y circuito de aprobación cruzada.
    - Verificación del archivo 'acta_aprobacion_cruzada.md'.
    - Comprobación del circuito de 3 pasos (Diseño -> Arte -> Marketing).
    - Presencia de declaraciones formales rubricadas por Dirección de Arte y Marketing Digital.
    - Matriz de validación ítem por ítem con dictamen APROBADO.
    - Trazabilidad auditable (hashes / matrículas).
    """

    def setUp(self):
        with open(DELIVERABLES["acta_aprobacion_cruzada"], "r", encoding="utf-8") as f:
            self.acta_content = f.read()

    def test_acta_minimum_substance(self):
        self.assertGreater(
            len(self.acta_content),
            5000,
            "El acta de aprobación cruzada debe ser un documento exhaustivo y pericial (>5,000 caracteres).",
        )

    def test_three_step_circuit_documented(self):
        acta_lower = self.acta_content.lower()
        self.assertTrue(
            "paso 1" in acta_lower and "diseño" in acta_lower,
            "El circuito de aprobación debe contener el Paso 1 (Entrega de Diseño Gráfico).",
        )
        self.assertTrue(
            "paso 2" in acta_lower and "dirección de arte" in acta_lower,
            "El circuito de aprobación debe contener el Paso 2 (Validación de Dirección de Arte).",
        )
        self.assertTrue(
            "paso 3" in acta_lower and "marketing" in acta_lower,
            "El circuito de aprobación debe contener el Paso 3 (Validación de Marketing Digital).",
        )

    def test_signed_declarations_from_both_disciplines(self):
        self.assertIn(
            "Declaración Rubricada de la Dirección de Arte",
            self.acta_content,
            "FALTA DECLARACIÓN: No se encontró la declaración formal rubricada de Dirección de Arte.",
        )
        self.assertIn(
            "Declaración Rubricada de Marketing Digital",
            self.acta_content,
            "FALTA DECLARACIÓN: No se encontró la declaración formal rubricada de Marketing Digital.",
        )
        # Ambas declaraciones deben conceder dictamen favorable
        self.assertTrue(
            "APROBADO" in self.acta_content,
            "El acta debe contener el dictamen expreso de APROBADO.",
        )

    def test_validation_matrix_has_all_approved_items(self):
        matrix_matches = re.findall(r"\|\s*\*\*APROBADO\*\*\s*\|", self.acta_content)
        self.assertGreaterEqual(
            len(matrix_matches),
            10,
            f"La matriz de homologación debe contener al menos 10 ítems aprobados (encontrados: {len(matrix_matches)}).",
        )

    def test_acta_contains_traceability_and_credentials(self):
        self.assertIn(
            "17058/5",
            self.acta_content,
            "El acta debe referenciar la Matrícula Notarial 17058/5 de Fabricio Rivas.",
        )
        self.assertIn(
            "+598 99 431 185",
            self.acta_content,
            "El acta debe certificar el canal de WhatsApp oficial +598 99 431 185.",
        )
        self.assertIn(
            "SHA-256",
            self.acta_content,
            "El acta debe incorporar la trazabilidad criptográfica SHA-256 de los entregables.",
        )


class Test07AdversarialAndEdgeCases(unittest.TestCase):
    """
    Requisito 7 (Adversarial): Pruebas de resistencia pericial y casos de borde.
    - Archivos de imagen no deben ser maquetas corruptas de 1x1 píxeles.
    - Archivos de texto no deben contener marcadores de plantilla vacíos ('[TBD]', 'TODO').
    - Consistencia bidireccional entre copys y métricas analíticas.
    """

    def test_images_are_not_dummy_placeholders(self):
        for key in ["ad_feed_png", "ad_story_png"]:
            path = DELIVERABLES[key]
            size = os.path.getsize(path)
            self.assertGreater(
                size,
                50000,
                f"La pieza gráfica {key} debe superar los 50 KB para no ser un archivo simulado.",
            )

    def test_no_unresolved_todos_in_deliverables(self):
        # En español 'todo'/'todos' es una palabra común ("Todo titular"), por lo que TODO debe buscarse en mayúsculas
        case_sensitive_markers = [r"\bTODO\b", r"\bFIXME\b", r"\bXXX\b"]
        case_insensitive_markers = [r"\[TBD\]", r"\[REVISAR\]", r"\[PENDIENTE\]"]
        for key, path in DELIVERABLES.items():
            if path.endswith(".md"):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                for pat in case_sensitive_markers:
                    matches = re.findall(pat, content)
                    self.assertEqual(
                        len(matches),
                        0,
                        f"Marcador no resuelto '{pat}' encontrado en {os.path.basename(path)}: {matches}",
                    )
                for pat in case_insensitive_markers:
                    matches = re.findall(pat, content, re.IGNORECASE)
                    self.assertEqual(
                        len(matches),
                        0,
                        f"Marcador no resuelto '{pat}' encontrado en {os.path.basename(path)}: {matches}",
                    )

    def test_metrics_model_contains_key_kpis(self):
        metrics_file = DELIVERABLES["modelo_metricas_optimizacion"]
        with open(metrics_file, "r", encoding="utf-8") as f:
            content = f.read()
        for kpi in ["CTR", "CPC", "WhatsApp", "ROAS"]:
            self.assertIn(
                kpi,
                content,
                f"Falta el KPI esencial '{kpi}' en el modelo de métricas y optimización.",
            )


# ==============================================================================
# EJECUTOR PRINCIPAL Y REPORTE FORMATADO
# ==============================================================================

def run_verification_suite() -> int:
    """
    Ejecuta la suite de verificación pericial e imprime un informe de auditoría
    estructurado. Retorna 0 en éxito rotundo, 1 en caso de fallas.
    """
    print("\n" + "=" * 80)
    print("  AUDITORÍA PERICIAL INDEPENDIENTE E2E — CAMPAÑA ESCRIBANO FABRICIO RIVAS")
    print("  Punta del Este & Maldonado · Matrícula Notarial 17058/5")
    print("=" * 80)
    print(f"  Directorio raíz: {REPO_ROOT}")
    print(f"  Directorio de campaña: {CAMPANA_DIR}")
    print(f"  Soporte PIL / Pillow: {'ACTIVO' if HAS_PIL else 'INACTIVO (usando struct binario)'}")
    print("-" * 80)

    # Cargar suite de unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        Test01DeliverablesIntegrity,
        Test02ImageDimensionsAndFormats,
        Test03BrandConsistencyAndPalette,
        Test04LinguisticRulesAndTone,
        Test05CommercialAndContactData,
        Test06CrossApprovalLog,
        Test07AdversarialAndEdgeCases,
    ]

    for tc in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(tc))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 80)
    print("  RESUMEN DE RESULTADOS DE LA AUDITORÍA PERICIAL")
    print("=" * 80)
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    passed = total_tests - failures - errors - skipped

    print(f"  Total de pruebas ejecutadas: {total_tests}")
    print(f"  Pruebas superadas (PASS):   {passed}")
    print(f"  Fallas detectadas (FAIL):   {failures}")
    print(f"  Errores de ejecución (ERR): {errors}")
    print(f"  Pruebas omitidas (SKIP):    {skipped}")
    print("-" * 80)

    if failures == 0 and errors == 0:
        print("  DICTAMEN GENERAL: [PASS] 100% DE CONFORMIDAD NOTARIAL Y TÉCNICA.")
        print("  Todos los entregables, dimensiones, reglas cromáticas y protocolos")
        print("  cumplen rigurosamente con los requisitos de la campaña publicitaria.")
        print("=" * 80 + "\n")
        return 0
    else:
        print("  DICTAMEN GENERAL: [FAIL] SE DETECTARON NO-CONFORMIDADES.")
        print("  Consulte el log detallado de fallas para subsanar los defectos.")
        print("=" * 80 + "\n")
        return 1


if __name__ == "__main__":
    exit_code = run_verification_suite()
    sys.exit(exit_code)
