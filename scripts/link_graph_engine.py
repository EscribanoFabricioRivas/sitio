#!/usr/bin/env python3
"""
Motor Determinístico e Idempotente de Enlazado Interno Editorial (3 Capas)
Escribano Público Fabricio Rivas (escribanofabriciorivas.com)
- Capa 1: Mención Editorial In-Text (<a class="fr-ctx-link">) — sin subrayado invasivo, con micro-indicador ↗
          Máximo 1 enlace por destino por página, solo en <p> del cuerpo, jamás auto-enlazado.
- Capa 2: Cápsula de Conexión Contextual (<div class="fr-ctx-capsule">) — conecta etapas consecutivas de un trámite.
- Capa 3: Rastro de Cluster Semántico (<section class="fr-cluster-trail">) — 3 guías/landings hermanas al pie de <main>.
"""
import os
import re
import glob

BASE_DIR = "/Users/arianawajntraub/Documents/antigravity/elegant-bardeen/sitio"
WORKTREE_DIR = "/Users/arianawajntraub/.gemini/antigravity/worktrees/elegant-bardeen/teamwork_preview_workflow_automation/sitio"

UTILITY_EXEMPT = {
    "contacto.html",
    "privacidad.html",
}

# Normalización de URL canónica interna por archivo relativo
def rel_to_url(rel: str) -> str:
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    if rel.endswith(".html"):
        return "/" + rel[:-len(".html")]
    return "/" + rel


