# ---------------------------------------------------------------
#  Navecitas v3.4 - modo Historia
#
#  Escenas animadas entre niveles. Monika habla por RADIO (Control de
#  Misión): sin sprites suyos, solo diálogo, estática y sonido de radio.
#  Cada escena es un fondo animado con código (nebulosa, planeta,
#  asteroides, radar, tormenta solar...) + cuadro de diálogo propio.
#
#  Para añadir o cambiar texto, edita ES_STORY (más abajo).
# ---------------------------------------------------------------

init -1 python:
    # canales propios: estática de fondo y "voz" de radio
    renpy.music.register_channel("es_radio", "sfx", True)
    renpy.music.register_channel("es_talk", "sfx", True)

# escenas que ya viste (se pueden repetir desde el menú: Jugar > Escenas)
default persistent._es_story_seen = []


init 12 python:
    import math
    import random

    # estado compartido entre el guion, el fondo y el cuadro de diálogo
    ES_ST = {"skip": False, "end": False, "noise": 0.1, "talk": False,
             "lines": [], "sid": None, "replay": False}

    ES_STORY_ORDER = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]

    # ------------------------------------------------------------
    #  GUION
    #  líneas: (quién, texto, ruido, condición)
    #    quién:  "m" Monika (radio) / "p" tú (radio) / "n" sistema
    #    ruido:  0.0 a 1.0 de interferencia (None = el de la escena)
    #    condición (opcional): "love" o "nolove" según el afecto
    #  si: nivel al que se llega (0-7), define nebulosa, planeta y color
    #  fx: capas animadas de la escena
    # ------------------------------------------------------------
    ES_STORY = {
        "s0": {
            "label": u"PRÓLOGO", "place": u"Órbita Terrestre",
            "si": 0, "neb": 0, "planet": (0, 230, 650, 2.6),
            "fx": ["shadow", "ship"], "ship": (840, 400), "noise": 0.12,
            "lines": [
                ("n", u"[[ ENLACE DE RADIO ESTABLECIDO ]", 0.35),
                ("m", u"...¿Me escuchas, [player]? Aquí Monika, Control de Misión. Probando, probando. Cambio.", 0.3),
                ("m", u"¡Ah, qué alivio! Tu señal llegó clara. Voy a seguir tu nave desde aquí, así que no estás solo ahí arriba.", None),
                ("m", u"Hace un rato mis sensores detectaron algo enorme acercándose a la Tierra: una Nave Nodriza, rodeada de muchísimas naves más pequeñas.", None),
                ("m", u"No sé qué quieren, pero no parece que vengan a conversar. Y eres el único piloto lo bastante cerca para detenerlas.", None),
                ("p", u"Recibido, Monika. Voy para allá.", None),
                ("m", u"Cuenta conmigo para lo que necesites: rutas, avisos y ánimos. Los ánimos son lo que mejor se me da.", None),
                ("m", u"Empezamos en la Órbita Terrestre. Despega cuando estés listo, [player]. ¡Y no te preocupes, sigo contigo en la frecuencia!", None),
            ],
        },
        "s1": {
            "label": u"CAPÍTULO 1", "place": u"Cinturón de Asteroides",
            "si": 1, "neb": 1, "planet": (1, 1050, 190, 1.5),
            "fx": ["rocks", "ship"], "ship": (500, 410), "noise": 0.22,
            "lines": [
                ("m", u"¡Lo lograste! El guardián cayó y la órbita quedó despejada. Sabía que podías, [player].", 0.1),
                ("m", u"Pero escucha: antes de caer, su radio mandó un mensaje hacia el Cinturón de Asteroides. Están pidiendo refuerzos.", None),
                ("m", u"Entre tantas rocas hay muchos escondites. Ten cuidado: una roca no es un enemigo, pero tampoco es tu amiga.", None),
                ("m", u"Entramos al cinturón... ¡ay, la señal se entrecorta con tanta piedra! ¿M-me escuchas? Te sigo en el radar.", 0.6),
            ],
        },
        "s2": {
            "label": u"CAPÍTULO 2", "place": u"Nebulosa Carmesí",
            "si": 2, "neb": 2, "planet": (2, 220, 210, 1.4),
            "fx": ["radar", "foes", "ship"], "ship": (430, 420), "noise": 0.2,
            "radar": (1010, 290, 150),
            "foes": [(0, 560, 190, 120, 0.5, 0.0, 1.0, 0.35),
                     (1, 700, 260, 150, 0.4, 2.0, 1.0, 0.30)],
            "lines": [
                ("m", u"Segundo jefe fuera. Cada vez que derrotas a uno, la red de comunicaciones enemiga pierde un pedazo.", 0.1),
                ("m", u"Con lo que quedó pude leer parte de su mensaje: todos se dirigen al mismo lugar, dentro de la Nebulosa Carmesí.", None),
                ("m", u"Esa nube roja confunde los instrumentos. Mi radar parece una sopa de puntitos, así que tendrás que fiarte de tus reflejos.", 0.35),
                ("m", u"Y de mi voz, claro. Mi voz siempre te va a llegar. ¡Rumbo a la nebulosa!", None),
            ],
        },
        "s3": {
            "label": u"CAPÍTULO 3", "place": u"Base Enemiga",
            "si": 3, "neb": 3, "planet": (3, 1060, 160, 1.3),
            "fx": ["skyline", "foes", "ship"], "ship": (420, 380), "noise": 0.12,
            "foes": [(3, 640, 215, 330, 0.35, 0.0, 1.0, 0.55),
                     (1, 800, 160, 380, 0.5, 2.5, 1.0, 0.45)],
            "lines": [
                ("m", u"¡Cruzaste el campo de monedas y derrotaste al jefe de la nebulosa! Mis instrumentos vuelven a la normalidad, qué descanso.", 0.1),
                ("m", u"Mira lo que apareció en el radar: una base enemiga escondida detrás de la nube. Ahí se reúnen todas las naves.", None),
                ("m", u"Hay torretas, tanques y vigilancia por todos lados. Aquí ya no mandan refuerzos pequeños, [player].", None),
                ("m", u"Si algo sale mal, respira y recuerda: solo cuenta el puntito del centro de tu nave. ¡Confío en ti!", None),
            ],
        },
        "s4": {
            "label": u"CAPÍTULO 4", "place": u"Tormenta Solar",
            "si": 4, "neb": 4, "planet": (4, 640, 130, 2.6),
            "fx": ["flares", "ship"], "ship": (640, 420), "noise": 0.5,
            "lines": [
                ("m", u"¡Base destruida! Ya casi puedo ver la Nave Nodriza en el radar, aunque todavía está muy lejos.", 0.15),
                ("m", u"Para llegar hay que cruzar una tormenta solar. Las llamaradas harán que mi señal se corte y vuelva... Si no me oyes un momento, no te asustes, ¿sí?", 0.55),
                ("m", u"Sigue derecho. Voy a quedarme repitiendo tu nombre en la radio hasta que la señal vuelva. [player]... [player]... ¿Ves? Así no te pierdes.", 0.85),
            ],
        },
        "s5": {
            "label": u"CAPÍTULO 5", "place": u"Campo de Hielo",
            "si": 5, "neb": 5, "planet": (5, 1030, 190, 1.6),
            "fx": ["snow", "ship"], "ship": (420, 410), "noise": 0.15,
            "lines": [
                ("m", u"...¿Sigues ahí? ¡Tu señal volvió! Qué bien, casi se me detiene el corazón. Digo, la radio.", 0.55),
                ("m", u"Más adelante hay un campo de hielo. El frío entorpece los motores, así que las balas enemigas vuelan más lento... pero son muchas.", None),
                ("m", u"Mantén la calma y pasa entre ellas. Y abrígate, aunque sea con cariño. Yo te mando calor desde aquí.", None),
            ],
        },
        "s6": {
            "label": u"CAPÍTULO 6", "place": u"Núcleo Alienígena",
            "si": 6, "neb": 6, "planet": (6, 760, 220, 2.2), "pulse": True,
            "fx": ["foes", "ship"], "ship": (330, 420), "noise": 0.18,
            "foes": [(2, 450, 170, 160, 0.9, 0.0, 1.0, 0.45),
                     (2, 560, 300, 200, 0.7, 2.0, 1.0, 0.40)],
            "lines": [
                ("m", u"El hielo se rompió y atrapaste monedas como si nada. Se nota que ya tienes práctica, [player].", 0.1),
                ("m", u"Escucha esto: detecté un latido. Algo vivo y enorme en el centro de su flota, un núcleo alienígena que alimenta a todas las naves.", None),
                ("m", u"Si lo detenemos, la Nave Nodriza se queda sin energía. Ese es el plan, y lo mejor es que solo tenemos que apuntar bien.", None),
                ("m", u"Se siente raro oír un latido por la radio... ¿o será el mío? Prepárate.", None),
            ],
        },
        "s7": {
            "label": u"CAPÍTULO 7", "place": u"Nave Nodriza",
            "si": 7, "neb": 7, "planet": (7, 930, 210, 1.9),
            "fx": ["alarm", "boss", "ship"], "ship": (380, 420), "noise": 0.3,
            "boss": (7, 900, 200, 2.6, 4.2, 0.9),
            "lines": [
                ("m", u"¡El núcleo se apagó! Hiciste lo imposible, [player]. Y ahora sí: ahí está. La Nave Nodriza.", 0.2),
                ("m", u"Es enorme, mucho más que todo lo que hemos visto, y está disparando con todo lo que le queda.", 0.35),
                ("p", u"Lo sé. Pero no voy a retroceder.", None),
                ("m", u"Lo sé. Por eso estoy tan orgullosa de ti. Pase lo que pase, estoy en tu frecuencia hasta el último segundo.", None),
                ("m", u"Última misión, [player]. ¡Vamos con todo!", None),
            ],
        },
        "s8": {
            "label": u"EPÍLOGO", "place": u"Amanecer sobre la Tierra",
            "si": 0, "neb": 0, "planet": (0, 640, 745, 3.2),
            "fx": ["dawn", "fire", "ship"], "ship": (640, 400), "noise": 0.06,
            "lines": [
                ("n", u"[[ LA NAVE NODRIZA SE HA DESACTIVADO ]", 0.4),
                ("m", u"...¿Lo oyes? Silencio en la frecuencia enemiga. ¡Se terminó, [player]! ¡Ganaste!", 0.25),
                ("m", u"La Tierra está a salvo, y justo delante de ti hay un amanecer precioso. Te lo mereces.", 0.05),
                ("m", u"Ya puedes volver a casa. Y si te quedaste con ganas de más, siempre podemos volar un poco más lejos juntos.", None),
                ("m", u"Gracias por no dejarme sola en la radio. Te quiero, [player]. Cambio y fuera.", None, "love"),
                ("m", u"Gracias por no dejarme sola en la radio, [player]. Fue un gran vuelo. Cambio y fuera.", None, "nolove"),
            ],
        },
    }

    def es_story_btn(sid):
        """Texto del botón de la lista de escenas."""
        if sid in persistent._es_story_seen:
            c = ES_STORY[sid]
            return u"%s - %s" % (c["label"].title(), c["place"])
        return u"???"

    def es_ease(x):
        x = max(0.0, min(1.0, x))
        return x * x * (3.0 - 2.0 * x)

    def es_story_skip():
        ES_ST["skip"] = True

    def es_tap():
        """Toque en la pantalla durante la radio: pasa al siguiente dialogo."""
        return True

    # ------------------------------------------------------------
    #  Sonido de radio
    # ------------------------------------------------------------
    def es_cb_common(event, talk, beep, interact):
        """Callback de los personajes de radio: 'kshh' al abrir, balbuceo de
        voz mientras se escribe el texto."""
        if not interact:
            return
        try:
            if event == "begin":
                renpy.music.play(ES_SND + ("beep.ogg" if beep else "radio_open.ogg"),
                                 channel="es_sfx")
            elif event == "show":
                if talk:
                    ES_ST["talk"] = True
                    renpy.music.play(ES_SND + talk, channel="es_talk", loop=True)
            elif event == "slow_done" or event == "end":
                ES_ST["talk"] = False
                renpy.music.stop(channel="es_talk", fadeout=0.08)
        except Exception:
            pass

    def es_cb_m(event, interact=True, **kwargs):
        es_cb_common(event, "radio_talk.ogg", False, interact)

    def es_cb_p(event, interact=True, **kwargs):
        es_cb_common(event, "radio_talk2.ogg", False, interact)

    def es_cb_n(event, interact=True, **kwargs):
        es_cb_common(event, None, True, interact)

    def es_say(who, text):
        if who == "m":
            es_radio_m(text)
        elif who == "p":
            es_radio_p(text)
        else:
            es_radio_n(text)

    # ------------------------------------------------------------
    #  Control de la escena (lo llama el label es_story_play)
    # ------------------------------------------------------------
    def es_story_begin(sid, replay=False):
        cfg = ES_STORY[sid]
        love = es_love()
        lines = []
        for ln in cfg["lines"]:
            cond = ln[3] if len(ln) > 3 else None
            if cond == "love" and not love:
                continue
            if cond == "nolove" and love:
                continue
            noise = ln[2] if (len(ln) > 2 and ln[2] is not None) else cfg.get("noise", 0.1)
            lines.append((ln[0], ln[1], noise))
        ES_ST["lines"] = lines
        ES_ST["sid"] = sid
        ES_ST["skip"] = False
        ES_ST["end"] = False
        ES_ST["talk"] = False
        ES_ST["noise"] = cfg.get("noise", 0.1)
        ES_ST["replay"] = replay
        if sid not in persistent._es_story_seen:
            persistent._es_story_seen = list(persistent._es_story_seen) + [sid]
        if replay:
            es_lock_ui()
        try:
            vol = persistent._es_vol_sfx
            for (ch, k) in (("es_radio", 0.35), ("es_talk", 0.7), ("es_sfx", 1.0),
                            ("es_sfx2", 1.0), ("es_sfx3", 1.0)):
                renpy.music.set_volume(max(0.0, min(1.0, vol * k)), channel=ch)
            renpy.music.play(ES_SND + "radio_static.ogg", channel="es_radio",
                             loop=True, fadein=0.6)
            # musica suave de fondo mientras hablamos por radio (se puede apagar en Ajustes)
            if persistent._es_radio_music:
                renpy.music.set_pause(False, channel="es_music")
                renpy.music.set_volume(max(0.0, min(1.0, persistent._es_vol_music * 0.5)),
                                       channel="es_music")
                renpy.music.play(es_track("radio_music"), channel="es_music",
                                 loop=True, fadein=1.2)
        except Exception:
            pass

    def es_story_run():
        """Reproduce las líneas una por una (cada una es un 'say' normal:
        toca para avanzar)."""
        L = ES_ST["lines"]
        for i in range(len(L)):
            if ES_ST["skip"]:
                break
            who, text, noise = L[i]
            ES_ST["noise"] = noise
            if noise >= 0.5:
                try:
                    renpy.music.play(ES_SND + "radio_crackle.ogg", channel="es_sfx3")
                except Exception:
                    pass
            es_say(who, text)
            nxt = L[i + 1][0] if i + 1 < len(L) else None
            if who != "n" and nxt != who and not ES_ST["skip"]:
                try:
                    renpy.music.play(ES_SND + "radio_close.ogg", channel="es_sfx2")
                except Exception:
                    pass

    def es_story_end():
        ES_ST["talk"] = False
        try:
            renpy.music.stop(channel="es_talk", fadeout=0.1)
            renpy.music.stop(channel="es_radio", fadeout=0.6)
            if persistent._es_radio_music:
                renpy.music.stop(channel="es_music", fadeout=0.5)
        except Exception:
            pass
        es_apply_volumes()
        if ES_ST["replay"]:
            es_unlock_ui()

    # ------------------------------------------------------------
    #  Barras de la "voz" de radio (en el cuadro de diálogo)
    # ------------------------------------------------------------
    class EsWave(renpy.Displayable):

        def __init__(self, **kwargs):
            super(EsWave, self).__init__(**kwargs)
            self.sc = {}

        def solid(self, h):
            s = self.sc.get(h)
            if s is None:
                s = Solid("#9bffb0", xysize=(4, h))
                self.sc[h] = s
            return s

        def render(self, width, height, st, at):
            r = renpy.Render(120, 34)
            talk = ES_ST["talk"]
            for i in range(16):
                if talk:
                    h = 4 + int(26 * abs(math.sin(st * 9.0 + i * 0.9) * math.sin(st * 5.3 + i * 1.7)))
                else:
                    h = 3 + int(2 * abs(math.sin(st * 2.0 + i)))
                h = max(2, min(30, h))
                r.blit(renpy.render(self.solid(h), 4, h, st, at), (i * 7, (34 - h) // 2))
            renpy.redraw(self, 1.0 / 24)
            return r

    # ------------------------------------------------------------
    #  Fondo animado de las escenas (solo depende del reloj)
    # ------------------------------------------------------------
    class EsStoryBG(renpy.Displayable):

        def __init__(self, sid, **kwargs):
            super(EsStoryBG, self).__init__(**kwargs)
            cfg = ES_STORY[sid]
            self.cfg = cfg
            self.fx = cfg.get("fx", [])
            self.sc = {}       # cache de Solid
            self.zc = {}       # cache de imágenes con zoom / alfa
            self.tc = {}       # cache de textos con alfa
            self.end_t = None
            self.rdt = 1.0 / 30
            si = cfg["si"]
            self.bgc = Solid(ES_STAGES[si][1])
            self.neb = Transform(self.I("neb%d" % cfg["neb"]), zoom=2.0)
            self.pidx, self.pcx, self.pcy, self.pzoom = cfg["planet"]
            self.pulse = cfg.get("pulse", False)
            self.star_s = self.I("star2")
            self.star_b = self.I("star1")
            sk = persistent._es_skin
            if sk < 0 or sk >= len(ES_SKINS) or not es_skin_unlocked(sk):
                sk = 0
            self.i_player = self.I("player" + ("" if sk == 0 else "_%d" % sk))
            self.black = [Solid("#000000%02x" % int(255 * i / 10.0)) for i in range(11)]
            self.nz = [Solid("#ffffff%02x" % a, xysize=(w, h))
                       for a in (20, 36, 54) for (w, h) in ((2, 2), (3, 2), (4, 3), (6, 2))]
            self.glitch = [Solid("#ffffff18", xysize=(w, 3)) for w in (160, 320, 520, 760)]

            rnd = random.Random(21)
            self.stars = []
            for (sp, k, n) in ((10, 0, 40), (26, 0, 26), (58, 1, 12)):
                for _i in range(n):
                    self.stars.append((rnd.uniform(0, ES_W), rnd.uniform(0, ES_H),
                                       sp, k, rnd.uniform(0, 6)))
            # asteroides
            self.rock_list = []
            for _i in range(18):
                z = rnd.choice((0.8, 1.2, 1.7, 2.4))
                self.rock_list.append((rnd.uniform(0, ES_W + 240), rnd.uniform(0, ES_H + 240),
                                       -rnd.uniform(25, 60) * (0.6 + z * 0.4),
                                       rnd.uniform(35, 80) * (0.6 + z * 0.4), z))
            # chispas de la tormenta solar
            self.spark_list = [(rnd.uniform(20, ES_W - 20), rnd.uniform(40, 150), rnd.uniform(0, 3.0))
                               for _i in range(16)]
            # copos de hielo
            self.flakes = [(rnd.uniform(0, ES_W), rnd.uniform(0, ES_H), rnd.uniform(18, 70),
                            rnd.uniform(0, 6.28), rnd.randint(0, 1)) for _i in range(44)]
            # edificios de la base enemiga
            self.towers = []
            x = -10
            while x < ES_W:
                w = rnd.choice((46, 62, 80, 54, 96))
                h = rnd.choice((50, 78, 110, 140, 90))
                wins = [(rnd.randint(4, max(5, w - 12)), rnd.randint(8, max(9, h - 14)),
                         rnd.uniform(0, 6.0)) for _i in range(5)]
                self.towers.append((x, w, h, wins, rnd.random() < 0.35))
                x += w + rnd.choice((6, 10, 18))
            # radar
            rd = cfg.get("radar")
            if rd:
                (rcx, rcy, rr) = rd
                self.rd = rd
                self.rd_dots = []
                for fr in (0.34, 0.67, 1.0):
                    for j in range(16):
                        a = j * (2 * math.pi / 16)
                        self.rd_dots.append((rr * fr * math.cos(a), rr * fr * math.sin(a)))
                for d in range(25, int(rr), 25):
                    self.rd_dots += [(d, 0), (-d, 0), (0, d), (0, -d)]
                self.blips = [(rnd.uniform(0.3, 0.9) * rr, rnd.uniform(0, 6.28)) for _i in range(6)]
            # fuegos artificiales
            self.fire_cols = ["#ffd24d", "#ff7aa8", "#9fe8ff", "#9bffb0", "#c79bff"]
            # textos
            O = [(2, "#000000", 0, 0)]
            self.t_cap1 = Text(cfg["label"], size=22, color="#9bffb0", outlines=O)
            self.t_cap2 = Text(cfg["place"], size=36, color="#ffe680", outlines=[(3, "#000000", 0, 0)])
            self.t_link = Text(u"ENLACE DE RADIO", size=20, color="#9bffb0")
            self.t_sig = Text(u"SEÑAL", size=18, color="#a8b8e0")
            self.t_alert = Text(u"¡ALERTA!", size=56, color="#ff4455", outlines=[(3, "#000000", 0, 0)])
            self.alert_on = "alarm" in self.fx

        # ---------- utilidades ----------
        def I(self, n):
            return renpy.displayable(ES_IMG + "es_" + n + ".png")

        def solid(self, color, w, h):
            key = (color, int(w), int(h))
            s = self.sc.get(key)
            if s is None:
                s = Solid(color, xysize=(int(w), int(h)))
                self.sc[key] = s
            return s

        def ov(self, color, a):
            """Capa de color a pantalla completa con transparencia."""
            a = max(0.0, min(0.9, a))
            q = int(a * 50)
            key = (color, q, "ov")
            s = self.sc.get(key)
            if s is None:
                s = Solid("%s%02x" % (color, int(255 * q / 50.0)))
                self.sc[key] = s
            return s

        def zimg(self, name, z, alpha=1.0):
            key = (name, int(z * 40 + 0.5), int(alpha * 10 + 0.5))
            d = self.zc.get(key)
            if d is None:
                d = Transform(self.I(name), zoom=key[1] / 40.0, alpha=key[2] / 10.0)
                self.zc[key] = d
            return d

        def atext(self, name, txt, a):
            key = (name, int(max(0.0, min(1.0, a)) * 10 + 0.5))
            d = self.tc.get(key)
            if d is None:
                d = Transform(txt, alpha=key[1] / 10.0)
                self.tc[key] = d
            return d

        def beat(self, t):
            s = math.sin(t * 3.4)
            s2 = math.sin(t * 3.4 - 0.9)
            return (max(0.0, s) ** 6) + 0.6 * (max(0.0, s2) ** 6)

        # ---------- capas de efectos ----------
        def fx_ship(self, r, t, P, PC):
            sx, sy = self.cfg.get("ship", (640, 420))
            k = es_ease(t / 2.4)
            y = sy + 330.0 * (1.0 - k) * (1.0 - k) + 7.0 * math.sin(t * 1.3)
            x = sx + 12.0 * math.sin(t * 0.9)
            fl = int(t * 26) % 2
            PC(self.solid("#ff9a2e", 10, 18 + 10 * fl), x, y + 28 + 9 + 5 * fl)
            PC(self.solid("#fff3b0", 4, 10 + 6 * fl), x, y + 28 + 5 + 3 * fl)
            PC(self.i_player, x, y)

        def fx_shadow(self, r, t, P, PC):
            PC(self.zimg("boss7", 3.4, 0.28), 1380 - 38.0 * t, 150 + 8.0 * math.sin(t * 0.4))
            for (gx, gy, sp) in ((1500, 250, 55), (1700, 330, 48), (1900, 200, 62)):
                PC(self.zimg("enemy1", 1.0, 0.25), gx - sp * t, gy + 10.0 * math.sin(t * 0.8 + gx))

        def fx_rocks(self, r, t, P, PC):
            for (x0, y0, vx, vy, z) in self.rock_list:
                x = (x0 + vx * t) % (ES_W + 240) - 120
                y = (y0 + vy * t) % (ES_H + 240) - 120
                PC(self.zimg("rock", z, 1.0), x, y)

        def fx_foes(self, r, t, P, PC):
            for (kind, cx, cy, amp, sp, ph, z, a) in self.cfg.get("foes", ()):
                PC(self.zimg("enemy%d" % (kind + 1), z, a),
                   cx + amp * math.sin(t * sp + ph), cy + 10.0 * math.sin(t * sp * 1.7 + ph))

        def fx_flares(self, r, t, P, PC):
            a = 0.10 + 0.07 * math.sin(t * 1.1) + (0.08 if int(t * 2.5) % 5 == 0 else 0.0)
            P(self.ov("#ff8a1e", a), 0, 0)
            for (x0, sp, ph) in self.spark_list:
                y = (ES_H + 40) - ((t * sp * 60.0 + ph * 300.0) % (ES_H + 80))
                x = x0 + 24.0 * math.sin(t * 1.2 + ph)
                if int(t * 6 + ph * 10) % 3:
                    P(self.solid("#ffd84d", 6, 6), x, y)
                else:
                    P(self.solid("#fff3b0", 4, 4), x, y)

        def fx_snow(self, r, t, P, PC):
            P(self.ov("#6fd3ff", 0.07), 0, 0)
            for (x0, y0, sp, ph, big) in self.flakes:
                y = (y0 + sp * t) % (ES_H + 20) - 10
                x = x0 + 30.0 * math.sin(t * 0.7 + ph)
                P(self.star_b if big else self.star_s, x, y)

        def fx_radar(self, r, t, P, PC):
            (cx, cy, rr) = self.rd
            P(self.solid("#07202ecc", 2 * rr + 24, 2 * rr + 24), cx - rr - 12, cy - rr - 12)
            for (dx, dy) in self.rd_dots:
                P(self.solid("#2f8f9f", 3, 3), cx + dx - 1, cy + dy - 1)
            ang = (t * 1.6) % (2 * math.pi)
            for (back, col) in ((0.0, "#7fffd4ff"), (0.14, "#7fffd490"), (0.28, "#7fffd450")):
                a = ang - back
                for i in range(1, 13):
                    d = rr * i / 12.0
                    P(self.solid(col, 4, 4), cx + d * math.cos(a) - 2, cy + d * math.sin(a) - 2)
            for (d, th) in self.blips:
                age = (ang - th) % (2 * math.pi)
                a = 1.0 - age / 3.2
                if a > 0.1:
                    PC(self.zimg("enemy1", 0.5, a), cx + d * math.cos(th), cy + d * math.sin(th))

        def fx_alarm(self, r, t, P, PC):
            P(self.ov("#ff1030", 0.04 + 0.12 * (0.5 + 0.5 * math.sin(t * 5.0))), 0, 0)
            if int(t * 2.5) % 2 == 0:
                PC(self.t_alert, ES_W / 2.0, 110)

        def fx_boss(self, r, t, P, PC):
            (idx, cx, cy, z0, z1, a) = self.cfg["boss"]
            z = z0 + (z1 - z0) * es_ease(t / 14.0)
            PC(self.zimg("boss%d" % idx, z, a), cx + 10.0 * math.sin(t * 0.5),
               cy + 6.0 * math.sin(t * 0.8))

        def fx_skyline(self, r, t, P, PC):
            base = 500
            for (x, w, h, wins, red) in self.towers:
                P(self.solid("#0a1018", w, h), x, base - h)
                P(self.solid("#142231", w, 4), x, base - h)
                for (wx, wy, ph) in wins:
                    if int(t * 1.5 + ph) % 4 != 0:
                        P(self.solid("#ffcf6a", 4, 6), x + wx, base - h + wy)
                if red and int(t * 1.2 + x) % 2 == 0:
                    P(self.solid("#ff4455", 5, 5), x + w / 2 - 2, base - h - 7)
            P(self.solid("#0a1018", ES_W, 40), 0, base)

        def fx_dawn(self, r, t, P, PC):
            k = es_ease(t / 12.0)
            P(self.ov("#ff7a3a", 0.28 * k), 0, 0)
            # franjas de luz cerca del horizonte
            for i in range(5):
                a8 = int(255 * (0.05 + 0.05 * i) * k) // 8 * 8
                P(self.solid("#ffb25a%02x" % a8, ES_W, 44), 0, 280 + i * 44)
            cx = 640
            cy = 650 - 260 * k
            for (R, col) in ((150, "#ff9a3a30"), (100, "#ffb84a"), (62, "#fff0b0")):
                for dy in range(-R, R, 8):
                    hw = int(math.sqrt(max(0.0, R * R - (dy + 4) * (dy + 4))))
                    if hw > 0:
                        P(self.solid(col, 2 * hw, 8), cx - hw, cy + dy)

        def fx_fire(self, r, t, P, PC):
            if t < 5.0:
                return
            for i in range(4):
                c = t - 5.0 + i * 0.55
                cyc = int(c / 2.2)
                age = c - cyc * 2.2
                rnd = random.Random(cyc * 13 + i * 7)
                cx = rnd.uniform(160, 1120)
                cy = rnd.uniform(110, 300)
                col = rnd.choice(self.fire_cols)
                angs = [j * 0.628 + rnd.uniform(-0.15, 0.15) for j in range(10)]
                if age < 0.36:
                    f = min(3, int(age / 0.09))
                    PC(self.zimg("boom%d" % f, 2.0 + age * 3.0, 1.0), cx, cy)
                elif age < 1.7:
                    a = age - 0.36
                    d = 140.0 * (1.0 - math.exp(-a * 2.2))
                    fall = 70.0 * a * a
                    s = self.solid(col, 6, 6) if a < 1.0 else self.solid(col, 4, 4)
                    for ang in angs:
                        P(s, cx + d * math.cos(ang), cy + d * math.sin(ang) + fall)

        # ---------- ruido de radio y HUD ----------
        def noise_layer(self, r, t, P):
            lv = ES_ST["noise"] + (0.06 if ES_ST["talk"] else 0.0)
            n = int(6 + 70 * lv)
            rnd = random.Random(int(t * 15))
            for _i in range(n):
                P(rnd.choice(self.nz), rnd.uniform(0, ES_W), rnd.uniform(0, ES_H))
            if lv > 0.3:
                for _i in range(1 + int(lv * 4)):
                    if rnd.random() < lv:
                        P(rnd.choice(self.glitch), rnd.uniform(0, ES_W - 200), rnd.uniform(60, ES_H - 40))
            return lv

        def render(self, width, height, st, at):
            t = st
            r = renpy.Render(ES_W, ES_H)

            def P(d, x, y):
                r.blit(renpy.render(d, ES_W, ES_H, st, at), (int(x), int(y)))

            def PC(d, cx, cy):
                rr = renpy.render(d, ES_W, ES_H, st, at)
                w, h = rr.get_size()
                r.blit(rr, (int(cx - w / 2.0), int(cy - h / 2.0)))

            P(self.bgc, 0, 0)
            ny = (t * 9.0) % ES_H
            P(self.neb, 0, ny)
            P(self.neb, 0, ny - ES_H)
            if "dawn" in self.fx:
                self.fx_dawn(r, t, P, PC)
            z = self.pzoom * (1.0 + (0.07 * self.beat(t) if self.pulse else 0.0))
            PC(self.zimg("planet%d" % self.pidx, z, 1.0), self.pcx, self.pcy + 8.0 * math.sin(t * 0.5))
            for (x, y0, sp, k, ph) in self.stars:
                if int((t + ph) * 1.6) % 9 == 0:
                    continue
                P(self.star_s if k == 0 else self.star_b, x, (y0 + sp * t) % ES_H)
            if self.pulse:
                P(self.ov("#b06bff", 0.03 + 0.07 * self.beat(t)), 0, 0)
            for name in self.fx:
                if name != "dawn":
                    getattr(self, "fx_" + name)(r, t, P, PC)

            lv = self.noise_layer(r, t, P)

            # barra superior de la radio
            k = es_ease(t / 0.8)
            by = int(-56 * (1.0 - k))
            P(self.solid("#000000", ES_W, 56), 0, by)
            P(self.solid("#9bffb044", ES_W, 2), 0, by + 56)
            if int(t * 1.6) % 2 == 0:
                P(self.solid("#ff4455", 10, 10), 24, by + 23)
            P(self.t_link, 44, by + 16)
            P(self.t_sig, 1090, by + 18)
            lit = 5 - int(lv * 5.5) + (1 if int(t * 7) % 5 == 0 else 0)
            for i in range(5):
                h = 8 + 5 * i
                col = "#9bffb0" if i < lit else "#2a3a4a"
                P(self.solid(col, 8, h), 1160 + i * 13, by + 42 - h)

            # título del capítulo
            a = min(1.0, max(0.0, (t - 0.7) / 0.5)) * min(1.0, max(0.0, (5.2 - t) / 0.6))
            if a > 0.05:
                PC(self.atext("c1", self.t_cap1, a), ES_W / 2.0, 82)
                PC(self.atext("c2", self.t_cap2, a), ES_W / 2.0, 116)

            # entrada y salida en negro
            fa = 0.0
            if t < 1.1:
                fa = 1.0 - es_ease((t - 0.15) / 0.95)
            if ES_ST["end"]:
                if self.end_t is None:
                    self.end_t = t
                fa = max(fa, es_ease((t - self.end_t) / 0.9))
            if fa > 0.02:
                P(self.black[min(10, int(fa * 10 + 0.5))], 0, 0)

            renpy.redraw(self, self.rdt)
            return r

        def visit(self):
            return [self.neb, self.i_player, self.star_s, self.star_b]

    # ------------------------------------------------------------
    #  Escena completa: fondo animado + cuadro de radio con los dialogos.
    #  Todo vive en UN displayable y los toques los recibe event() (igual que
    #  el juego), asi avanzar el dialogo no depende del sistema "say" de
    #  Ren'Py/MAS, que se bloquea con otras pantallas.
    # ------------------------------------------------------------
    class EsStoryScene(EsStoryBG):

        INTRO = 1.3          # segundos de fondo antes del primer dialogo
        CPS = 42.0           # letras por segundo
        BOX_X = 50
        BOX_Y = 516
        BOX_W = 1180
        BOX_H = 188
        TXT_W = 1040         # ancho maximo del texto
        OUT = 0.95           # duracion del fundido final

        def __init__(self, sid, **kwargs):
            super(EsStoryScene, self).__init__(sid, **kwargs)
            self.rdt = 1.0 / 20          # la escena es calmada: 20 cuadros bastan
            self.L = list(ES_ST["lines"])
            self.i = -1
            self.who = "n"
            self.rows = []
            self.full = 0
            self.typed = 0
            self.line_t = 0.0
            self.stage = "intro"         # intro / talk / outro / done
            self.end_st = None
            self.skip_t = None           # toque de "Saltar" pendiente de confirmar
            self.pending_skip = False
            self.wc = {}                 # ancho de cada palabra
            self.pc = {}                 # fragmentos de texto ya creados
            self.sp = None
            self.who_t = {}
            self.t_skip = self.tx(u"Saltar >>", 26, "#cfe0ff")
            self.t_skip2 = self.tx(u"¿Saltar? Toca otra vez", 26, "#ffe680")
            self.t_next = self.tx(u">", 30, "#9bffb0")

        # ---------- textos ----------
        def tx(self, s, size, color, bold=False, italic=False):
            return Text(s.replace("{", "{{"), size=size, color=color, bold=bold, italic=italic,
                        outlines=[(2, "#000000a0", 0, 0)], substitute=False)

        def wid(self, wd):
            w = self.wc.get(wd)
            if w is None:
                try:
                    w = renpy.render(self.tx(wd, 28, "#ffffff"), 4000, 200, 0, 0).get_size()[0]
                except Exception:
                    w = 14.0 * len(wd)
                self.wc[wd] = w
            return w

        def wrap(self, s):
            if self.sp is None:
                self.sp = max(4.0, self.wid(u"a a") - 2 * self.wid(u"a"))
            rows = []
            cur = []
            cw = 0.0
            for wd in s.split(u" "):
                ww = self.wid(wd)
                add = ww if not cur else self.sp + ww
                if cur and cw + add > self.TXT_W:
                    rows.append(u" ".join(cur))
                    cur = [wd]
                    cw = ww
                else:
                    cur.append(wd)
                    cw += add
            if cur:
                rows.append(u" ".join(cur))
            if len(rows) > 3:
                rows = rows[:2] + [u" ".join(rows[2:])]
            return rows

        # ---------- sonido ----------
        def snd(self, name, ch):
            try:
                renpy.music.play(ES_SND + name, channel=ch)
            except Exception:
                pass

        def talk_on(self):
            ES_ST["talk"] = True
            if self.who != "n":
                try:
                    renpy.music.play(ES_SND + ("radio_talk.ogg" if self.who == "m" else "radio_talk2.ogg"),
                                     channel="es_talk", loop=True)
                except Exception:
                    pass

        def talk_off(self):
            ES_ST["talk"] = False
            try:
                renpy.music.stop(channel="es_talk", fadeout=0.08)
            except Exception:
                pass

        # ---------- lineas ----------
        def start_line(self, st):
            self.i += 1
            who, text, noise = self.L[self.i]
            self.who = who
            ES_ST["noise"] = noise
            self.rows = self.wrap(es_sub(text))
            self.full = sum(len(r) for r in self.rows) + len(self.rows) - 1
            self.typed = 0
            self.line_t = st
            self.pc = {}
            self.stage = "talk"
            if noise >= 0.5:
                self.snd("radio_crackle.ogg", "es_sfx3")
            self.snd("beep.ogg" if who == "n" else "radio_open.ogg", "es_sfx")
            self.talk_on()

        def next_line(self, st):
            who = self.who
            nxt = self.L[self.i + 1][0] if self.i + 1 < len(self.L) else None
            if who != "n" and nxt != who:
                self.snd("radio_close.ogg", "es_sfx2")
            if self.i + 1 < len(self.L):
                self.start_line(st)
            else:
                self.finish(st)

        def finish(self, st):
            self.talk_off()
            self.stage = "outro"
            self.end_st = st
            ES_ST["end"] = True

        def do_skip(self, st):
            if self.stage in ("outro", "done"):
                return
            ES_ST["skip"] = True
            self.finish(st)

        def back(self):
            """Boton atras de Android: salta la escena."""
            self.pending_skip = True
            renpy.redraw(self, 0)

        def tap(self, st):
            if self.stage != "talk":
                return
            if self.typed < self.full:
                self.typed = self.full          # primer toque: termina de escribir
                self.talk_off()
            else:
                self.next_line(st)

        # ---------- entrada ----------
        def event(self, ev, x, y, st):
            if self.stage in ("outro", "done"):
                return None
            if ev.type == es_pygame.MOUSEBUTTONUP:
                if x >= 1060 and 58 <= y <= 124:
                    if self.skip_t is not None and st - self.skip_t < 2.5:
                        self.do_skip(st)
                    else:
                        self.skip_t = st
                else:
                    self.tap(st)
                renpy.redraw(self, 0)
            elif ev.type == es_pygame.KEYDOWN and getattr(ev, "key", None) in (13, 32, 271):
                self.tap(st)
                renpy.redraw(self, 0)
            return None

        # ---------- dibujo ----------
        def render(self, width, height, st, at):
            if self.stage == "intro" and st >= self.INTRO and not self.pending_skip:
                self.start_line(st)
            if self.pending_skip:
                self.pending_skip = False
                self.do_skip(st)
            if self.stage == "talk" and self.typed < self.full:
                k = int((st - self.line_t) * self.CPS)
                k = (k // 2) * 2
                if k >= self.full - 1:
                    k = self.full
                if k > self.typed:
                    self.typed = k
                if self.typed >= self.full:
                    self.talk_off()
            r = super(EsStoryScene, self).render(width, height, st, at)
            if self.stage == "talk":
                self.draw_box(r, st, at)
            if self.stage != "done" and self.stage != "intro":
                if self.skip_t is not None and st - self.skip_t >= 2.5:
                    self.skip_t = None
                armed = self.skip_t is not None
                r.blit(renpy.render(self.t_skip2 if armed else self.t_skip, 400, 60, st, at),
                       (1250 - (250 if armed else 130), 72))
            if self.stage == "outro" and st - self.end_st >= self.OUT + 0.05:
                self.stage = "done"
                renpy.end_interaction(True)
            return r

        def draw_box(self, r, st, at):
            def put(d, x, y, w=1280, h=720):
                r.blit(renpy.render(d, w, h, st, at), (x, y))
            bx, by = self.BOX_X, self.BOX_Y
            put(self.solid("#050a14ea", self.BOX_W, self.BOX_H), bx, by, self.BOX_W, self.BOX_H)
            put(self.solid("#9bffb044", self.BOX_W, 2), bx, by, self.BOX_W, 2)
            # barritas de la "voz"
            talking = ES_ST["talk"] and self.typed < self.full
            for n in range(5):
                if talking:
                    h = 4 + int(14 * abs(math.sin(st * 9.0 + n * 1.3)))
                else:
                    h = 4
                put(self.solid("#9bffb0", 5, h), bx + 30 + n * 9, by + 28 - h // 2, 5, h)
            if self.who != "n":
                wt = self.who_t.get(self.who)
                if wt is None:
                    nm = u"Monika · Control de Misión" if self.who == "m" else es_sub(u"[player] · Piloto")
                    wt = self.tx(nm, 24, "#9bffb0" if self.who == "m" else "#9fe8ff", bold=True)
                    self.who_t[self.who] = wt
                put(wt, bx + 92, by + 14, 600, 40)
            col = {"m": "#e8fff0", "p": "#e0f4ff"}.get(self.who, "#ffe680")
            remaining = self.typed
            for idx in range(len(self.rows)):
                row = self.rows[idx]
                take = min(len(row), remaining)
                if take <= 0:
                    break
                key = (idx, take)
                t = self.pc.get(key)
                if t is None:
                    t = self.tx(row[:take], 28, col, italic=(self.who == "n"))
                    self.pc[key] = t
                put(t, bx + 30, by + 58 + idx * 38, self.TXT_W + 80, 40)
                remaining -= len(row) + 1
            if self.typed >= self.full and int(st * 1.6) % 2 == 0:
                put(self.t_next, bx + self.BOX_W - 44, by + self.BOX_H - 48, 40, 40)


    # ------------------------------------------------------------
    #  Corre la partida. En el modo Historia intercala las escenas de radio:
    #  prólogo al empezar, una escena en la pantalla negra de cada salto
    #  hiperespacial y el epílogo al ganar.
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    #  Contextos limpios: la sala de MAS (con Monika) sigue dibujandose
    #  escondida detras de nuestras pantallas y eso gasta mucha GPU en el
    #  celular. Dentro de un contexto nuevo la capa "master" se vacia
    #  (solo en ese contexto) y al volver la sala sigue intacta.
    # ------------------------------------------------------------
    ES_CTX = {"rv": None, "game": None, "scene": None}

    def es_ui(name, *args):
        ES_CTX["rv"] = None
        renpy.call_in_new_context("es_ctx_screen", name, args)
        return ES_CTX["rv"]

    def es_story_show(sid, replay=False):
        es_story_begin(sid, replay)
        try:
            ES_CTX["scene"] = EsStoryScene(sid)
            renpy.call_in_new_context("es_ctx_scene")
        finally:
            ES_CTX["scene"] = None
            es_story_end()

    def es_run_game_core(mode, diff, pstage):
        game = EncodersShooter(mode, diff, pstage)
        if mode != "story":
            return renpy.call_screen("encoders_shooter_screen", game)
        es_story_show("s0", False)
        renpy.music.play(es_track("stage"), channel="es_music", loop=True, fadein=0.5)
        rv = None
        while True:
            rv = renpy.call_screen("encoders_shooter_screen", game)
            if isinstance(rv, tuple) and len(rv) == 2 and rv[0] == "story":
                # el juego pide una escena (estamos en la pantalla negra del salto)
                renpy.music.stop(channel="es_music", fadeout=0.3)
                es_story_show(rv[1], False)
                game.story_resume()      # al reanudar, start_stage vuelve a poner la musica
                continue
            break
        try:
            if rv["win"] and not rv["quit"]:
                es_story_show("s8", False)
        except Exception:
            pass
        return rv

    # ------------------------------------------------------------
    #  Video al perder (video/gameover.webm). Se reproduce a pantalla
    #  completa y se salta con un toque. No sale al salir de la partida,
    #  al ganar ni en el modo práctica.
    # ------------------------------------------------------------
    ES_GO_VIDEO = "Submods/Navecitas/video/gameover.webm"

    def es_gameover_video(sm):
        if not persistent._es_go_video:
            return
        if sm["win"] or sm["quit"] or sm["mode"] == "practice":
            return
        if not renpy.loadable(ES_GO_VIDEO):
            return
        # la musica de Monika sigue en pausa y la del juego ya se apagó
        renpy.movie_cutscene(ES_GO_VIDEO, stop_music=False)

    def es_fail_card(sm):
        """Tarjeta oscura de derrota: nivel, lugar y quien te detuvo."""
        if sm["win"] or sm["quit"] or sm["mode"] == "practice":
            return
        if not persistent._es_go_video:
            return
        stage = sm["stage"]
        place = ES_STAGES[(stage - 1) % ES_NST][0]
        who = sm.get("fail_who") or u"la oleada de enemigos"
        renpy.call_screen("es_fail_card", stage, place, who, sm["score"])
        # del negro de la tarjeta de vuelta al menu con un fundido suave
        renpy.transition(Dissolve(0.8))

    def es_run_game_inner(mode, diff, pstage):
        rv = es_run_game_core(mode, diff, pstage)
        es_gameover_video(rv)
        es_fail_card(rv)
        return rv

    def es_run_game(mode, diff, pstage):
        ES_CTX["game"] = None
        renpy.call_in_new_context("es_ctx_game", mode, diff, pstage)
        return ES_CTX["game"]

    # personajes de radio (Monika, tú y mensajes del sistema)
    es_radio_m = Character(u"Monika · Control de Misión", screen="es_radio_say",
                           callback=es_cb_m, who_color="#9bffb0", what_color="#e8fff0")
    es_radio_p = Character(u"[player] · Piloto", screen="es_radio_say",
                           callback=es_cb_p, who_color="#9fe8ff", what_color="#e0f4ff")
    es_radio_n = Character(None, screen="es_radio_say",
                           callback=es_cb_n, what_color="#ffe680", what_italic=True)


# ---------------------------------------------------------------
#  Estilos del cuadro de radio
# ---------------------------------------------------------------
style es_say_who is default:
    size 24
    bold True
    color "#9bffb0"
    outlines [(2, "#000000a0", 0, 0)]
style es_say_what is default:
    size 28
    color "#e8fff0"
    outlines [(2, "#000000a0", 0, 0)]
    slow_cps 45

transform es_card_fade(d):
    alpha 0.0
    pause d
    linear 0.7 alpha 1.0

transform es_card_black:
    alpha 0.0
    linear 0.6 alpha 1.0

transform es_blink:
    alpha 1.0
    pause 0.5
    alpha 0.25
    pause 0.5
    repeat


# ---------------------------------------------------------------
#  Pantallas
# ---------------------------------------------------------------

# fondo animado (se muestra con "show screen")
screen es_story_bg(sid):
    zorder 200
    default bg = EsStoryBG(sid)
    add bg

# escena de radio: fondo + dialogos en un solo displayable (los toques los maneja event)
screen es_story_scene(scene):
    modal True
    zorder 200
    add Solid("#000000")
    add scene
    key ES_BACK_KEY action Function(scene.back)
    key "game_menu" action Function(scene.back)

# cuadro de diálogo de radio (ya no se usa; se conserva por compatibilidad)
screen es_radio_say(who, what, **kwargs):
    zorder 205
    key "game_menu" action [Function(es_story_skip), Return(True)]
    key ES_BACK_KEY action [Function(es_story_skip), Return(True)]

    textbutton u"Saltar >>":
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 66
        text_size 26
        text_color "#cfe0ff"
        text_hover_color "#ffe680"
        text_outlines [(2, "#000000", 0, 0)]
        action [Function(es_story_skip), Return(True)]

    frame:
        background Solid("#050a14ea")
        xalign 0.5
        yalign 1.0
        yoffset -16
        xsize 1180
        ysize 188
        padding (30, 14, 30, 12)
        vbox:
            spacing 4
            hbox:
                spacing 14
                yminimum 34
                add EsWave() yalign 0.5
                if who:
                    text who id "who" style "es_say_who" yalign 0.5
            text what id "what" style "es_say_what"
        text u">" size 30 color "#9bffb0" xalign 1.0 yalign 1.0 at es_blink

# tarjeta oscura de derrota (despues del video): donde caiste, y vuelta al menu
screen es_fail_card(stage, place, who, score):
    modal True
    zorder 210
    default leaving = False
    add Solid("#000000")
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 14
        text u"DERROTA" size 84 color "#ff6688" outlines [(3, "#000000", 0, 0)] xalign 0.5 at es_card_fade(0.2)
        text (u"Caíste en el Nivel %d" % stage) size 40 color "#ffffff" xalign 0.5 at es_card_fade(0.9)
        text place size 34 color "#ffe680" xalign 0.5 at es_card_fade(1.3)
        text (u"Te detuvo " + who) size 30 color "#cfd8f0" xalign 0.5 at es_card_fade(1.8)
        text (u"Puntos: %d" % score) size 30 color "#9bffb0" xalign 0.5 at es_card_fade(2.2)
        text u"Toca para volver al menú" size 26 color "#aaaaaa" xalign 0.5 at es_card_fade(2.8)
    button:
        xfill True
        yfill True
        background None
        action SetScreenVariable("leaving", True)
        null
    key "game_menu" action SetScreenVariable("leaving", True)
    timer 8.0 action SetScreenVariable("leaving", True)
    if leaving:
        add Solid("#000000") at es_card_black
        timer 0.65 action Return(True)

# lista de escenas para volver a verlas
screen es_scenes_screen():
    modal True
    zorder 200

    default bg = EsMenuBG("title")

    add bg
    key "game_menu" action Return(0)

    frame:
        style "es_dk_panel"
        xalign 0.5
        yalign 0.5
        vbox:
            spacing 6
            text u"ESCENAS" style "es_dk_title" xalign 0.5
            text u"Vuelve a ver las escenas de la historia que ya desbloqueaste." style "es_dk_small" xalign 0.5
            viewport:
                xfill True
                ymaximum 360
                draggable True
                mousewheel True
                vbox:
                    spacing 6
                    for sid in ES_STORY_ORDER:
                        textbutton (es_story_btn(sid)):
                            style "es_dk_button"
                            xsize 560
                            xalign 0.5
                            sensitive (sid in persistent._es_story_seen)
                            action Return(sid)
            textbutton u"VOLVER" style "es_dk_button" xalign 0.5 action Return(0)


# ---------------------------------------------------------------
#  Reproduce una escena. Se llama desde el juego o desde el menú.
# ---------------------------------------------------------------
label es_story_play(sid, replay=False):
    $ renpy.block_rollback()
    $ es_story_show(sid, replay)
    return

# contexto limpio (sin la sala de MAS detras) para una escena de radio
label es_ctx_scene:
    $ renpy.scene()
    call screen es_story_scene(ES_CTX["scene"])
    return

# contexto limpio para mostrar una pantalla del menu de Navecitas
label es_ctx_screen(name, args):
    $ renpy.scene()
    $ ES_CTX["rv"] = renpy.call_screen(name, *args)
    return

# contexto limpio para toda la partida
label es_ctx_game(mode, diff, pstage):
    $ renpy.scene()
    $ ES_CTX["game"] = es_run_game_inner(mode, diff, pstage)
    return
