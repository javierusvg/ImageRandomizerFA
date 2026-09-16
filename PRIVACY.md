# Política de privacidad — Image Randomizer

**Última actualización:** 16 de septiembre de 2026

Image Randomizer es una aplicación de escritorio de uso personal, desarrollada de forma individual y sin fines comerciales, que muestra imágenes de referencia visual (para inspirar dibujo y diseño de personajes) combinando carpetas locales del propio ordenador del usuario con los tableros de Pinterest de la propia cuenta del usuario.

Esta página describe qué datos se acceden, cómo se usan y cómo se protegen cuando la aplicación se conecta con la cuenta de Pinterest del usuario mediante OAuth 2.0.

## Qué datos se acceden

Cuando el usuario conecta su cuenta de Pinterest desde la aplicación, esta accede únicamente a:

- La lista de tableros propios de la cuenta autenticada.
- Los pines (imágenes) contenidos en los tableros propios que el usuario decide sincronizar.

La aplicación **no** accede a tableros ni pines de otras cuentas, no publica contenido, no crea ni modifica pines ni tableros, y no realiza ninguna acción en nombre del usuario más allá de leer sus propios tableros.

## Cómo se usan esos datos

Las imágenes de los tableros conectados se cargan directamente en memoria desde la propia aplicación, para mostrarse junto a las imágenes de las carpetas locales del usuario dentro de la interfaz. No se procesan con ningún fin distinto al de visualización personal como referencia de dibujo.

## Dónde se almacenan los datos

- El token de acceso y el token de renovación (`access_token` / `refresh_token`) que Pinterest entrega tras la autenticación se guardan **únicamente en el ordenador local del usuario**, en un archivo de configuración de la propia aplicación.
- Estos tokens **nunca se envían a ningún servidor de terceros**, ni se recopilan, ni se almacenan en ninguna base de datos externa. La comunicación ocurre exclusivamente entre el ordenador del usuario y los servidores oficiales de Pinterest (`api.pinterest.com`).
- Las imágenes de los pines no se guardan como archivo permanente en el disco del usuario; se cargan en memoria mientras la aplicación está abierta y se descartan al cerrarla.

## Qué no se hace con los datos

- No se comparten, venden, alquilan ni transfieren datos a terceros bajo ninguna circunstancia.
- No se realiza seguimiento (tracking), analítica de comportamiento ni perfiles de usuario.
- No existe ningún servidor intermedio operado por el desarrollador: la aplicación es un programa local que el usuario ejecuta en su propio equipo.
- No se accede a información personal de la cuenta de Pinterest más allá de la necesaria para leer los tableros propios (no se accede a mensajes, contactos, datos de pago ni información de perfil no relacionada con tableros/pines).

## Revocar el acceso

El usuario puede revocar el acceso de la aplicación a su cuenta de Pinterest en cualquier momento desde la configuración de aplicaciones autorizadas de su cuenta de Pinterest (`pinterest.com` → Configuración → Aplicaciones/Apps autorizadas). Al revocarlo, la aplicación deja de poder renovar el token y las carpetas de Pinterest se desactivan automáticamente en la interfaz sin afectar al resto del programa.

El usuario también puede eliminar en cualquier momento el archivo local donde se guardan los tokens, sin necesidad de desinstalar la aplicación, para borrar la sesión guardada.

## Código abierto

El código fuente completo de Image Randomizer es público y puede revisarse en su repositorio de GitHub, incluida la forma exacta en que se gestionan los tokens de Pinterest y en que se realizan las peticiones a su API.

## Contacto

Para cualquier duda sobre esta política de privacidad o sobre el tratamiento de datos de la aplicación, puede contactarse a través del perfil de GitHub del desarrollador o del correo indicado en el repositorio del proyecto.

---

## Privacy Policy (English summary)

Image Randomizer is a personal, non-commercial desktop application that displays visual reference images by combining local folders with the user's own Pinterest boards.

- The app only reads the authenticated user's own boards and pins via Pinterest's OAuth 2.0 API. It never creates, modifies, or publishes any content, and never accesses other users' boards.
- Access and refresh tokens are stored **only locally** on the user's own computer and are never transmitted to any third-party server. All communication happens directly between the user's device and Pinterest's official API (`api.pinterest.com`).
- Pinterest images are loaded into memory for display only and are not permanently saved to disk.
- No data is sold, shared, or used for tracking or analytics of any kind.
- The user can revoke access at any time from their Pinterest account settings, or delete the local token file to end the session.
- The full source code is publicly available on the project's GitHub repository.
