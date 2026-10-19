# Contexto de trabajo — Escribano Fabricio Rivas

Este repo es el sitio estático (GitHub Pages, rama `main`) del Escribano Público Fabricio Rivas, Punta del Este y Maldonado, Uruguay. Matrícula 17058/5. Quien pide los trabajos es su responsable de marketing (MBA): quiere precisión, datos cruzados y decisiones, no listas de opciones ni idas y vueltas.

## Cómo trabajar (obligatorio)

1. **Antes de recomendar nada sobre Ads o el sitio, correr la auditoría de abajo completa y mostrar la evidencia.** No reaccionar a la última pregunta: mirar el sistema entero.
2. **No suponer.** Si un dato no está en la planilla o en el repo, decirlo y pedir una sola cosa concreta. No inventar causas (ver "Supuestos ya descartados").
3. **Un solo pedido por vez al otro Claude** (el de escritorio, que opera Ads/GA4/GTM en el navegador), en un bloque de texto listo para copiar, con "mostrame antes de aplicar".
4. **Una variable por prueba**, con fecha de inicio, regla de corte y fecha de evaluación.

## Auditoría por campaña (en este orden)

1. Gasto, clics, CPC, estrategia de puja y presupuesto diario actual.
2. Términos de búsqueda: sumar el costo visible y compararlo con el gasto total (lo que falta son búsquedas ocultas). Clasificar cada término: producto real / trámite que no hace el escribano / gente del rubro / basura.
3. Palabras clave: impresiones (las de 0 impresiones son una alarma), nivel de calidad y sus 3 componentes.
4. Cuota de impresiones: perdida por presupuesto contra perdida por ranking.
5. Competencia: Información de subastas y Centro de transparencia de anuncios. Pedirlo si no está.
6. Página de destino: qué URL usa cada anuncio, interacción y tiempo por fuente y dispositivo, y si habla de lo que se buscó.
7. Resultado real: cruzar el registro manual de consultas (fecha y hora) con los clics a WhatsApp y `llamada_click` de GA4.

## Datos

- Planilla (lectura): `1MKGODCaO9v9vD77A8pKsijzKMM8-5-G9osmVCfHADvg`. Pestañas Ads (lunes), GA4 (diaria), Search Console (mensual). Para tildes en nombres de pestaña, usar el nombre exacto que devuelve la lista de pestañas.
- GTM `GTM-KKH9D4KS`, GA4 `G-GW07MKDCFP`. Eventos reales: `whatsapp_click`, `llamada_click` (desde el 19/10/2026), `form_submit`. `formulario_contacto_enviado` está inflado: no usarlo.
- Las campañas inteligentes no se leen por script.
- La verdad es el registro manual de consultas reales (unas 5 por mes).

## Negocio y decisiones tomadas

- El cliente de real estate es el **comprador** que llega por una inmobiliaria (que trabaja para el vendedor) y quiere su propio escribano. Fabricio no tiene local a la calle: la confianza tiene que ser verificable (matrícula, reseñas, proceso claro).
- Certificaciones deberían ser la caja diaria. BPS y DGI existen, pero no son el foco.
- No hay campaña internacional: los extranjeros llegan gratis (ChatGPT, orgánico). Ubicación de Ads en "Presencia" desde el 19/10/2026; se evalúa el 18/11/2026.
- Presupuesto y puja no se tocan hasta el 18/11/2026.
- No importar a Ads conversiones de "toque" (clics). Estrategia: Maximizar clics.

## Tono y lenguaje

- Español: tratar de **tú con voseo rioplatense** ("coordinás", "tu firma"). Nunca usted.
- Tono sobrio, notarial, sereno. Sin consignas comerciales ("de su lado"), sin comparaciones con inmobiliarias o colegas, sin testimonios inventados.
- Portugués: **siempre de Brasil**. Inglés: neutro.
- No mencionar ARTOWER ni "trabajo en persona": decir "atención directa, también a distancia si estás en otro país".
- Fabricio graba videos solo en español (con subtítulos ES/EN).

## Supuestos ya descartados (no repetir)

- Los pedidos de "cómo llegar" de Maps (318) no son clientes: son gente que va al edificio o al shopping.
- Las inmobiliarias no son el cliente.
- "Escribanos habilitados" no es una negativa: lo buscan personas que verifican a un escribano.
- Timbres notariales y registros notariales no van como negativas.
- No agregar recurso de ubicación en Ads.

## Sitio

- Imágenes: un workflow (`.github/workflows/optimize-images.yml`) las comprime solo al subirlas. Nunca subir imágenes de más de 300 KB.
- Artículos nuevos de Criterio: borradores en la rama `claude/criterio-borradores`. Se publican solo con el OK de la usuaria.
