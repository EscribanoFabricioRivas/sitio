// Base de Conocimiento Viva 360° — Escribano Público Fabricio Rivas (Mat. 17058/5)
// Alimentada con las 26 páginas del sitio, el Pack Semana 1, las Placas Técnicas XXL y las Métricas Reales (Ads/GA4/GSC)

window.FR_KNOWLEDGE_BASE = {
  brand: {
    name: "Escribano Público Fabricio Rivas",
    matricula: "Matrícula Notarial 17058/5",
    location: "Punta del Este & Maldonado · Uruguay",
    distanceRule: "Atención directa, también a distancia si estás en otro país.",
    whatsapp: "+598 99 431 185",
    whatsappLink: "https://wa.me/59899431185",
    site: "https://escribanofabriciorivas.com",
    colors: {
      charcoal: "#111111",
      stone: "#e9e7e1",
      gold: "#c4ad7a",
      forest: "#1c2621",
      white: "#f5f4f0"
    },
    forbiddenWords: [
      { bad: "tenés", fix: "tienes", reason: "Prohibido el voseo (usar tuteo estricto)" },
      { bad: "podés", fix: "puedes", reason: "Prohibido el voseo (usar tuteo estricto)" },
      { bad: "querés", fix: "quieres", reason: "Prohibido el voseo (usar tuteo estricto)" },
      { bad: "coordinás", fix: "coordinas", reason: "Prohibido el voseo (usar tuteo estricto)" },
      { bad: "revisá", fix: "revisa", reason: "Prohibido el voseo (usar tuteo estricto)" },
      { bad: "escribime", fix: "escríbeme", reason: "Prohibido el voseo (usar tuteo estricto)" },
      { bad: "contactanos", fix: "contáctame", reason: "Prohibido el voseo y plural impersonal" },
      { bad: "consulte", fix: "consulta", reason: "Prohibido el trato de usted (usar tuteo)" },
      { bad: "coordine", fix: "coordina", reason: "Prohibido el trato de usted (usar tuteo)" },
      { bad: "artower", fix: "[eliminado]", reason: "Término prohibido por regla de marca" },
      { bad: "trabajo en persona", fix: "atención directa, también a distancia si estás en otro país", reason: "Frase prohibida por regla de marca" }
    ],
    backgrounds: [
      { id: "bg1", label: "Fachada Contemporánea La Barra (Piedra y Madera)", url: "../campana/fondos_ia/bg1.jpg" },
      { id: "bg2", label: "Residencia Pinares (Hormigón y Pinos)", url: "../campana/fondos_ia/bg2.jpg" },
      { id: "bg3", label: "Arquitectura Solanas (Luz de Tarde)", url: "../campana/fondos_ia/bg3.jpg" },
      { id: "bg4", label: "Patio Minimalista Punta del Este (Piedra Clara)", url: "../campana/fondos_ia/bg4.jpg" }
    ]
  },

  verticals: [
    {
      id: "re_comprador",
      name: "1. Real Estate Comprador (Reserva, Promesa y Títulos)",
      priority: "Alta (Core Business)",
      searchConsoleSignal: "escribano punta del este (Pos. 1.8 · 603 impr.)",
      pages: ["/real-estate.html", "/boleto-reserva-punta-del-este-1/", "/promesa-compraventa-punta-del-este-1/", "/compraventa-inmuebles-punta-del-este-1/", "/comprar-en-punta-del-este-seguridad-juridica/"],
      templates: {
        es: [
          {
            title: "EL PROCESO DE TU COMPRA EN 3 ETAPAS",
            tag: "GUÍA TÉCNICA NOTARIAL · PUNTA DEL ESTE",
            bullets: [
              "1. RESERVA: Bloquea el inmueble y deja tu seña en custodia notarial (Escrow).",
              "2. ESTUDIO 30 AÑOS: Tu escribano audita antecedentes, planos, BPS, DGI y deudas.",
              "3. ESCRITURA: Firma final y pago recién con certificados registrales limpios."
            ],
            takeaway: "En Uruguay el comprador elige a su escribano. No entregues dinero sin custodia.",
            cta: "Revisa tu reserva antes de firmar · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/compraventa-inmuebles-punta-del-este-1/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          },
          {
            title: "BOLETO DE RESERVA VS. PROMESA DE COMPRAVENTA",
            tag: "DIFERENCIA TÉCNICA CLAVE · URUGUAY",
            bullets: [
              "• BOLETO DE RESERVA: Es el acuerdo preliminar que fija precio, plazo y multa.",
              "• PROMESA INSCRIPTA: Otorga derecho real frente a terceros en el Registro.",
              "• CLÁUSULA ESENCIAL: Condiciona siempre tu seña a títulos perfectos."
            ],
            takeaway: "Tu escribano interviene antes del Boleto de Reserva, nunca después.",
            cta: "Envía tu borrador de reserva por WhatsApp · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/boleto-reserva-punta-del-este-1/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_dark"
          },
          {
            title: "QUÉ REVISA TU ESCRIBANO EN PH VS. CASA",
            tag: "AUDITORÍA PREVENTIVA · MALDONADO",
            bullets: [
              "• EN APARTAMENTO (PH): Reglamento de copropiedad, libre deuda de gastos comunes y fondo de reserva.",
              "• EN CASA / TERRENO: Plano de mensura inscripto, retiros municipales y certificado BPS de obra.",
              "• EN AMBOS: Títulos de 30 años sin observaciones e impuestos al día."
            ],
            takeaway: "Una obra no declarada en BPS o un plano vencido frena cualquier venta futura.",
            cta: "Coordina tu auditoría preventiva · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/real-estate.html",
            recommendedFormat: "1080x1920",
            recommendedStyle: "editorial"
          }
        ],
        en: [
          {
            title: "3 STEPS TO BUY PROPERTY IN PUNTA DEL ESTE",
            tag: "NOTARIAL DUE DILIGENCE · URUGUAY",
            bullets: [
              "1. RESERVATION (BOLETO): Locks the price while your deposit stays in notarial escrow.",
              "2. 30-YEAR TITLE SEARCH: Your Notary Public audits deeds, liens, tax clearance and plans.",
              "3. CLOSING DEED: Funds are released only when all Registry certificates are clean."
            ],
            takeaway: "In Uruguay, the buyer always chooses their own Notary Public (Escribano).",
            cta: "Direct guidance, also remotely from abroad · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/buying-property-punta-del-este-foreigners-1/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_dark"
          }
        ],
        pt: [
          {
            title: "COMO COMPRAR IMÓVEL EM PUNTA DEL ESTE COM SEGURANÇA",
            tag: "CRITÉRIO NOTARIAL · URUGUAI",
            bullets: [
              "1. RESERVA EM CUSTÓDIA: O sinal fica retido com o seu tabelião até a auditoria.",
              "2. AUDITORIA DE 30 ANOS: Verificação completa de títulos, plantas, impostos e condomínio.",
              "3. ESCRITURA DEFINITIVA: Assinatura presencial ou a distância por procuração."
            ],
            takeaway: "No Uruguai, o comprador escolhe o seu próprio Escribano de confiança.",
            cta: "Atendimento direto, também a distância · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/clientes-estrangeiros/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "editorial"
          }
        ]
      }
    },
    {
      id: "re_vendedor",
      name: "2. Real Estate Vendedor (Documentación antes de vender)",
      priority: "Alta (Nota Nueva Publicada)",
      searchConsoleSignal: "Nueva nota en Criterio Notarial (Indexación activa)",
      pages: ["/documentacion-vender-propiedad-punta-del-este-1/"],
      templates: {
        es: [
          {
            title: "DOCUMENTACIÓN PARA VENDER SIN DEMORAS",
            tag: "CRITERIO NOTARIAL · VENDEDORES",
            bullets: [
              "• ANTECEDENTES: Primeras copias de escrituras anteriores y planos de mensura.",
              "• CONSTRUCCIONES: Regularización de reformas ante Intendencia y BPS.",
              "• IMPUESTOS AL DÍA: Contribución Inmobiliaria, Primaria y gastos comunes."
            ],
            takeaway: "Revisar tu carpeta antes de publicar evita perder compradores listos para señar.",
            cta: "Prepara tu carpeta de venta hoy · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/documentacion-vender-propiedad-punta-del-este-1/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "editorial"
          }
        ],
        en: [
          {
            title: "SELLING PROPERTY IN PUNTA DEL ESTE: DOCUMENT CHECKLIST",
            tag: "SELLER'S NOTARIAL GUIDE · URUGUAY",
            bullets: [
              "• ORIGINAL DEEDS: Registered title deeds and updated survey plans (Plano de Mensura).",
              "• TAX & BPS CLEARANCE: Municipal taxes, Primary tax and construction clearance.",
              "• REMOTE POWER OF ATTORNEY: Sell securely without traveling to Uruguay."
            ],
            takeaway: "Pre-verifying your folder prevents delays when an buyer makes an offer.",
            cta: "Review your property documents · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/foreign-clients.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          }
        ],
        pt: [
          {
            title: "DOCUMENTOS PARA VENDER IMÓVEL EM PUNTA DEL ESTE",
            tag: "GUIA PARA PROPRIETÁRIOS · URUGUAI",
            bullets: [
              "• ESCRITURAS ORIGINAIS: Títulos anteriores e planta de mensura registrada.",
              "• OBRAS REGULARIZADAS: Certidões do BPS e impostos municipais em dia.",
              "• VENDA A DISTÂNCIA: Possibilidade de outorgar procuração sem viajar."
            ],
            takeaway: "Organizar a documentação antes da oferta garante um fechamento rápido.",
            cta: "Verifique a sua documentação · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/clientes-estrangeiros/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          }
        ]
      }
    },
    {
      id: "certificaciones",
      name: "3. Certificaciones de Firma (En el día, Bancos, Vehículos)",
      priority: "Muy Alta (Oportunidad SEO #1 en Search Console)",
      searchConsoleSignal: "certificar firma / cuánto sale certificar firma (Pos. 4–11 sin explotar)",
      pages: ["/certificar-firma-punta-del-este/", "/certificaciones-notariales-1/", "/certificacion-firma-en-el-dia-punta-del-este-1/", "/certificacion-firma-banco-maldonado-1/", "/poder-vehiculo.html"],
      templates: {
        es: [
          {
            title: "CERTIFICACIÓN DE FIRMAS EN EL DÍA",
            tag: "PUNTA DEL ESTE Y MALDONADO · FLUJO RÁPIDO",
            bullets: [
              "1. ENVÍA POR WHATSAPP: Foto de tu documento vigente y datos del trámite o banco.",
              "2. REVISIÓN PREVIA: Redactamos y verificamos los requisitos antes de tu llegada.",
              "3. FIRMA DIRECTA: Pasas únicamente a firmar y retiras tu documento en el acto."
            ],
            takeaway: "Para bancos, contratos, cartas poder, autorizaciones de viaje y vehículos.",
            cta: "Coordina tu certificación hoy · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/certificar-firma-punta-del-este/",
            recommendedFormat: "1080x1920",
            recommendedStyle: "technical_stone"
          },
          {
            title: "CERTIFICACIÓN DE FIRMA PARA BANCOS EN MALDONADO",
            tag: "CUMPLIMIENTO BANCARIO · SIN RECHAZOS",
            bullets: [
              "• FORMATO EXACTO: Adaptado a los requisitos de cada institución bancaria.",
              "• PERSONAS Y EMPRESAS: Certificación de firmas y control de representación societaria.",
              "• SIN ESPERAS: Envías la documentación por WhatsApp y firmas en horario coordinado."
            ],
            takeaway: "Evita idas y vueltas con el banco validando el texto notarial antes de imprimir.",
            cta: "Envía el pedido de tu banco · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/certificacion-firma-banco-maldonado-1/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_dark"
          }
        ],
        en: [
          {
            title: "SAME-DAY NOTARIAL SIGNATURE CERTIFICATION",
            tag: "PUNTA DEL ESTE & MALDONADO · URUGUAY",
            bullets: [
              "1. SEND VIA WHATSAPP: Photo of your Passport or ID and the document required.",
              "2. PRE-DRAFTING: We prepare the notarial certificate according to legal standards.",
              "3. SIGN & COLLECT: One brief appointment to sign and receive your certified document."
            ],
            takeaway: "Valid for Uruguayan banks, contracts, corporate documents and powers of attorney.",
            cta: "Schedule via WhatsApp · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/notarial-certifications-punta-del-este-1/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          }
        ],
        pt: [
          {
            title: "RECONHECIMENTO E CERTIFICAÇÃO DE ASSINATURA NO DIA",
            tag: "PUNTA DEL ESTE E MALDONADO · URUGUAI",
            bullets: [
              "1. ENVIE PELO WHATSAPP: Foto do seu documento (RG/Passaporte) e dados do ato.",
              "2. PREPARAÇÃO PRÉVIA: Redigimos a certificação conforme a exigência do banco ou órgão.",
              "3. ASSINATURA ÁGIL: Você comparece apenas para assinar e retirar no ato."
            ],
            takeaway: "Para bancos uruguaios, contratos, procurações e transferência de veículos.",
            cta: "Agende pelo WhatsApp · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/clientes-estrangeiros/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_dark"
          }
        ]
      }
    },
    {
      id: "extranjeros_poderes",
      name: "4. Clientes Extranjeros y Poderes a Distancia (Sin Viajar)",
      priority: "Alta (Argentina, Brasil, EE.UU., Europa)",
      searchConsoleSignal: "/foreign-clients (160 impresiones orgánicas)",
      pages: ["/clientes-extranjeros/", "/foreign-clients.html", "/clientes-estrangeiros/", "/poderes-desde-el-exterior.html", "/buying-property-punta-del-este-foreigners-1/"],
      templates: {
        es: [
          {
            title: "CÓMO COMPRAR O VENDER EN URUGUAY SIN VIAJAR",
            tag: "CLIENTES EN EL EXTERIOR · PASO A PASO",
            bullets: [
              "1. TEXTO NOTARIAL: Redactamos en Uruguay el modelo exacto de Poder Especial.",
              "2. FIRMA Y APOSTILLA: Lo firmas en tu país (escribano o consulado) con Apostilla de La Haya.",
              "3. PROTOCOLIZACIÓN: Lo inscribimos en Uruguay y firmamos tu operación en Punta del Este."
            ],
            takeaway: "Atención directa, también a distancia si estás en otro país.",
            cta: "Solicita el modelo de poder · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/poderes-desde-el-exterior.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          }
        ],
        en: [
          {
            title: "BUY OR SELL IN URUGUAY WITHOUT TRAVELING",
            tag: "REMOTE POWER OF ATTORNEY · FOREIGN CLIENTS",
            bullets: [
              "1. CUSTOM DRAFT: We draft the exact Special Power of Attorney required under Uruguayan law.",
              "2. LOCAL SIGNING & APOSTILLE: Sign in your country and attach the Hague Apostille.",
              "3. URUGUAYAN PROTOCOLIZATION: We register it in Uruguay to complete your closing safely."
            ],
            takeaway: "Direct guidance, also remotely if you are in another country.",
            cta: "Message us on WhatsApp · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/foreign-clients.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "editorial"
          }
        ],
        pt: [
          {
            title: "COMPRE OU VENDA NO URUGUAI SEM PRECISAR VIAJAR",
            tag: "PROCURAÇÃO DO EXTERIOR · CLIENTES BRASILEIROS",
            bullets: [
              "1. MINUTA URUGUAIA: Elaboramos o texto exato da Procuração Especial para o seu caso.",
              "2. CARTÓRIO E APOSTILA: Você assina no Brasil e aplica a Apostila de Haia.",
              "3. PROTOCOLIZAÇÃO NO URUGUAI: Validamos o documento para assinar a sua escritura."
            ],
            takeaway: "Atendimento direto, também a distância se você está em outro país.",
            cta: "Fale pelo WhatsApp · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/clientes-estrangeiros/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          }
        ]
      }
    },
    {
      id: "actas_constataciones",
      name: "5. Actas Notariales y Constataciones (Obras, Llaves, Hechos)",
      priority: "Media-Alta (Alto Valor en Punta del Este)",
      searchConsoleSignal: "/soluciones (312 impr. · 6 clics)",
      pages: ["/soluciones.html", "/CC1-criterio-certificaciones-notariales.html"],
      templates: {
        es: [
          {
            title: "CUÁNDO NECESITAS UN ACTA DE CONSTATACIÓN NOTARIAL",
            tag: "PRUEBA FEHACIENTE · PUNTA DEL ESTE",
            bullets: [
              "• ENTREGA O RECEPCIÓN DE INMUEBLES: Inventario y estado real antes o después de alquilar o comprar.",
              "• AVANCE O VICIOS DE OBRA: Registro notarial con fecha cierta y fotografías certificadas.",
              "• COMUNICACIONES Y HECHOS: Notificaciones presenciales o constatación de páginas y mensajes."
            ],
            takeaway: "Un acta notarial deja prueba plena antes de que el estado del bien cambie.",
            cta: "Coordina una constatación en el día · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/soluciones.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_dark"
          }
        ],
        en: [
          {
            title: "NOTARIAL INSPECTION & FACT-FINDING RECORDS (ACTAS)",
            tag: "LEGAL EVIDENCE IN PUNTA DEL ESTE",
            bullets: [
              "• PROPERTY HANDOVER: Certified inventory and condition report before or after tenancy or sale.",
              "• CONSTRUCTION PROGRESS: Official timestamped record of building stages or defects.",
              "• FORMAL NOTICES: In-person notarial notifications and digital evidence certification."
            ],
            takeaway: "Protect your property rights with indisputable notarial evidence in Uruguay.",
            cta: "Request a notarial inspection · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/foreign-clients.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          }
        ],
        pt: [
          {
            title: "ATAS NOTARIAIS DE CONSTATAÇÃO EM PUNTA DEL ESTE",
            tag: "PROVA JURÍDICA · IMÓVEIS E OBRAS",
            bullets: [
              "• VISTORIA E ENTREGA DE CHAVES: Registro oficial do estado do imóvel e inventário.",
              "• ACOMPANHAMENTO DE OBRA: Constatação de prazos, entregas ou defeitos construtivos.",
              "• NOTIFICAÇÕES FORMAIS: Prova plena com fé pública no Uruguai."
            ],
            takeaway: "Garanta prova jurídica imediata antes de qualquer alteração no imóvel.",
            cta: "Solicite uma constatação · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/clientes-estrangeiros/",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_dark"
          }
        ]
      }
    },
    {
      id: "sucesiones",
      name: "6. Sucesiones y Patrimonio en Uruguay (Residentes y Extranjeros)",
      priority: "Media (Ticket Alto)",
      searchConsoleSignal: "sucesiones-en-uruguay-primeros-pasos.html",
      pages: ["/sucesiones-en-uruguay-primeros-pasos.html"],
      templates: {
        es: [
          {
            title: "Bienes en Uruguay: Primeros Pasos en una Sucesión",
            tag: "PATRIMONIO Y SUCESIONES · URUGUAY",
            bullets: [
              "• LEY APLICABLE: Los inmuebles ubicados en Uruguay se rigen siempre por la ley uruguaya.",
              "• DOCUMENTACIÓN INICIAL: Partidas de estado civil, testamento (si existe) y títulos del bien.",
              "• TRÁMITE A DISTANCIA: Los herederos en el exterior pueden actuar mediante poder apostillado."
            ],
            takeaway: "Regularizar la sucesión a tiempo permite disponer o vender el inmueble sin bloqueos.",
            cta: "Consulta los pasos para tu caso · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/sucesiones-en-uruguay-primeros-pasos.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "editorial"
          }
        ],
        en: [
          {
            title: "INHERITANCE & PROBATE FOR PROPERTY IN URUGUAY",
            tag: "ESTATE PLANNING · PUNTA DEL ESTE",
            bullets: [
              "• URUGUAYAN JURISDICTION: Real estate located in Uruguay requires local probate proceedings.",
              "• REQUIRED DOCUMENTS: Civil registry certificates, property deeds and apostilled documents.",
              "• NO NEED TO TRAVEL: Heirs abroad can complete the entire process via Power of Attorney."
            ],
            takeaway: "Completing probate early allows heirs to sell or transfer the property without delay.",
            cta: "Direct guidance for foreign heirs · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/sucesiones-en-uruguay-primeros-pasos.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          }
        ],
        pt: [
          {
            title: "SUCESSÃO E INVENTÁRIO DE IMÓVEIS NO URUGUAI",
            tag: "DIREITO SUCESSÓRIO · PUNTA DEL ESTE",
            bullets: [
              "• LEI URUGUAIA: Imóveis situados no Uruguai exigem processo sucessório local.",
              "• DOCUMENTAÇÃO: Certidões apostiladas e títulos de propriedade do imóvel.",
              "• HERDEIROS NO BRASIL: Todo o trâmite pode ser conduzido por procuração, sem viajar."
            ],
            takeaway: "Regularizar a sucessão permite vender ou administrar o patrimônio com segurança.",
            cta: "Tire suas dúvidas pelo WhatsApp · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/sucesiones-en-uruguay-primeros-pasos.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_dark"
          }
        ]
      }
    },
    {
      id: "empresas_bps_inac",
      name: "7. Empresas, Certificados BPS/DGI e INAC Maldonado",
      priority: "Media (Flujo Corporativo Local)",
      searchConsoleSignal: "certificados notariales (Pos. 21 · oportunidad B2B)",
      pages: ["/certificados-bps-dgi.html", "/escribano-inac-maldonado-1/"],
      templates: {
        es: [
          {
            title: "CERTIFICADOS NOTARIALES PARA BPS, DGI E INAC",
            tag: "EMPRESAS Y COMERCIOS · MALDONADO",
            bullets: [
              "• BPS Y DGI: Certificación de representación, vigencia societaria, firmas y domicilios.",
              "• HABILITACIONES INAC: Certificados notariales específicos para empresas del rubro en Maldonado.",
              "• ENTREGA ÁGIL: Envías la documentación antecedente de la sociedad y retiras listo para presentar."
            ],
            takeaway: "Evita observaciones formales presentando certificados actualizados al día.",
            cta: "Solicita tu certificado societario · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/certificados-bps-dgi.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          }
        ],
        en: [
          {
            title: "CORPORATE NOTARIAL CERTIFICATES (BPS, DGI & BANKS)",
            tag: "COMPANIES IN MALDONADO & PUNTA DEL ESTE",
            bullets: [
              "• GOOD STANDING & REPRESENTATION: Official certification of company bylaws and directors.",
              "• TAX & REGULATORY FILINGS: Certificates for BPS, DGI, municipal permits and banks.",
              "• FAST TURNAROUND: Send corporate records digitally for pre-review."
            ],
            takeaway: "Keep your Uruguayan company compliant with accurate notarial certifications.",
            cta: "Contact via WhatsApp · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/certificados-bps-dgi.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_dark"
          }
        ],
        pt: [
          {
            title: "CERTIDÕES NOTARIAIS PARA EMPRESAS (BPS, DGI E BANCOS)",
            tag: "EMPRESAS EM MALDONADO E PUNTA DEL ESTE",
            bullets: [
              "• REPRESENTAÇÃO SOCIETÁRIA: Certificação de diretores, procuradores e vigência da sociedade.",
              "• ÓRGÃOS PÚBLICOS E BANCOS: Documentação pronta para BPS, DGI e abertura de contas.",
              "• AGILIDADE: Envie os documentos da empresa pelo WhatsApp para análise prévia."
            ],
            takeaway: "Mantenha a sua empresa no Uruguai regularizada sem burocracia.",
            cta: "Solicite pelo WhatsApp · +598 99 431 185",
            url: "https://escribanofabriciorivas.com/certificados-bps-dgi.html",
            recommendedFormat: "1080x1350",
            recommendedStyle: "technical_stone"
          }
        ]
      }
    }
  ],

  blogEntries: [
    {
      slug: "documentacion-vender-propiedad-punta-del-este-1",
      title: "Documentación para vender una propiedad en Punta del Este: qué revisar antes de ofrecerla",
      url: "https://escribanofabriciorivas.com/documentacion-vender-propiedad-punta-del-este-1/",
      verticalId: "re_vendedor",
      inSitemap: true,
      inLlmsTxt: true,
      indexedStatus: "Pendiente pedir indexación en Search Console (1 clic)",
      isNew: true,
      packDayRef: "Día 1 (Pack Semana 1 listo)"
    },
    {
      slug: "boleto-reserva-punta-del-este-1",
      title: "Boleto de reserva en Punta del Este: qué debes revisar antes de firmar y señar",
      url: "https://escribanofabriciorivas.com/boleto-reserva-punta-del-este-1/",
      verticalId: "re_comprador",
      inSitemap: true,
      inLlmsTxt: true,
      indexedStatus: "En Sitemap · Verificar en GSC",
      isNew: false,
      packDayRef: "Placa Técnica 02 lista"
    },
    {
      slug: "promesa-compraventa-punta-del-este-1",
      title: "Promesa de compraventa en Punta del Este: cuándo conviene y cómo protege al comprador",
      url: "https://escribanofabriciorivas.com/promesa-compraventa-punta-del-este-1/",
      verticalId: "re_comprador",
      inSitemap: true,
      inLlmsTxt: true,
      indexedStatus: "En Sitemap · Verificar en GSC",
      isNew: false,
      packDayRef: "Placa Técnica 02 lista"
    },
    {
      slug: "compraventa-inmuebles-punta-del-este-1",
      title: "Compraventa de inmuebles en Punta del Este: etapas, costos y rol de tu escribano",
      url: "https://escribanofabriciorivas.com/compraventa-inmuebles-punta-del-este-1/",
      verticalId: "re_comprador",
      inSitemap: true,
      inLlmsTxt: true,
      indexedStatus: "En Sitemap · Indexada",
      isNew: false,
      packDayRef: "Carrusel Día 2 + Placa Técnica 01"
    },
    {
      slug: "certificar-firma-punta-del-este",
      title: "Certificar firma en Punta del Este y Maldonado: requisitos y gestión en el día",
      url: "https://escribanofabriciorivas.com/certificar-firma-punta-del-este/",
      verticalId: "certificaciones",
      inSitemap: true,
      inLlmsTxt: true,
      indexedStatus: "Indexada (Pos. 4.0 en Google · 122 impr.)",
      isNew: false,
      packDayRef: "Día 5 (Pack Semana 1 listo)"
    },
    {
      slug: "buying-property-punta-del-este-foreigners-1",
      title: "Buying Property in Punta del Este for Foreigners: Legal Process & Notary Role",
      url: "https://escribanofabriciorivas.com/buying-property-punta-del-este-foreigners-1/",
      verticalId: "extranjeros_poderes",
      inSitemap: true,
      inLlmsTxt: true,
      indexedStatus: "En Sitemap · Inglés",
      isNew: false,
      packDayRef: "Placa Técnica 04 + Rotación EN"
    }
  ],

  week1Pack: [
    {
      day: "Día 1 · Lunes (ACCIÓN #1 DE ESTA SEMANA)",
      badge: "PRIORIDAD #1 ESTA SEMANA",
      vertical: "Real Estate Vendedor (Nota Nueva del Blog)",
      style: "Editorial Arquitectónico",
      title: "Documentación para vender una propiedad en Punta del Este sin frenar la operación",
      feedImg: "../campana/semana_1_pack_completo/piezas/dia1_feed_1080x1350.jpg",
      vertImg: "../campana/semana_1_pack_completo/piezas/dia1_vertical_1080x1920.jpg",
      blogUrl: "https://escribanofabriciorivas.com/documentacion-vender-propiedad-punta-del-este-1/",
      igCopy: `Cuando decides vender una propiedad en Punta del Este, el momento en que aparece un comprador interesado no es el momento para empezar a buscar los papeles.\n\nUna diferencia en los planos de mensura, una reforma no declarada en BPS o un antecedente dominial incompleto pueden enfriar o frenar una reserva lista para firmarse.\n\nEn la nueva nota de Criterio Notarial repaso la carpeta documental que conviene tener auditada antes de salir al mercado:\n• Títulos antecedentes y primeras copias inscriptas.\n• Plano de mensura vigente y situación catastral.\n• Libre de deuda de Contribución Inmobiliaria, Primaria y gastos comunes.\n• Regularidad de construcciones ante BPS.\n\nAtención directa, también a distancia si estás en otro país.\n\nLee la nota completa en escribanofabriciorivas.com o escríbeme por WhatsApp al +598 99 431 185.\n\n#EscribanoPuntaDelEste #RealEstateUruguay #PuntaDelEste #SeguridadJuridica #CompraventaInmobiliaria #Maldonado`,
      storyCopy: `NUEVA NOTA EN CRITERIO NOTARIAL · ¿Vas a vender tu propiedad en Punta del Este? Revisa los 4 documentos clave antes de recibir una oferta. Escríbeme por WhatsApp al +598 99 431 185.`,
      linkedinCopy: `En el mercado inmobiliario de Punta del Este y Maldonado, muchas operaciones se demoran o se caen entre la oferta y la reserva por un motivo evitable: la carpeta documental del inmueble recién se revisa cuando ya hay un comprador esperando.\n\nAcabo de publicar una nueva guía práctica en Criterio Notarial sobre qué documentación conviene auditar antes de poner una propiedad en venta (títulos, planos de mensura, situación en BPS y certificados comunes).\n\nPuedes leer el artículo completo aquí: https://escribanofabriciorivas.com/documentacion-vender-propiedad-punta-del-este-1/\n\nAtención directa, también a distancia si estás en otro país (+598 99 431 185).`,
      gbpCopy: `Nueva guía en Criterio Notarial: Documentación necesaria para vender una propiedad en Punta del Este sin demoras ni observaciones. Revisa títulos, planos y certificados antes de firmar la reserva. Consultas directas por WhatsApp al +598 99 431 185.`
    },
    {
      day: "Día 2 · Martes / Jueves (ACCIÓN #2 DE ESTA SEMANA · CARRUSEL TÉCNICO XXL)",
      badge: "PRIORIDAD #2 ESTA SEMANA (+ PAUTA US$ 2–3/DÍA)",
      vertical: "Real Estate Comprador (Proceso en 3 Etapas + PH vs. Casa)",
      style: "Híbrido: Portada Editorial + Placas Técnicas XXL Sin IA",
      title: "Carrusel Técnico XXL: Los 3 Momentos de tu Compra + Checklist PH vs. Casa",
      feedImg: "../campana/semana_1_pack_completo/piezas_tecnicas_sin_ia/tecnica_01_proceso_compraventa_1080x1350.jpg",
      extraImgs: [
        "../campana/semana_1_pack_completo/piezas/dia2_carrusel_01_1080x1350.jpg",
        "../campana/semana_1_pack_completo/piezas_tecnicas_sin_ia/tecnica_01_proceso_compraventa_1080x1350.jpg",
        "../campana/semana_1_pack_completo/piezas_tecnicas_sin_ia/tecnica_03_checklist_ph_vs_casa_1080x1350.jpg",
        "../campana/semana_1_pack_completo/piezas/dia2_carrusel_05_1080x1350.jpg"
      ],
      vertImg: "../campana/semana_1_pack_completo/piezas/dia2_vertical_1080x1920.jpg",
      blogUrl: "https://escribanofabriciorivas.com/compraventa-inmuebles-punta-del-este-1/",
      igCopy: `Desliza estas placas para ver exactamente cómo se protege tu inversión inmobiliaria en Punta del Este paso a paso:\n\n1️⃣ RESERVA (BOLETO DE RESERVA): Bloquea el inmueble y fija el precio. La seña (10%) queda en custodia notarial (Escrow) del escribano del comprador.\n2️⃣ AUDITORÍA DE 30 AÑOS: Estudio de títulos antecedentes, planos de mensura, libre deuda de impuestos, gastos comunes y construcciones en BPS.\n3️⃣ ESCRITURA DE COMPRAVENTA: Recién con todos los certificados registrales limpios se firma la transferencia y se libera el saldo.\n\nEn Uruguay, quien compra elige a su escribano de confianza. Consúltame antes de firmar la reserva.\n\nAtención directa, también a distancia si estás en otro país.\nWhatsApp directo: +598 99 431 185\n\n#CompraventaPuntaDelEste #InversionEnUruguay #EscribanoPublico #SeguridadJuridica #RealEstatePuntaDelEste`,
      storyCopy: `GUARDABLE · Los 3 pasos técnicos de una compraventa segura en Punta del Este + Qué revisa tu escribano en PH vs. Casa. Consúltame antes de firmar la reserva (+598 99 431 185).`,
      linkedinCopy: `En el derecho uruguayo, el escribano del comprador cumple una función de auditoría preventiva insustituible antes de entregar cualquier seña: retención en custodia (escrow), estudio de títulos de los últimos 30 años y control de regularidad en PH o padrón común.\n\nEn este resumen técnico detallo las 3 etapas clave de toda compraventa en Punta del Este y Maldonado.\n\nMás información en: https://escribanofabriciorivas.com/compraventa-inmuebles-punta-del-este-1/`,
      gbpCopy: `Asesoramiento notarial al comprador en Punta del Este y Maldonado: revisión de boleto de reserva, custodia de seña (escrow) y estudio de títulos de 30 años. Atención directa, también a distancia si estás en otro país. WhatsApp: +598 99 431 185.`
    },
    {
      day: "Día 3 · Reserva vs. Promesa de Compraventa (Placa Técnica XXL)",
      badge: "PLACA TÉCNICA XXL SIN IA",
      vertical: "Real Estate Comprador (Reserva vs. Promesa)",
      style: "Técnico XXL Carbón (#111111)",
      title: "Boleto de Reserva vs. Promesa de Compraventa: ¿Qué firmas primero?",
      feedImg: "../campana/semana_1_pack_completo/piezas_tecnicas_sin_ia/tecnica_02_reserva_vs_promesa_1080x1350.jpg",
      vertImg: "../campana/semana_1_pack_completo/piezas/dia3_vertical_1080x1920.jpg",
      blogUrl: "https://escribanofabriciorivas.com/boleto-reserva-punta-del-este-1/",
      igCopy: `Muchos compradores en Punta del Este confunden el Boleto de Reserva con la Promesa de Compraventa. Aquí tienes la diferencia técnica clara:\n\n• BOLETO DE RESERVA: Es el documento preliminar que bloquea la propiedad por 30 a 60 días mientras tu escribano estudia los títulos. Fija precio, plazo y multa.\n• PROMESA DE COMPRAVENTA INSCRIPTA: Se utiliza sobre todo en compras en pozo o en cuotas; al inscribirse en el Registro otorga un derecho real frente a terceros.\n• CLÁUSULA ESENCIAL: Toda reserva debe condicionar la operación a "títulos perfectos y libres de gravámenes".\n\nEnvíame el borrador por WhatsApp antes de firmar o transferir.\n+598 99 431 185 · escribanofabriciorivas.com`,
      storyCopy: `¿Boleto de Reserva o Promesa de Compraventa? Revisa la diferencia técnica antes de entregar tu seña en Punta del Este. WhatsApp +598 99 431 185.`,
      linkedinCopy: `Diferencia técnica fundamental al comprar inmuebles en Uruguay: alcance del Boleto de Reserva frente a la Promesa de Compraventa inscripta (Ley 8.733). Por qué el escribano del comprador debe intervenir antes de la firma inicial.\n\nLee más en: https://escribanofabriciorivas.com/boleto-reserva-punta-del-este-1/`,
      gbpCopy: `Revisión notarial de Boletos de Reserva y Promesas de Compraventa en Punta del Este. Protege tu seña con custodia notarial antes de firmar. Consultas por WhatsApp al +598 99 431 185.`
    },
    {
      day: "Día 4 · Clientes Extranjeros: Cómo Comprar o Vender Sin Viajar",
      badge: "PLACA TÉCNICA XXL + REEL 9:16",
      vertical: "Clientes Extranjeros / Poderes a Distancia",
      style: "Técnico XXL Piedra (#e9e7e1) + Portada Reel 9:16",
      title: "Cómo Comprar o Vender en Uruguay Sin Viajar (Poder Especial Apostillado)",
      feedImg: "../campana/semana_1_pack_completo/piezas_tecnicas_sin_ia/tecnica_04_poder_extranjeros_1080x1350.jpg",
      vertImg: "../campana/semana_1_pack_completo/piezas/dia4_reel_1080x1920.jpg",
      blogUrl: "https://escribanofabriciorivas.com/poderes-desde-el-exterior.html",
      igCopy: `Si vives en Argentina, Brasil, Estados Unidos o Europa, no necesitas viajar a Uruguay para firmar una reserva, una compraventa o una venta en Punta del Este:\n\n1️⃣ Redactamos en nuestro estudio el texto exacto del Poder Especial según la normativa uruguaya.\n2️⃣ Lo firmas ante escribano o consulado en tu ciudad y se le coloca la Apostilla de La Haya.\n3️⃣ Lo protocolizamos en el Registro de Protocolizaciones en Uruguay para que tenga plena validez en la firma.\n\nAtención directa, también a distancia si estás en otro país.\nCoordina por WhatsApp al +598 99 431 185.`,
      storyCopy: `¿Estás fuera de Uruguay? Así compras o vendes tu propiedad en Punta del Este sin viajar mediante Poder Especial Apostillado. Escríbeme al +598 99 431 185.`,
      linkedinCopy: `Gran parte de los compradores y propietarios en Punta del Este residen fuera de Uruguay. Mediante un Poder Especial redactado bajo criterio notarial uruguayo, apostillado en origen y protocolizado en nuestro país, toda la operatoria inmobiliaria se instrumenta a distancia con total validez.\n\nGuía completa: https://escribanofabriciorivas.com/poderes-desde-el-exterior.html`,
      gbpCopy: `Poderes desde el exterior y representación notarial a distancia en Punta del Este y Maldonado para clientes de Argentina, Brasil y el resto del mundo. WhatsApp: +598 99 431 185.`
    },
    {
      day: "Día 5 · Certificaciones de Firma en el Día (Punta del Este & Maldonado)",
      badge: "CAPTACIÓN RÁPIDA LOCAL",
      vertical: "Certificaciones Notariales",
      style: "Editorial Arquitectónico",
      title: "Certificación de firmas, poderes y actas con coordinación ágil por WhatsApp",
      feedImg: "../campana/semana_1_pack_completo/piezas/dia5_feed_1080x1350.jpg",
      vertImg: "../campana/semana_1_pack_completo/piezas/dia5_vertical_1080x1920.jpg",
      blogUrl: "https://escribanofabriciorivas.com/certificar-firma-punta-del-este/",
      igCopy: `¿Necesitas certificar una firma para un banco, un contrato, una carta poder o la compraventa de un vehículo en Punta del Este o Maldonado?\n\nPara que no pierdas tiempo esperando:\n1. Me envías por WhatsApp foto de tu documento y los datos del trámite.\n2. Preparamos y revisamos el documento notarial antes de que vengas.\n3. Pasas únicamente a firmar y te llevas el documento listo en el día.\n\nEscríbeme directo al WhatsApp +598 99 431 185.\n\n#CertificacionDeFirmas #EscribanoMaldonado #EscribanoPuntaDelEste #TramitesNotariales`,
      storyCopy: `Certificación de firmas en el día en Punta del Este y Maldonado. Envías los datos por WhatsApp y pasas directo a firmar: +598 99 431 185.`,
      linkedinCopy: `Agilidad notarial para particulares y empresas en Punta del Este y Maldonado: pre-revisión digital de documentación por WhatsApp para certificaciones de firmas bancarias, poderes, actas de constatación y certificados BPS/DGI.\n\nhttps://escribanofabriciorivas.com/certificar-firma-punta-del-este/`,
      gbpCopy: `Certificación de firmas en el día en Punta del Este y Maldonado para bancos, contratos, poderes y vehículos. Envía tus datos por WhatsApp al +598 99 431 185 y pasa directo a firmar.`
    }
  ],

  metricsSnapshot: {
    date: "2026-10-26",
    ads: {
      spend30d: "169,96",
      clicks30d: 135,
      reportedPrimaryConv: 6,
      realContactConv: 7,
      costPerRealContact: "24,28",
      campaigns: [
        { name: "Escribano Público en Uruguay (SMART)", status: "Activa", spend: "34,04", clicks: 57, note: "Clics baratos (0,60), pero incluye 5 'Directions' (cómo llegar) que inflan conversiones." },
        { name: "CAMPAÑA 3 (SEARCH)", status: "Activa", spend: "68,84", clicks: 61, note: "Gasta el 40% del presupuesto; requiere pasar whatsapp_click y formulario como primarias." },
        { name: "Certificaciones – PDE/Maldonado (SEARCH)", status: "Activa", spend: "67,08", clicks: 17, note: "CPC alto (≈ 3,95); cuenta 17 vistas de página como conversión secundaria." }
      ]
    },
    ga4: {
      sessions28d: 132,
      pageViews28d: 193,
      whatsappClicks28d: 15,
      formsSubmitted28d: 3,
      totalWebContacts28d: 18
    },
    searchConsole: [
      { query: "escribano punta del este", clicks: 13, impressions: 603, pos: "1,8", action: "Mantener liderazgo en Home y ficha local" },
      { query: "fabricio rivas", clicks: 7, impressions: 44, pos: "5,5", action: "Tráfico de marca directo" },
      { query: "certificar firma", clicks: 1, impressions: 2, pos: "4,0", action: "Impulsar con piezas y FAQ en /certificar-firma-punta-del-este/" },
      { query: "escribanos punta del este", clicks: 1, impressions: 56, pos: "10,6", action: "Subir de pos. 10 a top 3 con enlazado interno" },
      { query: "cuánto sale certificar una firma ante escribano", clicks: 0, impressions: 4, pos: "8,0–11,0", action: "Crear nota / sección explicando cómo se calcula el arancel notarial en Uruguay" }
    ]
  }
};
