# ImageRandomizerFA
Image Randomizer
⚠️ Proyecto en desarrollo activo. Este README es una versión temporal, pensada para tener una página mínima y presentable mientras se completa el proyecto (empaquetado en .exe e integración con Pinterest). El README definitivo, con capturas de pantalla, explicación técnica completa y guía de uso, llegará en la versión 1.0.

Qué es
Image Randomizer es una aplicación de escritorio personal que muestra un colage aleatorio de imágenes de referencia visual (armas, edificios, animales, naturaleza, etc.) para inspirar el diseño de personajes al dibujar.

Combina imágenes de carpetas locales del propio ordenador y, próximamente, de los tableros propios de Pinterest del usuario — todas dentro de un único conjunto ("pool"), donde cada imagen tiene la misma probabilidad de aparecer sin importar de qué carpeta o tablero provenga.

Estado actual
El proyecto avanza por versiones incrementales. A día de hoy están completas:

✅ Pool unificado de imágenes desde varias carpetas locales.

✅ Grid responsive tipo justified layout (sin recortar ninguna imagen).

✅ Randomizado global y por celda individual, con zoom al hacer clic.

✅ Temporizador configurable con alarma y aviso visual.

✅ Interfaz completa en español e inglés.

✅ Gestión de carpetas de origen desde la propia interfaz, con persistencia.

En curso:

🔧 Integración con la API de Pinterest, para sincronizar tableros propios como fuente de imágenes adicional, sin necesidad de descargarlas manualmente.

Tecnología
Python + PySide6 para la interfaz.

PyInstaller para la distribución como ejecutable.

Algoritmo de layout tipo Flickr (justified layout) reescrito desde cero en Python puro.

Persistencia en JSON para carpetas de origen, idioma y (próximamente) sesión de Pinterest.

Traducciones ES/EN mediante archivos de idioma propios.

Uso previsto
Aplicación de uso personal, pensada también como proyecto de portafolio. Cuando se complete el empaquetado, se publicará como ejecutable descargable directamente desde los releases de este repositorio, sin necesidad de instalar Python ni dependencias.

Privacidad
Si conectas tu cuenta de Pinterest, consulta la política de privacidad del proyecto, donde se explica exactamente qué datos se acceden y cómo se tratan.

Licencia
Pendiente de definir para la versión 1.0.

