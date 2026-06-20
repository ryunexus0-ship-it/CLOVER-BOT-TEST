# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import random
import json
import os
import asyncio
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

bot = commands.Bot(command_prefix="+", intents=intents, case_insensitive=True)

# =========================================================================
# 🗄️ CONFIGURACIÓN DE BASE DE DATOS (PostgreSQL - Railway)
# Agrega DATABASE_URL en las variables de entorno de Railway.
# =========================================================================

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

def init_db():
    """Crea la tabla si no existe y migra datos del JSON local si los hay."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bot_data (
                    id TEXT PRIMARY KEY,
                    value JSONB NOT NULL
                )
            """)
        conn.commit()

    # Migración automática desde el JSON local (solo se ejecuta una vez)
    json_path = "usuarios_rp.json"
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                datos = json.load(f)
            datos_actuales = cargar_datos()
            # Solo migra si la DB está vacía
            if not datos_actuales or datos_actuales == _defaults():
                guardar_datos(datos)
                os.rename(json_path, json_path + ".migrado")
                print("✅ Datos migrados desde usuarios_rp.json a PostgreSQL.")
        except Exception as e:
            print(f"⚠️ No se pudo migrar el JSON: {e}")

# =========================================================================
# 🔮 CONFIGURACIÓN DE SPINS - DIFICULTAD BALANCEADA (MÁS ACCESIBLE)
# =========================================================================

