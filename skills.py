# -*- coding: utf-8 -*-
# =========================================================================
# 🌿 SKILL TREES POR MAGIA — Black Clover Bot
# Cada magia tiene un árbol de habilidades desbloqueables con Skill Points.
# Los Skill Points solo los otorgan los administradores con +darsp.
# =========================================================================

# Estructura de cada habilidad:
# "id_habilidad": {
#     "nombre": str,
#     "desc": str,
#     "costo": int,          # Skill Points requeridos
#     "requiere": list[str]  # IDs de habilidades previas (vacío = disponible desde inicio)
# }

SKILL_TREES = {

    # ══════════════════════════════════════════════
    # 🔥 FUEGO
    # ══════════════════════════════════════════════
    "Fuego": {
        "mana_skin_fuego": {
            "nombre": "Mana Skin: Escudo de Brasa",
            "desc": "Recubres tu cuerpo con una capa de maná ardiente que absorbe el primer impacto mágico recibido.",
            "costo": 1,
            "requiere": []
        },
        "control_llamas": {
            "nombre": "Control de Llamas",
            "desc": "Aumentas la precisión de tus llamas, permitiendo moldearlas en formas definidas sin dispersión.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_fuego": {
            "nombre": "Mana Zone: Dominio Incandescente",
            "desc": "Extiendes tu maná al entorno, convirtiendo el área en un campo de fuego que obedece tu voluntad.",
            "costo": 3,
            "requiere": ["mana_skin_fuego", "control_llamas"]
        },
        "resistencia_termica": {
            "nombre": "Resistencia Térmica",
            "desc": "Tu cuerpo se adapta al calor extremo. Eres inmune a quemaduras propias y reduces el daño de fuego externo.",
            "costo": 2,
            "requiere": ["mana_skin_fuego"]
        },
        "llamarada_solar": {
            "nombre": "Llamarada Solar",
            "desc": "Técnica avanzada: concentras todo tu maná en un punto y liberas una columna de fuego de temperatura solar.",
            "costo": 4,
            "requiere": ["mana_zone_fuego", "resistencia_termica"]
        },
    },

    # ══════════════════════════════════════════════
    # 💧 AGUA
    # ══════════════════════════════════════════════
    "Agua": {
        "mana_skin_agua": {
            "nombre": "Mana Skin: Manto Fluido",
            "desc": "Una capa de agua densa cubre tu cuerpo, amortiguando golpes físicos y desviando proyectiles menores.",
            "costo": 1,
            "requiere": []
        },
        "sanacion_basica": {
            "nombre": "Sanación Básica",
            "desc": "Canalizas maná en forma de agua para cerrar heridas leves propias o de un aliado cercano.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_agua": {
            "nombre": "Mana Zone: Mar Interior",
            "desc": "Inundas el campo de batalla con tu maná acuoso, controlando las corrientes para ralentizar enemigos.",
            "costo": 3,
            "requiere": ["mana_skin_agua", "sanacion_basica"]
        },
        "sanacion_profunda": {
            "nombre": "Sanación Profunda",
            "desc": "Técnica avanzada de curación que regenera heridas graves en aliados, requiriendo alta concentración.",
            "costo": 2,
            "requiere": ["sanacion_basica"]
        },
        "vortice_abismal": {
            "nombre": "Vórtice Abismal",
            "desc": "Generas un remolino gigante de agua comprimida que tritura todo lo que atrapa en su interior.",
            "costo": 4,
            "requiere": ["mana_zone_agua", "sanacion_profunda"]
        },
    },

    # ══════════════════════════════════════════════
    # 🌪️ VIENTO
    # ══════════════════════════════════════════════
    "Viento": {
        "mana_skin_viento": {
            "nombre": "Mana Skin: Velo Aéreo",
            "desc": "Una corriente de aire rodea tu cuerpo, desviando ataques de proyectil y aumentando tu agilidad.",
            "costo": 1,
            "requiere": []
        },
        "vuelo_basico": {
            "nombre": "Vuelo Básico",
            "desc": "Canalizas viento bajo tus pies para levitar y desplazarte a baja altitud durante combate.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_viento": {
            "nombre": "Mana Zone: Ojo del Huracán",
            "desc": "Tu maná se expande como un ciclón. Controlas el viento del área, pudiendo redirigir hechizos enemigos.",
            "costo": 3,
            "requiere": ["mana_skin_viento", "vuelo_basico"]
        },
        "rafaga_cortante": {
            "nombre": "Ráfaga Cortante",
            "desc": "Comprimes el viento en hojas invisibles capaces de cortar acero con precisión quirúrgica.",
            "costo": 2,
            "requiere": ["mana_skin_viento"]
        },
        "tornado_devastador": {
            "nombre": "Tornado Devastador",
            "desc": "Invocas un tornado de nivel máximo que arrasa el campo de batalla arrastrando todo a su paso.",
            "costo": 4,
            "requiere": ["mana_zone_viento", "rafaga_cortante"]
        },
    },

    # ══════════════════════════════════════════════
    # 🪨 TIERRA
    # ══════════════════════════════════════════════
    "Tierra": {
        "mana_skin_tierra": {
            "nombre": "Mana Skin: Armadura de Piedra",
            "desc": "Cubres tu cuerpo con una capa de roca sólida que incrementa dramáticamente tu resistencia física.",
            "costo": 1,
            "requiere": []
        },
        "muro_terreo": {
            "nombre": "Muro Térreo",
            "desc": "Levantas instantáneamente una pared de tierra compacta para bloquear ataques entrantes.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_tierra": {
            "nombre": "Mana Zone: Dominio Sísmico",
            "desc": "Controlas el terreno en un radio amplio. Puedes crear grietas, elevar columnas o hundir el suelo.",
            "costo": 3,
            "requiere": ["mana_skin_tierra", "muro_terreo"]
        },
        "golpe_sismico": {
            "nombre": "Golpe Sísmico",
            "desc": "Golpeas el suelo liberando una onda de choque que derriba a todos los enemigos en el área.",
            "costo": 2,
            "requiere": ["muro_terreo"]
        },
        "fortaleza_titan": {
            "nombre": "Fortaleza Titán",
            "desc": "Te encierras en una armadura completa de tierra mágica. Tu movilidad baja pero eres casi indestructible.",
            "costo": 4,
            "requiere": ["mana_zone_tierra", "golpe_sismico"]
        },
    },

    # ══════════════════════════════════════════════
    # ❄️ HIELO
    # ══════════════════════════════════════════════
    "Hielo": {
        "mana_skin_hielo": {
            "nombre": "Mana Skin: Cristal Glacial",
            "desc": "Una capa de hielo mágico te recubre. Absorbe calor enemigo y ralentiza a quien te toque.",
            "costo": 1,
            "requiere": []
        },
        "congelamiento_basico": {
            "nombre": "Congelamiento Básico",
            "desc": "Puedes congelar superficies de contacto. Útil para atrapar extremidades o crear resbaladeros.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_hielo": {
            "nombre": "Mana Zone: Tundra Eterna",
            "desc": "La temperatura del área desciende a niveles mortales. El movimiento enemigo se ralentiza un 50%.",
            "costo": 3,
            "requiere": ["mana_skin_hielo", "congelamiento_basico"]
        },
        "lanza_glaciar": {
            "nombre": "Lanza Glaciar",
            "desc": "Proyectas lanzas de hielo de alta densidad que perforan defensas mágicas y físicas.",
            "costo": 2,
            "requiere": ["congelamiento_basico"]
        },
        "suspension_absoluta": {
            "nombre": "Suspensión Absoluta",
            "desc": "Técnica máxima: congelas todo lo que está en tu campo de visión en un instante.",
            "costo": 4,
            "requiere": ["mana_zone_hielo", "lanza_glaciar"]
        },
    },

    # ══════════════════════════════════════════════
    # 🌿 PLANTA
    # ══════════════════════════════════════════════
    "Planta": {
        "mana_skin_planta": {
            "nombre": "Mana Skin: Enredadera Viva",
            "desc": "Raíces delgadas cubren tu cuerpo y absorben golpes físicos, regenerándose con el maná del entorno.",
            "costo": 1,
            "requiere": []
        },
        "raices_trampa": {
            "nombre": "Raíces Trampa",
            "desc": "Haces brotar raíces del suelo que inmovilizan a un objetivo durante el combate.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_planta": {
            "nombre": "Mana Zone: Bosque Viviente",
            "desc": "El entorno florece bajo tu control. Árboles y enredaderas gigantes obedecen tus órdenes.",
            "costo": 3,
            "requiere": ["mana_skin_planta", "raices_trampa"]
        },
        "esporas_toxicas": {
            "nombre": "Esporas Tóxicas",
            "desc": "Liberas una nube de esporas que debilitan el maná del enemigo al inhalarlas.",
            "costo": 2,
            "requiere": ["raices_trampa"]
        },
        "coloso_vegetal": {
            "nombre": "Coloso Vegetal",
            "desc": "Invocas un gigantesco golem de madera y raíces que lucha a tu lado como guardián.",
            "costo": 4,
            "requiere": ["mana_zone_planta", "esporas_toxicas"]
        },
    },

    # ══════════════════════════════════════════════
    # 🟤 BARRO
    # ══════════════════════════════════════════════
    "Barro": {
        "mana_skin_barro": {
            "nombre": "Mana Skin: Costra de Légamo",
            "desc": "Una capa pegajosa de barro mágico recubre tu cuerpo, absorbiendo impactos y ralentizando atacantes.",
            "costo": 1,
            "requiere": []
        },
        "pantano_basico": {
            "nombre": "Pantano Básico",
            "desc": "Conviertes el suelo cercano en barro profundo que drena la agilidad de quien lo pise.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_barro": {
            "nombre": "Mana Zone: Ciénaga Absoluta",
            "desc": "El terreno completo se convierte en un pantano mágico. Moverse en él consume el doble de energía.",
            "costo": 3,
            "requiere": ["mana_skin_barro", "pantano_basico"]
        },
        "golem_barro": {
            "nombre": "Gólem de Barro",
            "desc": "Moldeas el barro en un guardián gigante que bloquea ataques y aplasta enemigos.",
            "costo": 2,
            "requiere": ["pantano_basico"]
        },
        "sumidero_infernal": {
            "nombre": "Sumidero Infernal",
            "desc": "Abres un sumidero de barro que absorbe hechizos de área y engulle a los enemigos atrapados.",
            "costo": 4,
            "requiere": ["mana_zone_barro", "golem_barro"]
        },
    },

    # ══════════════════════════════════════════════
    # 💨 HUMO
    # ══════════════════════════════════════════════
    "Humo": {
        "mana_skin_humo": {
            "nombre": "Mana Skin: Forma Gaseosa",
            "desc": "Tu cuerpo se vuelve parcialmente gaseoso, haciendo que ataques físicos directos te atraviesen.",
            "costo": 1,
            "requiere": []
        },
        "cortina_humo": {
            "nombre": "Cortina de Humo",
            "desc": "Generas una densa nube que bloquea la visión en el área, ideal para emboscadas y retiradas.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_humo": {
            "nombre": "Mana Zone: Niebla Tóxica",
            "desc": "El campo se llena de un humo mágico que confunde los sentidos y bloquea la percepción del maná.",
            "costo": 3,
            "requiere": ["mana_skin_humo", "cortina_humo"]
        },
        "asfixia_magica": {
            "nombre": "Asfixia Mágica",
            "desc": "Concentras el humo en los pulmones del enemigo, reduciendo su capacidad de pronunciar hechizos.",
            "costo": 2,
            "requiere": ["cortina_humo"]
        },
        "tormenta_cenicienta": {
            "nombre": "Tormenta Cenicienta",
            "desc": "Liberas una tormenta de humo abrasivo que corroe armaduras y quema la piel del enemigo.",
            "costo": 4,
            "requiere": ["mana_zone_humo", "asfixia_magica"]
        },
    },

    # ══════════════════════════════════════════════
    # 🪨 ROCA
    # ══════════════════════════════════════════════
    "Roca": {
        "mana_skin_roca": {
            "nombre": "Mana Skin: Piel Pétrea",
            "desc": "Tu piel se endurece como granito mágico, resistiendo cortes y golpes contundentes con facilidad.",
            "costo": 1,
            "requiere": []
        },
        "proyectil_rocoso": {
            "nombre": "Proyectil Rocoso",
            "desc": "Lanzas fragmentos de roca comprimida a alta velocidad, capaces de perforar armaduras básicas.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_roca": {
            "nombre": "Mana Zone: Campo Mineral",
            "desc": "Controlas la roca del entorno. Puedes crear barreras, lanzar pilares o aplastar con el techo.",
            "costo": 3,
            "requiere": ["mana_skin_roca", "proyectil_rocoso"]
        },
        "avalancha": {
            "nombre": "Avalancha",
            "desc": "Derrumbas toneladas de roca sobre un área, sepultando a los enemigos bajo el peso mineral.",
            "costo": 2,
            "requiere": ["proyectil_rocoso"]
        },
        "fortaleza_pétrea": {
            "nombre": "Fortaleza Pétrea",
            "desc": "Construyes en segundos una fortaleza de roca mágica que protege a todos los aliados dentro.",
            "costo": 4,
            "requiere": ["mana_zone_roca", "avalancha"]
        },
    },

    # ══════════════════════════════════════════════
    # ⛓️ CADENA
    # ══════════════════════════════════════════════
    "Cadena": {
        "mana_skin_cadena": {
            "nombre": "Mana Skin: Malla de Hierro",
            "desc": "Cadenas de maná envuelven tu cuerpo formando una malla que detiene cortes y proyectiles.",
            "costo": 1,
            "requiere": []
        },
        "amarre_basico": {
            "nombre": "Amarre Básico",
            "desc": "Lanzas cadenas de hierro mágico que inmovilizan extremidades de un objetivo.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_cadena": {
            "nombre": "Mana Zone: Prisión de Hierro",
            "desc": "Cadenas invisibles emergen del suelo en todo el radio de tu maná, inmovilizando a múltiples enemigos.",
            "costo": 3,
            "requiere": ["mana_skin_cadena", "amarre_basico"]
        },
        "cadena_selladora": {
            "nombre": "Cadena Selladora",
            "desc": "Una cadena especial que suprime el acceso al maná del objetivo mientras permanezca encadenado.",
            "costo": 2,
            "requiere": ["amarre_basico"]
        },
        "jaula_eterna": {
            "nombre": "Jaula Eterna",
            "desc": "Encierras al objetivo en una esfera de cadenas indestructibles que no puede romperse desde adentro.",
            "costo": 4,
            "requiere": ["mana_zone_cadena", "cadena_selladora"]
        },
    },

    # ══════════════════════════════════════════════
    # 🎲 DADOS
    # ══════════════════════════════════════════════
    "Dados": {
        "mana_skin_dados": {
            "nombre": "Mana Skin: Escudo del Azar",
            "desc": "Tu defensa varía según el azar. Cada ataque recibido tiene probabilidad de ser completamente negado.",
            "costo": 1,
            "requiere": []
        },
        "tiro_de_suerte": {
            "nombre": "Tiro de Suerte",
            "desc": "Lanzas un hechizo cuyo poder se determina al azar. Puede ser débil o devastadoramente poderoso.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_dados": {
            "nombre": "Mana Zone: Campo del Caos",
            "desc": "El campo de batalla se vuelve impredecible. Los hechizos de todos tienen resultados aleatorios amplificados.",
            "costo": 3,
            "requiere": ["mana_skin_dados", "tiro_de_suerte"]
        },
        "destino_forzado": {
            "nombre": "Destino Forzado",
            "desc": "Manipulas la probabilidad para que tu próximo ataque tenga el resultado más favorable posible.",
            "costo": 2,
            "requiere": ["tiro_de_suerte"]
        },
        "jackpot_magico": {
            "nombre": "¡Jackpot Mágico!",
            "desc": "Una explosión de maná puro con potencia máxima. Requiere cargar suerte en tres turnos previos.",
            "costo": 4,
            "requiere": ["mana_zone_dados", "destino_forzado"]
        },
    },

    # ══════════════════════════════════════════════
    # 💚 CURACIÓN
    # ══════════════════════════════════════════════
    "Curación": {
        "mana_skin_curacion": {
            "nombre": "Mana Skin: Aura Regenerativa",
            "desc": "Tu cuerpo emana maná curativo constantemente, sellando heridas menores en tiempo real.",
            "costo": 1,
            "requiere": []
        },
        "primer_auxilio": {
            "nombre": "Primer Auxilio",
            "desc": "Curas heridas externas de un aliado de forma rápida. Detiene hemorragias y alivia venenos simples.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_curacion": {
            "nombre": "Mana Zone: Santuario Viviente",
            "desc": "Todo aliado dentro de tu radio de maná regenera salud continuamente mientras permanezca en él.",
            "costo": 3,
            "requiere": ["mana_skin_curacion", "primer_auxilio"]
        },
        "restauracion_profunda": {
            "nombre": "Restauración Profunda",
            "desc": "Sanas heridas internas, huesos rotos y daño mágico acumulado en un aliado gravemente herido.",
            "costo": 2,
            "requiere": ["primer_auxilio"]
        },
        "resurreccion_parcial": {
            "nombre": "Resurrección Parcial",
            "desc": "Técnica extrema: estabilizas a un aliado al borde de la muerte, restaurando el mínimo vital de maná.",
            "costo": 4,
            "requiere": ["mana_zone_curacion", "restauracion_profunda"]
        },
    },

    # ══════════════════════════════════════════════
    # 🌑 CENIZA
    # ══════════════════════════════════════════════
    "Ceniza": {
        "mana_skin_ceniza": {
            "nombre": "Mana Skin: Capa de Polvo",
            "desc": "Ceniza mágica rodea tu cuerpo. Al recibir golpes, explota en una nube que cega al atacante.",
            "costo": 1,
            "requiere": []
        },
        "trampa_retardada": {
            "nombre": "Trampa Retardada",
            "desc": "Colocas ceniza explosiva en el suelo que detona cuando un enemigo la pisa.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_ceniza": {
            "nombre": "Mana Zone: Lluvia de Brasas",
            "desc": "El área se llena de ceniza flotante que puede detonar en cadena con una chispa de maná.",
            "costo": 3,
            "requiere": ["mana_skin_ceniza", "trampa_retardada"]
        },
        "polvo_corrosivo": {
            "nombre": "Polvo Corrosivo",
            "desc": "Ceniza especial que corroe el maná del objetivo, reduciendo la potencia de sus hechizos.",
            "costo": 2,
            "requiere": ["trampa_retardada"]
        },
        "explosion_final": {
            "nombre": "Explosión Final",
            "desc": "Detonas toda la ceniza del campo simultáneamente en una explosión que arrasa el área completa.",
            "costo": 4,
            "requiere": ["mana_zone_ceniza", "polvo_corrosivo"]
        },
    },

    # ══════════════════════════════════════════════
    # ⚡ RAYO
    # ══════════════════════════════════════════════
    "Rayo": {
        "mana_skin_rayo": {
            "nombre": "Mana Skin: Campo Electromagnético",
            "desc": "Un campo eléctrico rodea tu cuerpo, paralizando brevemente a quien intente tocarte.",
            "costo": 1,
            "requiere": []
        },
        "velocidad_relampago": {
            "nombre": "Velocidad Relámpago",
            "desc": "Canalizas electricidad en tus piernas, triplicando tu velocidad de desplazamiento.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_rayo": {
            "nombre": "Mana Zone: Tormenta Eléctrica",
            "desc": "El área se convierte en una tormenta de descargas. Cualquier metal o magia conductora explota.",
            "costo": 3,
            "requiere": ["mana_skin_rayo", "velocidad_relampago"]
        },
        "descarga_paralizante": {
            "nombre": "Descarga Paralizante",
            "desc": "Envías una descarga dirigida que paraliza el sistema nervioso mágico del objetivo por un turno.",
            "costo": 2,
            "requiere": ["velocidad_relampago"]
        },
        "rayo_divino": {
            "nombre": "Rayo Divino",
            "desc": "El ataque eléctrico más poderoso. Una columna de plasma cae del cielo sobre el objetivo.",
            "costo": 4,
            "requiere": ["mana_zone_rayo", "descarga_paralizante"]
        },
    },

    # ══════════════════════════════════════════════
    # 🏜️ ARENA
    # ══════════════════════════════════════════════
    "Arena": {
        "mana_skin_arena": {
            "nombre": "Mana Skin: Cuerpo de Arena",
            "desc": "Tu cuerpo se dispersa parcialmente en arena al recibir golpes, reduciendo el daño recibido.",
            "costo": 1,
            "requiere": []
        },
        "tormenta_arena": {
            "nombre": "Tormenta de Arena",
            "desc": "Invocas una ráfaga de arena que ciega y corta la piel de los enemigos en el área.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_arena": {
            "nombre": "Mana Zone: Desierto Infinito",
            "desc": "El suelo se convierte en arena movediza mágica que obedece tus órdenes.",
            "costo": 3,
            "requiere": ["mana_skin_arena", "tormenta_arena"]
        },
        "golem_arena": {
            "nombre": "Gólem de Arena",
            "desc": "Moldeas la arena en un guerrero gigante que pelea a tu lado y absorbe ataques.",
            "costo": 2,
            "requiere": ["tormenta_arena"]
        },
        "sepultura_del_desierto": {
            "nombre": "Sepultura del Desierto",
            "desc": "Hundes al objetivo en arena movediza mágica de la que es imposible escapar sin ayuda.",
            "costo": 4,
            "requiere": ["mana_zone_arena", "golem_arena"]
        },
    },

    # ══════════════════════════════════════════════
    # 🌑 OSCURIDAD
    # ══════════════════════════════════════════════
    "Oscuridad": {
        "mana_skin_oscuridad": {
            "nombre": "Mana Skin: Manto de Sombra",
            "desc": "La oscuridad te envuelve, dificultando que los enemigos te detecten y absorbiendo maná de ataques.",
            "costo": 1,
            "requiere": []
        },
        "absorcion_magica": {
            "nombre": "Absorción Mágica",
            "desc": "Al recibir un hechizo, puedes absorber parte de su maná para potenciar el siguiente ataque.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_oscuridad": {
            "nombre": "Mana Zone: Vacío Absoluto",
            "desc": "La luz desaparece del área. Solo tú puedes ver. Los enemigos quedan ciegos dentro de tu dominio.",
            "costo": 3,
            "requiere": ["mana_skin_oscuridad", "absorcion_magica"]
        },
        "espejo_oscuro": {
            "nombre": "Espejo Oscuro",
            "desc": "Devuelves el siguiente hechizo recibido contra su lanzador con el doble de potencia.",
            "costo": 2,
            "requiere": ["absorcion_magica"]
        },
        "katana_del_vacio": {
            "nombre": "Katana del Vacío",
            "desc": "Condensa la oscuridad en una hoja que corta tanto la materia como el flujo mágico del objetivo.",
            "costo": 4,
            "requiere": ["mana_zone_oscuridad", "espejo_oscuro"]
        },
    },

    # ══════════════════════════════════════════════
    # 🧵 HILOS
    # ══════════════════════════════════════════════
    "Hilos": {
        "mana_skin_hilos": {
            "nombre": "Mana Skin: Red Invisible",
            "desc": "Hilos imperceptibles rodean tu cuerpo, alertándote de ataques antes de que lleguen.",
            "costo": 1,
            "requiere": []
        },
        "control_corporal": {
            "nombre": "Control Corporal",
            "desc": "Insertas hilos en el cuerpo de un objetivo y controlas sus movimientos básicos.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_hilos": {
            "nombre": "Mana Zone: Telaraña de Maná",
            "desc": "El área se llena de hilos invisibles que detectan movimiento y pueden cortar carne a distancia.",
            "costo": 3,
            "requiere": ["mana_skin_hilos", "control_corporal"]
        },
        "marioneta": {
            "nombre": "Marioneta",
            "desc": "Control total del cuerpo de un objetivo durante un combate. Sus hechizos también obedecen.",
            "costo": 2,
            "requiere": ["control_corporal"]
        },
        "tramado_dimensional": {
            "nombre": "Tramado Dimensional",
            "desc": "Tejes hilos en el tejido espacial del entorno, impidiendo teletransportaciones o escapes.",
            "costo": 4,
            "requiere": ["mana_zone_hilos", "marioneta"]
        },
    },

    # ══════════════════════════════════════════════
    # 🔀 PERMUTACIÓN
    # ══════════════════════════════════════════════
    "Permutación": {
        "mana_skin_permutacion": {
            "nombre": "Mana Skin: Intercambio Reactivo",
            "desc": "Al recibir daño, intercambias automáticamente las propiedades del ataque, neutralizando su efecto.",
            "costo": 1,
            "requiere": []
        },
        "intercambio_basico": {
            "nombre": "Intercambio Básico",
            "desc": "Intercambias las propiedades físicas de dos objetos o hechizos en el campo de batalla.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_permutacion": {
            "nombre": "Mana Zone: Caos de Propiedades",
            "desc": "En tu zona, todos los objetos pueden intercambiar propiedades a tu voluntad.",
            "costo": 3,
            "requiere": ["mana_skin_permutacion", "intercambio_basico"]
        },
        "intercambio_vital": {
            "nombre": "Intercambio Vital",
            "desc": "Intercambias el daño recibido con el del atacante. Lo que te iban a hacer, se lo haces a ellos.",
            "costo": 2,
            "requiere": ["intercambio_basico"]
        },
        "permutacion_total": {
            "nombre": "Permutación Total",
            "desc": "Intercambias la posición, maná y propiedades físicas completas con cualquier objetivo en el área.",
            "costo": 4,
            "requiere": ["mana_zone_permutacion", "intercambio_vital"]
        },
    },

    # ══════════════════════════════════════════════
    # 🩸 SANGRE
    # ══════════════════════════════════════════════
    "Sangre": {
        "mana_skin_sangre": {
            "nombre": "Mana Skin: Armadura Sanguínea",
            "desc": "Tu sangre endurecida forma una coraza que absorbe impactos y se regenera con tu propio maná.",
            "costo": 1,
            "requiere": []
        },
        "control_fluidos": {
            "nombre": "Control de Fluidos",
            "desc": "Manipulas los fluidos corporales de un objetivo cercano, causando daño interno o parálisis.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_sangre": {
            "nombre": "Mana Zone: Mar Carmesí",
            "desc": "El área se llena de sangre mágica flotante que obedece tus órdenes como un fluido sensible.",
            "costo": 3,
            "requiere": ["mana_skin_sangre", "control_fluidos"]
        },
        "sellado_de_heridas": {
            "nombre": "Sellado de Heridas",
            "desc": "Coagulas y sellas las heridas de un aliado instantáneamente, evitando el desangrado.",
            "costo": 2,
            "requiere": ["control_fluidos"]
        },
        "torrente_carmesi": {
            "nombre": "Torrente Carmesí",
            "desc": "Lanzas una ola de sangre mágica comprimida que arrasa el campo con presión devastadora.",
            "costo": 4,
            "requiere": ["mana_zone_sangre", "sellado_de_heridas"]
        },
    },

    # ══════════════════════════════════════════════
    # 🌑 SOMBRA
    # ══════════════════════════════════════════════
    "Sombra": {
        "mana_skin_sombra": {
            "nombre": "Mana Skin: Cuerpo de Sombra",
            "desc": "Tu cuerpo se fusiona parcialmente con las sombras, siendo difícil de golpear con ataques físicos.",
            "costo": 1,
            "requiere": []
        },
        "viaje_sombrio": {
            "nombre": "Viaje Sombrío",
            "desc": "Te desplazas a través de las sombras del entorno, apareciendo detrás del enemigo.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_sombra": {
            "nombre": "Mana Zone: Dominio de la Penumbra",
            "desc": "Las sombras del área obedecen tus órdenes. Puedes inmovilizar, cortar o envolver a los enemigos.",
            "costo": 3,
            "requiere": ["mana_skin_sombra", "viaje_sombrio"]
        },
        "clon_sombrio": {
            "nombre": "Clon Sombrío",
            "desc": "Creas una réplica de sombra que imita tus movimientos y puede recibir ataques en tu lugar.",
            "costo": 2,
            "requiere": ["viaje_sombrio"]
        },
        "prision_de_sombras": {
            "nombre": "Prisión de Sombras",
            "desc": "Atrapa al objetivo en una dimensión de sombra pura donde no puede usar maná ni moverse.",
            "costo": 4,
            "requiere": ["mana_zone_sombra", "clon_sombrio"]
        },
    },

    # ══════════════════════════════════════════════
    # 💡 LUZ
    # ══════════════════════════════════════════════
    "Luz": {
        "mana_skin_luz": {
            "nombre": "Mana Skin: Escudo de Fotones",
            "desc": "Luz condensada forma una barrera que refleja hechizos de baja potencia automáticamente.",
            "costo": 1,
            "requiere": []
        },
        "velocidad_luz": {
            "nombre": "Velocidad de la Luz",
            "desc": "Te mueves a velocidad de fotón. Prácticamente imposible de seguir con la vista o el maná.",
            "costo": 2,
            "requiere": []
        },
        "mana_zone_luz": {
            "nombre": "Mana Zone: Dominio Radiante",
            "desc": "El área estalla en luz cegadora. Solo tú puedes ver con claridad dentro de tu dominio.",
            "costo": 3,
            "requiere": ["mana_skin_luz", "velocidad_luz"]
        },
        "espada_de_fotones": {
            "nombre": "Espada de Fotones",
            "desc": "Condensas luz en una hoja que corta a velocidad de disparo. Puede destruir defensas mágicas.",
            "costo": 3,
            "requiere": ["velocidad_luz"]
        },
        "juicio_divino": {
            "nombre": "Juicio Divino",
            "desc": "Lanzas una lluvia de espadas de luz que cubren el campo completo sin punto ciego.",
            "costo": 5,
            "requiere": ["mana_zone_luz", "espada_de_fotones"]
        },
    },

    # ══════════════════════════════════════════════
    # 🌌 ESPACIO
    # ══════════════════════════════════════════════
    "Espacio": {
        "mana_skin_espacio": {
            "nombre": "Mana Skin: Burbuja Espacial",
            "desc": "Creas micro-portales alrededor tuyo que desvían proyectiles enviándolos a otra ubicación.",
            "costo": 1,
            "requiere": []
        },
        "portal_basico": {
            "nombre": "Portal Básico",
            "desc": "Abres un portal de entrada y salida para teletransportarte instantáneamente a un punto visible.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_espacio": {
            "nombre": "Mana Zone: Distorsión Espacial",
            "desc": "El espacio dentro de tu radio se dobla. Las distancias son falsas y los ataques no llegan donde parecen.",
            "costo": 3,
            "requiere": ["mana_skin_espacio", "portal_basico"]
        },
        "desgarradura": {
            "nombre": "Desgarradura",
            "desc": "Abres una grieta en el espacio que corta cualquier cosa que atraviese su plano.",
            "costo": 2,
            "requiere": ["portal_basico"]
        },
        "cubo_espacial": {
            "nombre": "Cubo Espacial",
            "desc": "Encierras al objetivo en un cubo de espacio plegado. No puede moverse, saltar ni lanzar hechizos.",
            "costo": 4,
            "requiere": ["mana_zone_espacio", "desgarradura"]
        },
    },

    # ══════════════════════════════════════════════
    # ⚖️ GRAVEDAD
    # ══════════════════════════════════════════════
    "Gravedad": {
        "mana_skin_gravedad": {
            "nombre": "Mana Skin: Aura Gravitatoria",
            "desc": "Un campo gravitacional rodea tu cuerpo, aplastando proyectiles antes de que te alcancen.",
            "costo": 2,
            "requiere": []
        },
        "aplastamiento": {
            "nombre": "Aplastamiento",
            "desc": "Aumentas la gravedad sobre un objetivo, obligándolo a caer de rodillas bajo su propio peso.",
            "costo": 1,
            "requiere": []
        },
        "mana_zone_gravedad": {
            "nombre": "Mana Zone: Singularidad",
            "desc": "Controlas la gravedad en todo el campo. Puedes invertirla, multiplicarla o anularla a voluntad.",
            "costo": 4,
            "requiere": ["mana_skin_gravedad", "aplastamiento"]
        },
        "levitacion_masiva": {
            "nombre": "Levitación Masiva",
            "desc": "Elevas del suelo a todos los enemigos del área, dejándolos indefensos en el aire.",
            "costo": 2,
            "requiere": ["aplastamiento"]
        },
        "punto_de_colapso": {
            "nombre": "Punto de Colapso",
            "desc": "Creas un punto de gravedad infinita que aplasta todo lo que está en el radio en un instante.",
            "costo": 5,
            "requiere": ["mana_zone_gravedad", "levitacion_masiva"]
        },
    },

    # ══════════════════════════════════════════════
    # 🎭 MAGIAS RESTANTES (Combinación, Algodón, Alimentos,
    #    Escamas, Canto, Sello, Brújula, Maldición, Veneno,
    #    Modificación, Cristal, Espejos, Árbol Mitológico,
    #    Sueños, Huesos, Carne, Imitación, Pintura, Almas, Causalidad)
    # ══════════════════════════════════════════════
    "Combinación": {
        "mana_skin_combinacion": {"nombre": "Mana Skin: Enlace Reactivo", "desc": "Tu maná se sincroniza con el de aliados cercanos, compartiendo parte del daño recibido.", "costo": 1, "requiere": []},
        "enlace_magico": {"nombre": "Enlace Mágico", "desc": "Conectas tu maná con el de un aliado, permitiendo que sus hechizos ganen tu elemento.", "costo": 1, "requiere": []},
        "fusion_elemental": {"nombre": "Fusión Elemental", "desc": "Combinas tu magia con la de un aliado para crear un ataque dual imposible de bloquear individualmente.", "costo": 3, "requiere": ["enlace_magico"]},
        "amplificacion": {"nombre": "Amplificación", "desc": "El hechizo combinado se amplifica con tu maná añadido, duplicando el alcance y la potencia.", "costo": 2, "requiere": ["enlace_magico"]},
        "gran_union": {"nombre": "Gran Unión", "desc": "Fusionas el maná de hasta tres aliados en un único hechizo de potencia devastadora.", "costo": 4, "requiere": ["fusion_elemental", "amplificacion"]},
    },
    "Algodón": {
        "mana_skin_algodon": {"nombre": "Mana Skin: Relleno Absorbente", "desc": "El algodón mágico amortigua golpes físicos. Eres resistente a contusiones y caídas.", "costo": 1, "requiere": []},
        "trampa_algodon": {"nombre": "Trampa de Algodón", "desc": "Disparas bolas de algodón endurecido que atrapan extremidades al contacto.", "costo": 1, "requiere": []},
        "mana_zone_algodon": {"nombre": "Mana Zone: Nube de Algodón", "desc": "El área se llena de algodón flotante que amortigua todos los ataques, propios y enemigos.", "costo": 3, "requiere": ["mana_skin_algodon", "trampa_algodon"]},
        "presion_comprimida": {"nombre": "Presión Comprimida", "desc": "Comprimes el algodón hasta endurecerlo como acero, creando proyectiles o armaduras sólidas.", "costo": 2, "requiere": ["trampa_algodon"]},
        "tormenta_blanca": {"nombre": "Tormenta Blanca", "desc": "Lanzas una avalancha de algodón comprimido que entierra al enemigo bajo toneladas de material.", "costo": 4, "requiere": ["mana_zone_algodon", "presion_comprimida"]},
    },
    "Alimentos": {
        "mana_skin_alimentos": {"nombre": "Mana Skin: Aroma Reparador", "desc": "El aroma de tu magia restaura gradualmente el maná de aliados cercanos en combate.", "costo": 1, "requiere": []},
        "festin_rapido": {"nombre": "Festín Rápido", "desc": "Creas una ración mágica que restaura el maná de un aliado al instante.", "costo": 1, "requiere": []},
        "banquete_de_mana": {"nombre": "Banquete de Maná", "desc": "Preparas un banquete mágico que recupera el maná completo de todo el equipo tras el combate.", "costo": 3, "requiere": ["festin_rapido"]},
        "pocion_culinaria": {"nombre": "Poción Culinaria", "desc": "Preparas una poción comestible que otorga un buff temporal de fuerza o resistencia.", "costo": 2, "requiere": ["festin_rapido"]},
        "gran_banquete": {"nombre": "Gran Banquete Mágico", "desc": "Un festín épico que regenera por completo a todos los aliados del campo, incluso en combate.", "costo": 5, "requiere": ["banquete_de_mana", "pocion_culinaria"]},
    },
    "Escamas": {
        "mana_skin_escamas": {"nombre": "Mana Skin: Escamas Deflectoras", "desc": "Tus escamas mágicas desvían ataques de magia menores como una armadura de dragón.", "costo": 1, "requiere": []},
        "peso_magico": {"nombre": "Peso Mágico", "desc": "Aumentas el peso de los hechizos enemigos entrantes, haciendo que caigan antes de alcanzarte.", "costo": 1, "requiere": []},
        "mana_zone_escamas": {"nombre": "Mana Zone: Caparazón de Dragón", "desc": "El campo se llena de escamas flotantes que alteran la trayectoria de todos los ataques.", "costo": 3, "requiere": ["mana_skin_escamas", "peso_magico"]},
        "contra_golpe": {"nombre": "Contragolpe Escamoso", "desc": "Al recibir un ataque, tus escamas liberan la energía absorbida de vuelta al atacante.", "costo": 2, "requiere": ["peso_magico"]},
        "dragon_escamado": {"nombre": "Dragón Escamado", "desc": "Invocas una armadura completa de escamas de dragón mágico. Resistencia máxima por un turno.", "costo": 4, "requiere": ["mana_zone_escamas", "contra_golpe"]},
    },

    "Canto": {
        "mana_skin_canto": {"nombre": "Mana Skin: Barrera Sónica", "desc": "Tu voz genera una onda de sonido que absorbe impactos físicos alrededor tuyo.", "costo": 1, "requiere": []},
        "nota_potenciadora": {"nombre": "Nota Potenciadora", "desc": "Emites una nota mágica que incrementa la potencia de maná de aliados en el área.", "costo": 1, "requiere": []},
        "mana_zone_canto": {"nombre": "Mana Zone: Sinfonía de Combate", "desc": "Tu canto llena el campo. Los aliados reciben buffs y los enemigos son confundidos y aturdidos.", "costo": 3, "requiere": ["mana_skin_canto", "nota_potenciadora"]},
        "disonancia": {"nombre": "Disonancia", "desc": "Emites una frecuencia que interrumpe la concentración mágica del enemigo, cancelando su hechizo.", "costo": 2, "requiere": ["nota_potenciadora"]},
        "requiem": {"nombre": "Réquiem", "desc": "Un canto fúnebre que drena el maná de todos los enemigos en el área transfiriéndolo a tus aliados.", "costo": 4, "requiere": ["mana_zone_canto", "disonancia"]},
    },
    "Sello": {
        "mana_skin_sello": {"nombre": "Mana Skin: Sello Reactivo", "desc": "Al recibir un ataque mágico, un sello automático se activa bloqueando el seguimiento del hechizo.", "costo": 1, "requiere": []},
        "sello_basico": {"nombre": "Sello Básico", "desc": "Aplicas un sello en una herida o portal que impide que se reabra o sea usado.", "costo": 1, "requiere": []},
        "mana_zone_sello": {"nombre": "Mana Zone: Campo Sellado", "desc": "Nadie puede invocar portales, escapar o usar habilidades de movimiento dentro de tu campo.", "costo": 3, "requiere": ["mana_skin_sello", "sello_basico"]},
        "sello_de_mana": {"nombre": "Sello de Maná", "desc": "Bloqueas el acceso al maná de un objetivo por un turno completo.", "costo": 2, "requiere": ["sello_basico"]},
        "gran_sello": {"nombre": "Gran Sello", "desc": "Sellas a un objetivo por completo. No puede moverse, hablar ni acceder a su maná.", "costo": 4, "requiere": ["mana_zone_sello", "sello_de_mana"]},
    },
    "Brújula": {
        "mana_skin_brujula": {"nombre": "Mana Skin: Desvío Automático", "desc": "Los proyectiles dirigidos a ti son desviados automáticamente al activarse tu maná defensivo.", "costo": 1, "requiere": []},
        "redireccion": {"nombre": "Redirección", "desc": "Cambias la trayectoria de un hechizo enemigo para que golpee a otro objetivo.", "costo": 1, "requiere": []},
        "mana_zone_brujula": {"nombre": "Mana Zone: Campo de Redirección", "desc": "Todos los proyectiles del área pueden ser redirigidos a voluntad mientras estén dentro de tu campo.", "costo": 3, "requiere": ["mana_skin_brujula", "redireccion"]},
        "bucle_magico": {"nombre": "Bucle Mágico", "desc": "Haces que el hechizo enemigo rebote en bucle hasta consumir todo su maná y desaparecer.", "costo": 2, "requiere": ["redireccion"]},
        "tormenta_refleja": {"nombre": "Tormenta Refleja", "desc": "Rediriges todos los ataques del área hacia un punto central, creando una explosión masiva.", "costo": 4, "requiere": ["mana_zone_brujula", "bucle_magico"]},
    },
    "Maldición": {
        "mana_skin_maldicion": {"nombre": "Mana Skin: Aura Maldita", "desc": "Quien te golpee recibe una marca de maldición que drena su maná lentamente.", "costo": 1, "requiere": []},
        "maldicion_menor": {"nombre": "Maldición Menor", "desc": "Aplicas una maldición básica que impide la regeneración natural de maná del objetivo.", "costo": 1, "requiere": []},
        "mana_zone_maldicion": {"nombre": "Mana Zone: Tierra Maldita", "desc": "El área está bajo tu maldición. Cualquier curación dentro del campo falla automáticamente.", "costo": 3, "requiere": ["mana_skin_maldicion", "maldicion_menor"]},
        "maldicion_de_sangre": {"nombre": "Maldición de Sangre", "desc": "Una maldición que se activa al recibir daño. Cuanto más daño, más potente la maldición.", "costo": 2, "requiere": ["maldicion_menor"]},
        "maldicion_eterna": {"nombre": "Maldición Eterna", "desc": "Aplicas una maldición permanente que solo puede ser rota por magia de nivel supremo.", "costo": 5, "requiere": ["mana_zone_maldicion", "maldicion_de_sangre"]},
    },
    "Veneno": {
        "mana_skin_veneno": {"nombre": "Mana Skin: Piel Tóxica", "desc": "Tu cuerpo segrega veneno. Quien te golpee directamente recibe el efecto de envenenamiento.", "costo": 1, "requiere": []},
        "nube_toxica": {"nombre": "Nube Tóxica", "desc": "Liberas una nube venenosa que debilita los atributos físicos de quien la inhale.", "costo": 1, "requiere": []},
        "mana_zone_veneno": {"nombre": "Mana Zone: Pantano Tóxico", "desc": "El área se llena de miasma. Respirar en ella envenena progresivamente a los enemigos.", "costo": 3, "requiere": ["mana_skin_veneno", "nube_toxica"]},
        "veneno_magico": {"nombre": "Veneno Mágico", "desc": "Un veneno especial que corroe el maná en lugar del cuerpo. Reduce la potencia de hechizos.", "costo": 2, "requiere": ["nube_toxica"]},
        "plaga_del_pantano": {"nombre": "Plaga del Pantano", "desc": "Un veneno masivo que contagia entre enemigos cercanos propagándose como una plaga.", "costo": 4, "requiere": ["mana_zone_veneno", "veneno_magico"]},
    },
    "Modificación": {
        "mana_skin_modificacion": {"nombre": "Mana Skin: Adaptación Elemental", "desc": "Tu maná se adapta automáticamente al tipo de ataque recibido, ganando resistencia temporal.", "costo": 1, "requiere": []},
        "alterar_elemento": {"nombre": "Alterar Elemento", "desc": "Cambias el elemento de un hechizo propio en el momento del lanzamiento.", "costo": 1, "requiere": []},
        "mana_zone_modificacion": {"nombre": "Mana Zone: Campo Alterado", "desc": "Todos los hechizos en tu zona pueden ser modificados en elemento, tamaño o velocidad.", "costo": 3, "requiere": ["mana_skin_modificacion", "alterar_elemento"]},
        "contraforma": {"nombre": "Contraforma", "desc": "Al recibir un ataque elemental, lo transformas en su opuesto antes de que te impacte.", "costo": 2, "requiere": ["alterar_elemento"]},
        "maestro_de_elementos": {"nombre": "Maestro de Elementos", "desc": "Puedes modificar cualquier hechizo propio o aliado convirtiéndolo en cualquier elemento.", "costo": 4, "requiere": ["mana_zone_modificacion", "contraforma"]},
    },

    "Cristal": {
        "mana_skin_cristal": {"nombre": "Mana Skin: Coraza de Gemas", "desc": "Gemas mágicas cubren tu cuerpo formando una armadura de cristal casi indestructible.", "costo": 1, "requiere": []},
        "fragmento_cortante": {"nombre": "Fragmento Cortante", "desc": "Disparas fragmentos de cristal de alta densidad que perforan armaduras y escudos.", "costo": 1, "requiere": []},
        "mana_zone_cristal": {"nombre": "Mana Zone: Palacio de Cristal", "desc": "El área se llena de estructuras de cristal que reflejan ataques y crean laberintos defensivos.", "costo": 3, "requiere": ["mana_skin_cristal", "fragmento_cortante"]},
        "espejo_cristalino": {"nombre": "Espejo Cristalino", "desc": "Creas un cristal perfecto que refleja el siguiente ataque recibido en el mismo ángulo.", "costo": 2, "requiere": ["fragmento_cortante"]},
        "jaula_de_diamante": {"nombre": "Jaula de Diamante", "desc": "Encierras al objetivo en una prisión de cristal indestructible que bloquea todo el maná.", "costo": 4, "requiere": ["mana_zone_cristal", "espejo_cristalino"]},
    },
    "Espejos": {
        "mana_skin_espejos": {"nombre": "Mana Skin: Reflejo Mágico", "desc": "Hechizos de baja potencia son automáticamente reflejados al activarse tu piel de espejo.", "costo": 1, "requiere": []},
        "clon_espejo": {"nombre": "Clon Espejo", "desc": "Creas una réplica visual perfecta de ti mismo que confunde al enemigo sobre cuál es real.", "costo": 1, "requiere": []},
        "mana_zone_espejos": {"nombre": "Mana Zone: Sala de Espejos", "desc": "El campo se llena de espejos de maná. Los ataques rebotan y se duplican impredeciblemente.", "costo": 3, "requiere": ["mana_skin_espejos", "clon_espejo"]},
        "reflejo_amplificado": {"nombre": "Reflejo Amplificado", "desc": "Reflejas un hechizo enemigo duplicando su potencia de vuelta hacia el lanzador.", "costo": 2, "requiere": ["clon_espejo"]},
        "laberinto_infinito": {"nombre": "Laberinto Infinito", "desc": "El objetivo queda atrapado en un espacio de espejos sin salida. Sin orientación, sin escape.", "costo": 4, "requiere": ["mana_zone_espejos", "reflejo_amplificado"]},
    },
    "Árbol Mitológico": {
        "mana_skin_arbol": {"nombre": "Mana Skin: Corteza Sagrada", "desc": "La corteza del árbol del mundo te recubre. Absorbe daño mágico y lo convierte en maná.", "costo": 1, "requiere": []},
        "raiz_sanadora": {"nombre": "Raíz Sanadora", "desc": "Una raíz del árbol mitológico emerge y sana las heridas de un aliado.", "costo": 1, "requiere": []},
        "mana_zone_arbol": {"nombre": "Mana Zone: Bosque Sagrado", "desc": "El árbol del mundo se manifiesta. Sus raíces cubren el campo sanando aliados y atrapando enemigos.", "costo": 3, "requiere": ["mana_skin_arbol", "raiz_sanadora"]},
        "fruto_de_mana": {"nombre": "Fruto de Maná", "desc": "Produces un fruto mágico que restaura el maná completo de quien lo consuma.", "costo": 2, "requiere": ["raiz_sanadora"]},
        "gran_arbol": {"nombre": "Gran Árbol del Mundo", "desc": "El árbol mitológico completo se manifiesta. Sana a todos los aliados y aplasta a todos los enemigos.", "costo": 5, "requiere": ["mana_zone_arbol", "fruto_de_mana"]},
    },
    "Sueños": {
        "mana_skin_suenos": {"nombre": "Mana Skin: Velo Onírico", "desc": "Rodeas tu mente de maná onírico, siendo inmune a efectos de ilusión y confusión.", "costo": 1, "requiere": []},
        "ilusion_basica": {"nombre": "Ilusión Básica", "desc": "Creas una ilusión visual que confunde al enemigo sobre tu posición real.", "costo": 1, "requiere": []},
        "mana_zone_suenos": {"nombre": "Mana Zone: Dimensión Onírica", "desc": "Atrapas al objetivo en una dimensión donde sus peores miedos se vuelven reales para él.", "costo": 3, "requiere": ["mana_skin_suenos", "ilusion_basica"]},
        "pesadilla": {"nombre": "Pesadilla", "desc": "Invades la mente del objetivo infundiéndole terror, paralizándolo de miedo en el combate.", "costo": 2, "requiere": ["ilusion_basica"]},
        "sueño_eterno": {"nombre": "Sueño Eterno", "desc": "El objetivo cae en un sueño del que no puede despertar por sí solo. Fuera de combate completamente.", "costo": 5, "requiere": ["mana_zone_suenos", "pesadilla"]},
    },
    "Huesos": {
        "mana_skin_huesos": {"nombre": "Mana Skin: Exoesqueleto", "desc": "Huesos mágicos emergen de tu piel formando una armadura natural extremadamente dura.", "costo": 1, "requiere": []},
        "lanza_osea": {"nombre": "Lanza Ósea", "desc": "Disparas una lanza de hueso endurecido que perfora escudos mágicos.", "costo": 1, "requiere": []},
        "mana_zone_huesos": {"nombre": "Mana Zone: Campo Óseo", "desc": "El suelo erupciona en huesos gigantes que atrapan y cortan a los enemigos en el área.", "costo": 3, "requiere": ["mana_skin_huesos", "lanza_osea"]},
        "armadura_draconica": {"nombre": "Armadura Dracónica", "desc": "Cubres tu cuerpo en una coraza completa de huesos de dragón mágico. Máxima defensa.", "costo": 2, "requiere": ["lanza_osea"]},
        "foresta_de_huesos": {"nombre": "Foresta de Huesos", "desc": "El campo completo erupciona en un bosque de espinas óseas que hieren a todo lo que se mueve.", "costo": 4, "requiere": ["mana_zone_huesos", "armadura_draconica"]},
    },
    "Carne": {
        "mana_skin_carne": {"nombre": "Mana Skin: Regeneración Activa", "desc": "Tu cuerpo regenera heridas menores automáticamente gracias al maná muscular activo.", "costo": 1, "requiere": []},
        "hipertrofia": {"nombre": "Hipertrofia", "desc": "Aumentas temporalmente tu masa muscular con maná, ganando fuerza física brutal.", "costo": 1, "requiere": []},
        "mana_zone_carne": {"nombre": "Mana Zone: Campo Biológico", "desc": "En tu radio, puedes alterar la masa corporal de aliados y enemigos a voluntad.", "costo": 3, "requiere": ["mana_skin_carne", "hipertrofia"]},
        "regeneracion_avanzada": {"nombre": "Regeneración Avanzada", "desc": "Regeneras heridas graves incluyendo huesos rotos y daño mágico interno.", "costo": 2, "requiere": ["mana_skin_carne"]},
        "transformacion_bestial": {"nombre": "Transformación Bestial", "desc": "Tu cuerpo se transforma en una forma bestial de pura masa muscular mágica. Fuerza y resistencia máximas.", "costo": 5, "requiere": ["mana_zone_carne", "regeneracion_avanzada"]},
    },
    "Imitación": {
        "mana_skin_imitacion": {"nombre": "Mana Skin: Copia Reactiva", "desc": "Al recibir un ataque, copias automáticamente su tipo de maná para la siguiente defensa.", "costo": 1, "requiere": []},
        "copia_basica": {"nombre": "Copia Básica", "desc": "Tras tocar un hechizo enemigo, puedes replicarlo con la misma potencia.", "costo": 1, "requiere": []},
        "mana_zone_imitacion": {"nombre": "Mana Zone: Biblioteca Mágica", "desc": "En tu zona puedes copiar cualquier hechizo que veas lanzar, sin necesidad de tocarlo.", "costo": 3, "requiere": ["mana_skin_imitacion", "copia_basica"]},
        "imitacion_perfecta": {"nombre": "Imitación Perfecta", "desc": "Copias el hechizo con un 20% más de potencia que el original.", "costo": 2, "requiere": ["copia_basica"]},
        "arsenal_copiado": {"nombre": "Arsenal Copiado", "desc": "Puedes almacenar hasta 5 hechizos copiados y lanzarlos todos simultáneamente.", "costo": 5, "requiere": ["mana_zone_imitacion", "imitacion_perfecta"]},
    },
    "Pintura": {
        "mana_skin_pintura": {"nombre": "Mana Skin: Escudo Artístico", "desc": "Pintas un escudo en el aire que bloquea el siguiente ataque recibido.", "costo": 1, "requiere": []},
        "creacion_basica": {"nombre": "Creación Básica", "desc": "Pintas objetos o criaturas simples que se materializan con maná.", "costo": 1, "requiere": []},
        "mana_zone_pintura": {"nombre": "Mana Zone: Lienzo del Mundo", "desc": "El entorno se convierte en tu lienzo. Puedes pintar y materializar cualquier elemento en el campo.", "costo": 3, "requiere": ["mana_skin_pintura", "creacion_basica"]},
        "criatura_pintada": {"nombre": "Criatura Pintada", "desc": "Pintas un guardián complejo que pelea de manera autónoma a tu lado.", "costo": 2, "requiere": ["creacion_basica"]},
        "mundo_alternativo": {"nombre": "Mundo Alternativo", "desc": "Pintas una dimensión completa y teletransportas al objetivo a ella.", "costo": 5, "requiere": ["mana_zone_pintura", "criatura_pintada"]},
    },
    "Almas": {
        "mana_skin_almas": {"nombre": "Mana Skin: Barrera Espiritual", "desc": "Tu alma proyecta una barrera que bloquea efectos de maldición y alteración mental.", "costo": 1, "requiere": []},
        "toque_espiritual": {"nombre": "Toque Espiritual", "desc": "Tocas el alma del objetivo, leyendo sus intenciones y el próximo movimiento que planea.", "costo": 1, "requiere": []},
        "mana_zone_almas": {"nombre": "Mana Zone: Mar de Almas", "desc": "Las almas del entorno obedecen tu voluntad. Puedes invocarlas como aliados espectrales.", "costo": 3, "requiere": ["mana_skin_almas", "toque_espiritual"]},
        "alteracion_anímica": {"nombre": "Alteración Anímica", "desc": "Modificas los recuerdos recientes del objetivo, confundiéndolo sobre qué pasó en el combate.", "costo": 2, "requiere": ["toque_espiritual"]},
        "robo_de_alma": {"nombre": "Robo de Alma", "desc": "Extraes temporalmente el alma del objetivo. Sin ella, su cuerpo cae inconsciente.", "costo": 5, "requiere": ["mana_zone_almas", "alteracion_anímica"]},
    },
    "Causalidad": {
        "mana_skin_causalidad": {"nombre": "Mana Skin: Bucle Causal", "desc": "El daño recibido es registrado en la causalidad. El atacante lo recibirá de vuelta al final del turno.", "costo": 2, "requiere": []},
        "revertir_accion": {"nombre": "Revertir Acción", "desc": "Deshaces el último hechizo lanzado por el enemigo como si nunca hubiera ocurrido.", "costo": 2, "requiere": []},
        "mana_zone_causalidad": {"nombre": "Mana Zone: Campo Sin Causa", "desc": "En tu zona, ningún hechizo tiene efecto hasta que tú lo permitas. Eres el árbitro de la causalidad.", "costo": 4, "requiere": ["mana_skin_causalidad", "revertir_accion"]},
        "retroalimentacion": {"nombre": "Retroalimentación", "desc": "El daño acumulado de los últimos tres ataques recibidos se devuelve al origen en un instante.", "costo": 3, "requiere": ["revertir_accion"]},
        "paradoja_absoluta": {"nombre": "Paradoja Absoluta", "desc": "Rompes completamente la causalidad del objetivo. Sus acciones pasadas y futuras se anulan.", "costo": 6, "requiere": ["mana_zone_causalidad", "retroalimentacion"]},
    },
}


# =========================================================================
# 🎮 COMANDOS DEL SISTEMA DE SKILLS
# Importa esto en bot.py con: from skills import setup_skills
# y llama setup_skills(bot) al final de bot.py antes de bot.run()
# =========================================================================

import discord
from discord.ext import commands

def setup_skills(bot, cargar_datos, guardar_datos, verificar_usuario, es_admin_bot):

    # ── Helpers ──────────────────────────────────────────────────────────
    def _get_pj(datos, uid):
        u = datos[str(uid)]
        return u["slots"][u["slot_activo"]]

    # ── Dar Skill Points (solo admins) ───────────────────────────────────
    @bot.command(name="darsp")
    async def darsp(ctx, miembro: discord.Member = None, cantidad: int = None):
        """Admin: otorga Skill Points a un jugador. +darsp [@usuario] [cantidad]"""
        if not es_admin_bot(ctx):
            return await ctx.send("❌ Solo los administradores pueden otorgar Skill Points.")
        if not miembro or cantidad is None or cantidad <= 0:
            return await ctx.send("❌ Uso: `+darsp [@usuario] [cantidad]`")

        datos = cargar_datos()
        verificar_usuario(miembro.id, datos)
        pj = _get_pj(datos, miembro.id)
        pj.setdefault("skill_points", 0)
        pj["skill_points"] += cantidad
        guardar_datos(datos)

        embed = discord.Embed(title="✨ Skill Points Otorgados", color=discord.Color.from_rgb(138, 43, 226))
        embed.add_field(name="👤 Jugador:", value=miembro.mention, inline=True)
        embed.add_field(name="🔮 SP Recibidos:", value=f"`+{cantidad} SP`", inline=True)
        embed.add_field(name="💎 Total SP:", value=f"`{pj['skill_points']} SP`", inline=True)
        embed.set_footer(text=f"Otorgado por {ctx.author.display_name} • Usa +skills para ver tu árbol")
        await ctx.send(embed=embed)

    # ── Ver árbol de habilidades ─────────────────────────────────────────
    @bot.command(name="skills")
    async def skills(ctx, miembro: discord.Member = None):
        """Muestra el árbol de skills de tu magia actual. +skills [@usuario]"""
        miembro = miembro or ctx.author
        datos = cargar_datos()
        verificar_usuario(miembro.id, datos)
        pj = _get_pj(datos, miembro.id)
        pj.setdefault("skill_points", 0)
        pj.setdefault("habilidades", [])

        magia = pj.get("magia", "Ninguna")
        if magia == "Ninguna" or magia not in SKILL_TREES:
            return await ctx.send(f"❌ {miembro.mention} no tiene una magia con árbol de habilidades asignada.")

        arbol = SKILL_TREES[magia]
        desbloqueadas = pj["habilidades"]
        sp = pj["skill_points"]

        embed = discord.Embed(
            title=f"🌿 Árbol de Habilidades — {magia}",
            description=f"**{miembro.display_name}** | 💎 SP disponibles: `{sp}`",
            color=discord.Color.from_rgb(138, 43, 226)
        )

        for hid, h in arbol.items():
            desbloqueada = hid in desbloqueadas
            reqs = h["requiere"]
            reqs_ok = all(r in desbloqueadas for r in reqs)

            if desbloqueada:
                estado = "✅"
            elif reqs_ok:
                estado = f"🔓 ({h['costo']} SP)"
            else:
                req_nombres = ", ".join([arbol[r]["nombre"] for r in reqs if r in arbol])
                estado = f"🔒 Requiere: *{req_nombres}*"

            embed.add_field(
                name=f"{estado} {h['nombre']}",
                value=h["desc"],
                inline=False
            )

        embed.set_footer(text="Usa +aprender [nombre de habilidad] para desbloquear")
        await ctx.send(embed=embed)

    # ── Aprender habilidad ───────────────────────────────────────────────
    @bot.command(name="aprender")
    async def aprender(ctx, *, nombre_habilidad: str = None):
        """Desbloquea una habilidad usando Skill Points. +aprender [nombre]"""
        if not nombre_habilidad:
            return await ctx.send("❌ Uso: `+aprender [nombre de la habilidad]`")

        datos = cargar_datos()
        verificar_usuario(ctx.author.id, datos)
        pj = _get_pj(datos, ctx.author.id)
        pj.setdefault("skill_points", 0)
        pj.setdefault("habilidades", [])

        magia = pj.get("magia", "Ninguna")
        if magia == "Ninguna" or magia not in SKILL_TREES:
            return await ctx.send("❌ No tienes una magia con árbol de habilidades.")

        arbol = SKILL_TREES[magia]
        nombre_lower = nombre_habilidad.lower().strip()

        # Busca la habilidad por nombre (no por ID)
        hid_encontrado = None
        for hid, h in arbol.items():
            if h["nombre"].lower() == nombre_lower:
                hid_encontrado = hid
                break

        if not hid_encontrado:
            return await ctx.send(f"❌ No encontré `{nombre_habilidad}` en tu árbol de **{magia}**.\nUsa `+skills` para ver los nombres exactos.")

        h = arbol[hid_encontrado]

        if hid_encontrado in pj["habilidades"]:
            return await ctx.send(f"⚠️ Ya tienes **{h['nombre']}** desbloqueada.")

        reqs_faltantes = [arbol[r]["nombre"] for r in h["requiere"] if r not in pj["habilidades"]]
        if reqs_faltantes:
            return await ctx.send(f"🔒 Primero necesitas desbloquear: **{', '.join(reqs_faltantes)}**")

        if pj["skill_points"] < h["costo"]:
            return await ctx.send(f"❌ Necesitas `{h['costo']} SP` pero solo tienes `{pj['skill_points']} SP`.")

        pj["skill_points"] -= h["costo"]
        pj["habilidades"].append(hid_encontrado)
        guardar_datos(datos)

        embed = discord.Embed(
            title="🎉 ¡Habilidad Desbloqueada!",
            color=discord.Color.from_rgb(138, 43, 226)
        )
        embed.add_field(name="✨ Habilidad:", value=f"**{h['nombre']}**", inline=False)
        embed.add_field(name="📖 Descripción:", value=h["desc"], inline=False)
        embed.add_field(name="💎 SP Restantes:", value=f"`{pj['skill_points']} SP`", inline=True)
        embed.set_footer(text=f"Árbol de {magia}")
        await ctx.send(content=ctx.author.mention, embed=embed)

    # ── Ver habilidades desbloqueadas ────────────────────────────────────
    @bot.command(name="mishabilidades", aliases=["myhabilidades", "habilidades"])
    async def mishabilidades(ctx, miembro: discord.Member = None):
        """Muestra las habilidades desbloqueadas de un jugador. +mishabilidades"""
        miembro = miembro or ctx.author
        datos = cargar_datos()
        verificar_usuario(miembro.id, datos)
        pj = _get_pj(datos, miembro.id)
        pj.setdefault("habilidades", [])
        pj.setdefault("skill_points", 0)

        magia = pj.get("magia", "Ninguna")
        desbloqueadas = pj["habilidades"]
        sp = pj["skill_points"]

        embed = discord.Embed(
            title=f"📚 Habilidades de {miembro.display_name}",
            color=discord.Color.from_rgb(138, 43, 226)
        )
        embed.add_field(name="🪄 Magia:", value=magia, inline=True)
        embed.add_field(name="💎 SP disponibles:", value=f"`{sp} SP`", inline=True)

        if not desbloqueadas or magia not in SKILL_TREES:
            embed.description = "*Sin habilidades desbloqueadas aún.*"
        else:
            arbol = SKILL_TREES[magia]
            lista = []
            for hid in desbloqueadas:
                if hid in arbol:
                    lista.append(f"✅ **{arbol[hid]['nombre']}**")
            embed.description = "\n".join(lista) if lista else "*Sin habilidades desbloqueadas aún.*"

        embed.set_footer(text="Usa +skills para ver el árbol completo")
        await ctx.send(embed=embed)