# Diccionario de Entidades Semánticas (Español, Inglés y Portugués)
# Ordenado de frases más específicas a más generales para evitar colisiones
SEMANTIC_ENTITIES_ES = [
    (r"\bcertificaci(?:ón|ones) de firmas?\b", "/certificar-firma-punta-del-este"),
    (r"\bcertificar (?:una )?firma\b", "/certificar-firma-punta-del-este"),
    (r"\bfirma(?:s)? certificada(?:s)?\b", "/certificar-firma-punta-del-este"),
    (r"\bcertificaciones notariales\b", "/certificaciones-notariales-1/"),
    (r"\bcertificaci(?:ón|ones) notarial(?:es)?\b", "/certificaciones-notariales-1/"),
    (r"\bcertificaci(?:ón|ones) en el d(?:í|&#237;)a\b", "/certificacion-firma-en-el-dia-punta-del-este-1/"),
    (r"\bcertificaci(?:ón|ones) bancaria(?:s)?\b", "/certificacion-firma-banco-maldonado-1/"),
    (r"\bbancos? y entidades financieras\b", "/certificacion-firma-banco-maldonado-1/"),
    (r"\bcertificados? para BPS y DGI\b", "/certificados-bps-dgi"),
    (r"\bBPS y DGI\b", "/certificados-bps-dgi"),
    (r"\bhabilitaci(?:ón|ones) ante INAC\b", "/escribano-inac-maldonado-1/"),
    (r"\bINAC\b", "/escribano-inac-maldonado-1/"),
    (r"\bboleto de reserva\b", "/boleto-reserva-punta-del-este-1/"),
    (r"\bBoleto de reserva\b", "/boleto-reserva-punta-del-este-1/"),
    (r"\breserva(?:s)? de compraventa\b", "/boleto-reserva-punta-del-este-1/"),
    (r"\bboleto(?:s)? o reserva(?:s)?\b", "/boleto-reserva-punta-del-este-1/"),
    (r"\breserva, borrador\b", "/boleto-reserva-punta-del-este-1/"),
    (r"\bpromesas? de compraventa\b", "/promesa-compraventa-punta-del-este-1/"),
    (r"\bpromesa(?:s)? o compraventa(?:s)?\b", "/promesa-compraventa-punta-del-este-1/"),
    (r"\by promesa\b", "/promesa-compraventa-punta-del-este-1/"),
    (r"\bcompraventa(?:s)? de inmuebles\b", "/compraventa-inmuebles-punta-del-este-1/"),
    (r"\bcompraventa(?:s)? inmobiliaria(?:s)?\b", "/compraventa-inmuebles-punta-del-este-1/"),
    (r"\bescritura(?:s)? de compraventa\b", "/compraventa-inmuebles-punta-del-este-1/"),
    (r"\bavanzar con una compraventa\b", "/compraventa-inmuebles-punta-del-este-1/"),
    (r"\boperaciones inmobiliarias\b", "/real-estate"),
    (r"\bdecisiones inmobiliarias\b", "/real-estate"),
    (r"\binversi(?:ón|ones) inmobiliaria(?:s)?\b", "/real-estate"),
    (r"\bdocumentaci(?:ón|&#243;n) para vender\b", "/documentacion-vender-propiedad-punta-del-este-1/"),
    (r"\bvender una propiedad\b", "/documentacion-vender-propiedad-punta-del-este-1/"),
    (r"\bt(?:í|&#237;)tulos y antecedentes\b", "/comprar-en-punta-del-este-seguridad-juridica/"),
    (r"\bSituaci(?:ón|&#243;n) registral\b", "/comprar-en-punta-del-este-seguridad-juridica/"),
    (r"\binformaci(?:ón|&#243;n) registral y catastral\b", "/comprar-en-punta-del-este-seguridad-juridica/"),
    (r"\bpropiedad horizontal\b", "/compraventa-inmuebles-punta-del-este-1/"),
    (r"\bestudio de t(?:í|&#237;)tulos\b", "/comprar-en-punta-del-este-seguridad-juridica/"),
    (r"\bantecedentes dominiales\b", "/comprar-en-punta-del-este-seguridad-juridica/"),
    (r"\bseguridad jur(?:í|&#237;)dica\b", "/comprar-en-punta-del-este-seguridad-juridica/"),
    (r"\bpoder(?:es)? desde el exterior\b", "/poderes-desde-el-exterior"),
    (r"\bpoder(?:es)? especial(?:es)?\b", "/poderes-desde-el-exterior"),
    (r"\bpoder(?:es)? notarial(?:es)?\b", "/poderes-desde-el-exterior"),
    (r"\bmediante representaci(?:ón|&#243;n)\b", "/poderes-desde-el-exterior"),
    (r"\breside(?:n)? fuera del pa(?:í|&#237;)s\b", "/clientes-extranjeros/"),
    (r"\ba distancia\b", "/poderes-desde-el-exterior"),
    (r"\bapostilla(?:do|s)?\b", "/poderes-desde-el-exterior"),
    (r"\blegalizaci(?:ón|&#243;n) consular\b", "/clientes-extranjeros/"),
    (r"\btr(?:á|&#225;)mites bancarios\b", "/certificacion-firma-banco-maldonado-1/"),
    (r"\bclientes extranjeros\b", "/clientes-extranjeros/"),
    (r"\bcompradores extranjeros\b", "/clientes-extranjeros/"),
    (r"\bno residentes\b", "/clientes-extranjeros/"),
    (r"\bcarta poder para veh(?:í|&#237;)culos?\b", "/poder-vehiculo"),
    (r"\btransferencia de veh(?:í|&#237;)culos?\b", "/poder-vehiculo"),
    (r"\bveh(?:í|&#237;)culos(?:, sociedades)?\b", "/poder-vehiculo"),
    (r"\binmuebles, cuentas\b", "/real-estate"),
    (r"\bsucesiones(?: en Uruguay)?\b", "/sucesiones-en-uruguay-primeros-pasos"),
    (r"\btr(?:á|&#225;)mites? sucesorio(?:s)?\b", "/sucesiones-en-uruguay-primeros-pasos"),
    (r"\bherederos\b", "/sucesiones-en-uruguay-primeros-pasos"),
    (r"\bcriterio notarial\b", "/criterio-notarial"),
    (r"\bsoluciones notariales\b", "/soluciones"),
    (r"\bescribano p(?:ú|&#250;)blico\b", "/sobre-fabricio"),
    (r"\bintervenci(?:ón|&#243;n) del escribano\b", "/sobre-fabricio"),
]

