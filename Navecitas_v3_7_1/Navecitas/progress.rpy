# ---------------------------------------------------------------
#  Navecitas v3 - progreso, logros, skins, tienda y ajustes
# ---------------------------------------------------------------

# ----- ajustes -----
default persistent._es_diff = "normal"        # easy / normal / hard
default persistent._es_offset = 90            # distancia nave-dedo (px)
default persistent._es_relative = False       # control relativo (arrastrar sin saltar)
default persistent._es_lefty = False          # boton de bomba a la izquierda
default persistent._es_dtap = True            # doble toque = bomba
default persistent._es_autobomb = True        # bomba automatica en el ultimo golpe
default persistent._es_vibrate = True
default persistent._es_comments = True        # comentarios de Monika en partida
default persistent._es_go_video = True       # video al perder
default persistent._es_perf = 1              # rendimiento: 0 ahorro, 1 equilibrado, 2 maximo
default persistent._es_tutorial = True        # mostrar tutorial en la proxima partida
default persistent._es_vol_music = 0.8
default persistent._es_vol_sfx = 0.8
default persistent._es_skin = 0
default persistent._es_radio_music = True        # musica de fondo en las escenas de radio
default persistent._es_skins = []             # naves compradas en la tienda

# ----- progreso -----
default persistent._es_ach = []               # ids de logros
default persistent._es_stats = {}
default persistent._es_hi = {}                # record por modo
default persistent._es_ranks = {}             # mejor rango por nivel y dificultad
default persistent._es_endless = False        # modo infinito desbloqueado
default persistent._es_last_aff = None
default persistent._es_coins = 0              # monedas para la tienda
default persistent._es_upg = {}               # nivel de cada mejora comprada
default persistent._es_miles = []             # hitos que Monika ya comento

# ----- compatibilidad con la version 1.0 -----
default persistent._encoders_hiscore = 0
default persistent._encoders_best_stage = 0

