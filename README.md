# TFI Organización Empresarial - Automatización de Procesos (Soporte Nivel 1)

Este repositorio contiene la simulación de software correspondiente al Trabajo Final Integrador de la materia **Organización Empresarial** de la Tecnicatura Universitaria en Programación (UTN).

## 🤖 Arquitectura del Automatismo (FSM)
El Chatbot de atención primaria para Soporte Técnico está diseñado bajo el patrón de una **Máquina de Estados Finitos (FSM)**, lo que garantiza que la aplicación mantenga un control estricto sobre el contexto y flujo del usuario en todo momento.

### 🛡️ Robustez y "Camino Infeliz" Implementado
El diseño de código incluye el control predictivo de tres excepciones de negocio críticas:
1. **Input Mismatch:** El sistema valida los datos de entrada en los menús, evitando desbordamientos o congelamientos ante opciones inválidas.
2. **Timeout de Sesión:** Un temporizador asincrónico retorna al sistema al estado inicial liberando memoria si el usuario abandona la interacción.
3. **Fallo de Persistencia (try-catch):** Si la base de datos se encuentra fuera de servicio, el sistema captura el error de conexión y activa una cola de contingencia local (caché en memoria) para no perder los datos del cliente.