SEMANTIC_ENTITIES_EN = [
    (r"\bnotarial certifications?\b", "/notarial-certifications-punta-del-este-1/"),
    (r"\bsignature certifications?\b", "/notarial-certifications-punta-del-este-1/"),
    (r"\bcertify(?:ing)? signatures?\b", "/notarial-certifications-punta-del-este-1/"),
    (r"\bbuying property(?: in Punta del Este)?\b", "/buying-property-punta-del-este-foreigners-1/"),
    (r"\bproperty purchase(?:s)?\b", "/buying-property-punta-del-este-foreigners-1/"),
    (r"\breal estate transactions?\b", "/buying-property-punta-del-este-foreigners-1/"),
    (r"\breal estate operations?\b", "/real-estate"),
    (r"\bforeign clients\b", "/foreign-clients"),
    (r"\bforeign buyers\b", "/foreign-clients"),
    (r"\bnon-residents?\b", "/foreign-clients"),
    (r"\bpowers? of attorney\b", "/poderes-desde-el-exterior"),
    (r"\bapostille\b", "/poderes-desde-el-exterior"),
    (r"\btitle (?:search|deeds?|review)\b", "/real-estate"),
    (r"\bpublic notary\b", "/sobre-fabricio"),
]

SEMANTIC_ENTITIES_PT = [
    (r"\bclientes estrangeiros\b", "/clientes-estrangeiros/"),
    (r"\bcompradores estrangeiros\b", "/clientes-estrangeiros/"),
    (r"\bcompra de im(?:ó|&#243;)veis\b", "/real-estate"),
    (r"\bopera(?:çõ|&#231;&#245;)es imobili(?:á|&#225;)rias\b", "/real-estate"),
    (r"\bprocura(?:çã|&#231;&#227;|çõ|&#231;&#245;)o|procura(?:çõ|&#231;&#245;)es\b", "/poderes-desde-el-exterior"),
    (r"\bapostila(?:mento)?\b", "/poderes-desde-el-exterior"),
    (r"\bcertifica(?:çã|&#231;&#227;)o de assinatura(?:s)?\b", "/certificar-firma-punta-del-este"),
    (r"\btabeli(?:ã|&#227;)o|escribano p(?:ú|&#250;)blico\b", "/sobre-fabricio"),
]