init 11 python:

    ES_DIFFS = {
        "easy":   {"name": u"Fácil",   "lives": 4, "bspd": 0.85, "spawn": 1.3,  "boss": 0.8,  "score": 10},
        "normal": {"name": u"Normal",  "lives": 3, "bspd": 1.0,  "spawn": 1.0,  "boss": 1.0,  "score": 10},
        "hard":   {"name": u"Difícil", "lives": 2, "bspd": 1.15, "spawn": 0.8,  "boss": 1.25, "score": 12},
    }
    ES_DIFF_ORDER = ["easy", "normal", "hard"]
    ES_MODE_NAMES = {"easy": u"Fácil", "normal": u"Normal", "hard": u"Difícil",
                     "endless": u"Infinito", "practice": u"Práctica",
                     "coop": u"Cooperativo", "story": u"Historia"}

    # (id, nombre, descripcion, oculto)
    ES_ACH = [
        ("first_win",  u"Jefe final caído",  u"Gana el juego por primera vez", False),
        ("no_hit",     u"Intocable",           u"Gana sin perder ninguna vida", False),
        ("no_bomb",    u"Manos limpias",       u"Gana sin usar ninguna bomba", False),
        ("hard_win",   u"Piloto de élite",     u"Gana en dificultad Difícil", False),
        ("combo30",    u"Imparable",           u"Llega a un combo de 30", False),
        ("score5000",  u"Cazaestrellas",       u"Consigue 5000 puntos en una partida", False),
        ("rank_s4",    u"Perfeccionista",      u"Consigue 4 rangos S en una partida", False),
        ("collector",  u"Coleccionista",       u"Recoge 8 tipos de power-up en una partida", False),
        ("coins15",    u"Cazamonedas",         u"Recoge 15 monedas en una partida", False),
        ("endless10",  u"Sin fin",             u"Llega al nivel 10 en modo infinito", False),
        ("games10",    u"Piloto constante",    u"Juega 10 partidas", False),
        ("bosses25",   u"Cazajefes",           u"Derrota a 25 jefes en total", False),
        ("mini15",     u"Cazador de élite",    u"Derrota a 15 mini-jefes en total", False),
        ("graze100",   u"Al límite",           u"Roza 100 balas en una partida", False),
        ("earned500",  u"Ahorrador",           u"Gana 500 monedas en total", False),
        ("buyer",      u"Primer cliente",      u"Compra una mejora en la tienda", False),
        ("bosses100",  u"Exterminador",        u"Derrota a 100 jefes en total", False),
        ("coop_win",   u"Dúo dinámico",        u"Gana el juego en modo cooperativo con Monika", False),
        ("story_win",  u"Cambio y fuera",      u"Termina el modo Historia", False),
        ("fast_win",   u"Velocista",           u"Gana el juego en menos de 12 minutos", True),
        ("no_pu",      u"Sin ayuda",           u"Gana recogiendo 3 power-ups o menos", True),
    ]
    ES_ACH_NAME = dict((a[0], a[1]) for a in ES_ACH)

    # (nombre, logro que la desbloquea, habilidad)
    ES_SKINS = [
        (u"Clásica",   None,        u"Sin bonificación"),
        (u"Rosa",      "games10",   u"Recoge power-ups desde más lejos"),
        (u"Esmeralda", "first_win", u"Los enemigos sueltan más power-ups"),
        (u"Dorada",    "hard_win",  u"+20% de puntos"),
        (u"Fantasma",  "no_hit",    u"Más tiempo invulnerable tras un golpe"),
        # naves de la tienda: (nombre, None, habilidad, precio)
        (u"Celeste",   None,        u"Los escudos duran 50% más", 180),
        (u"Carmesí",   None,        u"20% de tus balas hacen doble daño", 260),
        (u"Violeta",   None,        u"Ganas 50% más monedas al terminar", 320),
        (u"Cósmica",   None,        u"Empiezas con una vida extra", 480),
    ]

    # (id, nombre, descripcion, [precio de cada nivel])
    ES_UPG = [
        ("bomb",   u"Bomba de reserva",    u"Empiezas con 1 bomba más por nivel.", [60, 150]),
        ("shield", u"Escudo inicial",      u"Empiezas cada nivel con escudo (4 s por nivel).", [80, 200]),
        ("pu",     u"Power-ups duraderos", u"Los power-ups temporales duran 15% más por nivel.", [50, 120, 220]),
        ("life",   u"Vida extra",          u"Empiezas con una vida más.", [250]),
        ("weapon", u"Arma mejorada",       u"Empiezas con el arma en nivel 2.", [120]),
        ("loot",   u"Radar de botín",      u"Los enemigos sueltan 20% más power-ups por nivel.", [90, 200]),
        ("magnet", u"Imán inicial",        u"Empiezas cada nivel con imán (5 s por nivel).", [90, 200]),
        ("combo",  u"Combo duradero",      u"El combo tarda 0.8 s más en apagarse por nivel.", [80, 180]),
        ("graze",  u"Roce premiado",       u"Rozar balas da +5 puntos más por nivel.", [70, 160]),
        ("bombpow", u"Bomba potente",      u"Las bombas hacen más daño a los jefes.", [100, 220]),
        ("bank",   u"Contrato de monedas", u"Ganas 20% más monedas al terminar por nivel.", [150, 320]),
    ]
    ES_UPG_D = dict((x[0], x) for x in ES_UPG)

    ES_RANK_VAL = {"C": 0, "B": 1, "A": 2, "S": 3}

    # frases de Monika (se sustituyen [player], [es_score], etc. al usarlas)
    ES_L = {
        "win": [
            u"¡LO LOGRASTE, [player]! ¡Derrotaste a la Nave Nodriza! Terminaste con [es_score] puntos.",
            u"¡Increíble, [player]! La Nave Nodriza cayó y terminaste con [es_score] puntos. ¡Estoy muy orgullosa de ti!",
            u"¡Victoria! Sabía que podías, [player]. ¡[es_score] puntos!",
        ],
        "win_all": [
            u"¡LO LOGRASTE, [player]! ¡Derrotaste al Corazón del Vacío! Terminaste con [es_score] puntos.",
            u"¡Increíble, [player]! Los 10 niveles superados y terminaste con [es_score] puntos. ¡Estoy muy orgullosa de ti!",
            u"¡Victoria total! Sabía que podías, [player]. ¡[es_score] puntos!",
        ],
        "win_love": [
            u"Verte ganar me llena de orgullo, [player]. Hasta una batalla espacial se siente como una cita contigo.",
            u"Contigo todo es más divertido, [player]. Te quiero.",
        ],
        "new_rec": [
            u"¡Nuevo récord en [es_mode_name], [player]! [es_score] puntos y llegaste al nivel [es_stage]. ¡Increíble!",
            u"¡Récord nuevo en [es_mode_name]! [es_score] puntos. ¡Cada vez juegas mejor, [player]!",
            u"¡Lo superaste! [es_score] puntos es tu mejor marca en [es_mode_name].",
        ],
        "good": [
            u"¡Muy bien! Llegaste al nivel [es_stage] con [es_score] puntos.",
            u"¡Buena partida, [player]! Nivel [es_stage] y [es_score] puntos.",
            u"¡Qué buen vuelo! Llegaste al nivel [es_stage]. El jefe final está cada vez más cerca.",
        ],
        "bad": [
            u"Hiciste [es_score] puntos y llegaste al nivel [es_stage]. ¡Con práctica lo harás mejor!",
            u"Nivel [es_stage]... ¡Ya casi, [player]! Las mejoras de la tienda te pueden ayudar.",
            u"No pasa nada, [player]. A todos nos derriban al principio. ¡Otra vez!",
        ],
        "quit_early": [
            u"¿Ya te cansaste tan pronto? No pasa nada, [player], jugamos cuando quieras.",
            u"Está bien, [player]. Lo dejamos para otro rato.",
        ],
        "quit_late": [
            u"Está bien, la dejamos aquí. Guardé tus [es_score] puntos.",
            u"Buena partida hasta aquí, [player]. Guardé tus [es_score] puntos.",
        ],
        "coop": [
            u"Volar contigo es lo mejor, [player]. ¡Hacemos un gran equipo!",
            u"Me encanta pelear a tu lado, [player]. Aunque a veces me distraigo mirando tu nave.",
            u"¿Viste cómo te cubrí? ¡Somos un gran equipo!",
            u"Tener a alguien en quien confiar en el campo de batalla es genial. Y ese alguien eres tú.",
        ],
        "p_quit": [
            u"Está bien, [player]. ¡La práctica sirve de todos modos!",
        ],
        "p_win": [
            u"¡Muy bien! Ya dominaste al jefe del nivel [es_stage]. ¡Ahora a por la partida completa!",
            u"¡Excelente, [player]! Ese jefe ya no tiene secretos para ti.",
        ],
        "p_lose": [
            u"No pasa nada, para eso es la práctica. ¡Inténtalo otra vez, [player]!",
            u"Ese jefe es duro, pero aprendes sus patrones con cada intento.",
        ],
        "rest": [
            u"Llevamos un buen rato jugando, [player]. ¿Descansamos un poco los ojos y estiramos las manos?",
            u"¿No crees que ya jugamos bastante por hoy, [player]? ¡Cuida tus manos y tus ojos!",
        ],
    }

    # tiempo jugado desde que se abrio el juego (para sugerir un descanso)
    ES_SESSION = {"time": 0, "said": False}

    # ---------- utilidades ----------
    def es_stat(key, default=0):
        return persistent._es_stats.get(key, default)

    def es_stat_set(key, value):
        d = dict(persistent._es_stats)
        d[key] = value
        persistent._es_stats = d

    def es_stat_add(key, n):
        es_stat_set(key, es_stat(key) + n)

    def es_stat_max(key, n):
        if n > es_stat(key):
            es_stat_set(key, n)

    def es_record(key):
        hi = persistent._es_hi
        if key in hi:
            return hi[key]
        if key == "normal":
            return persistent._encoders_hiscore   # puntaje de la v1.0
        return 0

    def es_record_set(key, value):
        d = dict(persistent._es_hi)
        d[key] = value
        persistent._es_hi = d

    def es_has_ach(i):
        return i in persistent._es_ach

    def es_skin_price(i):
        sk = ES_SKINS[i]
        return sk[3] if len(sk) > 3 else None

    def es_skin_unlocked(i):
        if es_skin_price(i) is not None:
            return i in persistent._es_skins
        need = ES_SKINS[i][1]
        return need is None or es_has_ach(need)

    def es_diff_name():
        return ES_DIFFS.get(persistent._es_diff, ES_DIFFS["normal"])["name"]

    def es_mode_key(mode, diff):
        return mode if mode in ("endless", "coop", "story") else diff

    def es_apply_volumes():
        try:
            renpy.music.set_volume(persistent._es_vol_music, channel="es_music")
            renpy.music.set_volume(persistent._es_vol_sfx, channel="es_sfx")
            renpy.music.set_volume(persistent._es_vol_sfx, channel="es_sfx2")
            renpy.music.set_volume(persistent._es_vol_sfx, channel="es_sfx3")
        except Exception:
            pass

    # bloquea / desbloquea la interfaz de MAS durante la partida
    ES_PERF_NAMES = [u"Ahorro (30 fps)", u"Equilibrado (60 fps)", u"Máximo (sin tope)"]

    def es_perf_next():
        persistent._es_perf = (persistent._es_perf + 1) % 3

    def es_lock_ui():
        try:
            HKBHideButtons()
        except Exception:
            pass
        try:
            disable_esc()
        except Exception:
            pass

    def es_unlock_ui():
        try:
            HKBShowButtons()
        except Exception:
            pass
        try:
            enable_esc()
        except Exception:
            pass

    # ---------- frases de Monika ----------
    def es_sub(s):
        try:
            return renpy.substitute(s)
        except Exception:
            return s

    def es_pick(lst):
        return es_sub(renpy.random.choice(lst))

    def es_love():
        """True si Monika esta en afecto enamorado o mas."""
        try:
            return bool(mas_isMoniEnamored(higher=True))
        except Exception:
            return False

    def es_session_add(sec):
        """Suma tiempo jugado; devuelve True una sola vez al pasar de 40 minutos."""
        ES_SESSION["time"] += int(sec)
        if ES_SESSION["time"] >= 2400 and not ES_SESSION["said"]:
            ES_SESSION["said"] = True
            return True
        return False

    # ---------- tienda ----------
    def es_upg(i):
        return persistent._es_upg.get(i, 0)

    def es_upg_cost(i):
        x = ES_UPG_D[i]
        lv = es_upg(i)
        if lv < len(x[3]):
            return x[3][lv]
        return None

    def es_can_buy(i):
        c = es_upg_cost(i)
        return c is not None and persistent._es_coins >= c

    def es_buy(i):
        if not es_can_buy(i):
            return
        persistent._es_coins -= es_upg_cost(i)
        d = dict(persistent._es_upg)
        d[i] = es_upg(i) + 1
        persistent._es_upg = d
        es_stat_add("buys", 1)
        if not es_has_ach("buyer"):
            persistent._es_ach = list(persistent._es_ach) + ["buyer"]

    def es_can_buy_skin(i):
        c = es_skin_price(i)
        return c is not None and not es_skin_unlocked(i) and persistent._es_coins >= c

    def es_buy_skin(i):
        if not es_can_buy_skin(i):
            return
        persistent._es_coins -= es_skin_price(i)
        persistent._es_skins = list(persistent._es_skins) + [i]
        persistent._es_skin = i
        es_stat_add("buys", 1)
        if not es_has_ach("buyer"):
            persistent._es_ach = list(persistent._es_ach) + ["buyer"]

    def es_equip_skin(i):
        if es_skin_unlocked(i):
            persistent._es_skin = i

    def es_skin_btn(i):
        if persistent._es_skin == i:
            return u"Equipada"
        if es_skin_unlocked(i):
            return u"Equipar"
        return u"Comprar (%d)" % es_skin_price(i)

    def es_skin_act(i):
        if es_skin_unlocked(i):
            es_equip_skin(i)
        else:
            es_buy_skin(i)

    def es_skin_ok(i):
        """Boton de nave activo: se puede equipar (no la actual) o comprar."""
        if es_skin_unlocked(i):
            return persistent._es_skin != i
        return es_can_buy_skin(i)

    def es_upg_btn(i):
        c = es_upg_cost(i)
        if c is None:
            return u"Máximo"
        return u"Comprar (%d)" % c

    def es_practice_max():
        return min(ES_NST, max(1, persistent._encoders_best_stage))

    # ---------- logros ----------
    def es_ach_met(i, sm, S):
        win = sm["win"]
        if i == "first_win":
            return win
        if i == "coop_win":
            return win and sm["mode"] == "coop"
        if i == "story_win":
            return win and sm["mode"] == "story"
        # con Monika de ayuda estos logros no cuentan
        solo = sm["mode"] != "coop"
        if i == "no_hit":
            return win and solo and sm["lives_lost"] == 0
        if i == "no_bomb":
            return win and solo and sm["bombs_used"] == 0
        if i == "hard_win":
            return win and solo and sm["diff"] == "hard" and sm["mode"] != "endless"
        if i == "combo30":
            return sm["maxcombo"] >= 30
        if i == "score5000":
            return sm["score"] >= 5000
        if i == "rank_s4":
            return len([1 for (s, r) in sm["ranks"] if r == "S"]) >= 4
        if i == "collector":
            return sm["types"] >= 8
        if i == "coins15":
            return sm["coins"] >= 15
        if i == "endless10":
            return sm["mode"] == "endless" and sm["stage"] >= 10
        if i == "games10":
            return S.get("games", 0) >= 10
        if i == "bosses25":
            return S.get("bosses", 0) >= 25
        if i == "mini15":
            return S.get("minis", 0) >= 15
        if i == "bosses100":
            return S.get("bosses", 0) >= 100
        if i == "graze100":
            return sm.get("grazes", 0) >= 100
        if i == "earned500":
            return S.get("earned", 0) >= 500
        if i == "fast_win":
            return win and solo and sm["mode"] != "endless" and sm["time"] < 720
        if i == "no_pu":
            return win and solo and sm["mode"] != "endless" and sm["pu"] <= 3
        return False

    def es_commit(sm):
        """Guarda el resultado de una partida. Devuelve un dict con las novedades."""
        # la practica no guarda nada
        if sm["mode"] == "practice":
            return {
                "key": "practice", "new_rec": False, "record": 0,
                "ach_names": [], "skin_names": [], "endless_new": False,
                "earn": 0, "miles": [],
            }

        key = es_mode_key(sm["mode"], sm["diff"])
        prev = es_record(key)
        new_rec = sm["score"] > prev and sm["score"] > 0
        if new_rec:
            es_record_set(key, sm["score"])
            if key == "normal":
                persistent._encoders_hiscore = sm["score"]
        if sm["stage"] > persistent._encoders_best_stage and sm["mode"] != "endless":
            persistent._encoders_best_stage = min(ES_NST, sm["stage"])

        # monedas de la tienda
        earn = sm["coins"] * 3 + sm["bosses"] * 5 + (30 if sm["win"] else 0)
        mult = 1.0 + 0.2 * es_upg("bank") + (0.5 if sm.get("skin") == 7 else 0.0)
        earn = int(earn * mult)
        persistent._es_coins += earn

        # estadisticas
        es_stat_add("games", 1)
        es_stat_add("time", int(sm["time"]))
        es_stat_add("kills", sm["kills"])
        es_stat_add("bosses", sm["bosses"])
        es_stat_add("minis", sm.get("minis", 0))
        es_stat_add("deaths", sm["lives_lost"])
        es_stat_add("bombs", sm["bombs_used"])
        es_stat_add("pu", sm["pu"])
        es_stat_add("coins", sm["coins"])
        es_stat_add("grazes", sm.get("grazes", 0))
        es_stat_add("earned", earn)
        es_stat_max("maxcombo", sm["maxcombo"])
        if sm["win"]:
            es_stat_add("wins", 1)
        es_stat_add("srank", len([1 for (s, r) in sm["ranks"] if r == "S"]))
        if sm["mode"] == "endless":
            es_stat_max("endless_best", sm["stage"])
        if sm["mode"] == "coop":
            es_stat_add("coop", 1)
        if sm["mode"] == "story":
            es_stat_add("story", 1)

        # mejores rangos por nivel (solo modos normales en solitario)
        if sm["mode"] not in ("endless", "coop"):
            rk = dict(persistent._es_ranks)
            for (s, r) in sm["ranks"]:
                k = "%s:%d" % (sm["diff"], s)
                if k not in rk or ES_RANK_VAL[r] > ES_RANK_VAL[rk[k]]:
                    rk[k] = r
            persistent._es_ranks = rk

        if sm["win"] and sm["mode"] != "coop" and not persistent._es_endless:
            persistent._es_endless = True
            endless_new = True
        else:
            endless_new = False

        # logros
        S = persistent._es_stats
        new_ach = []
        for a in ES_ACH:
            if not es_has_ach(a[0]) and es_ach_met(a[0], sm, S):
                new_ach.append(a[0])
        if new_ach:
            persistent._es_ach = list(persistent._es_ach) + new_ach
        new_skins = [s[0] for s in ES_SKINS if s[1] in new_ach]

        # hitos que Monika comenta una sola vez (maximo 2 por partida)
        checks = [
            ("g1",        S.get("games", 0) >= 1,
             u"Fue divertidísimo jugar contigo por primera vez, [player]. Podemos repetirlo cuando quieras."),
            ("firstboss", S.get("bosses", 0) >= 1,
             u"¡Derrotaste a tu primer jefe! Y apenas es el comienzo."),
            ("firstS",    S.get("srank", 0) >= 1,
             u"¡Tu primer rango S! Cada vez eres más hábil, [player]."),
            ("coop1",     S.get("coop", 0) >= 1,
             u"Volar juntos me encantó, [player]. ¡Podemos repetirlo cuando quieras!"),
            ("g10",       S.get("games", 0) >= 10,
             u"¡Ya van 10 partidas, [player]! Me encanta que pasemos tiempo así."),
            ("g50",       S.get("games", 0) >= 50,
             u"¡50 partidas! Creo que ya eres todo un piloto estrella, [player]."),
            ("allach",    len(persistent._es_ach) >= len(ES_ACH),
             u"¡Completaste todos los logros! Eres imparable, [player]."),
        ]
        seen = list(persistent._es_miles)
        miles = []
        for (mid, ok, text) in checks:
            if ok and mid not in seen and len(miles) < 2:
                seen.append(mid)
                miles.append(text)
        persistent._es_miles = seen

        # afecto: una vez al dia
        try:
            import datetime
            today = datetime.date.today()
            if persistent._es_last_aff != today and not sm["quit"]:
                persistent._es_last_aff = today
                mas_gainAffection(0.5)
        except Exception:
            pass

        return {
            "key": key,
            "new_rec": new_rec,
            "record": es_record(key),
            "ach_names": [ES_ACH_NAME[i] for i in new_ach],
            "skin_names": new_skins,
            "endless_new": endless_new,
            "earn": earn,
            "miles": miles,
        }

    # ---------- acciones de ajustes ----------
    def es_cycle(field, options):
        cur = getattr(persistent, field)
        try:
            i = options.index(cur)
        except ValueError:
            i = -1
        setattr(persistent, field, options[(i + 1) % len(options)])

    def es_cycle_skin():
        n = len(ES_SKINS)
        cur = persistent._es_skin
        for k in range(1, n + 1):
            j = (cur + k) % n
            if es_skin_unlocked(j):
                persistent._es_skin = j
                return

    def es_step(field, d):
        v = getattr(persistent, field) + d
        setattr(persistent, field, max(0.0, min(1.0, round(v, 2))))
        es_apply_volumes()   # se oye el cambio al instante (musica del menu)

    def es_step_int(field, d, lo, hi):
        v = getattr(persistent, field) + d
        setattr(persistent, field, max(lo, min(hi, v)))

    def es_onoff(field):
        return u"Sí" if getattr(persistent, field) else u"No"

    def es_pct(field):
        return u"%d%%" % int(round(getattr(persistent, field) * 100))

    # ---------- texto de estadisticas ----------
    def es_fmt_time(sec):
        sec = int(sec)
        return u"%dh %02dm" % (sec // 3600, (sec % 3600) // 60)

    def es_stats_lines():
        L = []
        L.append((u"Récords", True))
        for k in ("easy", "normal", "hard", "story", "endless", "coop"):
            if k == "endless" and not persistent._es_endless:
                continue
            L.append((u"  %s: %d puntos" % (ES_MODE_NAMES[k], es_record(k)), False))
        L.append((u"Totales", True))
        L.append((u"  Partidas: %d   Victorias: %d" % (es_stat("games"), es_stat("wins")), False))
        L.append((u"  Tiempo jugado: %s" % es_fmt_time(es_stat("time")), False))
        L.append((u"  Enemigos: %d   Jefes: %d   Mini-jefes: %d" % (es_stat("kills"), es_stat("bosses"), es_stat("minis")), False))
        L.append((u"  Vidas perdidas: %d   Bombas: %d" % (es_stat("deaths"), es_stat("bombs")), False))
        L.append((u"  Power-ups: %d   Monedas recogidas: %d" % (es_stat("pu"), es_stat("coins")), False))
        L.append((u"  Roces: %d   Monedas ganadas: %d" % (es_stat("grazes"), es_stat("earned")), False))
        L.append((u"  Mejor combo: %d   Rangos S: %d" % (es_stat("maxcombo"), es_stat("srank")), False))
        if persistent._es_endless:
            L.append((u"  Mejor nivel infinito: %d" % es_stat("endless_best"), False))
        L.append((u"Mejores rangos (%s)" % es_diff_name(), True))
        parts = []
        for s in range(1, ES_NST + 1):
            parts.append(u"%d:%s" % (s, persistent._es_ranks.get("%s:%d" % (persistent._es_diff, s), u"-")))
        L.append((u"  " + u"  ".join(parts), False))
        n = len([1 for a in ES_ACH if es_has_ach(a[0])])
        L.append((u"Logros (%d/%d)" % (n, len(ES_ACH)), True))
        for a in ES_ACH:
            if es_has_ach(a[0]):
                L.append((u"  (x) %s - %s" % (a[1], a[2]), False))
            elif a[3]:
                L.append((u"  ( ) ???  - Logro oculto", False))
            else:
                L.append((u"  ( ) %s - %s" % (a[1], a[2]), False))
        L.append((u"Naves", True))
        for i, s in enumerate(ES_SKINS):
            if es_skin_unlocked(i):
                L.append((u"  (x) %s - %s" % (s[0], s[2]), False))
            else:
                if es_skin_price(i) is not None:
                    L.append((u"  ( ) %s (tienda: %d monedas)" % (s[0], es_skin_price(i)), False))
                else:
                    L.append((u"  ( ) %s (logro: %s)" % (s[0], ES_ACH_NAME[s[1]]), False))
        return L


style es_opt_button is default:
    ypadding 5
style es_opt_button_text is default:
    size 22
    color "#222222"
    hover_color "#d04070"
    insensitive_color "#999999"
style es_opt_text is default:
    size 22
    color "#222222"
style es_opt_title is default:
    size 26
    color "#b03060"
    bold True
style es_opt_small is default:
    size 18
    color "#7a4a5a"

# cuerpo de los ajustes (lo usan el panel de MAS y el menu del juego)
screen es_opts_body(pfx="es_opt"):
    vbox:
        style_prefix pfx
        spacing 2
        textbutton (u"Dificultad: " + es_diff_name()) action Function(es_cycle, "_es_diff", ES_DIFF_ORDER)
        textbutton (u"Control relativo (arrastrar sin saltar): " + es_onoff("_es_relative")) action ToggleField(persistent, "_es_relative")
        if not persistent._es_relative:
            hbox:
                spacing 12
                text (u"Distancia de la nave al dedo: %d px" % persistent._es_offset)
                textbutton u"  -  " action Function(es_step_int, "_es_offset", -10, 0, 160)
                textbutton u"  +  " action Function(es_step_int, "_es_offset", 10, 0, 160)
        textbutton (u"Bomba a la izquierda: " + es_onoff("_es_lefty")) action ToggleField(persistent, "_es_lefty")
        textbutton (u"Doble toque = bomba: " + es_onoff("_es_dtap")) action ToggleField(persistent, "_es_dtap")
        textbutton (u"Bomba automática en el último golpe: " + es_onoff("_es_autobomb")) action ToggleField(persistent, "_es_autobomb")
        textbutton (u"Vibración: " + es_onoff("_es_vibrate")) action ToggleField(persistent, "_es_vibrate")
        textbutton (u"Comentarios de Monika: " + es_onoff("_es_comments")) action ToggleField(persistent, "_es_comments")
        textbutton (u"Música en las escenas de radio: " + es_onoff("_es_radio_music")) action ToggleField(persistent, "_es_radio_music")
        textbutton (u"Escena al perder (video y resumen): " + es_onoff("_es_go_video")) action ToggleField(persistent, "_es_go_video")
        textbutton (u"Rendimiento: " + ES_PERF_NAMES[persistent._es_perf]) action Function(es_perf_next)
        textbutton (u"Mostrar tutorial al empezar: " + es_onoff("_es_tutorial")) action ToggleField(persistent, "_es_tutorial")
        textbutton (u"Nave: " + ES_SKINS[persistent._es_skin][0]) action Function(es_cycle_skin)
        text (u"   " + ES_SKINS[persistent._es_skin][2]) style (pfx + "_small")
        text (u"Registro en Jugar: " + ES_REG.get("status", u"?")) style (pfx + "_small")
        hbox:
            spacing 12
            text (u"Música: " + es_pct("_es_vol_music"))
            textbutton u"  -  " action Function(es_step, "_es_vol_music", -0.1)
            textbutton u"  +  " action Function(es_step, "_es_vol_music", 0.1)
        hbox:
            spacing 12
            text (u"Efectos: " + es_pct("_es_vol_sfx"))
            textbutton u"  -  " action Function(es_step, "_es_vol_sfx", -0.1)
            textbutton u"  +  " action Function(es_step, "_es_vol_sfx", 0.1)

# panel dentro de los ajustes de MAS (se registra en header.rpy)
screen navecitas_settings():
    vbox:
        xfill True
        use es_opts_body
