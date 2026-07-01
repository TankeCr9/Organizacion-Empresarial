import time
import random

# Definición de Estados de la FSM
STATE_IDLE = "STATE_IDLE"
STATE_AWAITING_AUTH = "STATE_AWAITING_AUTH"
STATE_MAIN_MENU = "STATE_MAIN_MENU"
STATE_PROCESSING_SELF_SERVICE = "STATE_PROCESSING_SELF_SERVICE"
STATE_COLLECTING_INCIDENT_DATA = "STATE_COLLECTING_INCIDENT_DATA"
STATE_SCALED_TO_HUMAN = "STATE_SCALED_TO_HUMAN"

class ChatbotSoporteFSM:
    def __init__(self):
        self.current_state = STATE_IDLE
        self.id_intentos = 0
        self.datos_incidentes = {}

    def procesar_mensaje(self, mensaje):
        print(f"\n[Estado Actual: {self.current_state}] ➔ Usuario dice: '{mensaje}'")

        # 1. ESTADO: IDLE (Inicio de sesión)
        if self.current_state == STATE_IDLE:
            print("Chatbot: Hola! Bienvenido al Soporte Técnico Integrado. Por favor, ingrese su ID de cliente corporativo.")
            self.current_state = STATE_AWAITING_AUTH
            return

        # 2. ESTADO: AWAITING_AUTH (Validación de identidad)
        if self.current_state == STATE_AWAITING_AUTH:
            if mensaje.strip().lower() == "utn123": # ID Válido simulado
                print("Chatbot: ID verificado con éxito.")
                self._mostrar_menu()
                self.current_state = STATE_MAIN_MENU
            else:
                self.id_intentos += 1
                if self.id_intentos >= 3:
                    print("⚠️ CAMINO INFELIZ: Máximo de intentos alcanzado. Reseteando sesión de forma segura.")
                    self.current_state = STATE_IDLE
                    self.id_intentos = 0
                else:
                    print(f"Chatbot: ID inválido. Intente nuevamente (Intento {self.id_intentos}/3).")
            return

        # 3. ESTADO: MAIN_MENU (Menú de opciones)
        if self.current_state == STATE_MAIN_MENU:
            # 🛡️ EXCEPCIÓN 1: Entrada de Datos Inválida (Input Mismatch)
            if mensaje not in ["1", "2", "3"]:
                print("⚠️ EXCEPCIÓN: Input Mismatch detectado.")
                print("Chatbot: Opción no válida. Por favor, seleccione un número del 1 al 3 para continuar.")
                # Se mantiene en STATE_MAIN_MENU sin romper el bot
                return

            if mensaje == "1":
                self.current_state = STATE_PROCESSING_SELF_SERVICE
                print("Chatbot: Ejecutando subrutina de blanqueo automatizado de credenciales...")
                print("Chatbot: Se ha enviado un correo con su nueva contraseña temporal. Proceso finalizado.")
                self.current_state = STATE_IDLE
            elif mensaje in ["2", "3"]:
                self.current_state = STATE_COLLECTING_INCIDENT_DATA
                print("Chatbot: Por favor, describa brevemente la falla técnica y adjunte el log o captura (o escriba 'timeout' para simular abandono):")
            return

        # 4. ESTADO: COLLECTING_INCIDENT_DATA (Carga de datos del bug)
        if self.current_state == STATE_COLLECTING_INCIDENT_DATA:
            # 🛡️ EXCEPCIÓN 2: Abandono de Sesión (Timeout de 10 min simulado)
            if mensaje.strip().lower() == "timeout":
                print("⚠️ EXCEPCIÓN: Transcurrieron 10 minutos de inactividad (Timeout).")
                print("Chatbot: Sesión expirada por inactividad. Liberando memoria del canal de chat.")
                self.current_state = STATE_IDLE
                return

            self.datos_incidentes['descripcion'] = mensaje
            print("Chatbot: Datos del incidente recopilados. Intentando registrar el ticket en el sistema...")
            
            # 🛡️ EXCEPCIÓN 3: Fallo de Persistencia (Base de Datos caída)
            try:
                # Simulo una probabilidad de caída de red/BD (aquí forzamos el error para demostrar robustez)
                print("[Intentando conectar con la Base de Datos Corporativa...]")
                raise ConnectionError("Timeout al conectar con el servidor MySQL/PostgreSQL principal.")
            
            except ConnectionError as e:
                print(f"⚠️ EXCEPCIÓN CAPTURADA (try-catch): {e}")
                print("Mecanismo de contingencia: Guardando datos en caché local estructurada (Cola de memoria).")
                print("Chatbot: 'Estamos experimentando demoras en el servidor, pero guardamos tu solicitud en caché. Un técnico de Nivel 2 te contactará a la brevedad'.")
                self.current_state = STATE_SCALED_TO_HUMAN
            return

        # 5. ESTADO: SCALED_TO_HUMAN (Ticket derivado)
        if self.current_state == STATE_SCALED_TO_HUMAN:
            print("Sistema: El canal está bloqueado con derivación activa. Esperando resolución del Técnico de Nivel 2.")
            print("[Simulación: Técnico soluciona el problema de infraestructura en servidores y cierra el ticket]")
            self.current_state = STATE_IDLE
            print("Sistema: Ticket cerrado. Volviendo a STATE_IDLE.")
            return

# --- SIMULACIÓN DEL FLUJO OPERATIVO ---
if __name__ == "__main__":
    bot = ChatbotSoporteFSM()
    
    # Flujo Feliz e inicio
    bot.procesar_mensaje("Hola")
    bot.procesar_mensaje("utn123") # Autentica
    
    # Probar Excepción 1: Input Mismatch
    bot.procesar_mensaje("hola_profe") # Opción inválida
    bot.procesar_mensaje("2") # Elige reportar bug técnico
    
    # Probar Excepción 3: Base de Datos Caída (Manejo con try-catch y caché)
    bot.procesar_mensaje("El servidor de producción no responde al hacer peticiones HTTP.")
    
    # Liberar canal humano
    bot.procesar_mensaje("Cierre Técnico")