# Definición de los 4 Clusters Semánticos Notariales
CLUSTERS = {
    "certificaciones": {
        "kicker": "Recorrido Notarial Relacionado · Certificaciones y Organismos",
        "title": "Otras guías sobre certificación de firmas y actuaciones en el día",
        "hub_label": "Ver todas las soluciones →",
        "hub_url": "/soluciones",
        "cards": [
            {
                "url": "/certificar-firma-punta-del-este",
                "tag": "Atención inmediata",
                "title": "Certificar firma en Punta del Este y Maldonado",
                "desc": "Requisitos de identidad, coordinación en oficina ARTOWER y validez legal en el día.",
                "cta": "Ver requisitos y plazos",
            },
            {
                "url": "/certificacion-firma-en-el-dia-punta-del-este-1/",
                "tag": "Urgencias documentales",
                "title": "Certificación de firma en el día",
                "desc": "Cómo estructuramos documentos urgentes para contratos, autorizaciones y gestiones inmediatas.",
                "cta": "Leer criterio completo",
            },
            {
                "url": "/certificacion-firma-banco-maldonado-1/",
                "tag": "Entidades financieras",
                "title": "Certificación de firma para bancos en Maldonado",
                "desc": "Apertura de cuentas, actualización de legajos bancarios, declaratorias y poderes financieros.",
                "cta": "Conocer recaudos bancarios",
            },
            {
                "url": "/certificados-bps-dgi",
                "tag": "Empresas y contribuyentes",
                "title": "Certificados notariales para BPS y DGI",
                "desc": "Acreditación de representación, titularidad, giro comercial y vigencia societaria.",
                "cta": "Revisar documentación",
            },
            {
                "url": "/escribano-inac-maldonado-1/",
                "tag": "Habilitaciones comerciales",
                "title": "Certificación notarial para INAC en Maldonado",
                "desc": "Respaldo documental, titularidad y habilitación para empresas del sector cárnico y gastronómico.",
                "cta": "Ver trámite INAC",
            },
            {
                "url": "/certificaciones-notariales-1/",
                "tag": "Guía de criterio",
                "title": "Qué acredita una certificación notarial",
                "desc": "Diferencia entre firma certificada, testimonio por exhibición y protocolización notarial.",
                "cta": "Explorar guía técnica",
            },
        ],
    },
    "inmobiliario": {
        "kicker": "Recorrido Notarial Relacionado · Real Estate y Compraventas",
        "title": "Etapas clave de una operación inmobiliaria segura en Punta del Este",
        "hub_label": "Ir al Hub de Real Estate →",
        "hub_url": "/real-estate",
        "cards": [
            {
                "url": "/boleto-reserva-punta-del-este-1/",
                "tag": "Etapa 01 · Reserva",
                "title": "Reserva de compraventa inmobiliaria",
                "desc": "Cómo resguardar la seña, el plazo de estudio de títulos y las condiciones iniciales del acuerdo.",
                "cta": "Ver etapa de reserva",
            },
            {
                "url": "/promesa-compraventa-punta-del-este-1/",
                "tag": "Etapa 02 · Promesa",
                "title": "Promesa de compraventa e inscripción registral",
                "desc": "Protección del comprador frente a terceros, cronograma de pagos y posesión del inmueble.",
                "cta": "Analizar promesa",
            },
            {
                "url": "/compraventa-inmuebles-punta-del-este-1/",
                "tag": "Etapa 03 · Escrituración",
                "title": "Escritura de compraventa de inmuebles",
                "desc": "Cierre definitivo, control de certificados registrales y transferencia de dominio.",
                "cta": "Revisar cierre notarial",
            },
            {
                "url": "/comprar-en-punta-del-este-seguridad-juridica/",
                "tag": "Due Diligence · 30 años",
                "title": "Estudio de títulos y seguridad jurídica al comprar",
                "desc": "Auditoría de antecedentes dominiales, catastro, construcciones e impuestos antes de pagar.",
                "cta": "Leer auditoría de títulos",
            },
            {
                "url": "/documentacion-vender-propiedad-punta-del-este-1/",
                "tag": "Propietarios vendedores",
                "title": "Documentación necesaria para vender una propiedad",
                "desc": "Títulos antecedentes, planos de mensura, caracterización urbana y libre de deudas para no frenar la venta.",
                "cta": "Ver checklist de venta",
            },
            {
                "url": "/real-estate",
                "tag": "Práctica Inmobiliaria",
                "title": "Asesoramiento integral en Real Estate",
                "desc": "Acompañamiento directo para inversores, desarrolladores, compradores y vendedores en Maldonado.",
                "cta": "Explorar práctica completa",
            },
        ],
    },
    "extranjeros": {
        "kicker": "Recorrido Notarial Relacionado · Clientes Extranjeros y Distancia",
        "title": "Cómo operar, comprar o firmar en Uruguay sin residir en el país",
        "hub_label": "Ver atención a extranjeros →",
        "hub_url": "/clientes-extranjeros/",
        "cards": [
            {
                "url": "/clientes-extranjeros/",
                "tag": "Inversores no residentes",
                "title": "Atención notarial para clientes extranjeros",
                "desc": "Coordinación integral para compradores de Argentina, Brasil, EE.UU. y Europa que invierten en Punta del Este.",
                "cta": "Ver guía para no residentes",
            },
            {
                "url": "/poderes-desde-el-exterior",
                "tag": "Actuación a distancia",
                "title": "Poderes notariales desde el exterior y Apostilla",
                "desc": "Redacción del modelo exacto en Uruguay para firmar en tu país o consulado y operar sin viajar.",
                "cta": "Cómo otorgar un poder",
            },
            {
                "url": "/buying-property-punta-del-este-foreigners-1/",
                "tag": "English Guide · Real Estate",
                "title": "Buying property in Punta del Este as a foreigner",
                "desc": "Step-by-step legal framework, title deed due diligence, escrow and closing process in Uruguay.",
                "cta": "Read English guide",
            },
            {
                "url": "/notarial-certifications-punta-del-este-1/",
                "tag": "English Guide · Certifications",
                "title": "Notarial certifications & powers of attorney",
                "desc": "Document authentication, signature certification and apostille coordination in Maldonado.",
                "cta": "View English overview",
            },
            {
                "url": "/clientes-estrangeiros/",
                "tag": "Guia em Português",
                "title": "Assessoria notarial para clientes brasileiros",
                "desc": "Compra de imóveis, procurações e estruturação patrimonial em Punta del Este com segurança jurídica.",
                "cta": "Ler guia em Português",
            },
        ],
    },
    "patrimonio": {
        "kicker": "Recorrido Notarial Relacionado · Vehículos, Sucesiones y Criterio",
        "title": "Gestión patrimonial, automotores y planificación sucesoria",
        "hub_label": "Explorar Criterio Notarial →",
        "hub_url": "/criterio-notarial",
        "cards": [
            {
                "url": "/poder-vehiculo",
                "tag": "Automotores y rodados",
                "title": "Carta poder y transferencia de vehículos",
                "desc": "Autorización para conducir, vender o circular en Mercosur y compraventa con título inscripto.",
                "cta": "Ver trámites de vehículos",
            },
            {
                "url": "/sucesiones-en-uruguay-primeros-pasos",
                "tag": "Patrimonio familiar",
                "title": "Sucesiones en Uruguay: primeros pasos y plazos",
                "desc": "Documentación inicial, relación de bienes en Maldonado y regularización del tracto sucesorio.",
                "cta": "Consultar guía sucesoria",
            },
            {
                "url": "/sobre-fabricio",
                "tag": "Matrícula 17058/5",
                "title": "Sobre el Escribano Fabricio Rivas",
                "desc": "Trayectoria profesional, rigor técnico y atención personalizada desde Edificio ARTOWER en Punta del Este.",
                "cta": "Conocer el estudio",
            },
            {
                "url": "/criterio-notarial",
                "tag": "Biblioteca técnica",
                "title": "Criterio Notarial: artículos y análisis",
                "desc": "Publicaciones claras sobre compraventas, certificaciones, poderes y decisiones patrimoniales.",
                "cta": "Ver todos los artículos",
            },
            {
                "url": "/soluciones",
                "tag": "Mapa de servicios",
                "title": "Todas las soluciones notariales en Maldonado",
                "desc": "Resumen ejecutivo de cada área de práctica para individuos, familias y empresas.",
                "cta": "Ver servicios completos",
            },
        ],
    },
}

