# ---------------------------------------------------------------
#  Navecitas v3.4 - Minijuego de naves para MAS
#  8 niveles + 2 niveles bonus + modo infinito + practica + tienda
#  + modo Historia (story.rpy) + salto hiperespacial entre niveles.
#  Compatible con Ren'Py 7 (Python 2) y Ren'Py 8 (Python 3).
#
#  MUSICA PROPIA: pon en la carpeta audio/ archivos llamados
#  custom_stage.ogg, custom_stage2.ogg, custom_boss.ogg o
#  custom_boss2.ogg y custom_menu.ogg (tambien .mp3 / .opus) y se usaran en lugar
#  de la musica incluida. Si falta "2", usa la version sin numero.
# ---------------------------------------------------------------

init -1 python:
    renpy.music.register_channel("es_sfx", "sfx", False)
    renpy.music.register_channel("es_sfx2", "sfx", False)
    renpy.music.register_channel("es_sfx3", "sfx", False)
    renpy.music.register_channel("es_music", "music", True)

init 10 python:
    import random
    import math
    try:
        import pygame_sdl2 as es_pygame
    except ImportError:
        import pygame as es_pygame

    # tecla "atras" de Android (si no existe, Esc)
    ES_BACK_KEY = "K_AC_BACK" if hasattr(es_pygame, "K_AC_BACK") else "K_ESCAPE"

    ES_W = 1280
    ES_H = 720
    ES_IMG = "Submods/Navecitas/images/"
    ES_SND = "Submods/Navecitas/audio/"

    # Limites para que nunca haya lag
    ES_MAX_BULLETS = 48
    ES_MAX_ENEMIES = 9
    ES_MAX_EBULLETS = 48
    ES_MAX_BOOMS = 8
    ES_MAX_POWERUPS = 4
    ES_STARS = 30
    # fondos: nebulosa (640x360 al doble, se repite en vertical) y un planeta por nivel
    ES_PLANET_SZ = [(190, 190), (170, 170), (210, 210), (160, 160),
                    (220, 220), (299, 190), (299, 190), (250, 250),
                    (210, 210), (250, 250)]
    ES_NEB_SPD = 7.0       # px/s
    ES_PLANET_SPD = 11.0   # px/s

    # nombre, color de fondo, pesos de enemigos (basico, tirador, kamikaze, tanque,
    # dardo, francotirador, carguero)
    ES_STAGES = [
        (u"Órbita Terrestre",      "#070718", (10, 2, 0, 0, 0, 0, 0)),
        (u"Cinturón de Asteroides", "#0b0a1e", (8, 3, 3, 0, 2, 0, 0)),
        (u"Nebulosa Carmesí",      "#1a0710", (6, 3, 3, 2, 3, 0, 1)),
        (u"Base Enemiga",          "#0a1218", (5, 4, 3, 2, 3, 2, 2)),
        (u"Tormenta Solar",        "#1c1004", (5, 4, 4, 3, 3, 2, 2)),
        (u"Campo de Hielo",        "#06161c", (4, 4, 4, 3, 3, 3, 2)),
        (u"Núcleo Alienígena",     "#12081c", (3, 5, 4, 4, 3, 3, 3)),
        (u"Nave Nodriza",          "#1c0606", (3, 5, 5, 5, 3, 4, 3)),
        (u"Agujero Negro",         "#06031a", (2, 5, 5, 5, 4, 4, 4)),
        (u"Corazón del Vacío",     "#16030f", (2, 5, 5, 6, 4, 5, 5)),
    ]
    ES_NST = len(ES_STAGES)
    # tamano de cada tipo de enemigo (el 4 es la roca del nivel bonus) y puntos
    # 5-7: dardo (zigzag), francotirador y carguero (se divide al morir)
    ES_ESZ = [(60, 50), (60, 50), (60, 60), (90, 70), (56, 56), (56, 48), (64, 56), (88, 68)]
    ES_ESCORE = [10, 25, 15, 40, 5, 20, 30, 35]
    # posicion en los pesos de cada nivel -> tipo de enemigo (el 4 es la roca del bonus)
    ES_KINDMAP = [0, 1, 2, 3, 5, 6, 7]
    # ataques de cada jefe (se van alternando)
    ES_PATTERNS = [
        ["volley"],
        ["volley", "aimed"],
        ["rain", "volley"],
        ["aimed", "fan"],
        ["fan", "rain"],
        ["spiral", "volley"],
        ["spiral", "aimed", "rain"],
        ["spiral", "fan", "aimed", "rain"],
        ["spiral", "aimed", "fan", "rain"],
        ["fan", "spiral", "rain", "aimed", "volley"],
    ]
    # mini-jefes: aparecen a mitad de cada nivel (indice = nivel): nombre y ataques
    ES_MINI = [
        (u"Escolta Orbital",   ["volley", "aimed"]),
        (u"Centinela Pétreo",  ["volley", "walls"]),
        (u"Dron Carmesí",      ["fan", "zigzag"]),
        (u"Carguero Hostil",   ["aimed", "walls"]),
        (u"Escolta Solar",     ["rain", "zigzag", "aimed"]),
        (u"Centinela Glacial", ["fan", "walls", "aimed"]),
        (u"Dron Alienígena",   ["spiral", "walls", "zigzag"]),
        (u"Guardia Real",      ["spiral", "aimed", "walls", "zigzag"]),
        (u"Horizonte Roto",    ["spiral", "fan", "walls", "zigzag"]),
        (u"Latido del Vacío",  ["spiral", "aimed", "rain", "walls", "zigzag"]),
    ]
    # power-ups: 0 arma, 1 escudo, 2 vida, 3 bomba, 4 rapido, 5 x2,
    #            6 moneda (solo bonus), 7 iman, 8 drones, 9 laser, 10 tiempo lento
    ES_DROPS = ([0] * 26 + [1] * 16 + [2] * 7 + [3] * 14 + [4] * 12 + [5] * 12
                + [7] * 9 + [8] * 9 + [9] * 8 + [10] * 9)
    ES_RANK_BONUS = {"S": 500, "A": 300, "B": 150, "C": 0}

    # comentarios de Monika durante la partida
    ES_SAYS = {
        "start":    [u"¡Vamos, tú puedes!", u"¡A volar!", u"¡Yo te animo desde aquí!"],
        "hurt":     [u"¡Cuidado!", u"¡Auch! ¿Estás bien?", u"¡Tú puedes!", u"¡Esquiva con calma!"],
        "low":      [u"¡Última vida! Con calma...", u"¡Ánimo, aún no se acaba!",
                     u"Respira, tú puedes."],
        "boss":     [u"¡Ahí viene el jefe!", u"¡Concéntrate!", u"¡Fíjate en sus patrones!"],
        "mini":     [u"¡Un mini-jefe! ¡Cuidado!", u"¡Viene un guardián!", u"¡Es una escolta, concéntrate!"],
        "phase2":   [u"¡Se está enfureciendo!", u"¡Cambió de patrón!", u"¡Ahora va en serio!"],
        "clear":    [u"¡Lo hiciste!", u"¡Eso fue genial!", u"¡Un jefe menos!"],
        "rankS":    [u"¡Rango S! ¡Increíble!", u"¡Perfecto! ¡Rango S!"],
        "combo":    [u"¡Qué combo!", u"¡No pares!", u"¡Sigue así!"],
        "life":     [u"¡Una vida extra!", u"¡Qué alivio!"],
        "bomb":     [u"¡Boom!", u"¡Eso los despejó!", u"¡Bomba!"],
        "autobomb": [u"¡Bomba de emergencia!"],
        "laser":    [u"¡Qué rayo!", u"¡Pew pew!"],
        "drones":   [u"¡Ahora somos más!"],
        "bonus":    [u"¡Nivel bonus! ¡A recoger monedas!"],
        "graze":    [u"¡Qué reflejos!", u"¡Por un pelo!", u"¡Eso estuvo cerca!"],
        "m_intro":  [u"¡Juntos podemos!", u"¡Yo cubro tu espalda!", u"¡A volar juntos!"],
        "m_hit":    [u"¡Ay! Estoy bien, sigue tú.", u"¡Me dieron! Dame un segundo."],
        "m_save":   [u"¡Te cubro!", u"¡Yo me encargo de este golpe!", u"¡Cuidado, yo te protejo!"],
    }
    ES_STATUS_NAMES = [u"Rápido", u"x2", u"Imán", u"Drones", u"Láser", u"Lento"]
    # texto flotante al recoger cada power-up (mismo orden que ES_DROPS)
    ES_PU_NAMES = [u"¡Arma!", u"¡Escudo!", u"+1 vida", u"+1 bomba", u"¡Rápido!",
                   u"¡x2!", u"+1", u"¡Imán!", u"¡Drones!", u"¡Láser!", u"¡Lento!"]
    ES_PU_COL = ["#ffd24d", "#6fd3ff", "#ff7aa8", "#ff6a5a", "#ffe680",
                 "#ffb347", "#ffe066", "#c79bff", "#9bffb0", "#9fe8ff", "#b0b8ff"]

    def es_overlap(ax, ay, aw, ah, bx, by, bw, bh):
        return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah

    def es_track(name):
        """Musica personalizada si existe; si no, la incluida."""
        names = [name]
        if name[-1].isdigit():
            names.append(name.rstrip("0123456789"))
        for n in names:
            for ext in (".ogg", ".mp3", ".opus"):
                p = ES_SND + "custom_" + n + ext
                if renpy.loadable(p):
                    return p
        return ES_SND + name + ".ogg"


    class EncodersShooter(renpy.Displayable):

        # salto hiperespacial entre niveles (segundos): carga, impulso,
        # fundido a negro, pantalla negra con el titulo y llegada al nivel nuevo
        WP_A = 0.75
        WP_B = 1.8
        WP_C = 2.4
        WP_D = 3.6
        WP_ARR = 1.6

        def __init__(self, mode="normal", diff="normal", pstage=1, **kwargs):
            super(EncodersShooter, self).__init__(**kwargs)
            self.mode = mode
            self.endless = (mode == "endless")
            self.practice = (mode == "practice")
            self.start_n = max(1, min(ES_NST, int(pstage))) if self.practice else 1
            self.nst = 8 if mode == "story" else ES_NST     # la historia sigue siendo de 8 niveles
            self.quitting = False
            self.q_st0 = None
            self.relative = persistent._es_relative
            # tope de cuadros: 0 = ahorro (30), 1 = equilibrado (60), 2 = sin tope
            self.rdt = (0.0325, 0.0165, 0.0)[max(0, min(2, persistent._es_perf))]
            self.diff = diff if diff in ES_DIFFS else "normal"
            self.D = dict(ES_DIFFS[self.diff])
            self.coop = (mode == "coop")
            if self.coop:
                # con Monika de ayuda los enemigos aparecen mas y los jefes aguantan mas
                self.D["spawn"] *= 0.85
                self.D["boss"] *= 1.3

            # ajustes del jugador (se leen una vez por partida)
            self.opt_off = persistent._es_offset
            self.lefty = persistent._es_lefty
            self.dtap = persistent._es_dtap
            self.autobomb = persistent._es_autobomb
            self.vibrate = persistent._es_vibrate
            self.comments = persistent._es_comments
            sk = persistent._es_skin
            if sk < 0 or sk >= len(ES_SKINS) or not es_skin_unlocked(sk):
                sk = 0
            sfx = "" if sk == 0 else "_%d" % sk

            # habilidad de la nave elegida
            self.pick_pad = 12 if sk == 1 else 0        # Rosa: recoge de mas lejos
            self.drop_mult = 1.5 if sk == 2 else 1.0    # Esmeralda: mas power-ups
            self.sk_sc = 12 if sk == 3 else 10          # Dorada: +20% de puntos
            self.inv_hit = 2.4 if sk == 4 else 1.6      # Fantasma: mas invulnerable
            self.sk = sk
            self.shield_mult = 1.5 if sk == 5 else 1.0  # Celeste: escudos mas largos
            self.crit = 0.2 if sk == 6 else 0.0         # Carmesi: 20% de balas con doble dano
            self.sk_life = 1 if sk == 8 else 0          # Cosmica: una vida extra

            # mejoras compradas en la tienda
            self.up_bomb = es_upg("bomb")
            self.up_shield = es_upg("shield")
            self.up_life = es_upg("life")
            self.up_weapon = es_upg("weapon")
            self.pu_dur = 1.0 + 0.15 * es_upg("pu")
            self.drop_mult *= 1.0 + 0.2 * es_upg("loot")          # Radar de botin
            self.up_magnet = es_upg("magnet")                     # Iman inicial
            self.combo_len = 3.5 + 0.8 * es_upg("combo")          # Combo duradero
            self.bomb_pow = 0.1 + 0.04 * es_upg("bombpow")        # Bomba potente
            self.graze_pts = 5 + 5 * es_upg("graze")              # Roce premiado

            L = renpy.displayable
            I = lambda n: L(ES_IMG + "es_" + n + ".png")
            self.i_player = I("player" + sfx)
            self.i_bullet = I("bullet" + sfx)
            self.i_en = [I("enemy1"), I("enemy2"), I("enemy3"), I("enemy4"), I("rock"),
                         I("enemy5"), I("enemy6"), I("enemy7")]
            self.i_ebullet = I("ebullet")
            self.i_star = [I("star1"), I("star2")]
            self.i_heart = I("heart")
            self.i_boom = [I("boom%d" % i) for i in range(4)]
            self.i_pu = [I("powerup_w"), I("powerup_s"), I("powerup_h"),
                         I("powerup_b"), I("powerup_r"), I("powerup_x"),
                         I("coin"), I("powerup_m"), I("powerup_d"),
                         I("powerup_l"), I("powerup_t")]
            self.i_boss = [I("boss%d" % i) for i in range(ES_NST)]  # 160x112
            self.i_mini = [I("mini%d" % i) for i in range(ES_NST)]  # 128x92
            self.i_shield = I("shield")
            self.i_bombbtn = I("bombbtn")    # 100x100
            self.i_drone = I("drone")
            self.i_monika = I("monika")      # 56x56
            self.i_neb = [Transform(I("neb%d" % i), zoom=2.0) for i in range(ES_NST)]
            self.i_planet = [I("planet%d" % i) for i in range(ES_NST)]
            self.bgs = [Solid(s[1]) for s in ES_STAGES]
            self.flash_s = [Solid("#ffffff40"), Solid("#ffffff80"), Solid("#ffffffb8")]
            self.laser_o = Solid("#5fd0ff55", xysize=(28, ES_H))
            self.laser_i = Solid("#e8fbffcc", xysize=(10, ES_H))
            self.bar_bg = Solid("#000000aa", xysize=(408, 16))
            self.bars = [None] + [Solid("#ff4455", xysize=(20 * k, 10))
                                  for k in range(1, 21)]
            T = lambda s, sz, c: Text(s, size=sz, color=c, outlines=[(3, "#000000", 0, 0)])
            self.T = T
            self.t_warn = T(u"¡ADVERTENCIA!", 80, "#ff4455")
            self.t_clear = T(u"¡NIVEL COMPLETADO!", 70, "#66ff99")
            self.t_pause = T(u"PAUSA", 90, "#ffffff")
            self.t_resume = T(u"Toca para continuar", 36, "#dddddd")
            self.t_ph2 = T(u"¡FASE 2!", 80, "#ffb347")
            self.t_count = [None] + [T(u"%d" % i, 150, "#ffffff") for i in (1, 2, 3)]
            self.t_ready = T(u"¡Prepárate!", 40, "#dddddd")
            self.t_msave_on = Text(u"Monika: cubriéndote", size=24, color="#9bffb0",
                                   outlines=[(2, "#000000", 0, 0)])
            self.t_msave_off = Text(u"Monika: recargando", size=24, color="#aaaaaa",
                                    outlines=[(2, "#000000", 0, 0)])
            self.t_mstun = Text(u"¡Ay!", size=24, color="#ffffff",
                                outlines=[(2, "#000000", 0, 0)])
            self.float_cache = {}
            # animacion de salto entre niveles
            self.black_s = [Solid("#000000%02x" % int(255 * i / 10.0)) for i in range(11)]
            self.flame_o = [Solid("#ff9a2e", xysize=(14, h)) for h in (18, 34, 52, 74)]
            self.flame_i = [Solid("#fff3b0", xysize=(6, int(h * 0.6))) for h in (18, 34, 52, 74)]
            self.t_jump = T(u"¡SALTO HIPERESPACIAL!", 60, "#9fe8ff")
            self.streak_cache = {}
            self.bar_cache = {}
            self.core_o = Solid("#ff4466", xysize=(10, 10))
            self.core_i = Solid("#ffffff", xysize=(6, 6))
            self.say_cache = {}
            self.all_images = ([self.i_player, self.i_bullet, self.i_ebullet,
                                self.i_heart, self.i_shield, self.i_bombbtn,
                                self.i_drone, self.i_monika]
                               + self.i_en + self.i_star + self.i_boom
                               + self.i_pu + self.i_boss + self.i_mini + self.i_neb + self.i_planet)
            self.reset()

        # ---------- estado ----------
        def reset(self):
            self.px = ES_W / 2.0
            self.py = ES_H - 120.0
            self.tx = self.px
            self.ty = self.py
            self.bullets = []    # [x, y, vx]
            self.enemies = []    # [basex, y, speed, phase, kind, hp, shoot_t, x, (espera)]
            self.pending = []    # enemigos nuevos (hijos del carguero)
            self.ebullets = []   # [x, y, vx]
            self.booms = []      # [x, y, t]
            self.powerups = []   # [x, y, tipo]
            self.boss = None     # [x, y, hp, maxhp, dir, shoot_t]
            self.volley = 0
            self.spiral = 0.0
            self.stars = []     # capa lejana (lenta) y cercana (rapida)
            for i in range(ES_STARS):
                typ = random.randint(0, 1)
                spd = random.uniform(40, 100) if typ == 0 else random.uniform(140, 260)
                self.stars.append([random.uniform(0, ES_W), random.uniform(0, ES_H),
                                   spd, typ])
            self.score = 0
            self.lives = self.D["lives"] + self.up_life + self.sk_life
            self.bombs = 1 + self.up_bomb
            self.wl = 2 if self.up_weapon else 1
            for n in ("shield", "rapid", "x2", "magnet", "drones", "laser", "slow",
                      "flash", "inv", "fire_t", "over_t", "elapsed", "combo_t",
                      "dang", "dr_t", "laser_t", "ph2_t", "say_t", "say_cd",
                      "coin_t", "shake", "resume_t", "ach_t",
                      "arrive_t", "ship_dy", "wp_black", "mini_t"):
                setattr(self, n, 0.0)
            self.star_mul = 1.0
            self.wp_lines = []
            self.wp_title = None
            self.wp_tf = {}
            self.warp_kind = None
            self.warp_n = 1
            self.warp_story = False
            self.warp_story_done = False
            self.warp_launched = False
            self.spawn_t = 1.0
            self.over = False
            self.leaving = False     # fundido a negro al salir de la derrota
            self.leave_t = 0.0
            self.fail_who = u""
            self.victory = False
            self.paused = False
            self.auto_paused = False
            self.confirm = False
            self.last_st = None
            self.last_tap = -9.0
            self.tap_x = 0
            self.tap_y = 0
            self.down = False
            self.anc_x = 0
            self.anc_y = 0
            self.anc_tx = self.tx
            self.anc_ty = self.ty
            self.floats = []     # [x, y, t, Text]
            self.toasts = []     # [Text, t]
            self.toasted = set()
            self.grazes = 0
            self.shoot_n = 0
            self.sfx_i = 0
            # companera Monika (modo cooperativo)
            self.mx = ES_W / 2.0 + 110
            self.my = ES_H - 100.0
            self.m_side = 1
            self.m_stun = 0.0
            self.m_inv = 0.0
            self.m_fire = 0.5
            self.m_save = 1 if self.coop else 0
            self.neb_y = 0.0
            self.planet = None     # [x, y] del planeta de fondo
            # contadores de la partida
            self.combo = 0
            self.maxcombo = 0
            self.kills = 0
            self.bosses = 0
            self.minis = 0
            self.mini_txt = None
            self.hits = 0
            self.lives_lost = 0
            self.bombs_used = 0
            self.pu_count = 0
            self.pu_types = set()
            self.coins = 0
            self.ranks = []
            self.ph2 = False
            self.rank_txt = None
            self.say_txt = None
            self.hud_key = None
            self.hud_txt = None
            self.st_key = None
            self.st_txt = None
            self.cb_key = None
            self.cb_txt = None
            self.bomb_key = None
            self.bomb_txt = None
            self.over_txt = None
            self.start_stage(self.start_n, True)

        def start_stage(self, n, first=False):
            self.stage = n
            self.si = (n - 1) % ES_NST          # indice de fondo/jefe/ataques
            self.dsc = min(n, 16)               # escala de dificultad
            self.phase = "intro"
            self.phase_t = 0.0
            self.stage_t = 0.0
            self.stage_hits = 0
            self.stage_spawned = 0
            self.stage_killed = 0
            self.ph2 = False
            self.mini_done = False
            # planeta de fondo de este nivel (baja muy despacio)
            self.planet = [random.uniform(180, ES_W - 180), random.uniform(-40, 200)]
            name = ES_STAGES[self.si][0]
            self.banner = [
                self.T(u"NIVEL %d" % n, 80, "#ffffff"),
                Text(name, size=42, color="#ffe680", outlines=[(2, "#000000", 0, 0)]),
            ]
            if self.up_shield:
                self.shield = max(self.shield, 4.0 * self.up_shield)
            if self.up_magnet:
                self.magnet = max(self.magnet, 5.0 * self.up_magnet)
            if first:
                self.say("m_intro" if self.coop else "start", True)
                if n > 1:
                    self.set_music(self.stage_track(n))
            else:
                self.set_music(self.stage_track(n))

        def start_bonus(self):
            self.phase = "bonus"
            self.phase_t = 0.0
            self.spawn_t = 0.5
            self.coin_t = 0.8
            self.banner = [
                self.T(u"NIVEL BONUS", 80, "#ffe066"),
                Text(u"¡Esquiva las rocas y atrapa monedas!", size=38, color="#ffffff",
                     outlines=[(2, "#000000", 0, 0)]),
            ]
            self.say("bonus", True)

        def sfx(self, name):
            # el disparo usa su propio canal (y suena cada 3 tiros) para no
            # cortar explosiones ni recompensas; el resto rota entre 2 canales
            if name == "shoot":
                self.shoot_n += 1
                if self.shoot_n % 3 != 1:
                    return
                ch = "es_sfx3"
            else:
                self.sfx_i = 1 - self.sfx_i
                ch = "es_sfx2" if self.sfx_i else "es_sfx"
            renpy.music.play(ES_SND + name + ".ogg", channel=ch)

        def buzz(self, t):
            if self.vibrate:
                try:
                    renpy.vibrate(t)
                except Exception:
                    pass

        def stage_track(self, n):
            si = (n - 1) % ES_NST
            if si == 8:
                return "stage3"
            if si == 9:
                return "stage4"
            return "stage" if n % 2 else "stage2"

        def boss_track(self):
            if self.si == 8:
                return "boss3"
            if self.si == 9:
                return "boss4"
            return "boss" if self.si < 4 else "boss2"

        def set_music(self, name):
            renpy.music.play(es_track(name), channel="es_music", loop=True,
                             fadeout=0.4, fadein=0.4)

        def say(self, key, force=False):
            if not self.comments:
                return
            if self.say_cd > 0 and not force:
                return
            txt = u"Monika: " + random.choice(ES_SAYS[key])
            t = self.say_cache.get(txt)
            if t is None:
                t = Text(txt, size=30, color="#9bffb0", outlines=[(2, "#000000", 0, 0)])
                self.say_cache[txt] = t
            self.say_txt = t
            self.say_t = 2.8
            self.say_cd = 5.0

        def add_float(self, x, y, s, color):
            if len(self.floats) >= 8:
                return
            key = (s, color)
            t = self.float_cache.get(key)
            if t is None:
                t = Text(s, size=26, color=color, outlines=[(2, "#000000", 0, 0)])
                self.float_cache[key] = t
            self.floats.append([x, y, 0.0, t])

        def check_live(self):
            """Avisa en pantalla cuando se cumple un logro durante la partida."""
            if self.practice:
                return
            cand = (("combo30", self.maxcombo >= 30),
                    ("score5000", self.score >= 5000),
                    ("coins15", self.coins >= 15),
                    ("collector", len(self.pu_types) >= 8),
                    ("graze100", self.grazes >= 100))
            for (i, ok) in cand:
                if ok and i not in self.toasted and not es_has_ach(i):
                    self.toasted.add(i)
                    self.toasts.append([self.T(u"¡Logro: %s!" % ES_ACH_NAME[i], 34, "#ffe066"), 3.2])

        def add_boom(self, x, y):
            if len(self.booms) < ES_MAX_BOOMS:
                self.booms.append([x, y, 0.0])

        def combo_mult(self):
            c = self.combo
            if c < 5:
                return 10
            if c < 10:
                return 15
            if c < 20:
                return 20
            return 30

        def add_score(self, n, combo=True):
            m = self.combo_mult() if combo else 10
            x2 = 2 if self.x2 > 0 else 1
            self.score += n * x2 * m * self.D["score"] * self.sk_sc // 1000

        def toggle_pause(self):
            if self.over:
                return
            self.paused = not self.paused
            self.auto_paused = False
            renpy.music.set_pause(self.paused, channel="es_music")
            if not self.paused:
                self.last_st = None
                self.resume_t = 2.4     # cuenta atras 3-2-1 antes de seguir
            renpy.redraw(self, 0)

        def ask_quit(self):
            if self.over:
                return
            self.confirm = True
            if not self.paused:
                self.toggle_pause()

        def cancel_quit(self):
            self.confirm = False
            if self.paused:
                self.toggle_pause()

        def back_key(self):
            """Boton 'atras' de Android / Esc: abre o cierra el cuadro de salir."""
            if self.over:
                return
            if self.confirm:
                self.cancel_quit()
            else:
                self.ask_quit()

        def do_quit(self):
            """Salir: fundido a negro (lo dibuja render) y luego finish_quit."""
            self.confirm = False
            self.quitting = True
            self.q_st0 = None
            try:
                renpy.music.set_pause(False, channel="es_music")
                renpy.music.stop(channel="es_music", fadeout=0.9)
                renpy.music.play(ES_SND + "warp.ogg", channel="es_sfx")
            except Exception:
                pass
            renpy.redraw(self, 0)

        def finish_quit(self):
            return self.summary(True)

        def summary(self, quit=False):
            return {
                "score": self.score, "stage": self.stage, "win": self.victory,
                "quit": quit, "mode": self.mode, "diff": self.diff,
                "hits": self.hits, "lives_lost": self.lives_lost,
                "bombs_used": self.bombs_used, "maxcombo": self.maxcombo,
                "kills": self.kills, "bosses": self.bosses,
                "time": self.elapsed, "pu": self.pu_count, "coins": self.coins,
                "ranks": list(self.ranks), "types": len(self.pu_types),
                "grazes": self.grazes, "skin": self.sk, "minis": self.minis,
                "fail_who": self.fail_who,
            }

        # ---------- acciones ----------
        def shoot(self):
            if len(self.bullets) > ES_MAX_BULLETS - 3:
                return
            x = self.px - 3
            y = self.py - 38
            if self.wl == 1:
                self.bullets.append([x, y, 0])
            elif self.wl == 2:
                self.bullets.append([x - 12, y, 0])
                self.bullets.append([x + 12, y, 0])
            else:
                self.bullets.append([x, y, 0])
                self.bullets.append([x - 14, y + 6, -140])
                self.bullets.append([x + 14, y + 6, 140])
            self.sfx("shoot")

        def use_bomb(self, auto=False):
            if self.bombs <= 0 or self.over or self.paused or self.resume_t > 0:
                return
            self.bombs -= 1
            self.bombs_used += 1
            self.flash = 0.4
            self.shake = 0.35
            self.sfx("bomb")
            for e in self.enemies:
                if e[5] > 0:
                    self.kill(e, False)
            self.ebullets = []
            if self.boss is not None:
                self.boss[2] -= max(8, int(self.boss[3] * self.bomb_pow))
            self.inv = max(self.inv, 0.6)
            if not auto:
                self.say("bomb")

        def drop(self, x, y, force=None, chance=0.11):
            if len(self.powerups) >= ES_MAX_POWERUPS:
                return
            if force is None:
                if random.random() > chance:
                    return
                force = random.choice(ES_DROPS)
            self.powerups.append([x, y, force])

        def kill(self, e, drops=True):
            e[5] = 0
            self.kills += 1
            self.stage_killed += 1
            self.combo += 1
            self.combo_t = self.combo_len
            if self.combo > self.maxcombo:
                self.maxcombo = self.combo
            self.add_score(ES_ESCORE[e[4]])
            w, h = ES_ESZ[e[4]]
            self.add_boom(e[7] + w / 2.0, e[1] + h / 2.0)
            self.sfx("boom")
            if drops and e[4] != 4:
                self.drop(e[7] + w / 2.0, e[1] + h / 2.0,
                          chance={3: 0.35, 7: 0.3, 6: 0.16}.get(e[4], 0.11) * self.drop_mult)
            if drops and e[4] == 7:
                # el carguero suelta dos enemigos basicos al romperse
                for dx in (-34, 34):
                    nx = max(40.0, min(ES_W - 100.0, e[7] + 14 + dx))
                    self.stage_spawned += 1
                    self.pending.append([nx, e[1] + 14, random.uniform(100, 150) + self.dsc * 9,
                                         random.uniform(0, 6.28), 0, 1, 99.0, nx])

        def hurt(self):
            self.hits += 1
            self.stage_hits += 1
            self.combo = 0
            if self.shield > 0:
                self.shield = 0.0
                self.inv = 1.0
                self.sfx("hit")
                self.buzz(0.08)
                return
            if self.coop and self.m_save > 0:
                # Monika absorbe un golpe por nivel
                self.m_save -= 1
                self.inv = 1.4
                self.shake = 0.25
                self.add_float(self.px - 40, self.py - 50, u"¡Te cubro!", "#9bffb0")
                self.sfx("hit")
                return
            if self.lives == 1 and self.autobomb and self.bombs > 0:
                self.use_bomb(True)
                self.inv = max(self.inv, 1.2)
                return
            self.lives -= 1
            self.lives_lost += 1
            self.inv = self.inv_hit
            self.shake = 0.25
            self.wl = max(1, self.wl - 1)
            self.add_boom(self.px, self.py)
            self.buzz(0.2)
            if self.lives <= 0:
                self.finish(False)
            else:
                self.sfx("hit")

        def laser_tick(self):
            x0 = self.px - 9
            for e in self.enemies:
                if e[5] <= 0:
                    continue
                w, h = ES_ESZ[e[4]]
                if (e[7] + w > x0 and e[7] < x0 + 18 and e[1] + h > 0
                        and e[1] < self.py - 20):
                    e[5] -= 1
                    if e[5] <= 0:
                        self.kill(e)
            bs = self.boss
            if bs is not None and bs[1] > -60 and bs[0] + self.bbox(bs)[0] > x0 and bs[0] - self.bbox(bs)[0] < x0 + 18:
                bs[2] -= 2
            for b in self.ebullets:
                if abs(b[0] + 3 - self.px) < 14 and b[1] < self.py:
                    b[1] = ES_H + 100

        # ---------- jefes ----------
        def spawn_boss(self):
            n = self.stage
            hp = int((45 + 26 * (n - 1)) * self.D["boss"])
            self.boss = [ES_W / 2.0, -130.0, hp, hp, 1, 1.5]
            self.phase = "boss"
            self.phase_t = 0.0
            self.volley = 0
            self.ph2 = False
            self.sfx("warning")
            self.say("boss", True)
            self.set_music(self.boss_track())

        def bbox(self, bs):
            """(medio ancho, desfase superior, ancho, alto) de la caja de golpe."""
            if len(bs) > 6:
                return (52, 8, 104, 66)
            return (70, 10, 140, 90)

        def spawn_mini(self):
            n = self.stage
            hp = max(14, int((45 + 26 * (n - 1)) * self.D["boss"] * 0.42))
            self.boss = [ES_W / 2.0, -110.0, hp, hp, random.choice((-1, 1)), 1.2, self.si]
            self.mini_done = True
            self.mini_t = 2.0
            self.mini_txt = [self.T(u"¡MINI-JEFE!", 70, "#ffb347"),
                             Text(ES_MINI[self.si][0], size=36, color="#ffffff",
                                  outlines=[(2, "#000000", 0, 0)])]
            self.sfx("warning")
            self.say("mini", True)

        def mini_down(self, bs):
            self.minis += 1
            self.add_score(150 + 60 * min(self.stage, 12), False)
            for i in range(4):
                self.add_boom(bs[0] + random.uniform(-50, 50), bs[1] + random.uniform(10, 70))
            self.sfx("boom")
            self.shake = 0.35
            self.buzz(0.2)
            self.drop(bs[0], bs[1] + 50, chance=2.0)
            self.ebullets = []
            self.boss = None
            self.say("clear", True)

        def boss_fire(self, bs):
            if len(self.ebullets) > ES_MAX_EBULLETS - 12:
                return
            if len(bs) > 6:
                pats = ES_MINI[bs[6]][1]
            else:
                pats = ES_PATTERNS[self.si]
                if self.ph2:
                    pats = pats + ["wide"]
            pat = pats[self.volley % len(pats)]
            self.volley += 1
            x = bs[0]
            y = bs[1] + (72 if len(bs) > 6 else 100)
            E = self.ebullets
            if pat == "volley":
                for dx in (-60, 0, 60):
                    E.append([x + dx - 3, y, 0])
            elif pat == "fan":
                for vx in (-270, -180, -90, 0, 90, 180, 270):
                    E.append([x - 3, y, vx])
            elif pat == "wide":
                for i in range(10):
                    E.append([x - 3, y, -300 + 600 * i / 9.0])
            elif pat == "aimed":
                vy = (300 + self.dsc * 12) * self.D["bspd"]
                dy = max(40.0, self.py - y)
                for off in (-70, 0, 70):
                    vx = (self.px - (x + off)) / dy * vy
                    E.append([x + off - 3, y, max(-380, min(380, vx))])
            elif pat == "rain":
                for i in range(6):
                    E.append([random.uniform(40, ES_W - 40), -10, 0])
            elif pat == "walls":
                # pared de balas con un hueco de 3 espacios
                gap = random.randint(1, 9)
                for i in range(11):
                    if abs(i - gap) > 1:
                        E.append([60 + i * 116 - 3, -10, 0])
            elif pat == "zigzag":
                # abanico inclinado que cambia de lado en cada disparo
                self.spiral += 1.0
                d = 1 if int(self.spiral) % 2 else -1
                for k in range(5):
                    E.append([x - 3, y, d * (40 + 70 * k)])
            else:   # spiral
                self.spiral += 0.55
                for i in range(4):
                    E.append([x - 3, y, 250 * math.sin(self.spiral + i * 1.5708)])

        def boss_down(self, bs):
            self.bosses += 1
            self.add_score(300 + 150 * min(self.stage, 12), False)
            for i in range(5):
                self.add_boom(bs[0] + random.uniform(-70, 70),
                              bs[1] + random.uniform(10, 90))
            self.sfx("boom")
            self.shake = 0.6
            if self.coop:
                self.m_save = 1
            self.buzz(0.3)
            # rango del nivel
            hits = self.stage_hits
            ratio = self.stage_killed / float(max(1, self.stage_spawned))
            pts = (2 if hits == 0 else (1 if hits == 1 else 0))
            pts += 2 if ratio >= 0.85 else (1 if ratio >= 0.6 else 0)
            pts += 1 if self.phase_t < 16 + 2 * min(self.stage, 8) else 0
            rank = "S" if pts >= 5 else ("A" if pts == 4 else ("B" if pts >= 2 else "C"))
            bonus = ES_RANK_BONUS[rank]
            self.score += bonus
            self.ranks.append((self.stage, rank))
            self.rank_txt = self.T(u"Rango %s   +%d" % (rank, bonus), 54,
                                   {"S": "#ffe066", "A": "#9bffb0", "B": "#9fd0ff",
                                    "C": "#cccccc"}[rank])
            self.say("rankS" if rank == "S" else "clear", True)
            # limpiar pantalla
            for e in self.enemies:
                if e[5] > 0:
                    self.add_boom(e[7] + 30, e[1] + 25)
            self.enemies = []
            self.pending = []
            self.powerups = self.powerups[:2] + [
                [bs[0] - 40, bs[1] + 60, 2 if self.lives < 5 else 3],
                [bs[0] + 40, bs[1] + 60, 0]]
            self.ebullets = []
            self.boss = None
            self.phase = "clear"
            self.phase_t = 0.0
            renpy.music.stop(channel="es_music", fadeout=0.6)
            self.sfx("clear")

        # ---------- salto hiperespacial entre niveles ----------
        def begin_warp(self, kind):
            self.phase = "warp"
            self.phase_t = 0.0
            self.warp_kind = kind
            n = self.stage + 1
            self.warp_n = n
            self.warp_story = (self.mode == "story" and kind == "stage")
            self.warp_story_done = False
            self.warp_launched = False
            self.enemies = []
            self.pending = []
            self.mini_t = 0.0
            self.ebullets = []
            self.bullets = []
            self.powerups = []
            self.boss = None
            self.laser = 0.0
            self.say_t = 0.0
            if kind == "stage":
                nm = ES_STAGES[(n - 1) % ES_NST][0]
                self.wp_title = [self.T(u"NIVEL %d" % n, 80, "#ffffff"),
                                 Text(nm, size=42, color="#ffe680", outlines=[(2, "#000000", 0, 0)])]
            else:
                self.wp_title = [self.T(u"NIVEL BONUS", 80, "#ffe066"),
                                 Text(u"¡Esquiva las rocas y atrapa monedas!", size=38, color="#ffffff",
                                      outlines=[(2, "#000000", 0, 0)])]
            self.wp_tf = {}
            self.wp_lines = [[random.uniform(0, ES_W), random.uniform(-ES_H, ES_H),
                              random.uniform(0.6, 1.4), random.randint(0, 1)]
                             for _i in range(34)]
            self.star_mul = 1.0
            self.ship_dy = 0.0
            self.wp_black = 0.0
            self.sfx("warp")

        def warp_update(self, dt):
            t = self.phase_t
            if t < self.WP_A:
                # carga: la nave tiembla y las estrellas empiezan a estirarse
                k = t / self.WP_A
                self.star_mul = 1.0 + 3.0 * k * k
                self.ship_dy = 0.0
                self.shake = max(self.shake, 0.08 + 0.3 * k)
            elif t < self.WP_B:
                # impulso: la nave sale disparada hacia arriba
                tb = t - self.WP_A
                if not self.warp_launched:
                    self.warp_launched = True
                    self.flash = 0.42
                    self.shake = 0.5
                    self.buzz(0.25)
                self.star_mul = 4.0 + 26.0 * min(1.0, tb / 0.45)
                self.ship_dy = -1300.0 * tb * tb
            elif t < self.WP_C:
                # el escenario queda atras y la pantalla se funde a negro
                self.star_mul = 30.0
                self.ship_dy = -2400.0
                self.wp_black = (t - self.WP_B) / (self.WP_C - self.WP_B)
            else:
                self.star_mul = 30.0
                self.ship_dy = -2400.0
                self.wp_black = 1.0
                if self.warp_story and not self.warp_story_done:
                    # modo Historia: en la pantalla negra entra la escena
                    renpy.end_interaction(("story", "s%d" % (self.warp_n - 1)))
                elif t >= self.WP_D:
                    self.finish_warp()

        def finish_warp(self):
            if self.warp_kind == "bonus":
                self.start_bonus()
            else:
                self.start_stage(self.warp_n)
            self.arrive_t = self.WP_ARR
            self.star_mul = 12.0
            self.ship_dy = 340.0
            self.wp_black = 1.0
            self.fire_t = 0.3
            self.sfx("arrive")

        def story_resume(self):
            """Se llama al volver de una escena de historia."""
            self.warp_story_done = True
            self.phase_t = self.WP_C + 0.45
            self.last_st = None
            self.down = False

        def streak(self, h, k):
            h = max(16, (int(h) // 16) * 16)
            key = (h, k)
            s = self.streak_cache.get(key)
            if s is None:
                cols = ["#9fb8ff90", "#ffffffd0", "#6fd3ff60", "#ffe6a060"]
                s = Solid(cols[k], xysize=(2 if k in (0, 2) else 4, h))
                self.streak_cache[key] = s
            return s

        def wp_alpha(self, i, a):
            key = (i, int(a * 10 + 0.5))
            tf = self.wp_tf.get(key)
            if tf is None:
                tf = Transform(self.wp_title[i], alpha=key[1] / 10.0)
                self.wp_tf[key] = tf
            return tf

        # ---------- logica ----------
        def spawn_enemy(self):
            s = self.dsc
            w = ES_STAGES[self.si][2]
            r = random.uniform(0, sum(w))
            kind = 0
            for i, v in enumerate(w):
                r -= v
                if r <= 0:
                    kind = ES_KINDMAP[i]
                    break
            bx = random.uniform(80, ES_W - 80)
            if kind == 0:
                spd = random.uniform(80, 130) + s * 9
                hp = 1
            elif kind == 1:
                spd = random.uniform(80, 130) * 0.7 + s * 7
                hp = 3
            elif kind == 2:
                spd = 250 + s * 12
                hp = 1
            elif kind == 5:
                spd = 150 + s * 8
                hp = 1
            elif kind == 6:
                spd = 170.0
                hp = 3 + s // 5
            elif kind == 7:
                spd = 50 + s * 3
                hp = 5 + s
            else:
                spd = 55 + s * 5
                hp = 6 + s
            self.stage_spawned += 1
            self.enemies.append([bx, -70.0, spd, random.uniform(0, 6.28),
                                 kind, hp, random.uniform(0.8, 1.8), bx,
                                 (4.2 if kind == 6 else 0.0)])

        def spawn_rock(self):
            bx = random.uniform(60, ES_W - 60)
            self.enemies.append([bx, -60.0, random.uniform(170, 260), 0.0,
                                 4, 2, 99.0, bx])

        def update(self, dt):
            smul = self.star_mul      # 1 normal; mucho mas en el salto hiperespacial
            for s in self.stars:
                s[1] += s[2] * dt * smul
                if s[1] > ES_H:
                    s[1] = -4
                    s[0] = random.uniform(0, ES_W)
            if smul > 1.5:
                for L in self.wp_lines:
                    L[1] += 520.0 * L[2] * min(smul, 14.0) * dt
                    if L[1] > ES_H + 40:
                        L[1] = random.uniform(-500, -20)
                        L[0] = random.uniform(0, ES_W)

            self.neb_y = (self.neb_y + ES_NEB_SPD * dt * smul) % ES_H
            if self.planet is not None:
                self.planet[1] += ES_PLANET_SPD * dt * smul
                if self.planet[1] > ES_H + 160:
                    self.planet = None

            for b in self.booms:
                b[2] += dt
            self.booms = [b for b in self.booms if b[2] < 0.32]
            if self.flash > 0:
                self.flash -= dt
            if self.shake > 0:
                self.shake -= dt
            for f in self.floats:
                f[1] -= 55 * dt
                f[2] += dt
            self.floats = [f for f in self.floats if f[2] < 0.9]
            for tt in self.toasts:
                tt[1] -= dt
            self.toasts = [tt for tt in self.toasts if tt[1] > 0]
            if self.say_t > 0:
                self.say_t -= dt
            if self.say_cd > 0:
                self.say_cd -= dt

            if self.over:
                self.over_t += dt
                if self.leaving:
                    self.leave_t += dt
                    if self.leave_t >= 0.8:
                        renpy.end_interaction(self.summary())
                return

            # llegada al nivel nuevo: sale de la pantalla negra y frena
            if self.arrive_t > 0:
                self.arrive_t = max(0.0, self.arrive_t - dt)
                kk = self.arrive_t / self.WP_ARR
                self.star_mul = 1.0 + 11.0 * kk * kk * kk
                self.ship_dy = 340.0 * kk * kk
                self.wp_black = max(0.0, (kk - 0.62) / 0.38)
                if self.arrive_t <= 0:
                    self.star_mul = 1.0
                    self.ship_dy = 0.0
                    self.wp_black = 0.0

            st = self.dsc
            self.elapsed += dt
            self.ach_t -= dt
            if self.ach_t <= 0:
                self.ach_t = 0.5
                self.check_live()
            self.phase_t += dt
            for name in ("inv", "shield", "rapid", "x2", "magnet", "drones",
                         "laser", "slow", "ph2_t", "mini_t"):
                v = getattr(self, name)
                if v > 0:
                    setattr(self, name, v - dt)
            if self.combo > 0:
                self.combo_t -= dt
                if self.combo_t <= 0:
                    self.combo = 0

            # tiempo "lento" para enemigos y sus balas
            edt = dt * 0.5 if self.slow > 0 else dt

            # fases del nivel
            if self.phase == "intro":
                if self.phase_t > 2.5:
                    self.phase = "wave"
                    self.phase_t = 0.0
            elif self.phase == "wave":
                self.stage_t += dt
                tb = 28 + 2 * min(st, 8)
                if (not self.mini_done and not self.practice and self.stage >= 2
                        and self.boss is None and self.stage_t >= tb * 0.5):
                    self.spawn_mini()
                if self.stage_t >= tb and self.boss is None:
                    self.spawn_boss()
            elif self.phase == "clear":
                if self.phase_t > 3.0:
                    if self.practice:
                        self.finish(True)
                        return
                    if not self.endless and self.stage >= self.nst:
                        self.finish(True)
                        return
                    self.begin_warp("bonus" if self.si in (2, 5) else "stage")
            elif self.phase == "bonus":
                if self.phase_t > 15.0:
                    self.begin_warp("stage")

            # salto hiperespacial: la nave acelera, deja el escenario y se pasa
            # por una pantalla negra al siguiente nivel (sin disparos ni choques)
            if self.phase == "warp":
                self.warp_update(dt)
                return

            # nave del jugador (suavizada)
            k = min(1.0, dt * 14.0)
            self.px += (self.tx - self.px) * k
            self.py += (self.ty - self.py) * k

            if self.coop:
                self.monika_update(dt)

            # disparo automatico
            self.fire_t -= dt
            if self.fire_t <= 0:
                base = 0.2 if self.wl < 3 else 0.17
                self.fire_t = base * (0.55 if self.rapid > 0 else 1.0)
                self.shoot()

            # drones
            if self.drones > 0:
                self.dang += dt * 3.2
                self.dr_t -= dt
                if self.dr_t <= 0:
                    self.dr_t = 0.45
                    if len(self.bullets) < ES_MAX_BULLETS - 2:
                        for (dx, dy) in self.drone_pos():
                            self.bullets.append([self.px + dx - 3, self.py + dy - 14, 0])

            # laser
            if self.laser > 0:
                self.laser_t -= dt
                if self.laser_t <= 0:
                    self.laser_t = 0.1
                    self.laser_tick()

            # balas y power-ups
            for b in self.bullets:
                b[1] -= 760 * dt
                b[0] += b[2] * dt
            self.bullets = [b for b in self.bullets
                            if b[1] > -20 and -20 < b[0] < ES_W + 20]
            vy = (300 + st * 12) * self.D["bspd"] * edt
            for b in self.ebullets:
                b[1] += vy
                b[0] += b[2] * edt
            self.ebullets = [b for b in self.ebullets
                             if b[1] < ES_H + 20 and -20 < b[0] < ES_W + 20]
            for p in self.powerups:
                if self.magnet > 0:
                    dx = self.px - p[0]
                    dy = self.py - p[1]
                    d = math.hypot(dx, dy) + 0.01
                    if d < 380:
                        p[0] += dx / d * 430 * dt
                        p[1] += dy / d * 430 * dt
                        continue
                p[1] += 150 * dt
            self.powerups = [p for p in self.powerups if p[1] < ES_H + 40]

            # jefe
            bs = self.boss
            if bs is not None:
                if bs[2] <= 0:
                    if len(bs) > 6:
                        self.mini_down(bs)
                    else:
                        self.boss_down(bs)
                    bs = None
                else:
                    if len(bs) < 7 and not self.ph2 and bs[1] >= 60 and bs[2] <= bs[3] * 0.5:
                        self.ph2 = True
                        self.ph2_t = 1.8
                        self.ebullets = []
                        self.sfx("warning")
                        self.say("phase2", True)
                    if bs[1] < 60:
                        bs[1] += 90 * dt
                    else:
                        spd = (110 + st * 18) * (1.3 if self.ph2 else 1.0)
                        bs[0] += bs[4] * spd * edt
                        if bs[0] > ES_W - 100:
                            bs[4] = -1
                        elif bs[0] < 100:
                            bs[4] = 1
                        bs[5] -= edt
                        if bs[5] <= 0:
                            iv = max(0.55, 1.4 - 0.1 * st) * (0.75 if self.ph2 else 1.0)
                            if len(bs) > 6:
                                iv *= 1.25
                            bs[5] = iv
                            self.boss_fire(bs)

            # aparicion de enemigos
            if self.phase == "bonus":
                if self.phase_t > 1.5:
                    self.spawn_t -= dt
                    if self.spawn_t <= 0:
                        self.spawn_t = 0.42
                        if len(self.enemies) < ES_MAX_ENEMIES:
                            self.spawn_rock()
                    self.coin_t -= dt
                    if self.coin_t <= 0:
                        self.coin_t = 0.65
                        if len(self.powerups) < 10 and self.phase_t < 13.5:
                            self.powerups.append([random.uniform(60, ES_W - 60), -20.0, 6])
            elif self.phase in ("wave", "boss") or (self.phase == "intro" and self.phase_t > 1.2):
                self.spawn_t -= dt
                if self.spawn_t <= 0:
                    base = max(0.38, 1.25 - st * 0.1) * self.D["spawn"]
                    self.spawn_t = base * (2.4 if self.boss else 1.0)
                    if len(self.enemies) < (4 if self.boss else ES_MAX_ENEMIES):
                        self.spawn_enemy()

            # mover enemigos
            for e in self.enemies:
                kind = e[4]
                e[1] += e[2] * edt
                if kind == 2:       # kamikaze: persigue en horizontal
                    dx = (self.px - e[7]) * 2.0
                    e[7] += max(-200.0, min(200.0, dx)) * edt
                elif kind == 4:     # roca
                    e[7] = e[0]
                elif kind == 5:     # dardo: zigzag amplio y rapido
                    e[7] = max(20.0, min(ES_W - 76.0, e[0] + math.sin(self.elapsed * 4.5 + e[3]) * 170))
                elif kind == 6:     # francotirador: baja, se detiene, apunta y se va
                    e[7] = e[0] + math.sin(self.elapsed * 1.2 + e[3]) * 25
                    if e[1] < 95 and e[8] > 0:
                        e[2] = 170.0
                    elif e[8] > 0:
                        e[2] = 0.0
                        e[8] -= edt
                    else:
                        e[2] = 260.0
                elif kind == 7:     # carguero: lento, se divide al morir
                    e[7] = e[0] + math.sin(self.elapsed * 1.4 + e[3]) * 40
                else:
                    e[7] = e[0] + math.sin(self.elapsed * 2.0 + e[3]) * 60
                if kind == 1 or kind == 3:
                    e[6] -= edt
                    if e[6] <= 0 and e[1] > 0:
                        w = ES_ESZ[kind][0]
                        if len(self.ebullets) < ES_MAX_EBULLETS - 4:
                            if kind == 1:
                                e[6] = max(0.9, 2.0 - st * 0.1)
                                self.ebullets.append([e[7] + w / 2 - 3, e[1] + 45, 0])
                            else:
                                e[6] = max(1.3, 2.4 - st * 0.1)
                                for vx in (-110, 0, 110):
                                    self.ebullets.append([e[7] + w / 2 - 3, e[1] + 55, vx])
                        else:
                            e[6] = 0.5
                if kind == 6 and e[2] == 0.0:
                    e[6] -= edt
                    if e[6] <= 0:
                        if len(self.ebullets) < ES_MAX_EBULLETS - 4:
                            e[6] = max(1.1, 1.9 - st * 0.06)
                            sx = e[7] + 30
                            sy = e[1] + 52
                            vy = (300 + st * 12) * self.D["bspd"]
                            dy = max(40.0, self.py - sy)
                            vx = max(-380.0, min(380.0, (self.px - sx) / dy * vy))
                            self.ebullets.append([sx - 3, sy, vx])
                        else:
                            e[6] = 0.5

            # balas vs enemigos
            for e in self.enemies:
                if e[5] <= 0:
                    continue
                w, h = ES_ESZ[e[4]]
                for b in self.bullets:
                    if b[1] < -50:
                        continue
                    if es_overlap(b[0], b[1], 6, 18, e[7] + 4, e[1] + 4, w - 8, h - 8):
                        b[1] = -100
                        e[5] -= 2 if (self.crit and random.random() < self.crit) else 1
                        if e[5] <= 0:
                            self.kill(e)
                        break

            # balas vs jefe
            if bs is not None:
                for b in self.bullets:
                    if b[1] < -50:
                        continue
                    if es_overlap(b[0], b[1], 6, 18, bs[0] - self.bbox(bs)[0], bs[1] + self.bbox(bs)[1],
                                                 self.bbox(bs)[2], self.bbox(bs)[3]):
                        b[1] = -100
                        bs[2] -= 2 if (self.crit and random.random() < self.crit) else 1

            self.bullets = [b for b in self.bullets if b[1] > -20]
            self.enemies = [e for e in self.enemies
                            if e[5] > 0 and e[1] < ES_H + 70]
            if self.pending:
                self.enemies += self.pending
                self.pending = []

            # recoger power-ups
            for p in self.powerups:
                pd = self.pick_pad
                if es_overlap(self.px - 22 - pd, self.py - 24 - pd, 44 + 2 * pd, 48 + 2 * pd,
                              p[0] - 18, p[1] - 18, 36, 36):
                    t = p[2]
                    s0 = self.score
                    d = self.pu_dur
                    if t != 6:
                        self.pu_count += 1
                        self.pu_types.add(t)
                    if t == 0:
                        if self.wl < 3:
                            self.wl += 1
                        else:
                            self.add_score(50, False)
                    elif t == 1:
                        self.shield = 8.0 * d * self.shield_mult
                    elif t == 2:
                        if self.lives < 5:
                            self.lives += 1
                            self.say("life")
                        else:
                            self.add_score(50, False)
                    elif t == 3:
                        if self.bombs < 3:
                            self.bombs += 1
                        else:
                            self.add_score(50, False)
                    elif t == 4:
                        self.rapid = 10.0 * d
                    elif t == 5:
                        self.x2 = 15.0 * d
                    elif t == 6:
                        self.coins += 1
                        self.add_score(30, False)
                    elif t == 7:
                        self.magnet = 10.0 * d
                    elif t == 8:
                        self.drones = 14.0 * d
                        self.say("drones")
                    elif t == 9:
                        self.laser = 5.0 * d
                        self.laser_t = 0.0
                        self.say("laser")
                    else:
                        self.slow = 6.0 * d
                    nm = ES_PU_NAMES[t]
                    if t in (0, 2, 3) and self.score > s0:
                        nm = u"+%d" % (self.score - s0)
                    self.add_float(p[0] - 20, p[1] - 30, nm, ES_PU_COL[t])
                    p[1] = ES_H + 100
                    self.sfx("pickup")
            self.powerups = [p for p in self.powerups if p[1] < ES_H + 40]

            # roces: puntos por pasar cerca de una bala sin que te toque
            if self.inv <= 0 and not self.over:
                for b in self.ebullets:
                    if (len(b) == 3 and abs(b[0] + 3 - self.px) < 30
                            and abs(b[1] + 7 - self.py) < 30):
                        b.append(1)
                        self.grazes += 1
                        self.add_score(self.graze_pts, False)
                        if self.grazes in (25, 50, 100):
                            self.say("graze")

            # choques con el jugador (solo cuenta el nucleo de la nave: 12x14)
            if self.inv <= 0 and not self.over:
                hit = False
                cx = self.px - 6
                cy = self.py - 7
                for e in self.enemies:
                    w, h = ES_ESZ[e[4]]
                    if es_overlap(cx, cy, 12, 14,
                                  e[7] + 8, e[1] + 8, w - 16, h - 16):
                        self.add_boom(e[7] + w / 2.0, e[1] + h / 2.0)
                        e[5] = 0
                        hit = True
                for b in self.ebullets:
                    if es_overlap(cx, cy, 12, 14, b[0], b[1], 6, 15):
                        b[1] = ES_H + 100
                        hit = True
                if bs is not None and es_overlap(cx, cy, 12, 14,
                                                 bs[0] - self.bbox(bs)[0], bs[1] + self.bbox(bs)[1],
                                                 self.bbox(bs)[2], self.bbox(bs)[3]):
                    hit = True
                if hit:
                    self.hurt()

        # ---------- companera Monika (IA) ----------
        def monika_update(self, dt):
            if self.m_stun > 0:
                self.m_stun -= dt
            if self.m_inv > 0:
                self.m_inv -= dt

            # destino: a un lado de la nave del jugador
            gx = self.px + self.m_side * 110
            if gx < 50 or gx > ES_W - 50:
                self.m_side = -self.m_side
                gx = self.px + self.m_side * 110
            gy = self.py + 20

            # esquivar balas que vienen hacia ella
            push = 0
            for b in self.ebullets:
                if self.my - 150 < b[1] < self.my + 10 and abs(b[0] + 3 - self.mx) < 44:
                    push += 1 if b[0] + 3 < self.mx else -1
                    if b[0] + 3 == self.mx:
                        push += self.m_side
            if push != 0:
                gx = self.mx + (100 if push > 0 else -100)

            k = min(1.0, dt * 6.0)      # mas lenta que el jugador: se nota que es una IA
            self.mx += (gx - self.mx) * k
            self.my += (gy - self.my) * k
            self.mx = max(36.0, min(ES_W - 36.0, self.mx))
            self.my = max(80.0, min(ES_H - 40.0, self.my))

            if self.over:
                return

            # disparo (usa el mismo nivel de arma que el jugador)
            if self.m_stun <= 0:
                self.m_fire -= dt
                if self.m_fire <= 0:
                    self.m_fire = 0.32 * (0.55 if self.rapid > 0 else 1.0)
                    if len(self.bullets) < ES_MAX_BULLETS - 4:
                        x = self.mx - 3
                        y = self.my - 38
                        if self.wl == 1:
                            self.bullets.append([x, y, 0])
                        elif self.wl == 2:
                            self.bullets.append([x - 10, y, 0])
                            self.bullets.append([x + 10, y, 0])
                        else:
                            self.bullets.append([x, y, 0])
                            self.bullets.append([x - 12, y + 6, -120])
                            self.bullets.append([x + 12, y + 6, 120])

            # si la tocan, se aturde un momento (no pierde nada)
            if self.m_inv <= 0:
                cx = self.mx - 6
                cy = self.my - 7
                hit = False
                for b in self.ebullets:
                    if es_overlap(cx, cy, 12, 14, b[0], b[1], 6, 15):
                        b[1] = ES_H + 100
                        hit = True
                for e in self.enemies:
                    w, h = ES_ESZ[e[4]]
                    if e[5] > 0 and es_overlap(cx, cy, 12, 14, e[7] + 8, e[1] + 8, w - 16, h - 16):
                        self.add_boom(e[7] + w / 2.0, e[1] + h / 2.0)
                        e[5] = 0
                        hit = True
                bs = self.boss
                if bs is not None and es_overlap(cx, cy, 12, 14, bs[0] - self.bbox(bs)[0], bs[1] + self.bbox(bs)[1],
                                                 self.bbox(bs)[2], self.bbox(bs)[3]):
                    hit = True
                if hit:
                    self.m_stun = 2.0
                    self.m_inv = 3.0
                    self.add_boom(self.mx, self.my)
                    self.add_float(self.mx - 20, self.my - 50, u"¡Ay!", "#ffffff")

        def drone_pos(self):
            a = self.dang
            c = 62 * math.cos(a)
            s = 14 * math.sin(a)
            return [(c, s - 4), (-c, -s - 4)]

        def finish(self, win):
            self.over = True
            self.victory = win
            self.over_t = 0.0
            self.combo = 0
            self.leaving = False
            self.leave_t = 0.0
            if not win:
                # donde fallamos (lo muestra la tarjeta de derrota)
                bs = self.boss
                if bs is not None and len(bs) > 6:
                    self.fail_who = u"el mini-jefe " + ES_MINI[bs[6]][0]
                elif bs is not None:
                    self.fail_who = u"el jefe del nivel"
                elif self.phase == "bonus":
                    self.fail_who = u"las rocas del nivel bonus"
                else:
                    self.fail_who = u"la oleada de enemigos"
            renpy.music.stop(channel="es_music", fadeout=1.5)
            if win:
                if not self.practice:
                    self.score += 1000 + 300 * self.lives
                self.sfx("clear")
                head = self.T(u"¡VICTORIA!", 90, "#ffe066")
            else:
                self.sfx("gameover")
                head = self.T(u"GAME OVER", 84, "#ff6688")
            if self.endless:
                line = u"Puntos: %d   Nivel: %d" % (self.score, self.stage)
            else:
                line = u"Puntos: %d   Nivel: %d/%d" % (self.score, self.stage, self.nst)
            self.over_txt = [
                head,
                Text(line, size=40, color="#ffffff", outlines=[(2, "#000000", 0, 0)]),
                Text(u"Toca para continuar", size=32, color="#cccccc",
                     outlines=[(2, "#000000", 0, 0)]),
            ]

        # ---------- dibujo ----------
        def put(self, r, d, x, y, st, at):
            r.blit(renpy.render(d, ES_W, ES_H, st, at), (int(x), int(y)))

        def center(self, r, d, y, st, at):
            tr = renpy.render(d, ES_W, ES_H, st, at)
            tw, th = tr.get_size()
            r.blit(tr, (int((ES_W - tw) / 2), int(y)))

        def render(self, width, height, st, at):
            # si pasa mucho tiempo entre cuadros (app en segundo plano), pausa sola
            if (self.last_st is not None and not self.paused and not self.over
                    and st - self.last_st > 1.0):
                self.paused = True
                self.auto_paused = True
                renpy.music.set_pause(True, channel="es_music")
            if self.paused or self.last_st is None:
                dt = 0.0
            else:
                dt = min(st - self.last_st, 0.05)   # evita saltos tras pausas
            self.last_st = st
            if not self.paused:
                if self.resume_t > 0:
                    # cuenta atras tras reanudar: el juego espera, la nave sigue al dedo
                    self.resume_t -= dt
                    k = min(1.0, dt * 14.0)
                    self.px += (self.tx - self.px) * k
                    self.py += (self.ty - self.py) * k
                else:
                    self.update(dt)

            # temblor de pantalla (solo el mundo, no el HUD)
            ox = oy = 0
            if self.shake > 0 and not self.paused:
                m = min(14.0, self.shake * 26.0)
                ox = random.uniform(-m, m)
                oy = random.uniform(-m, m)

            r = renpy.Render(ES_W, ES_H)
            put = self.put

            def putw(d, x, y):
                put(r, d, x + ox, y + oy, st, at)

            put(r, self.bgs[self.si], 0, 0, st, at)
            # nebulosa que se desplaza lento (dos copias para que no haya corte)
            put(r, self.i_neb[self.si], 0, self.neb_y, st, at)
            put(r, self.i_neb[self.si], 0, self.neb_y - ES_H, st, at)
            if self.planet is not None:
                pw, ph = ES_PLANET_SZ[self.si]
                putw(self.i_planet[self.si], self.planet[0] - pw / 2.0,
                     self.planet[1] - ph / 2.0)
            sm = self.star_mul
            for s in self.stars:
                if sm > 2.5:
                    h = min(520, int(s[2] * sm * 0.05))
                    putw(self.streak(h, s[3]), s[0], s[1] - h)
                putw(self.i_star[s[3]], s[0], s[1])
            if sm > 2.5:
                for L in self.wp_lines:
                    h = min(560, int(260 * min(sm, 14.0) * 0.09 * L[2]))
                    putw(self.streak(h, L[3] + 2), L[0], L[1] - h)
            for p in self.powerups:
                putw(self.i_pu[p[2]], p[0] - 18, p[1] - 18)
            for b in self.bullets:
                putw(self.i_bullet, b[0], b[1])
            for b in self.ebullets:
                putw(self.i_ebullet, b[0], b[1])
            for e in self.enemies:
                putw(self.i_en[e[4]], e[7], e[1])

            bs = self.boss
            if bs is not None:
                if len(bs) > 6:
                    putw(self.i_mini[bs[6]], bs[0] - 64, bs[1])
                else:
                    putw(self.i_boss[self.si], bs[0] - 80, bs[1])

            if not self.over and self.laser > 0 and (self.laser > 1 or int(self.laser * 10) % 2 == 0):
                putw(self.laser_o, self.px - 14, self.py - 30 - ES_H)
                putw(self.laser_i, self.px - 5, self.py - 30 - ES_H)

            # durante el salto la nave (y Monika) se desplazan y sale la llama
            sy = self.ship_dy
            sx = 0.0
            warping = (self.phase == "warp" and self.phase_t < self.WP_C) or self.arrive_t > 0
            if self.phase == "warp" and self.phase_t < self.WP_A:
                sx = random.uniform(-4.0, 4.0)
            if warping and not self.over:
                fl = int(self.elapsed * 30) % 2
                lvl = min(3, 1 + int(self.star_mul / 6.0))
                li = max(0, min(3, lvl - fl))
                putw(self.flame_o[li], self.px + sx - 7, self.py + 22 + sy)
                putw(self.flame_i[li], self.px + sx - 3, self.py + 22 + sy)
                if self.coop:
                    putw(self.flame_o[li], self.mx + sx - 7, self.my + 22 + sy)
                    putw(self.flame_i[li], self.mx + sx - 3, self.my + 22 + sy)
            if not self.over and not (self.inv > 0 and int(self.inv * 12) % 2 == 0):
                putw(self.i_player, self.px - 28 + sx, self.py - 28 + sy)
                if self.shield > 0 and (self.shield > 2 or int(self.shield * 8) % 2 == 0):
                    putw(self.i_shield, self.px - 42 + sx, self.py - 42 + sy)
            if self.coop and not self.over:
                if not (self.m_inv > 0 and int(self.m_inv * 12) % 2 == 0):
                    putw(self.i_monika, self.mx - 28 + sx, self.my - 28 + sy)
            if not self.over:
                # nucleo: lo unico que cuenta como golpe
                putw(self.core_o, self.px - 5 + sx, self.py - 5 + sy)
                putw(self.core_i, self.px - 3 + sx, self.py - 3 + sy)
            if not self.over and self.drones > 0 and (self.drones > 2 or int(self.drones * 8) % 2 == 0):
                for (dx, dy) in self.drone_pos():
                    putw(self.i_drone, self.px + dx - 12 + sx, self.py + dy - 12 + sy)

            for b in self.booms:
                f = min(3, int(b[2] / 0.08))
                putw(self.i_boom[f], b[0] - 36, b[1] - 36)

            if self.flash > 0:
                put(r, self.flash_s[min(2, int(self.flash / 0.14))], 0, 0, st, at)

            # HUD (los textos solo se rehacen cuando cambian)
            key = (self.score, self.stage, self.wl)
            if key != self.hud_key:
                self.hud_key = key
                if self.endless:
                    s = u"Puntos: %d   Nivel: %d   Arma: %d" % key
                else:
                    s = u"Puntos: %d   Nivel: %d/%d   Arma: %d" % (key[0], key[1], self.nst, key[2])
                self.hud_txt = Text(s, size=30, color="#ffffff",
                                    outlines=[(2, "#000000", 0, 0)])
            put(r, self.hud_txt, 20, 12, st, at)
            for i in range(max(0, self.lives)):
                put(r, self.i_heart, 20 + i * 28, 52, st, at)

            k2 = tuple([int(v + 0.99) if v > 0 else 0 for v in
                        (self.rapid, self.x2, self.magnet, self.drones,
                         self.laser, self.slow)])
            if k2 != self.st_key:
                self.st_key = k2
                parts = [u"%s %ds" % (ES_STATUS_NAMES[i], v) for i, v in enumerate(k2) if v]
                self.st_txt = Text(u"   ".join(parts), size=26, color="#ffe680",
                                   outlines=[(2, "#000000", 0, 0)]) if parts else None
            if self.st_txt is not None:
                put(r, self.st_txt, 20, 92, st, at)

            ck = (self.combo, self.combo_mult()) if self.combo >= 3 else None
            if ck != self.cb_key:
                self.cb_key = ck
                if ck:
                    self.cb_txt = Text(u"Combo %d  (x%.1f)" % (ck[0], ck[1] / 10.0),
                                       size=28, color="#ffb347",
                                       outlines=[(2, "#000000", 0, 0)])
                else:
                    self.cb_txt = None
            if self.cb_txt is not None:
                put(r, self.cb_txt, 20, 124, st, at)
            if self.coop:
                put(r, self.t_msave_on if self.m_save > 0 else self.t_msave_off,
                    20, 160, st, at)

            # boton de bomba
            bx = 20 if self.lefty else 1160
            put(r, self.i_bombbtn, bx, 610, st, at)
            if self.bombs != self.bomb_key:
                self.bomb_key = self.bombs
                self.bomb_txt = Text(u"x%d" % self.bombs, size=34, color="#ffffff",
                                     outlines=[(3, "#000000", 0, 0)])
            put(r, self.bomb_txt, (bx + 105) if self.lefty else (bx - 40), 650, st, at)

            if bs is not None:
                k = max(1, int(math.ceil(20.0 * max(0, bs[2]) / bs[3])))
                put(r, self.bar_bg, 436, 16, st, at)
                put(r, self.bars[min(20, k)], 440, 19, st, at)

            # salto: fundido a negro y pantalla de cambio de nivel
            if self.wp_black > 0.02:
                put(r, self.black_s[min(10, int(self.wp_black * 10 + 0.5))], 0, 0, st, at)
            if self.phase == "warp":
                tw = self.phase_t
                if tw < self.WP_C - 0.3 and int(tw * 5) % 2 == 0:
                    self.center(r, self.t_jump, 250, st, at)
                if tw >= self.WP_C and self.wp_title is not None:
                    a = min(1.0, (tw - self.WP_C) / 0.35)
                    self.center(r, self.wp_alpha(0, a), 240, st, at)
                    self.center(r, self.wp_alpha(1, a), 335, st, at)
                    prog = min(1.0, (tw - self.WP_C) / (self.WP_D - self.WP_C))
                    bw = int(prog * 24) * 20
                    if bw > 0:
                        bar = self.bar_cache.get(bw)
                        if bar is None:
                            bar = Solid("#ffe680", xysize=(bw, 4))
                            self.bar_cache[bw] = bar
                        self.center(r, bar, 410, st, at)

            # carteles
            if self.phase == "intro" and not self.over:
                self.center(r, self.banner[0], 240, st, at)
                self.center(r, self.banner[1], 335, st, at)
            elif self.phase == "bonus" and self.phase_t < 2.2 and not self.over:
                self.center(r, self.banner[0], 240, st, at)
                self.center(r, self.banner[1], 335, st, at)
            elif self.phase == "boss" and self.phase_t < 2.2 and int(self.phase_t * 4) % 2 == 0:
                self.center(r, self.t_warn, 260, st, at)
            elif self.phase == "clear" and not self.over:
                self.center(r, self.t_clear, 230, st, at)
                if self.rank_txt is not None:
                    self.center(r, self.rank_txt, 320, st, at)
            if self.ph2_t > 0 and int(self.ph2_t * 5) % 2 == 0:
                self.center(r, self.t_ph2, 260, st, at)
            if self.mini_t > 0 and self.mini_txt is not None and int(self.mini_t * 5) % 2 == 0:
                self.center(r, self.mini_txt[0], 230, st, at)
                self.center(r, self.mini_txt[1], 320, st, at)

            for f in self.floats:
                put(r, f[3], f[0], f[1], st, at)
            for i, tt in enumerate(self.toasts[:2]):
                self.center(r, tt[0], 170 + 44 * i, st, at)

            if self.resume_t > 0 and not self.paused and not self.over:
                n = min(3, max(1, int(math.ceil(self.resume_t / 0.8))))
                self.center(r, self.t_count[n], 250, st, at)
                self.center(r, self.t_ready, 420, st, at)

            if self.say_t > 0 and self.say_txt is not None and not self.over:
                self.center(r, self.say_txt, 665, st, at)

            if self.paused and not self.quitting:
                self.center(r, self.t_pause, 300, st, at)
                if self.auto_paused:
                    self.center(r, self.t_resume, 410, st, at)

            if self.over and not self.victory:
                # derrota: la pantalla se va oscureciendo poco a poco
                k = min(7, int(min(1.0, self.over_t / 1.4) * 7 + 0.5))
                if k > 0:
                    put(r, self.black_s[k], 0, 0, st, at)
            if self.over and self.over_txt:
                self.center(r, self.over_txt[0], 200, st, at)
                self.center(r, self.over_txt[1], 330, st, at)
                self.center(r, self.over_txt[2], 400, st, at)
            if self.over and self.leaving:
                # al tocar: fundido a negro total (tapa tambien el texto)
                k = min(10, int(min(1.0, self.leave_t / 0.8) * 10 + 0.5))
                put(r, self.black_s[k], 0, 0, st, at)

            if self.quitting:
                # al salir: fundido a negro de ~0.9 s (el texto tambien se apaga)
                if self.q_st0 is None:
                    self.q_st0 = st
                k = min(10, int(min(1.0, (st - self.q_st0) / 0.9) * 10 + 0.5))
                put(r, self.black_s[k], 0, 0, st, at)

            if not self.paused or self.quitting:
                renpy.redraw(self, self.rdt)
            return r

        # ---------- entrada (touch = mouse en Android) ----------
        def event(self, ev, x, y, st):
            if self.over:
                if self.over_t > 1.0 and ev.type == es_pygame.MOUSEBUTTONUP:
                    if self.victory:
                        return self.summary()
                    if not self.leaving:
                        # derrota: la pantalla se funde a negro y luego sigue la escena
                        self.leaving = True
                        self.leave_t = 0.0
                return None
            if self.paused:
                if (self.auto_paused and not self.confirm
                        and ev.type == es_pygame.MOUSEBUTTONUP):
                    self.toggle_pause()
                return None
            if ev.type == es_pygame.MOUSEBUTTONUP:
                self.down = False
            if self.phase == "warp":
                return None     # durante el salto no se controla la nave ni se lanzan bombas
            if ev.type == es_pygame.MOUSEBUTTONDOWN and getattr(ev, "button", 1) == 1:
                self.down = True
                self.anc_x = x
                self.anc_y = y
                self.anc_tx = self.tx
                self.anc_ty = self.ty
                bx = 20 if self.lefty else 1160
                if bx - 20 <= x <= bx + 120 and y > 590:
                    self.use_bomb()
                    self.down = False
                    return None
                if self.dtap:
                    if (st - self.last_tap < 0.32 and abs(x - self.tap_x) < 90
                            and abs(y - self.tap_y) < 90):
                        self.last_tap = -9.0
                        self.use_bomb()
                        return None
                    self.last_tap = st
                    self.tap_x = x
                    self.tap_y = y
            if ev.type in (es_pygame.MOUSEMOTION, es_pygame.MOUSEBUTTONDOWN):
                if self.relative:
                    # control relativo: la nave se mueve lo mismo que el dedo
                    if self.down:
                        self.tx = max(30, min(ES_W - 30, self.anc_tx + (x - self.anc_x)))
                        self.ty = max(60, min(ES_H - 40, self.anc_ty + (y - self.anc_y)))
                else:
                    self.tx = max(30, min(ES_W - 30, x))
                    self.ty = max(60, min(ES_H - 40, y - self.opt_off))   # nave sobre el dedo
            return None

        def visit(self):
            return self.all_images


screen encoders_shooter_screen(game):
    modal True
    zorder 200
    add Solid("#000000")
    add game
    key ES_BACK_KEY action Function(game.back_key)
    key "K_ESCAPE" action Function(game.back_key)
    if game.quitting:
        timer 1.0 action Function(game.finish_quit)
    elif not game.confirm:
        hbox:
            xalign 1.0
            yalign 0.0
            xoffset -15
            yoffset 10
            spacing 30
            textbutton (u"Reanudar" if game.paused else u"Pausa"):
                text_size 28
                text_color "#ffffff"
                text_hover_color "#ffcc66"
                action Function(game.toggle_pause)
            textbutton u"Salir":
                text_size 28
                text_color "#ffffff"
                text_hover_color "#ffcc66"
                action Function(game.ask_quit)
    else:
        frame:
            xalign 0.5
            yalign 0.5
            padding (50, 30)
            background Solid("#000000e0")
            vbox:
                spacing 18
                text u"¿Salir de la partida?" size 38 color "#ffffff" xalign 0.5
                text u"Se guardará tu puntaje actual." size 26 color "#cccccc" xalign 0.5
                hbox:
                    spacing 60
                    xalign 0.5
                    textbutton u"Sí, salir":
                        text_size 32
                        text_color "#ffffff"
                        text_hover_color "#ffcc66"
                        action Function(game.do_quit)
                    textbutton u"Seguir jugando":
                        text_size 32
                        text_color "#ffffff"
                        text_hover_color "#ffcc66"
                        action Function(game.cancel_quit)