RAZAS = {
    "Humano": {"rareza": "🟢 Común", "peso": 0.55, "desc": "La raza predominante en el Reino de Clover. Poseen gran adaptabilidad.", "gif": "https://media.tenor.com/7gNl6lH1x30AAAAC/black-clover-asta.gif"},
    "Medio-Elfo": {"rareza": "🔵 Raro", "peso": 0.20, "desc": "Sangre híbrida que combina el ingenio humano con el maná elfo.", "gif": "https://media.tenor.com/k6lP0q9BvzoAAAAC/yuno-black-clover.gif"},
    "Enano": {"rareza": "🔵 Raro", "peso": 0.14, "desc": "Raza subterránea experta en la creación física y la magia de tierra/minerales.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Elfo": {"rareza": "🟡 Legendario", "peso": 0.07, "desc": "Criaturas ancestrales bendecidas por el maná con inmensas reservas mágicas.", "gif": "https://media.tenor.com/k6lP0q9BvzoAAAAC/yuno-black-clover.gif"},
    "Demonio": {"rareza": "🔴 Mítico", "peso": 0.02, "desc": "Seres del inframundo portadores de magia negativa y poder maldito devastador.", "gif": "https://media.tenor.com/T_7U9kX8t-AAAAAC/black-clover-licht.gif"},
    "Espíritu": {"rareza": "🔴 Mítico", "peso": 0.015, "desc": "Entidades divinas elementales que eligen a magos excepcionales.", "gif": "https://media.tenor.com/NOnw3uT07U8AAAAC/sylph-black-clover.gif"},
    "Humano del Inframundo": {"rareza": "⚫ Prohibido", "peso": 0.004, "desc": "Humanos alterados por contratos demoníacos oscuros.", "gif": "https://media.tenor.com/Z4_ZlI-8hJMAAAAd/zenon-zogratis-zenon.gif"},
    "Híbrido Oscuro": {"rareza": "⚫ Prohibido", "peso": 0.001, "desc": "La unión prohibida de dos fuerzas incompatibles en un solo ser.", "gif": "https://media.tenor.com/Z4_ZlI-8hJMAAAAd/zenon-zogratis-zenon.gif"}
}

GRIMORIOS = {
    "Grimorio de 3 Hojas": {"rareza": "🟢 Común", "peso": 0.60, "desc": "Símbolo de integridad, esperanza y amor. El estándar de los Caballeros Mágicos.", "gif": "https://media.tenor.com/wP0Cg70L4QYAAAAC/noelle-grimoire.gif"},
    "Grimorio de las Palas": {"rareza": "🔵 Raro", "peso": 0.11, "desc": "Procedente del helado Reino de la Pala, ideal para magias oscuras.", "gif": "https://media.tenor.com/b28S75W9e3IAAAAC/black-clover-grimoire.gif"},
    "Grimorio de los Diamantes": {"rareza": "🔵 Raro", "peso": 0.11, "desc": "Procedente del Reino del Diamante, enfocado en magias de alta densidad.", "gif": "https://media.tenor.com/4B68jCunm7UAAAAC/black-clover-grimoires.gif"},
    "Grimorio de los Corazones": {"rareza": "🔵 Raro", "peso": 0.10, "desc": "Procedente del Reino del Corazón, con técnicas mágicas naturales y fluidas.", "gif": "https://media.tenor.com/wP0Cg70L4QYAAAAC/noelle-grimoire.gif"},
    "Grimorio de 4 Hojas": {"rareza": "🟡 Legendario", "peso": 0.05, "desc": "En la cuarta hoja reside la buena fortuna. Bendecido por el maná.", "gif": "https://media.tenor.com/qU_M729lVBgAAAAC/yuno-grimoire.gif"},
    "Grimorio de 5 Hojas": {"rareza": "🔴 Mítico", "peso": 0.02, "desc": "En las primeras tres reside la fe, la esperanza y el amor. En la cuarta la fortuna... y en la quinta el Demonio.", "gif": "https://media.tenor.com/asta-demon.gif"},
    "Sin Grimorio": {"rareza": "⚫ Especial", "peso": 0.01, "desc": "No posees libro físico, tu magia se manifiesta de maneras exóticas o nulas.", "gif": "https://media.tenor.com/b7201wR38vAAAAAC/asta-demon.gif"}
}

MAGIAS = {
    "Fuego": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Alta potencia destructiva que consume todo a su paso.", "gif": "https://media.tenor.com/A6m2wH_4N00AAAAC/mereoleona-vermillion-black-clover.gif"},
    "Agua": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Gran versatilidad fluida, capaz de sanar o atacar ferozmente.", "gif": "https://media.tenor.com/wP0Cg70L4QYAAAAC/noelle-grimoire.gif"},
    "Viento": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Ráfagas veloces, tornados cortantes y movilidad mágica superior.", "gif": "https://media.tenor.com/N7bVndmU4jIAAAAC/yuno-grimoire.gif"},
    "Tierra": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Resistencia absoluta, creación de muros y control del terreno.", "gif": "https://media.tenor.com/6Cg6y7_b-6MAAAAC/black-clover-sol.gif"},
    "Hielo": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Control de masas, congelamiento y generación de defensas de escarcha.", "gif": "https://media.tenor.com/R_W9ZclE05cAAAAC/black-clover-ice.gif"},
    "Planta": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Creación de vegetación, raíces restrictivas y amarres tácticos.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Barro": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Terreno pantanoso que drena la agilidad y atrapa a los oponentes.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Humo": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Estrategias de evasión y asfixia nublando la vista del campo.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Roca": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Proyectiles contundentes y corazas pesadas de piedra mineral.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Cadena": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Cadenas de hierro mágico perfectas para restringir y amarrar magos.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Dados": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Tus hechizos ganan potencia según la suerte del tiro numérico obtenido.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Curación": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Recuperación constante de heridas y vitalidad en el campo.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Ceniza": {"rareza": "🟢 Común", "peso": 0.04, "desc": "Hechizos trampa retardados hechos de pólvora y residuos calcinados.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Rayo": {"rareza": "🔵 Raro", "peso": 0.02, "desc": "Velocidad eléctrica inigualable y ataques perforantes de alto impacto.", "gif": "https://media.tenor.com/T_7U9kX8t-AAAAAC/black-clover-licht.gif"},
    "Arena": {"rareza": "🔵 Raro", "peso": 0.02, "desc": "Invocación de tormentas de arena compacta y golems pesados.", "gif": "https://media.tenor.com/6Cg6y7_b-6MAAAAC/black-clover-sol.gif"},
    "Oscuridad": {"rareza": "🔵 Raro", "peso": 0.02, "desc": "Atrae y absorbe hechizos enemigos distorsionando el espacio.", "gif": "https://media.tenor.com/vH_w96K7QAAAAC/yami-black-clover.gif"},
    "Hilos": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Manipulación de hilos invisibles para controlar cuerpos o tejer defensas.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Permutación": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Intercambia propiedades físicas de los objetos o magias lanzadas.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Combinación": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Permite enlazar hechizos propios con los de tus aliados eficazmente.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Algodón": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Creación de almohadillas mágicas que amortiguan impactos y atrapan.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Alimentos": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Cocina mágica capaz de restaurar las reservas de maná de un equipo.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Escamas": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Armadura de escamas que altera el peso de la magia enemiga.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Canto": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Ondas sonoras mágicas que potencian aliados o confunden rivales.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Sello": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Habilidad experta para bloquear portales, heridas o hechizos rivales.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Brújula": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Redirecciona y desvía cualquier hechizo de proyectil que te lancen.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Sangre": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Manipulación de fluidos biológicos y control corporal bajo maldición.", "gif": "https://media.tenor.com/gK96GZas9ksAAAAC/witch-queen-black-clover.gif"},
    "Maldición": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Hechizos de desgaste continuo que impiden la sanación del objetivo.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Veneno": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Nubes tóxicas ácidas que merman los atributos físicos gradualmente.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Sombra": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Viaja a través de la oscuridad de las sombras y restringe movimientos.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Modificación": {"rareza": "🔵 Raro", "peso": 0.015, "desc": "Altera las propiedades mágicas elementales de los ataques en combate.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Cristal": {"rareza": "🟣 Épico", "peso": 0.01, "desc": "Genera estructuras de gemas de alta densidad sumamente duras.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Espejos": {"rareza": "🟣 Épico", "peso": 0.01, "desc": "Refleja ataques enemigos duplicando o clonando su trayectoria.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Árbol Mitológico": {"rareza": "🟣 Épico", "peso": 0.01, "desc": "Invoca raíces gigantescas del árbol del mundo para sanación masiva.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Sueños": {"rareza": "🟣 Épico", "peso": 0.01, "desc": "Atrapa mentes enemigas dentro de una dimensión donde controlas las reglas.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Huesos": {"rareza": "🟣 Épico", "peso": 0.01, "desc": "Creación y endurecimiento de osamentas afiladas para defensa y ataque.", "gif": "https://media.tenor.com/Z4_ZlI-8hJMAAAAd/zenon-zogratis-zenon.gif"},
    "Carne": {"rareza": "🟣 Épico", "peso": 0.01, "desc": "Regeneración instantánea y alteración de la masa muscular física.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Imitación": {"rareza": "🟣 Épico", "peso": 0.01, "desc": "Copia a la perfección hechizos enemigos tras tocarlos directamente.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Luz": {"rareza": "🟡 Legendario", "peso": 0.006, "desc": "Velocidad divina destellante y espadas de fotones purificadoras.", "gif": "https://media.tenor.com/wP0Cg70L4QYAAAAC/noelle-grimoire.gif"},
    "Espacio": {"rareza": "🟡 Legendario", "peso": 0.006, "desc": "Apertura de portales interdimensionales y desgarradura espacial.", "gif": "https://media.tenor.com/GzB9Gj9yA-4AAAAC/langris-black-clover.gif"},
    "Pintura": {"rareza": "🟡 Legendario", "peso": 0.006, "desc": "Versatilidad artística capaz de recrear cualquier elemento con maná.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Gravedad": {"rareza": "🔴 Mítico", "peso": 0.002, "desc": "Manipulación del peso gravitatorio; aplasta ejércitos y dobla espacio.", "gif": "https://media.tenor.com/Z4_ZlI-8hJMAAAAd/zenon-zogratis-zenon.gif"},
    "Almas": {"rareza": "🔴 Mítico", "peso": 0.002, "desc": "Toca y altera los conceptos o la memoria espiritual de un objetivo.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Causalidad": {"rareza": "🔴 Mítico", "peso": 0.001, "desc": "Rompe la causa y efecto. Regresa el daño recibido directo a su origen.", "gif": "https://i.imgur.com/vH_w9Wz.gif"}
}

DEMONIOS = {
    "Enjambre Menor Rojo": {"rareza": "🟢 Rango Bajo", "peso": 0.30, "desc": "Un demonio menor común que imbuye fuego infernal básico en tus ataques.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Enjambre Menor Alado": {"rareza": "🟢 Rango Bajo", "peso": 0.30, "desc": "Demonio inferior que concede vuelo rústico y ráfagas de viento corrupto.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Abominación Básica": {"rareza": "🟢 Rango Bajo", "peso": 0.20, "desc": "Miasma oscuro de bajo nivel que drena lentamente la estamina de los rivales.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Gimodelo": {"rareza": "🔵 Rango Medio", "peso": 0.03, "desc": "Contrato de Nacht. Otorga la Unión de Sombra con características físicas y fuerza de Toro.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Slotos": {"rareza": "🔵 Rango Medio", "peso": 0.03, "desc": "Contrato de Nacht. Otorga la Unión de Sombra con la resistencia masiva del Caballo.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Plumede": {"rareza": "🔵 Rango Medio", "peso": 0.03, "desc": "Contrato de Nacht. Otorga agilidad felina suprema y sigilo absoluto entre las sombras.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Walgner": {"rareza": "🔵 Rango Medio", "peso": 0.03, "desc": "Contrato de Nacht. Capaz de emitir chirridos ultrasónicos que aturden y confunden rivales.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Zagred": {"rareza": "🔴 Alto Rango", "peso": 0.01, "desc": "El demonio de la palabra (Kotodama). Todo lo que pronuncia se materializa en el campo.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Lucifugus": {"rareza": "🔴 Alto Rango", "peso": 0.01, "desc": "Portador de un aura de destrucción absoluta que aniquila la vida a su alrededor.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Liebe": {"rareza": "⭐ Especial", "peso": 0.01, "desc": "El demonio de la Anti-Magia. Cancela, anula y rebota cualquier tipo de manifestación mágica.", "gif": "https://media.tenor.com/b7201wR38vAAAAAC/asta-demon.gif"},
    "Megicula": {"rareza": "👑 Supremo", "peso": 0.004, "desc": "La deidad de las maldiciones de sangre y acero. Desgasta y bloquea curaciones enemigas.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Adrammelech": {"rareza": "👑 Supremo", "peso": 0.004, "desc": "Un demonio de alto rango sumamente analítico dotado de una velocidad y evasión absurda.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Lilith": {"rareza": "👑 Supremo", "peso": 0.003, "desc": "Demonio gemelo del hielo supremo. Capaz de congelar incluso conceptos intangibles.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Naamah": {"rareza": "👑 Supremo", "peso": 0.003, "desc": "Demonio gemelo del fuego supremo. Sus llamas calcinan la magia y reducen todo a cenizas.", "gif": "https://i.imgur.com/vH_w9Wz.gif"},
    "Lucifero": {"rareza": "👑 Supremo", "peso": 0.001, "desc": "El Rey del Inframundo. Su magia de Gravedad aplasta ejércitos enteros sin esfuerzo.", "gif": "https://media.tenor.com/Z4_ZlI-8hJMAAAAd/zenon-zogratis-zenon.gif"},
    "Beelzebub": {"rareza": "👑 Supremo", "peso": 0.0005, "desc": "Señor de los cubos espaciales. Capaz de desgarrar y controlar las dimensiones del mapa.", "gif": "https://media.tenor.com/Z4_ZlI-8hJMAAAAd/zenon-zogratis-zenon.gif"},
    "Astaroth": {"rareza": "👑 Supremo", "peso": 0.0005, "desc": "Demonio del Tiempo. Su presencia congela o acelera el envejecimiento de los hechizos.", "gif": "https://media.tenor.com/b7201wR38vAAAAAC/asta-demon.gif"}
}

TIENDA_ITEMS_BASE = {
    "capa": {"nombre": "Capa de Escuadrón", "precio": 1500, "desc": "Otorga +5% de defensa general en rol.", "es_arma": False},
    "pocion": {"nombre": "Poción de Maná", "precio": 500, "desc": "Recupera energía mágica instantáneamente.", "es_arma": False},
    "anillo": {"nombre": "Anillo de Maná", "precio": 4000, "desc": "Estabiliza hechizos haciéndolos más precisos.", "es_arma": False},
    "espada_antigua": {"nombre": "Espada de Acero Antiguo", "precio": 3500, "desc": "Arma equipable lista para encantar con estadísticas.", "es_arma": True}
}

# =========================================================================
# 🧬 STATS BASE POR RAZA
# Estos son los stats que se suman al obtener una raza y se restan al cambiarla.
# =========================================================================
STATS_POR_RAZA = {
    "Humano":                {"fuerza": 5, "vida": 5, "agilidad": 5, "suerte": 5},
    "Medio-Elfo":            {"fuerza": 4, "vida": 5, "agilidad": 6, "suerte": 5},
    "Enano":                 {"fuerza": 9, "vida": 6, "agilidad": 2, "suerte": 3},
    "Elfo":                  {"fuerza": 3, "vida": 4, "agilidad": 7, "suerte": 6},
    "Demonio":               {"fuerza": 8, "vida": 7, "agilidad": 4, "suerte": 1},
    "Espíritu":              {"fuerza": 1, "vida": 2, "agilidad": 9, "suerte": 8},
    "Humano del Inframundo": {"fuerza": 9, "vida": 8, "agilidad": 6, "suerte": 5},
    "Híbrido Oscuro":        {"fuerza": 5, "vida": 6, "agilidad": 8, "suerte": 3},
}

def aplicar_stats_raza(pj: dict, raza_nueva: str, raza_anterior: str = None):
    """
    Quita los stats de la raza anterior y aplica los de la nueva.
    No toca los puntos que el jugador haya invertido manualmente.
    Consulta tanto razas base como razas personalizadas guardadas en la DB.
    """
    datos = cargar_datos()
    razas_custom = datos.get("razas_custom", {})
    pool_stats = {**STATS_POR_RAZA, **{k: v["stats"] for k, v in razas_custom.items()}}

    if raza_anterior and raza_anterior in pool_stats:
        stats_viejos = pool_stats[raza_anterior]
        for stat, valor in stats_viejos.items():
            pj[stat] = max(0, pj.get(stat, 0) - valor)

    if raza_nueva in pool_stats:
        stats_nuevos = pool_stats[raza_nueva]
        for stat, valor in stats_nuevos.items():
            pj[stat] = pj.get(stat, 0) + valor

LISTA_RANGOS = [
    "Mago normal", "Mago", "Caballero Mágico junior", "Caballero Mágico Intermedio",
    "Caballero Mágico Superior", "Caballero Mágico maximo", "Rey mago"
]

def calcular_rango(puntos: int) -> str:
    indice = puntos // 1000
    if indice >= len(LISTA_RANGOS): return LISTA_RANGOS[-1]
    return LISTA_RANGOS[indice]

def _defaults():
    return {
        "ordenes": {}, "admins": [], "co_owners": [], "canal_logs": None,
        "comandos_creados": {}, "tienda_personalizada": {}, "tablero_misiones": [],
        "razas_custom": {}
    }

def cargar_datos():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT value FROM bot_data WHERE id = 'global'")
                row = cur.fetchone()
                if row:
                    datos = row[0]
                    datos.setdefault("ordenes", {})
                    datos.setdefault("admins", [])
                    datos.setdefault("co_owners", [])
                    datos.setdefault("canal_logs", None)
                    datos.setdefault("comandos_creados", {})
                    datos.setdefault("tienda_personalizada", {})
                    datos.setdefault("tablero_misiones", [])
                    datos.setdefault("razas_custom", {})
                    return datos
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")
    return _defaults()

def guardar_datos(datos):
    datos.setdefault("ordenes", {})
    datos.setdefault("admins", [])
    datos.setdefault("co_owners", [])
    datos.setdefault("canal_logs", None)
    datos.setdefault("comandos_creados", {})
    datos.setdefault("tienda_personalizada", {})
    datos.setdefault("tablero_misiones", [])
    datos.setdefault("razas_custom", {})
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO bot_data (id, value)
                    VALUES ('global', %s)
                    ON CONFLICT (id) DO UPDATE SET value = EXCLUDED.value
                """, (Json(datos),))
            conn.commit()
    except Exception as e:
        print(f"❌ Error al guardar datos: {e}")

def plantilla_personaje():
    return {
        "nombre_rp": "Sin registrar",
        "raza": "Ninguna", "magia": "Ninguna", "grimorio": "Ninguno", "demonio": "Ninguno",
        "rango": "Mago normal", "puntos": 0, "misiones_hechas": [],
        "dinero": 1000, "inventario": [],
        "puntos_stats": 20, "fuerza": 0, "vida": 0, "agilidad": 0, "suerte": 0,
        "armas_equipadas": {}, "personaje_exclusivo": "Ninguno"
    }

def verificar_usuario(user_id, datos):
    uid = str(user_id)
    if uid not in datos:
        datos[uid] = {
            "slot_activo": "1", "rerolls": 5,
            "spins_realizados": {"raza": False, "magia": False, "grimorio": False, "demonio": False},
            "slots": {"1": plantilla_personaje(), "2": plantilla_personaje(), "3": plantilla_personaje()}
        }
    user = datos[uid]
    user.setdefault("spins_realizados", {"raza": False, "magia": False, "grimorio": False, "demonio": False})
    user["spins_realizados"].setdefault("demonio", False)
        
    for s in ["1", "2", "3"]:
        if s not in user["slots"]: user["slots"][s] = plantilla_personaje()
        pj = user["slots"][s]
        pj.setdefault("demonio", "Ninguno")
        pj.setdefault("nombre_rp", "Sin registrar")
        pj.setdefault("dinero", 1000)
        pj.setdefault("inventario", [])
        pj.setdefault("puntos", 0)
        pj.setdefault("misiones_hechas", [])
        pj.setdefault("puntos_stats", 20)
        pj.setdefault("fuerza", 0)
        pj.setdefault("vida", 0)
        pj.setdefault("agilidad", 0)
        pj.setdefault("suerte", 0)
        pj.setdefault("armas_equipadas", {})
        pj.setdefault("personaje_exclusivo", "Ninguno")
        if pj.get("rango") not in LISTA_RANGOS: pj["rango"] = "Mago normal"

def es_admin_bot(ctx):
    datos = cargar_datos()
    return ctx.author.guild_permissions.administrator or ctx.author.id in datos.get("admins", []) or ctx.author.id == bot.owner_id or ctx.author.id in datos.get("co_owners", [])

def es_owner_o_coowner():
    async def predicate(ctx):
        datos = cargar_datos()
        es_co_owner = ctx.author.id in datos.get("co_owners", [])
        es_owner_real = ctx.author.id == bot.owner_id
        if es_owner_real or es_co_owner: return True
        raise commands.NotOwner("No tienes rango de Creador o Co-Owner.")
    return commands.check(predicate)

def obtener_demonios_ocupados(datos_totales):
    ocupados = set()
    for uid, info in datos_totales.items():
        if uid in ["ordenes", "admins", "co_owners", "canal_logs", "comandos_creados", "tienda_personalizada", "tablero_misiones"]: continue
        slots = info.get("slots", {})
        for s_id, pj in slots.items():
            dem = pj.get("demonio", "Ninguno")
            if dem and dem != "Ninguno":
                ocupados.add(dem)
    return ocupados

async def asignar_rol_automatico(ctx, tipo: str, nombre_objeto: str):
    try:
        lista_remover = []
        if tipo == "raza":
            lista_remover = [r.lower() for r in RAZAS.keys()]
        elif tipo == "magia":
            lista_remover = [m.lower() for m in MAGIAS.keys()]
        elif tipo == "grimorio":
            lista_remover = [g.lower() for g in GRIMORIOS.keys()]
        elif tipo == "demonio":
            lista_remover = [d.lower() for d in DEMONIOS.keys()]

        roles_a_remover = []
        for role in ctx.author.roles:
            for item in lista_remover:
                if item in role.name.lower() and nombre_objeto.lower() not in role.name.lower():
                    roles_a_remover.append(role)
                    break
        if roles_a_remover:
            await ctx.author.remove_roles(*roles_a_remover)

        for role in ctx.guild.roles:
            if nombre_objeto.lower() in role.name.lower():
                await ctx.author.add_roles(role)
                break
    except:
        pass

# =========================================================
# MODULO DE LOGICA DE SPINS
# =========================================================
async def ejecutar_spin_logica(ctx, tipo: str, es_reroll: bool):
    type_clean = tipo.lower().strip()
    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    user = datos[str(ctx.author.id)]
    slot = user["slot_activo"]
    pj = user["slots"][slot]

    if type_clean == "demonio":
        if pj.get("grimorio") != "Grimorio de 5 Hojas":
            return await ctx.send(f"❌ {ctx.author.mention}, ¡tu grimorio actual es `{pj.get('grimorio')}`! Necesitas poseer el **Grimorio de 5 Hojas**.")

    if not es_reroll and user["spins_realizados"].get(type_clean, False):
        return await ctx.send(f"⚠️ Usa `+rr {type_clean}` para cambiar tu {type_clean}.")
    if es_reroll:
        if user["rerolls"] <= 0: return await ctx.send("❌ Sin Rerolls globales disponibles.")
        user["rerolls"] -= 1

    if type_clean == "raza": pool = RAZAS
    elif type_clean == "magia": pool = MAGIAS
    elif type_clean == "grimorio": pool = GRIMORIOS
    else: pool = DEMONIOS

    # Si es raza, mezclar con razas personalizadas
    if type_clean == "raza":
        razas_custom = datos.get("razas_custom", {})
        pool = {**RAZAS, **{k: {**v, "peso": v["peso"]} for k, v in razas_custom.items()}}

    nombres = list(pool.keys())
    pesos = [pool[n]["peso"] for n in nombres]
    elegido = "Ninguno"
    
    if type_clean == "demonio":
        demonios_ocupados = obtener_demonios_ocupados(datos)
        intentos = 0
        while intentos < 100:
            intentos += 1
            candidato = random.choices(nombres, weights=pesos, k=1)[0]
            if pool[candidato]["rareza"] == "🟢 Rango Bajo":
                elegido = candidato
                break
            if candidato not in demonios_ocupados:
                elegido = candidato
                break
        if elegido == "Ninguno": elegido = "Abominación Básica"
    else:
        elegido = random.choices(nombres, weights=pesos, k=1)[0]
    
    pj[type_clean] = elegido
    user["spins_realizados"][type_clean] = True

    # Aplicar stats base si el spin es de raza
    if type_clean == "raza":
        raza_anterior = pj.get("raza_anterior", None)
        aplicar_stats_raza(pj, elegido, raza_anterior)
        pj["raza_anterior"] = elegido

    guardar_datos(datos)

    await asignar_rol_automatico(ctx, type_clean, elegido)

    embed = discord.Embed(title=f"✨ ¡Giro de {type_clean.upper()}! ✨", color=discord.Color.from_rgb(47, 49, 54), description=f"*{pool[elegido]['desc']}*")
    embed.add_field(name="🔮 Obtenido:", value=f"**{elegido}**").add_field(name="⭐ Rareza:", value=f"`{pool[elegido]['rareza']}`")
    if type_clean == "raza":
        datos_check = cargar_datos()
        razas_custom = datos_check.get("razas_custom", {})
        pool_stats_spin = {**STATS_POR_RAZA, **{k: v["stats"] for k, v in razas_custom.items()}}
        if elegido in pool_stats_spin:
            s = pool_stats_spin[elegido]
            embed.add_field(
                name="📊 Stats de Raza:",
                value=f"💪 Fuerza `+{s['fuerza']}` | ❤️ Vida `+{s['vida']}` | ⚡ Agilidad `+{s['agilidad']}` | 🍀 Suerte `+{s['suerte']}`",
                inline=False
            )
    embed.set_image(url=pool[elegido]["gif"])
    await ctx.send(content=ctx.author.mention, embed=embed)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def spin(ctx, tipo: str = None):
    if not tipo or tipo.lower() not in ["raza", "magia", "grimorio", "demonio"]: 
        return await ctx.send("❌ Uso: `+spin raza/magia/grimorio/demonio`")
    await ejecutar_spin_logica(ctx, tipo, False)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def rr(ctx, tipo: str = None):
    if not tipo or tipo.lower() not in ["raza", "magia", "grimorio", "demonio"]: 
        return await ctx.send("❌ Uso: `+rr raza/magia/grimorio/demonio`")
    await ejecutar_spin_logica(ctx, tipo, True)

# =========================================================
# NUEVOS COMANDOS: ENTRENAMIENTO Y ASCENDER
# =========================================================

@bot.command(name="entrenamiento", aliases=["entrenar"])
@commands.cooldown(1, 30, commands.BucketType.user)
async def entrenamiento(ctx):
    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    slot = datos[str(ctx.author.id)]["slot_activo"]
    pj = datos[str(ctx.author.id)]["slots"][slot]
    
    stats_ganados = random.randint(5, 15)
    pj["puntos_stats"] += stats_ganados
    guardar_datos(datos)
    
    embed = discord.Embed(
        title="⚔️ ¡Sesión de Entrenamiento Finalizada! ⚔️",
        description=f"{ctx.author.mention}, has completado tus ejercicios físicos y de control de maná en el **Slot {slot}**.",
        color=discord.Color.from_rgb(255, 127, 0)
    )
    embed.add_field(name="✨ Puntos de Stats Obtenidos:", value=f"`+{stats_ganados} Puntos Libres`", inline=True)
    embed.set_footer(text="Usa +addstat [fuerza/vida/agilidad/suerte] [cantidad] para asignarlos.")
    await ctx.send(embed=embed)

@bot.command(name="acender", aliases=["ascender"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def acender(ctx):
    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    slot = datos[str(ctx.author.id)]["slot_activo"]
    pj = datos[str(ctx.author.id)]["slots"][slot]
    
    rango_actual = pj.get("rango", "Mago normal")
    
    try:
        idx_actual = LISTA_RANGOS.index(rango_actual)
    except ValueError:
        idx_actual = 0
        pj["rango"] = LISTA_RANGOS[0]

    if idx_actual >= len(LISTA_RANGOS) - 1:
        return await ctx.send(f"👑 {ctx.author.mention}, ¡ya has alcanzado el rango máximo absoluto: **{rango_actual}**!")

    if pj["puntos"] < 1000:
        return await ctx.send(f"❌ {ctx.author.mention}, requieres al menos **1000 puntos de XP** acumulados para ascender. Actualmente tienes `{pj['puntos']} Pts`.")

    pj["puntos"] -= 1000
    nuevo_rango = LISTA_RANGOS[idx_actual + 1]
    pj["rango"] = nuevo_rango
    guardar_datos(datos)

    embed = discord.Embed(
        title="🎖️ ¡Ascenso Imperial Otorgado! 🎖️",
        description=f"¡Felicidades {ctx.author.mention}! Tus méritos han sido reconocidos en el **Slot {slot}**.",
        color=discord.Color.from_rgb(0, 204, 255)
    )
    embed.add_field(name="📉 Costo:", value="`-1000 Pts`", inline=True)
    embed.add_field(name="👑 Nuevo Rango:", value=f"**{nuevo_rango}**", inline=True)
    await ctx.send(embed=embed)


# Panel Interactivos de Perfil
class PerfilView(discord.ui.View):
    def __init__(self, miembro, ctx):
        super().__init__(timeout=60.0)
        self.miembro = miembro
        self.ctx = ctx
        self.pagina = 1

    async def generar_embed(self):
        datos_usuarios = cargar_datos()
        verificar_usuario(self.miembro.id, datos_usuarios)
        user = datos_usuarios[str(self.miembro.id)]
        slot = user["slot_activo"]
        pj = user["slots"][slot]

        if self.pagina == 1:
            embed = discord.Embed(title=f"📖 Ficha de Rol - {self.miembro.display_name}", color=discord.Color.from_rgb(47, 49, 54))
            embed.description = f"🎴 **Slot Activo:** {slot}\n👤 **Nombre de Rol:** {pj['nombre_rp']}\n👑 **Exclusivo:** {pj.get('personaje_exclusivo', 'Ninguno')}\n\n🧬 **Raza:**\n{pj['raza']}\n\n🪄 **Magia:**\n{pj['magia']}\n\n🍀 **Grimorio:**\n{pj['grimorio']}\n\n😈 **Demonio Alojado:**\n`{pj.get('demonio', 'Ninguno')}`\n\n🎟️ **Spins (RR):** ⭐ {user['rerolls']}\n💎 **Skill Points:** `{pj.get('skill_points', 0)} SP`"
            return embed
        elif self.pagina == 2:
            embed = discord.Embed(title=f"💰 Billetera e Inventario", color=discord.Color.gold())
            inv_lista = ", ".join([f"`{i}`" for i in pj["inventario"]]) if pj["inventario"] else "*Vacío*"
            armas_desc = ""
            if pj["armas_equipadas"]:
                for arma, stats in pj["armas_equipadas"].items():
                    encantos = [f"{k.capitalize()}+{v}" for k, v in stats.items() if v > 0]
                    armas_desc += f"⚔️ **{arma}** {f'({', '.join(encantos)})' if encantos else '*(Sin encantar)*'}\n"
            else: armas_desc = "*Ninguna*"
            embed.description = f"🎴 **Slot Activo:** {slot}\n\n🪙 **Yenes:** {pj['dinero']} ¥\n\n🎒 **Mochila:**\n{inv_lista}\n\n⚔️ **Armamento:**\n{armas_desc}\n👑 **Rango:** {pj['rango']} ({pj['puntos']} Pts)"
            return embed
        elif self.pagina == 3:
            return discord.Embed(title=f"⚔️ Historial de Misiones", description="\n".join([f"✅ {m}" for m in pj["misiones_hechas"][-5:]]) if pj["misiones_hechas"] else "*Sin misiones*", color=discord.Color.purple())

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.grey)
    async def boton_atras(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("❌ No puedes controlar esto.", ephemeral=True)
        self.pagina = 3 if self.pagina == 1 else self.pagina - 1
        await interaction.response.edit_message(embed=await self.generar_embed(), view=self)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.grey)
    async def boton_siguiente(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("❌ No puedes controlar esto.", ephemeral=True)
        self.pagina = 1 if self.pagina == 3 else self.pagina + 1
        await interaction.response.edit_message(embed=await self.generar_embed(), view=self)

# Sinopsis de comandos
class ComandosDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Sistema de Rol (Pág 1)", description="Registros, Perfiles, Atributos y Giros", emoji="🎮"),
            discord.SelectOption(label="Economía y Armas (Pág 2)", description="Tienda, Compras, Balance y Encantos", emoji="🪙"),
            discord.SelectOption(label="Staff Administrativo (Pág 3)", description="Misiones, Dinero, Rangos y Órdenes", emoji="🛡️"),
            discord.SelectOption(label="Poderes de Owner (Pág 4)", description="Administración suprema, Exclusivos y Wipeos", emoji="👑"),
            discord.SelectOption(label="Logs y Creación (Pág 5)", description="Control de auditorías y comandos dinámicos", emoji="⚙️"),
            discord.SelectOption(label="Sistema de Skills (Pág 6)", description="Árbol de habilidades por magia", emoji="🌿"),
        ]
        super().__init__(placeholder="Selecciona una categoría de comandos...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.view.ctx.author.id: return await interaction.response.send_message("❌ Menú bloqueado.", ephemeral=True)
        if self.values[0] == "Sistema de Rol (Pág 1)": self.view.pagina = 1
        elif self.values[0] == "Economía y Armas (Pág 2)": self.view.pagina = 2
        elif self.values[0] == "Staff Administrativo (Pág 3)": self.view.pagina = 3
        elif self.values[0] == "Poderes de Owner (Pág 4)": self.view.pagina = 4
        elif self.values[0] == "Logs y Creación (Pág 5)": self.view.pagina = 5
        elif self.values[0] == "Sistema de Skills (Pág 6)": self.view.pagina = 6
        await interaction.response.edit_message(embed=self.view.generar_embed_pagina(), view=self.view)

class ComandosView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.ctx = ctx
        self.pagina = 1
        self.add_item(ComandosDropdown())

    def generar_embed_pagina(self):
        embed = discord.Embed(color=discord.Color.from_rgb(43, 45, 49))
        embed.set_footer(text=f"Página {self.pagina}/6 • {self.ctx.author.display_name}")
        if self.pagina == 1:
            embed.title = "🎮 Sistema de Rolplay (Jugadores)"
            embed.description = (
                "**+crearpj [Nombre]**\n└ Registra tu personaje.\n\n"
                "**+cambiarnombre [Nombre]**\n└ Cambia el nombre de tu PJ.\n\n"
                "**+perfil [@usuario]**\n└ Panel interactivo completo. Muestra raza, magia, grimorio, demonio, SP y más.\n\n"
                "**+pj [@usuario]**\n└ Resumen rápido de datos.\n\n"
                "**+slot [1/2/3]**\n└ Cambia de Slot de rol.\n\n"
                "**+reclamar**\n└ Recompensa diaria.\n\n"
                "**+entrenamiento**\n└ Entrena para ganar puntos de stats libres.\n\n"
                "**+acender**\n└ Asciende al próximo rango por 1000 Pts.\n\n"
                "**+stats [@usuario]**\n└ Muestra tus atributos de combate.\n\n"
                "**+addstat [fuerza/vida/agilidad/suerte] [cantidad]**\n└ Asigna tus puntos de stats libres.\n\n"
                "**+spin [raza/magia/grimorio/demonio]**\n└ Gira tu ficha de personaje.\n\n"
                "**+rr [raza/magia/grimorio/demonio]**\n└ Reroll gastando 1 turno de reroll."
            )
        elif self.pagina == 2:
            embed.title = "🪙 Economía, Tienda y Equipamiento"
            embed.description = (
                "**+tienda**\n└ Catálogo completo de objetos.\n\n"
                "**+comprar [id]**\n└ Compra un ítem de la tienda.\n\n"
                "**+balance [@usuario]**\n└ Consulta el dinero actual.\n\n"
                "**+encantar [fuerza/vida/agilidad/suerte]**\n└ Añade +2 al stat elegido en tu arma equipada por 2000 ¥.\n\n"
                "**+ranking**\n└ Top 10 magos más poderosos del servidor.\n\n"
                "**+listordenes**\n└ Clasificación de escuadrones por estrellas."
            )
        elif self.pagina == 3:
            embed.title = "🛡️ Staff Administrativo y Narración"
            embed.description = (
                "**+darmision [@usuario] [puntos] [desc]**\n└ Premia misiones completadas.\n\n"
                "**+crear_mision [recompensa] [desc]**\n└ Publica una misión en el tablero.\n\n"
                "**+add [@usuario] [cantidad]**\n└ Da yenes a un jugador.\n\n"
                "**+remover_yenes [@usuario] [cantidad]**\n└ Quita yenes a un jugador.\n\n"
                "**+dar_rr [@usuario] [cantidad]**\n└ Regala rerolls.\n\n"
                "**+darstat [@usuario] [stat/libre] [cantidad]**\n└ Otorga puntos de estadística directamente.\n\n"
                "**+darsp [@usuario] [cantidad]**\n└ Otorga Skill Points para desbloquear habilidades.\n\n"
                "**+add_item / +remove_item**\n└ Gestiona ítems de la tienda.\n\n"
                "**+crear_orden / +addstar / +deletestar**\n└ Control de escuadrones.\n\n"
                "**+narrar [1-5] [Enemigo]**\n└ Genera acciones de combate narradas."
            )
        elif self.pagina == 4:
            embed.title = "👑 Privado Owner, Co-Owner & Creador"
            embed.description = (
                "**+dar_exclusivo / +quitar_exclusivo / +lista_exclusivos**\n└ Gestión de personajes canon.\n\n"
                "**+crear_jerarquia**\n└ Inyecta todos los roles decorados automáticamente.\n\n"
                "**+daradmin / +quitaradmin**\n└ Asigna o revoca permisos de admin bot.\n\n"
                "**+daryuno / +quitaryuno**\n└ Asigna o revoca rango Co-Owner.\n\n"
                "**+viento_divino [msg]**\n└ Comunicado global con @everyone.\n\n"
                "**+darmitico [@usuario]**\n└ Menú interactivo para dar raza/magia/grimorio/demonio sin spins.\n\n"
                "**+impuesto_real [cantidad]**\n└ Cobra yenes a todos los jugadores.\n\n"
                "**+banco_infinito**\n└ Recursos ilimitados para el owner.\n\n"
                "**+wipe [@usuario]**\n└ Borra todos los datos de un jugador.\n\n"
                "**+shutdown**\n└ Apaga el bot."
            )
        elif self.pagina == 5:
            embed.title = "⚙️ Módulos de Auditoría y Personalización"
            embed.description = (
                "**+setlog [#canal]**\n└ Establece el canal de registros de auditoría.\n\n"
                "**+crear_comando [nombre] [respuesta]**\n└ Crea un comando personalizado de respuesta.\n\n"
                "**+eliminar_comando [nombre]**\n└ Elimina un comando personalizado.\n\n"
                "**+lista_comandos**\n└ Lista todos los comandos personalizados creados."
            )
        elif self.pagina == 6:
            embed.title = "🌿 Sistema de Habilidades (Skills)"
            embed.description = (
                "**+skills [@usuario]**\n└ Muestra el árbol de habilidades completo de tu magia.\n"
                "  Indica qué está desbloqueado ✅, qué puedes comprar 🔓 y qué está bloqueado 🔒.\n\n"
                "**+aprender [nombre de habilidad]**\n└ Desbloquea una habilidad gastando Skill Points.\n"
                "  Usa el nombre exacto que aparece en `+skills`.\n\n"
                "**+mishabilidades [@usuario]**\n└ Lista rápida de las habilidades ya desbloqueadas.\n\n"
                "**+darsp [@usuario] [cantidad]** *(Solo Staff)*\n└ Otorga Skill Points a un jugador.\n"
                "  Los SP son independientes de los puntos de stats.\n\n"
                "📌 **¿Cómo funciona?**\n"
                "└ Cada magia tiene un árbol exclusivo de 5 habilidades.\n"
                "└ Las habilidades tienen prereqs — desbloquea desde la base.\n"
                "└ Los SP solo los dan los admins, no se ganan automáticamente."
            )
        return embed

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.blurple, row=1)
    async def boton_atras(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("❌ Bloqueado.", ephemeral=True)
        self.pagina = 6 if self.pagina == 1 else self.pagina - 1
        await interaction.response.edit_message(embed=self.generar_embed_pagina(), view=self)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.blurple, row=1)
    async def boton_siguiente(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id: return await interaction.response.send_message("❌ Bloqueado.", ephemeral=True)
        self.pagina = 1 if self.pagina == 6 else self.pagina + 1
        await interaction.response.edit_message(embed=self.generar_embed_pagina(), view=self)

PERSONAJES_EXCLUSIVOS = {
    "asta": {"nombre": "Asta", "fuerza": 20, "vida": 15, "agilidad": 10, "desc": "Antimagia. Fuerza descomunal y resistencia física absoluta."},
    "yami": {"nombre": "Yami Sukehiro", "fuerza": 25, "vida": 15, "agilidad": 5, "desc": "Magia de Oscuridad. Cortes dimensionales destructivos."},
    "noelle": {"nombre": "Noelle Silva", "fuerza": 5, "vida": 20, "agilidad": 15, "desc": "Magia de Agua. Armadura de Valquiria de altísima vitalidad."},
    "yuno": {"nombre": "Yuno Grinberryall", "fuerza": 8, "vida": 12, "agilidad": 25, "desc": "Magia de Viento. Bendecido por el espíritu de sílfide."},
    "zenon": {"nombre": "Zenon Zogratis", "fuerza": 22, "vida": 22, "agilidad": 11, "desc": "Magia de Huesos y Espacial. Contiene el poder de Beelzebub."},
    "dante": {"nombre": "Dante Zogratis", "fuerza": 26, "vida": 24, "agilidad": 5, "desc": "Magia de Gravedad y Cuerpo. Regeneración gracias a Lucifero."},
    "julius": {"nombre": "Julius Novachrono", "fuerza": 10, "vida": 20, "agilidad": 30, "desc": "Magia de Tiempo. Rey Mago. Control temporal absoluto."}
}

@bot.command(name="reclamar")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def reclamar(ctx):
    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    slot = datos[str(ctx.author.id)]["slot_activo"]
    pj = datos[str(ctx.author.id)]["slots"][slot]
    rango_actual = pj.get("rango", "Mago normal")
    
    recompensa_dinero = 500
    puntos_regalo = 100
    if rango_actual == "Caballero Mágico junior": recompensa_dinero, puntos_regalo = 1000, 150
    elif rango_actual == "Caballero Mágico Intermedio": recompensa_dinero, puntos_regalo = 1800, 200
    elif rango_actual == "Caballero Mágico Superior": recompensa_dinero, puntos_regalo = 2500, 250
    elif rango_actual == "Caballero Mágico maximo": recompensa_dinero, puntos_regalo = 4000, 350
    elif rango_actual == "Rey mago": recompensa_dinero, puntos_regalo = 6000, 500

    pj["dinero"] += recompensa_dinero
    pj["puntos"] += puntos_regalo
    pj["rango"] = calcular_rango(pj["puntos"])
    guardar_datos(datos)

    embed = discord.Embed(title="═━  ᰋ  𝆬  🪷  ִ  ¡Recompensa Diaria Reclamada!  ִ   ⊹", description=f"> 💫 {ctx.author.mention}, por pertenecer al rango **{rango_actual}**, has obtenido tus recursos imperiales en tu **Slot {slot}**.", color=discord.Color.from_rgb(0, 255, 204))
    embed.add_field(name="🪙 Yenes:", value=f"`+{recompensa_dinero} ¥` 💰", inline=True).add_field(name="✨ Puntos XP:", value=f"`+{puntos_regalo} Pts` 🔮", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="crear_jerarquia", aliases=["crear-jerarquia"])
async def crear_jerarquia(ctx):
    if not ctx.author.guild_permissions.administrator: return await ctx.send("❌ Sin permisos.")
    await ctx.send("⏳ *Inyectando roles decorados... Espera.*")
    razas_roles = list(RAZAS.keys())
    grimorios_roles = list(GRIMORIOS.keys())
    magias_roles = list(MAGIAS.keys())

    roles_a_crear = [
        {"name": "🎨 ───✧ RESERVADO ✧───", "color": discord.Color.default()},
        {"name": "ᶻz﹒⏆﹒Owner﹒⟢", "color": discord.Color.from_rgb(255, 0, 85)},
        {"name": "ᶻz﹒⏆﹒Co owner﹒⟢", "color": discord.Color.from_rgb(255, 85, 0)},
        {"name": "ᶻz﹒⏆﹒Head admin﹒⟢", "color": discord.Color.from_rgb(230, 0, 255)},
        {"name": "⌑﹒ꔫ﹒Admin﹒⟢", "color": discord.Color.from_rgb(153, 0, 255)},
        {"name": "⌑﹒ꔫ﹒Asistente﹒⟢", "color": discord.Color.from_rgb(0, 204, 255)},
        {"name": "⌑﹒ꔫ﹒Moderador﹒⟢", "color": discord.Color.from_rgb(0, 255, 102)},
        {"name": "⏆﹒⿻﹒Developer﹒﹒┄", "color": discord.Color.from_rgb(255, 187, 0)},
        {"name": "⏆﹒⿻﹒Staff﹒﹒┄", "color": discord.Color.from_rgb(51, 255, 170)},
        {"name": "﹙◞◟﹚﹒(Mini staff)﹒﹒✾", "color": discord.Color.from_rgb(119, 255, 170)},
        {"name": "⿴﹒﹒⌑﹒Bots﹒✦", "color": discord.Color.from_rgb(127, 140, 141)},
        {"name": "🌿 ───✧ CIUDADANOS ✧───", "color": discord.Color.default()},
        {"name": "⿴﹒﹒⌑﹒Verificado﹒✦", "color": discord.Color.blue()},
        {"name": "[e]﹒谷﹒⏆﹒Miembro﹒⭔", "color": discord.Color.green()},
        {"name": "╭╯﹒〣ꔫ﹒***．⟡﹒ RAZAS ﹒﹒⪨﹒***", "color": discord.Color.default()}
    ]
    for r in razas_roles: roles_a_crear.append({"name": f"ılıl﹐𖥻﹒ {r} ﹒౨ৎ", "color": discord.Color.red()})
    roles_a_crear.append({"name": "╭╯﹒〣ꔫ﹒***．⟡﹒ GRIMORIOS ﹒﹒⪨﹒***", "color": discord.Color.default()})
    for g in grimorios_roles: roles_a_crear.append({"name": f"∿﹒✢﹒ {g} ﹒ᶻz", "color": discord.Color.gold()})
    roles_a_crear.append({"name": "╭╯﹒〣ꔫ﹒***．⟡﹒ MAGIAS ﹒﹒⪨﹒***", "color": discord.Color.default()})
    for index, m in enumerate(magias_roles):
        estilos = [f"⌑﹒ꔫ﹒ {m} ﹒⟢", f"⿴﹒﹒⌑﹒ {m} ﹒✦", f"⟢﹒ᶻz﹒ {m} ﹒➜", f"𖥻﹒✿﹒ {m} ﹒﹙◞◟﹚"]
        roles_a_crear.append({"name": estilos[index % len(estilos)], "color": discord.Color.purple()})

    roles_a_crear.extend([
        {"name": "🌸 ───✧ NOTIFICACIONES ✧───", "color": discord.Color.default()},
        {"name": "✿﹒Alianza﹒ꗃ﹒﹒⭔", "color": discord.Color.teal()},
        {"name": "✿﹒Sorteos﹒ꗃ﹒﹒⭔", "color": discord.Color.orange()},
        {"name": "✿﹒Anuncio﹒ꗃ﹒﹒⭔", "color": discord.Color.gold()},
        {"name": "✿﹒Revivir chat﹒ꗃ﹒﹒⭔", "color": discord.Color.dark_grey()}
    ])
    for rol_data in roles_a_crear:
        try:
            await ctx.guild.create_role(name=rol_data["name"], color=rol_data["color"], reason="Jerarquía")
            await asyncio.sleep(0.15)
        except: pass
    await ctx.send("✅ Roles creados.")

@bot.command(name="dar_exclusivo")
async def dar_exclusivo(ctx, miembro: discord.Member = None, id_personaje: str = None):
    if not es_admin_bot(ctx): return
    if not miembro or not id_personaje: return await ctx.send("❌ Uso: `+dar_exclusivo [@usuario] [id]`")
    id_limpia = id_personaje.lower().strip()
    if id_limpia not in PERSONAJES_EXCLUSIVOS: return await ctx.send("❌ ID inválido.")
    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    slot = datos[str(miembro.id)]["slot_activo"]
    pj = datos[str(miembro.id)]["slots"][slot]
    
    personaje_antiguo = pj.get("personaje_exclusivo", "Ninguno")
    if personaje_antiguo != "Ninguno":
        id_antigua = next((k for k, v in PERSONAJES_EXCLUSIVOS.items() if v["nombre"].lower() == personaje_antiguo.lower()), None)
        if id_antigua:
            pj["fuerza"] = max(0, pj["fuerza"] - PERSONAJES_EXCLUSIVOS[id_antigua]["fuerza"])
            pj["vida"] = max(0, pj["vida"] - PERSONAJES_EXCLUSIVOS[id_antigua]["vida"])
            pj["agilidad"] = max(0, pj["agilidad"] - PERSONAJES_EXCLUSIVOS[id_antigua]["agilidad"])

    p_nuevo = PERSONAJES_EXCLUSIVOS[id_limpia]
    pj["personaje_exclusivo"] = p_nuevo["nombre"]
    pj["fuerza"] += p_nuevo["fuerza"]
    pj["vida"] += p_nuevo["vida"]
    pj["agilidad"] += p_nuevo["agilidad"]
    guardar_datos(datos)
    await ctx.send(f"✅ Otorgado **{p_nuevo['nombre']}** a {miembro.mention}.")

@bot.command(name="quitar_exclusivo")
async def quitar_exclusivo(ctx, miembro: discord.Member = None):
    if not es_admin_bot(ctx): return
    if not miembro: return await ctx.send("❌ Uso: `+quitar_exclusivo [@usuario]`")
    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    slot = datos[str(miembro.id)]["slot_activo"]
    pj = datos[str(miembro.id)]["slots"][slot]
    personaje_actual = pj.get("personaje_exclusivo", "Ninguno")
    if personaje_actual == "Ninguno": return await ctx.send("❌ No tiene personaje exclusivo.")
    id_limpia = next((k for k, v in PERSONAJES_EXCLUSIVOS.items() if v["nombre"].lower() == personaje_actual.lower()), None)
    if id_limpia:
        pj["fuerza"] = max(0, pj["fuerza"] - PERSONAJES_EXCLUSIVOS[id_limpia]["fuerza"])
        pj["vida"] = max(0, pj["vida"] - PERSONAJES_EXCLUSIVOS[id_limpia]["vida"])
        pj["agilidad"] = max(0, pj["agilidad"] - PERSONAJES_EXCLUSIVOS[id_limpia]["agilidad"])
    pj["personaje_exclusivo"] = "Ninguno"
    guardar_datos(datos)
    await ctx.send(f"🧹 Removido de {miembro.mention}.")

@bot.command(name="lista_exclusivos")
async def lista_exclusivos(ctx):
    embed = discord.Embed(title="⚜️ Personajes Exclusivos Disponibles ⚜️", color=discord.Color.dark_blue())
    for k, v in PERSONAJES_EXCLUSIVOS.items():
        embed.add_field(name=f"👤 {v['nombre']} (`{k}`)", value=f"📊 💪 F +{v['fuerza']} | ❤️ V +{v['vida']} | ⚡ A +{v['agilidad']}", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="crearpj")
async def crearpj(ctx, *, nombre: str = None):
    if not nombre: return await ctx.send("❌ Uso: `+crearpj [Nombre]`")
    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    slot = datos[str(ctx.author.id)]["slot_activo"]
    datos[str(ctx.author.id)]["slots"][slot]["nombre_rp"] = nombre
    guardar_datos(datos)
    await ctx.send(f"✅ Slot {slot} registrado como **{nombre}**.")

@bot.command(name="cambiarnombre")
async def cambiarnombre(ctx, *, nombre: str = None):
    if not nombre: return await ctx.send("❌ Uso: `+cambiarnombre [Nombre]`")
    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    slot = datos[str(ctx.author.id)]["slot_activo"]
    datos[str(ctx.author.id)]["slots"][slot]["nombre_rp"] = nombre
    guardar_datos(datos)
    await ctx.send(f"🔄 Nombre cambiado en Slot {slot}.")

@bot.command(name="pj")
async def pj_info(ctx, miembro: discord.Member = None):
    miembro = miembro or ctx.author
    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    slot = datos[str(miembro.id)]["slot_activo"]
    pj = datos[str(miembro.id)]["slots"][slot]
    embed = discord.Embed(title=f"👤 Slot {slot}", color=discord.Color.green())
    embed.add_field(name="Usuario:", value=miembro.mention).add_field(name="Nombre RP:", value=pj['nombre_rp']).add_field(name="Canon:", value=pj.get('personaje_exclusivo', 'Ninguno'))
    await ctx.send(embed=embed)

@bot.command(name="daryuno")
@commands.is_owner()
async def daryuno(ctx, miembro: discord.Member):
    datos = cargar_datos()
    if miembro.id not in datos["co_owners"]: datos["co_owners"].append(miembro.id)
    guardar_datos(datos)
    await ctx.send(f"👑 {miembro.mention} ahora es Co-Owner.")

@bot.command(name="quitaryuno")
@commands.is_owner()
async def quitaryuno(ctx, miembro: discord.Member):
    datos = cargar_datos()
    if miembro.id in datos["co_owners"]: datos["co_owners"].remove(miembro.id)
    guardar_datos(datos)
    await ctx.send(f"🧹 Revocado Rango Yuno a {miembro.mention}.")

@bot.command(name="viento_divino")
@es_owner_o_coowner()
async def viento_divino(ctx, *, mensaje: str):
    embed = discord.Embed(title="🌪️ ¡Decreto del Co-Owner Yuno! 🌪️", description=mensaje, color=discord.Color.green())
    await ctx.send(content="@everyone", embed=embed)

@bot.command(name="darmitico", aliases=["dar_mitico", "darpoder"])
@es_owner_o_coowner()
async def dar_mitico(ctx, miembro: discord.Member = None):
    """Menú interactivo para asignar raza/magia/grimorio/demonio a un usuario."""
    if not miembro:
        return await ctx.send("❌ Uso: `+darmitico [@usuario]`")

    class TipoSelect(discord.ui.Select):
        def __init__(self):
            super().__init__(
                placeholder="1️⃣ Elige el tipo...",
                options=[
                    discord.SelectOption(label="Raza", emoji="🧬"),
                    discord.SelectOption(label="Magia", emoji="🪄"),
                    discord.SelectOption(label="Grimorio", emoji="🍀"),
                    discord.SelectOption(label="Demonio", emoji="😈"),
                ]
            )

        async def callback(self, interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                return await interaction.response.send_message("❌ No puedes usar esto.", ephemeral=True)
            tipo_elegido = self.values[0].lower()
            _datos_tmp = cargar_datos()
            if tipo_elegido == "raza":
                pool = {**RAZAS, **_datos_tmp.get("razas_custom", {})}
            elif tipo_elegido == "magia":   pool = MAGIAS
            elif tipo_elegido == "grimorio": pool = GRIMORIOS
            else:                            pool = DEMONIOS

            # Divide el pool en chunks de 25 (límite de Discord)
            items = list(pool.keys())
            chunks = [items[i:i+25] for i in range(0, len(items), 25)]

            class ObjetoSelect(discord.ui.Select):
                def __init__(self, opciones):
                    opts = [discord.SelectOption(
                        label=nombre[:100],
                        description=pool[nombre]["rareza"]
                    ) for nombre in opciones]
                    super().__init__(placeholder=f"2️⃣ Elige {tipo_elegido}...", options=opts)

                async def callback(self2, interaction2: discord.Interaction):
                    if interaction2.user.id != ctx.author.id:
                        return await interaction2.response.send_message("❌ No puedes usar esto.", ephemeral=True)
                    objeto = self2.values[0]
                    datos = cargar_datos()
                    verificar_usuario(miembro.id, datos)
                    slot = datos[str(miembro.id)]["slot_activo"]
                    pj_target = datos[str(miembro.id)]["slots"][slot]
                    pj_target[tipo_elegido] = objeto
                    # Aplicar stats base si es raza
                    if tipo_elegido == "raza":
                        raza_anterior = pj_target.get("raza_anterior", None)
                        aplicar_stats_raza(pj_target, objeto, raza_anterior)
                        pj_target["raza_anterior"] = objeto
                    # Si es demonio, también marcar spin como hecho
                    if tipo_elegido == "demonio":
                        datos[str(miembro.id)]["spins_realizados"]["demonio"] = True
                    else:
                        datos[str(miembro.id)]["spins_realizados"][tipo_elegido] = True
                    guardar_datos(datos)
                    await asignar_rol_automatico(ctx, tipo_elegido, objeto)
                    embed = discord.Embed(
                        title="👑 ¡Poder Infundido!",
                        color=discord.Color.from_rgb(255, 215, 0)
                    )
                    embed.add_field(name="👤 Usuario:", value=miembro.mention, inline=True)
                    embed.add_field(name="📌 Tipo:", value=tipo_elegido.capitalize(), inline=True)
                    embed.add_field(name="✨ Otorgado:", value=f"**{objeto}**", inline=True)
                    embed.add_field(name="⭐ Rareza:", value=pool[objeto]["rareza"], inline=True)
                    embed.set_footer(text=f"Otorgado por {ctx.author.display_name}")
                    await interaction2.response.edit_message(embed=embed, view=None)

            # Si hay más de 25 items, agrega un selector de página
            view2 = discord.ui.View(timeout=60)
            if len(chunks) > 1:
                for idx, chunk in enumerate(chunks):
                    s = ObjetoSelect(chunk)
                    s.placeholder = f"2️⃣ {tipo_elegido.capitalize()} (parte {idx+1}/{len(chunks)})..."
                    view2.add_item(s)
            else:
                view2.add_item(ObjetoSelect(chunks[0]))

            embed2 = discord.Embed(
                title=f"👑 Otorgar {tipo_elegido.capitalize()}",
                description=f"Elige el/la **{tipo_elegido}** para {miembro.mention}",
                color=discord.Color.from_rgb(255, 215, 0)
            )
            await interaction.response.edit_message(embed=embed2, view=view2)

    view = discord.ui.View(timeout=60)
    view.add_item(TipoSelect())
    embed = discord.Embed(
        title="👑 Otorgar Poder Mítico",
        description=f"Selecciona qué tipo de poder quieres dar a {miembro.mention}",
        color=discord.Color.from_rgb(255, 215, 0)
    )
    await ctx.send(embed=embed, view=view)

@bot.command(name="impuesto_real")
@es_owner_o_coowner()
async def impuesto_real(ctx, cantidad: int):
    if cantidad <= 0: return
    datos = cargar_datos()
    for uid in datos:
        if uid in ["ordenes", "admins", "co_owners", "canal_logs", "comandos_creados", "tienda_personalizada", "tablero_misiones"]: continue
        s = datos[uid].get("slot_activo", "1")
        if "slots" in datos[uid] and s in datos[uid]["slots"]:
            datos[uid]["slots"][s]["dinero"] = max(0, datos[uid]["slots"][s]["dinero"] - cantidad)
    guardar_datos(datos)
    await ctx.send("💸 Impuesto Real cobrado.")

@bot.command(name="banco_infinito")
@es_owner_o_coowner()
async def banco_infinito(ctx):
    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    slot = datos[str(ctx.author.id)]["slot_activo"]
    datos[str(ctx.author.id)]["rerolls"] = 999
    datos[str(ctx.author.id)]["slots"][slot]["dinero"] = 999999
    guardar_datos(datos)
    await ctx.send("👑 Recursos Infinitas.")

@bot.command(name="wipe")
@es_owner_o_coowner()
async def wipe(ctx, miembro: discord.Member):
    datos = cargar_datos()
    if str(miembro.id) in datos: del datos[str(miembro.id)]
    guardar_datos(datos)
    await ctx.send(f"🧹 Wipeado {miembro.mention}.")

@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("🛑 Apagando...")
    await bot.close()

@bot.command(name="crear_orden")
async def crear_orden(ctx, canal: discord.TextChannel = None, *, nombre_orden: str = None):
    if not es_admin_bot(ctx): return
    if not canal or not nombre_orden: return
    datos = cargar_datos()
    datos["ordenes"][nombre_orden.strip().lower()] = {"nombre_real": nombre_orden, "estrellas": 0, "canal_id": canal.id}
    guardar_datos(datos)
    await ctx.send(f"🏰 Orden {nombre_orden} creada.")

@bot.command(name="daradmin")
@commands.is_owner()
async def daradmin(ctx, miembro: discord.Member):
    datos = cargar_datos()
    if miembro.id not in datos["admins"]: datos["admins"].append(miembro.id)
    guardar_datos(datos)
    await ctx.send(f"🛡️ Admin bot asignado a {miembro.mention}.")

@bot.command(name="quitaradmin")
@commands.is_owner()
async def quitaradmin(ctx, miembro: discord.Member):
    datos = cargar_datos()
    if miembro.id in datos["admins"]: datos["admins"].remove(miembro.id)
    guardar_datos(datos)
    await ctx.send(f"🧹 Admin bot revocado a {miembro.mention}.")

@bot.command(name="add")
async def add(ctx, miembro: discord.Member = None, cantidad: int = None):
    if not es_admin_bot(ctx): return
    if not miembro or cantidad is None or cantidad <= 0: return
    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    slot = datos[str(miembro.id)]["slot_activo"]
    datos[str(miembro.id)]["slots"][slot]["dinero"] += cantidad
    guardar_datos(datos)
    await ctx.send(f"🪙 +{cantidad} Yenes entregados.")

@bot.command(name="remover_yenes")
async def remover_yenes(ctx, miembro: discord.Member = None, cantidad: int = None):
    if not es_admin_bot(ctx): return
    if not miembro or cantidad is None or cantidad <= 0: return
    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    slot = datos[str(miembro.id)]["slot_activo"]
    datos[str(miembro.id)]["slots"][slot]["dinero"] = max(0, datos[str(miembro.id)]["slots"][slot]["dinero"] - cantidad)
    guardar_datos(datos)
    await ctx.send("📉 Fondos retirados.")

@bot.command(name="dar_rr")
async def dar_rr(ctx, miembro: discord.Member = None, cantidad: int = None):
    if not es_admin_bot(ctx): return
    if not miembro or cantidad is None or cantidad <= 0: return
    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    datos[str(miembro.id)]["rerolls"] += cantidad
    guardar_datos(datos)
    await ctx.send(f"🎟️ +{cantidad} Rerolls.")

@bot.command(name="addstar")
async def addstar(ctx, cantidad: int = None, *, nombre_orden: str = None):
    if not es_admin_bot(ctx) or cantidad is None or not nombre_orden: return
    datos = cargar_datos()
    k = nombre_orden.strip().lower()
    if k in datos["ordenes"]: datos["ordenes"][k]["estrellas"] += cantidad
    guardar_datos(datos)
    await ctx.send("✨ Estrellas sumadas.")

@bot.command(name="deletestar")
async def deletestar(ctx, cantidad: int = None, *, nombre_orden: str = None):
    if not es_admin_bot(ctx) or cantidad is None or not nombre_orden: return
    datos = cargar_datos()
    k = nombre_orden.strip().lower()
    if k in datos["ordenes"]: datos["ordenes"][k]["estrellas"] -= cantidad
    guardar_datos(datos)
    await ctx.send("📉 Estrellas restadas.")

@bot.command(name="listordenes")
async def listordenes(ctx):
    datos = cargar_datos()
    if not datos.get("ordenes"): return await ctx.send("🏰 No hay órdenes.")
    embed = discord.Embed(title="⚜️ Clasificación Oficial ⚜️", color=discord.Color.dark_purple())
    for o in sorted(datos["ordenes"].values(), key=lambda x: x["estrellas"], reverse=True):
        embed.add_field(name=o['nombre_real'], value=f"✨ Estrellas: {o['estrellas']}", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ranking", aliases=["top"])
async def ranking(ctx):
    datos = cargar_datos()
    lista = []
    for uid, info in datos.items():
        if uid in ["ordenes", "admins", "co_owners", "canal_logs", "comandos_creados", "tienda_personalizada", "tablero_misiones"]: continue
        m = ctx.guild.get_member(int(uid))
        name = m.display_name if m else f"Mago ({uid})"
        pj = info.get("slots", {}).get(info.get("slot_activo", "1"), {})
        lista.append({"n": name, "p": pj.get("puntos", 0), "r": pj.get("rango", "Mago normal")})
    embed = discord.Embed(title="🏆 TOP 10 Magos 🏆", color=discord.Color.red())
    for i, m in enumerate(sorted(lista, key=lambda x: x["p"], reverse=True)[:10]):
        embed.add_field(name=f"#{i+1} {m['n']}", value=f"⭐ Puntos: **{m['p']}** | `{m['r']}`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="stats")
async def stats(ctx, miembro: discord.Member = None):
    miembro = miembro or ctx.author
    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    pj = datos[str(miembro.id)]["slots"][datos[str(miembro.id)]["slot_activo"]]
    embed = discord.Embed(title=f"📊 Stats — {miembro.display_name}", description=f"💪 Fuerza: `{pj['fuerza']}`\n❤️ Vida: `{pj['vida']}`\n⚡ Agilidad: `{pj['agilidad']}`\n🍀 Suerte: `{pj['suerte']}`\n✨ Puntos libres: `{pj['puntos_stats']}`", color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command(name="addstat")
async def addstat(ctx, estadistica: str = None, cantidad: int = None):
    if not estadistica or cantidad is None or cantidad <= 0: 
        return await ctx.send("❌ Uso correcto: `+addstat [fuerza/vida/agilidad/suerte] [cantidad]`")
    
    stat_target = estadistica.lower().strip()
    if stat_target not in ["fuerza", "vida", "agilidad", "suerte"]:
        return await ctx.send("❌ Estadística inválida.")

    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    pj = datos[str(ctx.author.id)]["slots"][datos[str(ctx.author.id)]["slot_activo"]]
    
    if pj["puntos_stats"] < cantidad: 
        return await ctx.send("❌ No posees suficientes puntos libres.")
        
    pj["puntos_stats"] -= cantidad
    pj[stat_target] += cantidad
    guardar_datos(datos)
    await ctx.send(f"✅ Se asignaron +{cantidad} puntos a **{stat_target.capitalize()}**.")

@bot.command(name="darstat")
async def darstat(ctx, miembro: discord.Member = None, estadistica: str = None, cantidad: int = None):
    """Admin: da puntos de estadística directamente a un jugador. +darstat [@usuario] [fuerza/vida/agilidad/suerte/libre] [cantidad]"""
    if not es_admin_bot(ctx):
        return await ctx.send("❌ No tienes permisos para usar este comando.")
    if not miembro or not estadistica or cantidad is None or cantidad <= 0:
        return await ctx.send("❌ Uso: `+darstat [@usuario] [fuerza/vida/agilidad/suerte/libre] [cantidad]`")

    stat_target = estadistica.lower().strip()
    if stat_target not in ["fuerza", "vida", "agilidad", "suerte", "libre"]:
        return await ctx.send("❌ Estadística inválida. Usa: `fuerza`, `vida`, `agilidad`, `suerte` o `libre` (puntos sin asignar).")

    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    pj = datos[str(miembro.id)]["slots"][datos[str(miembro.id)]["slot_activo"]]

    if stat_target == "libre":
        pj["puntos_stats"] += cantidad
        campo = "Puntos Libres"
    else:
        pj[stat_target] += cantidad
        campo = stat_target.capitalize()

    guardar_datos(datos)

    embed = discord.Embed(
        title="📊 Estadísticas Otorgadas",
        color=discord.Color.from_rgb(0, 204, 102)
    )
    embed.add_field(name="👤 Jugador:", value=miembro.mention, inline=True)
    embed.add_field(name="📈 Estadística:", value=f"**{campo}**", inline=True)
    embed.add_field(name="✨ Cantidad:", value=f"`+{cantidad}`", inline=True)
    embed.set_footer(text=f"Otorgado por {ctx.author.display_name}")
    await ctx.send(embed=embed)

@bot.command(name="encantar")
async def encantar(ctx, stat_a_encantar: str = None):
    if not stat_a_encantar or stat_a_encantar.lower().strip() not in ["fuerza", "vida", "agilidad", "suerte"]: 
        return await ctx.send("❌ Elige una estadística válida para encantar.")
    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    pj = datos[str(ctx.author.id)]["slots"][datos[str(ctx.author.id)]["slot_activo"]]
    if not pj.get("armas_equipadas") or pj["dinero"] < 2000: return
    nombre_arma = list(pj["armas_equipadas"].keys())[0]
    pj["dinero"] -= 2000
    pj["armas_equipadas"][nombre_arma].setdefault(stat_a_encantar.lower(), 0)
    pj["armas_equipadas"][nombre_arma][stat_a_encantar.lower()] += 2
    guardar_datos(datos)
    await ctx.send("✨ Arma Encantada.")

@bot.command()
async def tienda(ctx):
    datos = cargar_datos()
    embed = discord.Embed(title="🛒 Tienda Clover 🛒", color=discord.Color.gold())
    for k, v in TIENDA_ITEMS_BASE.items(): embed.add_field(name=f"{v['nombre']} (`{k}`)", value=f"💰 **{v['precio']} ¥**\n*{v['desc']}*", inline=False)
    for k, v in datos.get("tienda_personalizada", {}).items(): embed.add_field(name=f"{v['nombre']} (`{k}`)", value=f"💰 **{v['precio']} ¥**", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def comprar(ctx, itemId: str = None):
    if not itemId: return
    id_l = itemId.lower().strip()
    datos = cargar_datos()
    item = TIENDA_ITEMS_BASE.get(id_l) or datos.get("tienda_personalizada", {}).get(id_l)
    if not item: return
    verificar_usuario(ctx.author.id, datos)
    pj = datos[str(ctx.author.id)]["slots"][datos[str(ctx.author.id)]["slot_activo"]]
    if pj["dinero"] < item["precio"]: return
    pj["dinero"] -= item["precio"]
    if item.get("es_arma"): pj["armas_equipadas"][item["nombre"]] = {"fuerza": 0, "vida": 0, "agilidad": 0, "suerte": 0}
    else: pj["inventario"].append(item["nombre"])
    guardar_datos(datos)
    await ctx.send("✅ Ítem comprado.")

@bot.command(name="add_item")
async def add_item(ctx, id_item: str = None, precio: int = None, *, nombre_y_desc: str = None):
    if not es_admin_bot(ctx) or not id_item or precio is None or not nombre_y_desc: return
    datos = cargar_datos()
    datos["tienda_personalizada"][id_item.lower().strip()] = {"nombre": nombre_y_desc, "precio": precio, "es_arma": False}
    guardar_datos(datos)
    await ctx.send("✅ Agregado a la tienda.")

@bot.command(name="remove_item")
async def remove_item(ctx, id_item: str = None):
    if not es_admin_bot(ctx) or not id_item: return
    datos = cargar_datos()
    if id_item.lower().strip() in datos["tienda_personalizada"]: del datos["tienda_personalizada"][id_item.lower().strip()]
    guardar_datos(datos)
    await ctx.send("🗑️ Eliminado de la tienda.")

@bot.command(name="crear_mision")
async def crear_mision(ctx, recompensa: int = None, *, descripcion: str = None):
    if not es_admin_bot(ctx) or recompensa is None or not descripcion: return
    datos = cargar_datos()
    datos["tablero_misiones"].append({"id": len(datos["tablero_misiones"]) + 1, "recompensa": recompensa, "desc": descripcion})
    guardar_datos(datos)
    await ctx.send("📜 Misión publicada.")

@bot.command(name="darmision")
async def darmision(ctx, miembro: discord.Member, puntos: int, *, descripcion_mision: str):
    if not es_admin_bot(ctx) or puntos <= 0: return
    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    pj = datos[str(miembro.id)]["slots"][datos[str(miembro.id)]["slot_activo"]]
    pj["puntos"] += puntos
    pj["dinero"] += (puntos * 2)
    pj["puntos_stats"] += max(2, (puntos // 100) * 5)
    pj["misiones_hechas"].append(f"{descripcion_mision} (+{puntos} Pts)")
    pj["rango"] = calcular_rango(pj["puntos"])
    guardar_datos(datos)
    await ctx.send(f"✅ Misión guardada para {miembro.mention}.")

@bot.command(name="narrar")
async def narrar(ctx, rango: str = None, *, enemigo: str = None):
    if not rango or not enemigo: return
    acciones = {
        "5": ["El enemigo saca un arma oxidada.", "El rival lanza piedras de maná débil."],
        "4": ["El oponente levanta una barrera agrietada.", "El contrincante retrocede."],
        "3": ["El enemigo invoca un elemental mediano.", "El oponente ejecuta una atadura."],
        "2": ["El rival libera un hechizo de área medio.", "El enemigo imbuye magia veloz en sus pies."],
        "1": ["💥 ¡Peligro Absoluto! Hechizo definitivo.", "El jefe absorbe maná natural duplicando su fuerza."]
    }
    if rango in acciones: await ctx.send(embed=discord.Embed(title="⚔️ Acción de Combate ⚔️", description=f"**Objetivo:** {enemigo}\n**Acción:** *{random.choice(acciones[rango])}*", color=discord.Color.red()))

@bot.command()
async def slot(ctx, numero: str = None):
    if numero not in ["1", "2", "3"]: return
    datos = cargar_datos()
    verificar_usuario(ctx.author.id, datos)
    datos[str(ctx.author.id)]["slot_activo"] = numero
    guardar_datos(datos)
    await ctx.send(f"🔄 Cambiado al Slot {numero}.")

@bot.command(name="perfil")
async def perfil(ctx, miembro: discord.Member = None):
    miembro = miembro or ctx.author
    view = PerfilView(miembro, ctx)
    await ctx.send(embed=await view.generar_embed(), view=view)

@bot.command(aliases=["bal"])
async def balance(ctx, miembro: discord.Member = None):
    miembro = miembro or ctx.author
    datos = cargar_datos()
    verificar_usuario(miembro.id, datos)
    s = datos[str(miembro.id)]["slot_activo"]
    await ctx.send(f"🪙 Balance Slot {s}: **{datos[str(miembro.id)]['slots'][s]['dinero']} ¥**.")

@bot.command(name="comandos")
async def comandos(ctx):
    view = ComandosView(ctx)
    await ctx.send(embed=view.generar_embed_pagina(), view=view)



# =========================================================================
# 🧬 SISTEMA DE RAZAS PERSONALIZADAS — Panel interactivo
# =========================================================================

def _embed_raza_panel(datos: dict) -> discord.Embed:
    razas_custom = datos.get("razas_custom", {})
    embed = discord.Embed(title="🧬 Panel de Gestión de Razas", color=discord.Color.from_rgb(138, 43, 226))
    embed.add_field(name="📚 Razas Base:", value=str(len(RAZAS)), inline=True)
    embed.add_field(name="✨ Razas Custom:", value=str(len(razas_custom)), inline=True)
    if razas_custom:
        lista = "\n".join([f"• **{n}** — {v['rareza']} | 🎲 `{v['peso']*100:.1f}%`" for n, v in razas_custom.items()])
        embed.add_field(name="📋 Listado:", value=lista, inline=False)
    else:
        embed.add_field(name="📋 Listado:", value="*Ninguna creada aún.*", inline=False)
    embed.set_footer(text="Selecciona una acción con los botones")
    return embed


class RazasPanelView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.ctx = ctx

    def _check(self, interaction):
        return interaction.user.id == self.ctx.author.id

    @discord.ui.button(label="➕ Crear Raza", style=discord.ButtonStyle.green, row=0)
    async def crear(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self._check(interaction):
            return await interaction.response.send_message("❌ Solo el admin puede usar esto.", ephemeral=True)
        await interaction.response.send_modal(CrearRazaModal(self.ctx))

    @discord.ui.button(label="✏️ Editar Raza", style=discord.ButtonStyle.blurple, row=0)
    async def editar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self._check(interaction):
            return await interaction.response.send_message("❌ Solo el admin puede usar esto.", ephemeral=True)
        datos = cargar_datos()
        razas_custom = datos.get("razas_custom", {})
        if not razas_custom:
            return await interaction.response.send_message("❌ No hay razas personalizadas para editar.", ephemeral=True)
        await interaction.response.send_message(
            "Selecciona la raza a editar:",
            view=SeleccionarRazaView(self.ctx, razas_custom, "editar"),
            ephemeral=True
        )

    @discord.ui.button(label="🗑️ Borrar Raza", style=discord.ButtonStyle.red, row=0)
    async def borrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self._check(interaction):
            return await interaction.response.send_message("❌ Solo el admin puede usar esto.", ephemeral=True)
        datos = cargar_datos()
        razas_custom = datos.get("razas_custom", {})
        if not razas_custom:
            return await interaction.response.send_message("❌ No hay razas personalizadas para borrar.", ephemeral=True)
        await interaction.response.send_message(
            "Selecciona la raza a eliminar:",
            view=SeleccionarRazaView(self.ctx, razas_custom, "borrar"),
            ephemeral=True
        )

    @discord.ui.button(label="🔍 Ver Info", style=discord.ButtonStyle.grey, row=1)
    async def ver_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self._check(interaction):
            return await interaction.response.send_message("❌ Solo el admin puede usar esto.", ephemeral=True)
        datos = cargar_datos()
        todas = {**RAZAS, **datos.get("razas_custom", {})}
        await interaction.response.send_message(
            "Selecciona la raza para ver su info:",
            view=SeleccionarRazaView(self.ctx, todas, "info"),
            ephemeral=True
        )

    @discord.ui.button(label="🔄 Actualizar", style=discord.ButtonStyle.grey, row=1)
    async def actualizar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self._check(interaction):
            return await interaction.response.send_message("❌", ephemeral=True)
        datos = cargar_datos()
        await interaction.response.edit_message(embed=_embed_raza_panel(datos), view=self)


class SeleccionarRazaView(discord.ui.View):
    def __init__(self, ctx, pool: dict, accion: str):
        super().__init__(timeout=60.0)
        self.ctx = ctx
        self.accion = accion
        items = list(pool.keys())[:25]
        options = [discord.SelectOption(label=n[:100], description=pool[n].get("rareza", "")[:100]) for n in items]
        select = discord.ui.Select(placeholder=f"Elige una raza para {accion}...", options=options)
        select.callback = self._on_select
        self.add_item(select)
        self._pool = pool

    async def _on_select(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("❌", ephemeral=True)
        nombre = interaction.data["values"][0]

        if self.accion == "info":
            raza = self._pool[nombre]
            stats = raza.get("stats", STATS_POR_RAZA.get(nombre, {"fuerza":0,"vida":0,"agilidad":0,"suerte":0}))
            embed = discord.Embed(title=f"🧬 {nombre}", description=raza.get("desc",""), color=discord.Color.from_rgb(138, 43, 226))
            embed.add_field(name="⭐ Rareza:", value=raza.get("rareza","—"), inline=True)
            embed.add_field(name="🎲 Prob:", value=f"`{raza.get('peso',0)*100:.2f}%`", inline=True)
            if raza.get("poder"):
                embed.add_field(name="✨ Poder:", value=raza["poder"], inline=False)
            if raza.get("desventaja"):
                embed.add_field(name="⚠️ Desventaja:", value=raza["desventaja"], inline=False)
            embed.add_field(name="📊 Stats:", value=f"💪`{stats['fuerza']}` ❤️`{stats['vida']}` ⚡`{stats['agilidad']}` 🍀`{stats['suerte']}`", inline=False)
            if raza.get("gif","").startswith("http"):
                embed.set_image(url=raza["gif"])
            return await interaction.response.edit_message(content=None, embed=embed, view=None)

        if self.accion == "borrar":
            class ConfirmarView(discord.ui.View):
                def __init__(self2):
                    super().__init__(timeout=30.0)
                @discord.ui.button(label="✅ Confirmar", style=discord.ButtonStyle.red)
                async def confirmar(self2, inter: discord.Interaction, btn):
                    datos = cargar_datos()
                    datos["razas_custom"].pop(nombre, None)
                    guardar_datos(datos)
                    await inter.response.edit_message(content=f"🗑️ Raza **{nombre}** eliminada.", view=None)
                @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.grey)
                async def cancelar(self2, inter: discord.Interaction, btn):
                    await inter.response.edit_message(content="Cancelado.", view=None)
            return await interaction.response.edit_message(content=f"⚠️ ¿Eliminar **{nombre}**? No se puede deshacer.", view=ConfirmarView())

        if self.accion == "editar":
            datos = cargar_datos()
            raza = datos["razas_custom"].get(nombre, {})
            await interaction.response.send_modal(EditarRazaModal(self.ctx, nombre, raza))


class CrearRazaModal(discord.ui.Modal, title="🧬 Crear Nueva Raza"):
    nombre     = discord.ui.TextInput(label="Nombre de la Raza", placeholder="Ej: Dragón Ancestral", max_length=50)
    rareza     = discord.ui.TextInput(label="Rareza y Peso (rareza|0.05)", placeholder="Ej: 🔴 Mítico|0.02", max_length=50)
    descripcion= discord.ui.TextInput(label="Descripción", style=discord.TextStyle.paragraph, placeholder="Origen y características...", max_length=300)
    poder_desv = discord.ui.TextInput(label="Poder | Desventaja (separados por |)", style=discord.TextStyle.paragraph, placeholder="Poder especial | Desventaja de la raza", max_length=400)
    stats_gif  = discord.ui.TextInput(label="Stats y GIF  (fuerza/vida/agilidad/suerte | url)", placeholder="Ej: 7/5/4/4 | https://i.imgur.com/xyz.gif", max_length=200)

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    async def on_submit(self, interaction: discord.Interaction):
        try:
            rar_parts = self.rareza.value.split("|")
            rareza_txt = rar_parts[0].strip()
            peso_val = float(rar_parts[1].strip()) if len(rar_parts) > 1 else 0.01
        except:
            return await interaction.response.send_message("❌ Formato rareza inválido. Usa: `🔴 Mítico|0.02`", ephemeral=True)

        try:
            pd_parts = self.poder_desv.value.split("|")
            poder_txt = pd_parts[0].strip()
            desv_txt = pd_parts[1].strip() if len(pd_parts) > 1 else "Sin desventaja definida."
        except:
            return await interaction.response.send_message("❌ Formato poder/desventaja inválido.", ephemeral=True)

        try:
            sg_parts = self.stats_gif.value.split("|")
            nums = [int(x.strip()) for x in sg_parts[0].split("/")]
            if len(nums) != 4 or any(v < 0 or v > 20 for v in nums):
                raise ValueError
            fuerza, vida, agilidad, suerte = nums
            gif_url = sg_parts[1].strip() if len(sg_parts) > 1 and sg_parts[1].strip().startswith("http") else "https://i.imgur.com/vH_w9Wz.gif"
        except:
            return await interaction.response.send_message("❌ Formato stats inválido. Usa: `7/5/4/4 | https://gif.url`", ephemeral=True)

        nombre_raza = self.nombre.value.strip()
        datos = cargar_datos()
        datos.setdefault("razas_custom", {})
        if nombre_raza in RAZAS or nombre_raza in datos["razas_custom"]:
            return await interaction.response.send_message(f"❌ Ya existe una raza llamada **{nombre_raza}**.", ephemeral=True)

        datos["razas_custom"][nombre_raza] = {
            "rareza": rareza_txt, "peso": peso_val,
            "desc": self.descripcion.value.strip(),
            "poder": poder_txt, "desventaja": desv_txt, "gif": gif_url,
            "stats": {"fuerza": fuerza, "vida": vida, "agilidad": agilidad, "suerte": suerte}
        }
        guardar_datos(datos)

        embed = discord.Embed(title=f"✅ ¡Raza **{nombre_raza}** Creada!", color=discord.Color.from_rgb(138, 43, 226))
        embed.add_field(name="⭐ Rareza:", value=rareza_txt, inline=True)
        embed.add_field(name="🎲 Probabilidad:", value=f"`{peso_val*100:.2f}%`", inline=True)
        embed.add_field(name="📖 Descripción:", value=self.descripcion.value.strip(), inline=False)
        embed.add_field(name="✨ Poder:", value=poder_txt, inline=False)
        embed.add_field(name="⚠️ Desventaja:", value=desv_txt, inline=False)
        embed.add_field(name="📊 Stats Base:", value=f"💪`{fuerza}` ❤️`{vida}` ⚡`{agilidad}` 🍀`{suerte}`", inline=False)
        embed.set_footer(text=f"Creada por {self.ctx.author.display_name}")
        if gif_url != "https://i.imgur.com/vH_w9Wz.gif":
            embed.set_image(url=gif_url)
        await interaction.response.send_message(embed=embed)


class EditarRazaModal(discord.ui.Modal, title="✏️ Editar Raza"):
    rareza     = discord.ui.TextInput(label="Rareza y Peso (rareza|0.05)", max_length=50)
    descripcion= discord.ui.TextInput(label="Descripción", style=discord.TextStyle.paragraph, max_length=300)
    poder_desv = discord.ui.TextInput(label="Poder | Desventaja", style=discord.TextStyle.paragraph, max_length=400)
    stats_gif  = discord.ui.TextInput(label="Stats y GIF (fuerza/vida/agilidad/suerte | url)", max_length=200)

    def __init__(self, ctx, nombre_raza: str, raza: dict):
        super().__init__(title=f"✏️ Editar: {nombre_raza[:35]}")
        self.ctx = ctx
        self.nombre_raza = nombre_raza
        s = raza.get("stats", {"fuerza":0,"vida":0,"agilidad":0,"suerte":0})
        self.rareza.default      = f"{raza.get('rareza','')}|{raza.get('peso',0.01)}"
        self.descripcion.default = raza.get("desc","")
        self.poder_desv.default  = f"{raza.get('poder','')} | {raza.get('desventaja','')}"
        self.stats_gif.default   = f"{s['fuerza']}/{s['vida']}/{s['agilidad']}/{s['suerte']} | {raza.get('gif','')}"

    async def on_submit(self, interaction: discord.Interaction):
        try:
            rar_parts = self.rareza.value.split("|")
            rareza_txt = rar_parts[0].strip()
            peso_val = float(rar_parts[1].strip()) if len(rar_parts) > 1 else 0.01
        except:
            return await interaction.response.send_message("❌ Formato rareza inválido.", ephemeral=True)

        try:
            pd_parts = self.poder_desv.value.split("|")
            poder_txt = pd_parts[0].strip()
            desv_txt = pd_parts[1].strip() if len(pd_parts) > 1 else "Sin desventaja."
        except:
            return await interaction.response.send_message("❌ Formato poder/desventaja inválido.", ephemeral=True)

        try:
            sg_parts = self.stats_gif.value.split("|")
            nums = [int(x.strip()) for x in sg_parts[0].split("/")]
            if len(nums) != 4 or any(v < 0 or v > 20 for v in nums):
                raise ValueError
            fuerza, vida, agilidad, suerte = nums
            gif_url = sg_parts[1].strip() if len(sg_parts) > 1 and sg_parts[1].strip().startswith("http") else "https://i.imgur.com/vH_w9Wz.gif"
        except:
            return await interaction.response.send_message("❌ Formato stats inválido.", ephemeral=True)

        datos = cargar_datos()
        datos["razas_custom"][self.nombre_raza].update({
            "rareza": rareza_txt, "peso": peso_val,
            "desc": self.descripcion.value.strip(),
            "poder": poder_txt, "desventaja": desv_txt, "gif": gif_url,
            "stats": {"fuerza": fuerza, "vida": vida, "agilidad": agilidad, "suerte": suerte}
        })
        guardar_datos(datos)

        embed = discord.Embed(title=f"✏️ Raza **{self.nombre_raza}** Actualizada", color=discord.Color.orange())
        embed.add_field(name="⭐ Rareza:", value=rareza_txt, inline=True)
        embed.add_field(name="📊 Stats:", value=f"💪`{fuerza}` ❤️`{vida}` ⚡`{agilidad}` 🍀`{suerte}`", inline=False)
        await interaction.response.send_message(embed=embed)


@bot.command(name="razas", aliases=["gestionrazas", "panelrazas"])
async def gestion_razas(ctx):
    """Panel interactivo para gestionar razas. +razas"""
    if not es_admin_bot(ctx):
        return await ctx.send("❌ Solo los administradores pueden gestionar razas.")
    datos = cargar_datos()
    await ctx.send(embed=_embed_raza_panel(datos), view=RazasPanelView(ctx))


@bot.command(name="inforaza")
async def inforaza(ctx, *, nombre_raza: str = None):
    """Muestra la ficha de una raza. +inforaza [nombre]"""
    if not nombre_raza:
        return await ctx.send("❌ Uso: `+inforaza [nombre de la raza]`")
    datos = cargar_datos()
    razas_custom = datos.get("razas_custom", {})
    todas = {**RAZAS, **razas_custom}
    if nombre_raza not in todas:
        return await ctx.send(f"❌ No encontré **{nombre_raza}**. Usa `+razas` para ver el listado.")
    raza = todas[nombre_raza]
    stats = raza.get("stats", STATS_POR_RAZA.get(nombre_raza, {"fuerza":0,"vida":0,"agilidad":0,"suerte":0}))
    embed = discord.Embed(title=f"🧬 {nombre_raza}", description=raza.get("desc",""), color=discord.Color.from_rgb(138, 43, 226))
    embed.add_field(name="⭐ Rareza:", value=raza.get("rareza","—"), inline=True)
    embed.add_field(name="🎲 Probabilidad:", value=f"`{raza.get('peso',0)*100:.2f}%`", inline=True)
    if raza.get("poder"):
        embed.add_field(name="✨ Poder:", value=raza["poder"], inline=False)
    if raza.get("desventaja"):
        embed.add_field(name="⚠️ Desventaja:", value=raza["desventaja"], inline=False)
    embed.add_field(name="📊 Stats Base:", value=f"💪 Fuerza `{stats['fuerza']}` | ❤️ Vida `{stats['vida']}` | ⚡ Agilidad `{stats['agilidad']}` | 🍀 Suerte `{stats['suerte']}`", inline=False)
    if raza.get("gif","").startswith("http"):
        embed.set_image(url=raza["gif"])
    await ctx.send(embed=embed)



# =========================================================================
# 🚀 ARRANQUE DEL BOT
# =========================================================================

from skills import setup_skills
setup_skills(bot, cargar_datos, guardar_datos, verificar_usuario, es_admin_bot)

TOKEN = os.environ.get("TOKEN")
bot.run(TOKEN)