# Cápsula contextual específica según el cluster / página
CAPSULE_BY_CLUSTER = {
    "inmobiliario": {
        "kicker": "Continuidad jurídica en Real Estate",
        "text": "Toda reserva o promesa de compraventa debe encadenarse con el <strong>estudio de títulos por 30 años</strong> y la revisión previa de planos y tributos para evitar observaciones al escriturar.",
        "btn_label": "Ver guía de estudio de títulos ↗",
        "btn_url": "/comprar-en-punta-del-este-seguridad-juridica/",
        "alt_btn_label": "Ver etapa de promesa de compraventa ↗",
        "alt_btn_url": "/promesa-compraventa-punta-del-este-1/",
    },
    "certificaciones": {
        "kicker": "Coordinación ágil en Punta del Este y Maldonado",
        "text": "Si necesitas presentar documentación ante <strong>bancos, BPS, DGI o INAC</strong>, preparamos la certificación notarial verificando previamente los recaudos que exige cada institución.",
        "btn_label": "Ver certificaciones bancarias ↗",
        "btn_url": "/certificacion-firma-banco-maldonado-1/",
        "alt_btn_label": "Ver certificados para BPS y DGI ↗",
        "alt_btn_url": "/certificados-bps-dgi",
    },
    "extranjeros": {
        "kicker": "Operaciones sin viajar a Uruguay",
        "text": "Si resides en el exterior, redactamos el <strong>modelo exacto de poder especial</strong> según la ley uruguaya para que solo debas firmarlo y apostillarlo en tu ciudad de origen.",
        "btn_label": "Ver guía de poderes desde el exterior ↗",
        "btn_url": "/poderes-desde-el-exterior",
        "alt_btn_label": "Ver compraventa inmobiliaria en Uruguay ↗",
        "alt_btn_url": "/real-estate",
    },
    "patrimonio": {
        "kicker": "Respaldo documental en cada decisión",
        "text": "Ya sea para regularizar una <strong>sucesión con bienes en Maldonado</strong>, otorgar una carta poder de automotor o estructurar una compraventa, revisamos cada antecedente antes de firmar.",
        "btn_label": "Explorar todas las soluciones ↗",
        "btn_url": "/soluciones",
        "alt_btn_label": "Ver compraventa e inmuebles ↗",
        "alt_btn_url": "/real-estate",
    },
}


def classify_page_cluster(rel: str) -> str:
    r = rel.lower()
    if any(k in r for k in ["foreign", "extranjero", "estrangeiro", "poderes-desde-el-exterior", "notarial-certifications", "buying-property"]):
        return "extranjeros"
    if any(k in r for k in ["boleto", "promesa", "compraventa", "real-estate", "comprar-en-punta", "documentacion-vender"]):
        return "inmobiliario"
    if any(k in r for k in ["certifica", "bps-dgi", "inac"]):
        return "certificaciones"
    return "patrimonio"


def detect_lang(rel: str) -> str:
    r = rel.lower()
    if "estrangeiros" in r:
        return "pt"
    if any(k in r for k in ["foreign", "buying-property", "notarial-certifications"]):
        return "en"
    return "es"


def strip_previous_engine_injections(html: str) -> str:
    """Hace que el motor sea 100% idempotente al re-ejecutarse."""
    # Quitar bloque de Capa 2 y Capa 3 previos
    html = re.sub(
        r"<!-- START FR-CTX-CAPSULE -->.*?<!-- END FR-CTX-CAPSULE -->\s*",
        "",
        html,
        flags=re.S,
    )
    html = re.sub(
        r"<!-- START FR-CLUSTER-TRAIL -->.*?<!-- END FR-CLUSTER-TRAIL -->\s*",
        "",
        html,
        flags=re.S,
    )
    # Desenvolver <a class="fr-ctx-link" data-auto="1" href="...">texto</a>
    html = re.sub(
        r'<a\s+class="fr-ctx-link"\s+data-auto="1"\s+href="[^"]+">(.*?)</a>',
        r"\1",
        html,
        flags=re.S,
    )
    return html


def inject_layer1_inline_links(html: str, self_url: str, lang: str) -> tuple[str, int]:
    """
    Inyecta hasta 4 menciones editoriales (<a class="fr-ctx-link" data-auto="1" href="...">)
    únicamente dentro de etiquetas <p> que estén dentro de <main> (o fuera de header/footer),
    respetando máximo 1 aparición por URL de destino y jamás enlazando a self_url.
    """
    entities = (
        SEMANTIC_ENTITIES_EN
        if lang == "en"
        else (SEMANTIC_ENTITIES_PT if lang == "pt" else SEMANTIC_ENTITIES_ES)
    )
    used_targets = {self_url, self_url.rstrip("/"), self_url + "/"}
    injected_count = 0

    # Separar el bloque principal (<main>...</main>) si existe para no tocar topbar, header ni footer
    main_match = re.search(r"(<main\b[^>]*>)(.*?)(</main>)", html, flags=re.S | re.I)
    if main_match:
        prefix = html[: main_match.start(2)]
        work_area = main_match.group(2)
        suffix = html[main_match.end(2) :]
    else:
        # Si no hay <main>, trabajamos entre </header> y <footer
        h_end = html.lower().find("</header>")
        f_start = html.lower().find("<footer")
        if h_end != -1 and f_start != -1 and h_end < f_start:
            prefix = html[: h_end + len("</header>")]
            work_area = html[h_end + len("</header>") : f_start]
            suffix = html[f_start:]
        else:
            return html, 0

    def process_paragraph(p_match: re.Match) -> str:
        nonlocal injected_count
        open_tag, p_inner, close_tag = p_match.group(1), p_match.group(2), p_match.group(3)
        if injected_count >= 4:
            return p_match.group(0)
        # No tocar párrafos que sean leads de hero o que ya tengan botones
        if 'class="lead"' in open_tag or 'class="br1-lead"' in open_tag or "btn" in p_inner:
            return p_match.group(0)

        # Proteger enlaces <a>...</a> o tags internos existentes con placeholders
        protected = []

        def protect_tag(m: re.Match) -> str:
            idx = len(protected)
            protected.append(m.group(0))
            return f"__PROT_{idx}__"

        safe_text = re.sub(r"<a\b[^>]*>.*?</a>|<[^>]+>", protect_tag, p_inner, flags=re.S | re.I)

        for pattern, target_url in entities:
            if injected_count >= 4:
                break
            norm_target = target_url.rstrip("/")
            if target_url in used_targets or norm_target in used_targets:
                continue
            m = re.search(pattern, safe_text, flags=re.I)
            if m:
                matched_phrase = m.group(0)
                replacement = f'<a class="fr-ctx-link" data-auto="1" href="{target_url}">{matched_phrase}</a>'
                safe_text = safe_text[: m.start()] + replacement + safe_text[m.end() :]
                # Proteger el nuevo link recién insertado para que ningún otro patrón lo pise
                idx = len(protected)
                protected.append(replacement)
                safe_text = safe_text.replace(replacement, f"__PROT_{idx}__", 1)
                used_targets.add(target_url)
                used_targets.add(norm_target)
                injected_count += 1
                break  # Máximo 1 enlace auto-inyectado por párrafo para lectura limpia

        # Restaurar placeholders
        for idx in range(len(protected) - 1, -1, -1):
            safe_text = safe_text.replace(f"__PROT_{idx}__", protected[idx])

        return f"{open_tag}{safe_text}{close_tag}"

    work_area = re.sub(r"(<(?:p|li)\b[^>]*>)(.*?)(</(?:p|li)>)", process_paragraph, work_area, flags=re.S | re.I)
    return prefix + work_area + suffix, injected_count


def build_layer2_capsule(cluster_key: str, self_url: str, lang: str) -> str:
    cap = CAPSULE_BY_CLUSTER.get(cluster_key, CAPSULE_BY_CLUSTER["patrimonio"])
    btn_url = cap["btn_url"]
    btn_label = cap["btn_label"]
    if btn_url.rstrip("/") == self_url.rstrip("/"):
        btn_url = cap["alt_btn_url"]
        btn_label = cap["alt_btn_label"]

    if lang == "en":
        kicker = "Connected Notarial Guidance"
        text = "Every real estate reservation, power of attorney, or certification in Punta del Este is backed by our <strong>30-year title search and direct document verification</strong>."
        btn_label = "Explore Real Estate Practice ↗" if self_url.rstrip("/") != "/real-estate" else "View Notarial Certifications ↗"
        btn_url = "/real-estate" if self_url.rstrip("/") != "/real-estate" else "/notarial-certifications-punta-del-este-1/"
    elif lang == "pt":
        kicker = "Continuidade Jurídica no Uruguai"
        text = "Toda reserva, procuração ou escritura em Punta del Este conta com <strong>auditoria de títulos de 30 anos</strong> e atendimento direto em nosso escritório no Edifício ARTOWER."
        btn_label = "Ver prática de Real Estate ↗"
        btn_url = "/real-estate"
    else:
        kicker = cap["kicker"]
        text = cap["text"]

    return (
        "<!-- START FR-CTX-CAPSULE -->\n"
        '<div class="container" style="margin-top:18px;margin-bottom:18px;">\n'
        '  <div class="fr-ctx-capsule">\n'
        '    <div class="fr-ctx-capsule-copy">\n'
        f'      <span class="fr-ctx-capsule-kicker">{kicker}</span>\n'
        f'      <p class="fr-ctx-capsule-text">{text}</p>\n'
        "    </div>\n"
        f'    <a class="fr-ctx-capsule-btn" href="{btn_url}">{btn_label}</a>\n'
        "  </div>\n"
        "</div>\n"
        "<!-- END FR-CTX-CAPSULE -->\n"
    )


def build_layer3_cluster_trail(cluster_key: str, self_url: str, lang: str) -> str:
    cluster = CLUSTERS.get(cluster_key, CLUSTERS["patrimonio"])
    cards = [
        c
        for c in cluster["cards"]
        if c["url"].rstrip("/") != self_url.rstrip("/")
    ][:3]

    kicker = cluster["kicker"]
    title = cluster["title"]
    hub_label = cluster["hub_label"]
    hub_url = cluster["hub_url"]
    if hub_url.rstrip("/") == self_url.rstrip("/"):
        hub_url = "/soluciones" if self_url.rstrip("/") != "/soluciones" else "/criterio-notarial"
        hub_label = "Ver todas las guías y soluciones →"

    if lang == "en":
        kicker = "Related Legal & Notarial Guides · Punta del Este"
        title = "Continue reading on property law, powers of attorney, and certifications"
        hub_label = "All Foreign Client Resources →"
        hub_url = "/foreign-clients" if self_url.rstrip("/") != "/foreign-clients" else "/real-estate"
    elif lang == "pt":
        kicker = "Guias Notariais Relacionados · Punta del Este"
        title = "Continue lendo sobre compra de imóveis, procurações e certificações"
        hub_label = "Ver todas as soluções →"
        hub_url = "/soluciones"

    cards_html = []
    for c in cards:
        cards_html.append(
            f'      <a class="fr-cluster-card" href="{c["url"]}">\n'
            "        <div>\n"
            f'          <div class="fr-cluster-card-tag">{c["tag"]}</div>\n'
            f'          <h3>{c["title"]}</h3>\n'
            f'          <p>{c["desc"]}</p>\n'
            "        </div>\n"
            f'        <span class="fr-cluster-card-cta">{c["cta"]} <span>↗</span></span>\n'
            "      </a>"
        )

    return (
        "<!-- START FR-CLUSTER-TRAIL -->\n"
        '<section class="fr-cluster-trail" aria-label="Guías notariales vinculadas">\n'
        '  <div class="container">\n'
        '    <div class="fr-cluster-head">\n'
        "      <div>\n"
        f'        <p class="fr-cluster-kicker">{kicker}</p>\n'
        f'        <h2 class="fr-cluster-title">{title}</h2>\n'
        "      </div>\n"
        f'      <a class="fr-cluster-hub-link" href="{hub_url}">{hub_label}</a>\n'
        "    </div>\n"
        '    <div class="fr-cluster-grid">\n'
        + "\n".join(cards_html)
        + "\n    </div>\n"
        "  </div>\n"
        "</section>\n"
        "<!-- END FR-CLUSTER-TRAIL -->\n"
    )


def process_all_pages(base_dir: str):
    all_html = sorted(glob.glob(os.path.join(base_dir, "**/*.html"), recursive=True))
    updated = 0
    for p in all_html:
        rel = os.path.relpath(p, base_dir).replace("\\", "/")
        if rel.startswith(("campana/", "panel/", "instagram-carrusel/")):
            continue
        if rel in UTILITY_EXEMPT:
            continue

        raw_html = open(p, encoding="utf-8", errors="ignore").read()
        clean_html = strip_previous_engine_injections(raw_html)

        self_url = rel_to_url(rel)
        lang = detect_lang(rel)
        cluster_key = classify_page_cluster(rel)

        # Capa 1: Enlaces editoriales in-text
        html_l1, count_l1 = inject_layer1_inline_links(clean_html, self_url, lang)

        # Capa 2 y Capa 3: Cápsula contextual + Rastro de Cluster Semántico antes de </main> o <footer
        capsule_block = build_layer2_capsule(cluster_key, self_url, lang)
        trail_block = build_layer3_cluster_trail(cluster_key, self_url, lang)
        combined_blocks = capsule_block + trail_block

        if "</main>" in html_l1:
            final_html = html_l1.replace("</main>", combined_blocks + "</main>", 1)
        elif "<footer" in html_l1:
            idx = html_l1.find("<footer")
            final_html = html_l1[:idx] + combined_blocks + html_l1[idx:]
        else:
            final_html = html_l1

        open(p, "w", encoding="utf-8").write(final_html)
        updated += 1
        print(f"[OK] {rel:54} | Cluster: {cluster_key:15} | InText: {count_l1} | Capsule: 1 | Trail: 4")

    print(f"\nTotal páginas públicas actualizadas en {base_dir}: {updated}")


if __name__ == "__main__":
    process_all_pages(BASE_DIR)
    if os.path.exists(WORKTREE_DIR):
        import shutil
        shutil.copyfile(
            os.path.join(BASE_DIR, "style.css"),
            os.path.join(WORKTREE_DIR, "style.css"),
        )
        process_all_pages(WORKTREE_DIR)
