# ---------------------------------------------------------------
#  Navecitas - menu de inicio, fondos tematicos y musica de menu
#
#  MUSICA PROPIA DEL MENU: pon audio/custom_menu.ogg (o .mp3/.opus)
#  y se usara en lugar de menu.ogg.
# ---------------------------------------------------------------

init 12 python:
    import time

    ES_T0 = time.time()

    # frases que salen en la esquina del menu de inicio
    ES_TIPS = [
        u"Solo cuenta como golpe el puntito del centro de tu nave.",
        u"Rozar las balas da puntos extra. ¡Atrévete!",
        u"Las monedas del nivel bonus valen mucho en la tienda.",
        u"En cooperativo, Monika te cubre un golpe por nivel.",
        u"Un combo alto multiplica tus puntos hasta x3.",
        u"Toca dos veces la pantalla para lanzar una bomba.",
        u"Los jefes cambian de ataque cuando les queda la mitad de la vida.",
        u"A mitad de cada nivel aparece un mini-jefe con ataques propios.",
        u"Los francotiradores apuntan a tu nave: no te quedes quieto.",
        u"Los cargueros sueltan dos enemigos al romperse.",
        u"En el modo Historia, Monika te guía por radio entre niveles.",
        u"Tras cada jefe tu nave da un salto hiperespacial al siguiente nivel.",
        u"Cada nave que desbloqueas tiene una habilidad propia.",
        u"El modo práctica es ideal para aprender los patrones de un jefe.",
    ]

    # temas de fondo: nebulosa, planeta (indice, centro x, centro y, zoom) y extras animados
    ES_MENU_THEMES = {
        "title":    {"bg": "#05051a", "neb": 6, "planet": (0, 120, 700, 2.4), "extras": "fleet"},
        "shop":     {"bg": "#0b0612", "neb": 4, "planet": (4, 1090, 170, 1.5), "extras": "coins"},
        "settings": {"bg": "#050a1c", "neb": 5, "planet": (5, 1040, 610, 1.7), "extras": "gears"},
        "stats":    {"bg": "#060a14", "neb": 3, "planet": (3, 1110, 520, 1.7), "extras": "none"},
    }

    # enemigos "de adorno" del menu de inicio: carril x, desfase, tipo, amplitud
    ES_FLEET = [
        (330.0, 0.0, 0, 130.0),
        (330.0, 3.4, 1, 110.0),
        (480.0, 1.6, 0, 120.0),
        (480.0, 4.9, 2, 100.0),
    ]

    def es_menu_tip():
        return random.choice(ES_TIPS)

    # ---------- musica del menu ----------
    def es_menu_music():
        """Pausa la musica de MAS y arranca la del menu (si no esta ya sonando)."""
        es_apply_volumes()
        try:
            renpy.music.set_pause(True, channel="music")
        except Exception:
            pass
        p = es_track("menu")
        try:
            cur = renpy.music.get_playing(channel="es_music")
        except Exception:
            cur = None
        if cur != p:
            renpy.music.set_pause(False, channel="es_music")
            renpy.music.play(p, channel="es_music", loop=True, fadein=0.8)

    def es_menu_music_stop():
        """Apaga la musica del menu y devuelve la de MAS."""
        try:
            renpy.music.set_pause(False, channel="es_music")
            renpy.music.stop(channel="es_music", fadeout=0.6)
        except Exception:
            pass
        try:
            renpy.music.set_pause(False, channel="music")
        except Exception:
            pass

    # ---------- fondo animado (solo depende del reloj: no guarda estado) ----------
    class EsMenuBG(renpy.Displayable):

        def __init__(self, theme="title", **kwargs):
            super(EsMenuBG, self).__init__(**kwargs)
            cfg = ES_MENU_THEMES.get(theme, ES_MENU_THEMES["title"])
            self.extras = cfg["extras"]
            I = lambda n: renpy.displayable(ES_IMG + "es_" + n + ".png")
            self.bgc = Solid(cfg["bg"])
            self.neb = Transform(I("neb%d" % cfg["neb"]), zoom=2.0)
            pi, self.pcx, self.pcy, pz = cfg["planet"]
            self.planet = Transform(I("planet%d" % pi), zoom=pz)
            self.star_s = I("star2")     # 2x2
            self.star_b = I("star1")     # 4x4
            rnd = random.Random(11)
            self.stars = []
            for (sp, k, n) in ((12, 0, 34), (30, 0, 22), (64, 1, 12)):
                for _i in range(n):
                    self.stars.append((rnd.uniform(0, ES_W), rnd.uniform(0, ES_H),
                                       sp, k, rnd.uniform(0, 6)))
            self.vis = [self.neb, self.planet, self.star_s, self.star_b]

            sk = persistent._es_skin
            if sk < 0 or sk >= len(ES_SKINS) or not es_skin_unlocked(sk):
                sk = 0
            sfx = "" if sk == 0 else "_%d" % sk
            if self.extras == "fleet":
                self.i_player = I("player" + sfx)
                self.i_bullet = I("bullet" + sfx)
                self.i_monika = I("monika")
                self.i_mbullet = I("bullet_2")
                self.i_en = [I("enemy1"), I("enemy2"), I("enemy3")]
                self.i_boom = [I("boom%d" % i) for i in range(4)]
                self.ghost = [Transform(I("enemy1"), alpha=0.35),
                              Transform(I("enemy3"), alpha=0.35)]
                self.boss = Transform(I("boss7"), zoom=2.2, alpha=0.2)
                self.vis += ([self.i_player, self.i_bullet, self.i_monika, self.i_mbullet,
                              self.boss] + self.i_en + self.i_boom + self.ghost)
            elif self.extras == "coins":
                self.coin = I("coin")
                rc = random.Random(5)
                self.coin_pos = [(rc.uniform(20, ES_W - 60), rc.uniform(0, ES_H + 80),
                                  rc.uniform(28, 85), rc.uniform(0, 6.28))
                                 for _i in range(16)]
                self.vis.append(self.coin)
            elif self.extras == "gears":
                self.gears_s = [I("gear%d" % i) for i in range(9)]
                self.gears_b = [Transform(g, zoom=1.8) for g in self.gears_s]
                self.vis += self.gears_s + self.gears_b

        def render(self, width, height, st, at):
            t = time.time() - ES_T0
            r = renpy.Render(ES_W, ES_H)

            def put(d, x, y):
                r.blit(renpy.render(d, ES_W, ES_H, st, at), (int(x), int(y)))

            def putc(d, cx, cy):
                rr = renpy.render(d, ES_W, ES_H, st, at)
                w, h = rr.get_size()
                r.blit(rr, (int(cx - w / 2.0), int(cy - h / 2.0)))

            put(self.bgc, 0, 0)
            ny = (t * 9.0) % ES_H
            put(self.neb, 0, ny)
            put(self.neb, 0, ny - ES_H)
            putc(self.planet, self.pcx, self.pcy + 8.0 * math.sin(t * 0.5))
            for (x, y0, sp, k, ph) in self.stars:
                if int((t + ph) * 1.6) % 9 == 0:      # parpadeo
                    continue
                put(self.star_s if k == 0 else self.star_b, x, (y0 + sp * t) % ES_H)

            ex = self.extras
            if ex == "fleet":
                # jefe fantasma al fondo y naves enemigas que cruzan
                put(self.boss, 880 + 30.0 * math.sin(t * 0.4), -20 + 10.0 * math.sin(t * 0.6))
                put(self.ghost[0], (t * 40.0) % (ES_W + 240) - 120, 330 + 20.0 * math.sin(t * 1.1))
                put(self.ghost[1], ES_W + 120 - (t * 32.0 + 400) % (ES_W + 240),
                    420 + 24.0 * math.sin(t * 0.9 + 1.0))
                px = 330.0
                mx = 480.0
                py = 500.0 + 8.0 * math.sin(t * 1.3)
                my = 548.0 + 8.0 * math.sin(t * 1.1 + 1.0)
                # disparos (se detienen donde explotan los enemigos)
                for (sx, sy, bimg) in ((px, py, self.i_bullet), (mx, my, self.i_mbullet)):
                    ph = t % 0.24
                    for k in range(8):
                        by = sy - 34 - 680.0 * (ph + k * 0.24)
                        if by < 215:
                            break
                        put(bimg, sx - 3, by)
                for (lane, off, kind, amp) in ES_FLEET:
                    c = (t + off) % 6.5
                    if c < 3.2:
                        k = c / 3.2
                        x = lane + amp * (1 - k) * math.sin(c * 2.4)
                        y = -50.0 + 255.0 * k
                        w, h = ES_ESZ[kind]
                        put(self.i_en[kind], x - w / 2.0, y - h / 2.0)
                    elif c < 3.52:
                        f = min(3, int((c - 3.2) / 0.08))
                        put(self.i_boom[f], lane - 36, 205 - 36)
                put(self.i_player, px - 28, py - 28)
                put(self.i_monika, mx - 28, my - 28)
            elif ex == "coins":
                for (x, y0, sp, ph) in self.coin_pos:
                    y = (y0 + sp * t) % (ES_H + 80) - 40
                    put(self.coin, x + 10.0 * math.sin(t * 1.4 + ph), y)
            elif ex == "gears":
                a = int(((t * 14.0) % 45.0) / 5.0)       # 0..8 (el engranaje se repite cada 45 grados)
                putc(self.gears_b[a], 1130, 130)
                putc(self.gears_s[8 - a], 1005, 236)
                putc(self.gears_s[a], 70, 650)

            renpy.redraw(self, 1.0 / 30)
            return r

        def visit(self):
            return self.vis


# ---------------------------------------------------------------
#  Estilos (oscuros, pixel-art, a juego con el juego)
# ---------------------------------------------------------------
style es_dk_text is default:
    size 24
    color "#e8f0ff"
    outlines [(2, "#000000a0", 0, 0)]
style es_dk_head is es_dk_text:
    size 28
    bold True
    color "#ffe680"
style es_dk_title is es_dk_text:
    size 38
    bold True
    color "#ffe680"
    outlines [(3, "#1b2a6b", 0, 0)]
style es_dk_small is es_dk_text:
    size 20
    color "#a8b8e0"
style es_dk_tip is es_dk_text:
    size 20
    italic True
    color "#cfe0ff"
style es_dk_chiptext is es_dk_text:
    size 21
    color "#ffffff"

style es_dk_panel is default:
    background Frame("Submods/Navecitas/images/es_panel.png", 9, 9, 9, 9)
    padding (26, 18, 26, 18)
style es_dk_chip is default:
    background Frame("Submods/Navecitas/images/es_btn.png", 9, 9, 9, 9)
    padding (16, 6, 16, 6)
style es_dk_cardframe is default:
    background Frame("Submods/Navecitas/images/es_btn.png", 9, 9, 9, 9)
    padding (18, 10, 18, 10)
    xfill True

style es_dk_button is default:
    background Frame("Submods/Navecitas/images/es_btn.png", 9, 9, 9, 9)
    hover_background Frame("Submods/Navecitas/images/es_btn_hover.png", 9, 9, 9, 9)
    insensitive_background Frame("Submods/Navecitas/images/es_btn_off.png", 9, 9, 9, 9)
    selected_idle_background Frame("Submods/Navecitas/images/es_btn_sel.png", 9, 9, 9, 9)
    selected_hover_background Frame("Submods/Navecitas/images/es_btn_sel.png", 9, 9, 9, 9)
    xpadding 22
    ypadding 9
    activate_sound "Submods/Navecitas/audio/click.ogg"
style es_dk_button_text is es_dk_text:
    size 26
    color "#e8f0ff"
    hover_color "#ffffff"
    selected_color "#baffd0"
    insensitive_color "#6a7494"
    xalign 0.5

style es_dk_main_button is es_dk_button:
    xsize 380
    ysize 56
style es_dk_main_button_text is es_dk_button_text:
    yalign 0.5

style es_dk_chipbtn is es_dk_button:
    xpadding 16
    ypadding 5
style es_dk_chipbtn_text is es_dk_button_text:
    size 22

style es_dk_buy is es_dk_button:
    xsize 220
style es_dk_buy_text is es_dk_button_text:
    size 24

style es_dk_card is es_dk_button:
    xfill True
    xpadding 18
    ypadding 3
style es_dk_card_title is es_dk_text:
    size 26
    bold True
    color "#ffe680"
    hover_color "#ffffff"
    insensitive_color "#6a7494"
style es_dk_card_desc is es_dk_text:
    size 19
    color "#b8c8f0"
    hover_color "#e8f0ff"
    insensitive_color "#56607e"

# filas de ajustes (sobre el panel oscuro): sin fondo, con resaltado al tocar
style es_dko_button is default:
    background None
    hover_background Solid("#5fd0ff22")
    xpadding 12
    ypadding 3
    activate_sound "Submods/Navecitas/audio/click.ogg"
style es_dko_button_text is es_dk_text:
    size 23
    hover_color "#ffe680"
    insensitive_color "#6a7494"
style es_dko_text is es_dk_text:
    size 23
style es_dko_small is es_dk_small:
    size 19
    xoffset 12


# ---------------------------------------------------------------
#  Animaciones de entrada
# ---------------------------------------------------------------
transform es_logo_in:
    yoffset -140
    alpha 0.0
    ease 0.9 yoffset 0 alpha 1.0
    block:
        ease 2.2 yoffset 7
        ease 2.2 yoffset -3
        repeat

transform es_fade_in(d=0.0):
    alpha 0.0
    pause d
    ease 0.6 alpha 1.0

transform es_black_out:
    alpha 1.0
    pause 0.25
    ease 1.0 alpha 0.0

transform es_black_in:
    alpha 0.0
    ease 0.8 alpha 1.0

transform es_black_title:
    alpha 0.0
    zoom 1.18
    pause 0.7
    parallel:
        ease 1.0 alpha 1.0
    parallel:
        ease 1.4 zoom 1.0

transform es_slide(d=0.0):
    xoffset 460
    alpha 0.0
    pause d
    ease 0.45 xoffset 0 alpha 1.0


# ---------------------------------------------------------------
#  Menu de inicio
#  Devuelve: story / normal / coop / endless / practice / scenes /
#            shop / stats / options / tutorial / quit
# ---------------------------------------------------------------
screen es_title_screen():
    modal True
    zorder 200

    default panel = "main"
    default bg = EsMenuBG("title")
    default tip = es_menu_tip()
    default fade = es_take_fade()

    add bg
    key "game_menu" action If(panel == "modes", SetScreenVariable("panel", "main"), Return("quit"))

    # logo
    vbox:
        xalign 0.5
        ypos 18
        spacing 2
        add (ES_IMG + "es_logo.png") xalign 0.5 at es_logo_in
        add (ES_IMG + "es_logo_sub.png") xalign 0.5 at es_fade_in(0.9)

    if panel == "main":
        vbox:
            xpos 830
            ypos 235
            spacing 12
            textbutton u"JUGAR" style "es_dk_main_button" action SetScreenVariable("panel", "modes") at es_slide(0.00)
            textbutton u"TIENDA" style "es_dk_main_button" action Return("shop") at es_slide(0.07)
            textbutton u"ESTADÍSTICAS Y LOGROS" style "es_dk_main_button" action Return("stats") at es_slide(0.14)
            textbutton u"AJUSTES" style "es_dk_main_button" action Return("options") at es_slide(0.21)
            textbutton u"CÓMO SE JUEGA" style "es_dk_main_button" action Return("tutorial") at es_slide(0.28)
            textbutton u"SALIR" style "es_dk_main_button" action Return("quit") at es_slide(0.35)
    else:
        frame:
            style "es_dk_panel"
            xpos 690
            ypos 168
            xsize 540
            at es_fade_in(0.0)
            vbox:
                spacing 5
                text u"ELIGE UN MODO" style "es_dk_head" xalign 0.5
                button:
                    style "es_dk_card"
                    action Return("story")
                    vbox:
                        text u"HISTORIA" style "es_dk_card_title"
                        text u"Misión por radio con Monika, con escenas." style "es_dk_card_desc"
                button:
                    style "es_dk_card"
                    action Return("normal")
                    vbox:
                        text u"NORMAL" style "es_dk_card_title"
                        text u"10 niveles, 2 bonus y un jefe final." style "es_dk_card_desc"
                button:
                    style "es_dk_card"
                    action Return("coop")
                    vbox:
                        text u"COOPERATIVO" style "es_dk_card_title"
                        text u"Monika vuela contigo y te cubre." style "es_dk_card_desc"
                button:
                    style "es_dk_card"
                    action Return("endless")
                    sensitive persistent._es_endless
                    vbox:
                        text u"INFINITO" style "es_dk_card_title"
                        text (u"Los niveles no terminan. ¿Hasta dónde llegas?" if persistent._es_endless else u"Bloqueado: gana el juego una vez.") style "es_dk_card_desc"
                button:
                    style "es_dk_card"
                    action Return("practice")
                    sensitive persistent._encoders_best_stage >= 2
                    vbox:
                        text u"PRÁCTICA" style "es_dk_card_title"
                        text (u"Entrena contra los jefes que ya conoces." if persistent._encoders_best_stage >= 2 else u"Bloqueado: llega al nivel 2.") style "es_dk_card_desc"
                hbox:
                    xalign 0.5
                    spacing 8
                    text u"Dificultad:" style "es_dk_text" yalign 0.5
                    for d in ES_DIFF_ORDER:
                        textbutton (ES_DIFFS[d]["name"]) style "es_dk_chipbtn" action SetField(persistent, "_es_diff", d)
                hbox:
                    xalign 0.5
                    spacing 12
                    textbutton u"VOLVER" style "es_dk_button" action SetScreenVariable("panel", "main")
                    textbutton u"ESCENAS" style "es_dk_button" sensitive len(persistent._es_story_seen) > 0 action Return("scenes")

    # datos del jugador
    hbox:
        xpos 24
        ypos 664
        spacing 12
        frame:
            style "es_dk_chip"
            text (u"Récord: %d" % es_record(es_mode_key("normal", persistent._es_diff))) style "es_dk_chiptext"
        frame:
            style "es_dk_chip"
            text (u"Monedas: %d" % persistent._es_coins) style "es_dk_chiptext"
        frame:
            style "es_dk_chip"
            text (u"Logros: %d/%d" % (len(persistent._es_ach), len(ES_ACH))) style "es_dk_chiptext"
    text tip style "es_dk_tip" xalign 1.0 xoffset -24 ypos 686 at es_fade_in(1.2)

    # el menu aparece desde la pantalla negra (solo justo despues de ella)
    if fade:
        add Solid("#000000") at es_black_out


# ---------------------------------------------------------------
#  Pantalla negra al elegir el minijuego: la sala se funde a negro,
#  aparece el logo con un destello y se pasa al menu.
# ---------------------------------------------------------------
init 13 python:
    ES_FADE = {"on": False}

    def es_set_fade():
        ES_FADE["on"] = True

    def es_take_fade():
        v = ES_FADE["on"]
        ES_FADE["on"] = False
        return v

    def es_exit_sfx():
        try:
            es_apply_volumes()
            renpy.music.play(ES_SND + "warp.ogg", channel="es_sfx")
            renpy.music.stop(channel="es_music", fadeout=1.2)
        except Exception:
            pass

    def es_black_sfx():
        try:
            es_apply_volumes()
            renpy.music.play(ES_SND + "warp.ogg", channel="es_sfx")
        except Exception:
            pass

screen es_black_intro():
    modal True
    zorder 300

    add Solid("#000000") at es_black_in
    add (ES_IMG + "es_logo.png") xalign 0.5 yalign 0.45 at es_black_title
    on "show" action Function(es_black_sfx)
    timer 2.6 action [Function(es_set_fade), Return(True)]


# Pantalla negra al salir: el menu se funde a negro y la musica baja
screen es_black_exit():
    modal True
    zorder 300

    add Solid("#000000") at es_black_in
    text u"¡Hasta pronto!" size 44 color "#ffe680" outlines [(3, "#1b2a6b", 0, 0)] xalign 0.5 yalign 0.5 at es_black_title
    on "show" action Function(es_exit_sfx)
    timer 2.0 action Return(True)


# ---------------------------------------------------------------
#  Tienda
# ---------------------------------------------------------------
screen es_shop_screen():
    modal True
    zorder 200

    default bg = EsMenuBG("shop")

    add bg
    key "game_menu" action Return(True)

    frame:
        style "es_dk_panel"
        xalign 0.5
        ypos 16
        xsize 1020
        vbox:
            spacing 8
            fixed:
                xfill True
                ysize 50
                text u"TIENDA ESPACIAL" style "es_dk_title" ypos 2
                hbox:
                    xalign 1.0
                    spacing 8
                    yalign 0.5
                    add (ES_IMG + "es_coin.png") yalign 0.5
                    text (u"%d" % persistent._es_coins) style "es_dk_title" yalign 0.5
            text u"Las monedas se ganan al recogerlas, vencer jefes y ganar partidas." style "es_dk_small"
            viewport:
                xfill True
                ymaximum 440
                draggable True
                mousewheel True
                vbox:
                    spacing 8
                    text u"MEJORAS" style "es_dk_head"
                    for up in ES_UPG:
                        frame:
                            style "es_dk_cardframe"
                            hbox:
                                xfill True
                                vbox:
                                    xsize 720
                                    text (u"%s   (%d/%d)" % (up[1], es_upg(up[0]), len(up[3]))) style "es_dk_head"
                                    text up[2] style "es_dk_small"
                                textbutton (es_upg_btn(up[0])):
                                    style "es_dk_buy"
                                    yalign 0.5
                                    sensitive es_can_buy(up[0])
                                    action Function(es_buy, up[0])
                    text u"NAVES" style "es_dk_head" ypos 6
                    for i in range(len(ES_SKINS)):
                        if es_skin_price(i) is not None:
                            frame:
                                style "es_dk_cardframe"
                                hbox:
                                    xfill True
                                    spacing 14
                                    add (ES_IMG + "es_player_%d.png" % i) yalign 0.5
                                    vbox:
                                        xsize 640
                                        yalign 0.5
                                        text ES_SKINS[i][0] style "es_dk_head"
                                        text ES_SKINS[i][2] style "es_dk_small"
                                    textbutton (es_skin_btn(i)):
                                        style "es_dk_buy"
                                        yalign 0.5
                                        sensitive es_skin_ok(i)
                                        action Function(es_skin_act, i)
            textbutton u"VOLVER" style "es_dk_button" xalign 0.5 action Return(True)


# ---------------------------------------------------------------
#  Ajustes
# ---------------------------------------------------------------
screen es_options_screen():
    modal True
    zorder 200

    default bg = EsMenuBG("settings")

    add bg
    key "game_menu" action Return(True)

    frame:
        style "es_dk_panel"
        xpos 40
        ypos 16
        xsize 880
        vbox:
            spacing 8
            text u"AJUSTES" style "es_dk_title"
            viewport:
                xfill True
                ymaximum 540
                draggable True
                mousewheel True
                use es_opts_body("es_dko")
            textbutton u"VOLVER" style "es_dk_button" xalign 0.5 action Return(True)


# ---------------------------------------------------------------
#  Estadisticas y logros
# ---------------------------------------------------------------
screen es_stats_screen():
    modal True
    zorder 200

    default bg = EsMenuBG("stats")

    add bg
    key "game_menu" action Return(True)

    frame:
        style "es_dk_panel"
        xalign 0.5
        ypos 16
        xsize 1040
        vbox:
            spacing 8
            text u"ESTADÍSTICAS Y LOGROS" style "es_dk_title"
            viewport:
                xfill True
                ymaximum 540
                draggable True
                mousewheel True
                vbox:
                    spacing 2
                    for line in es_stats_lines():
                        if line[1]:
                            text (line[0]) style "es_dk_head" ypos 6
                        else:
                            text (line[0]) style "es_dk_text"
            textbutton u"VOLVER" style "es_dk_button" xalign 0.5 action Return(True)


# ---------------------------------------------------------------
#  Practica (devuelve el nivel elegido, o 0 para volver)
# ---------------------------------------------------------------
screen es_practice_screen():
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
            spacing 7
            text u"PRÁCTICA" style "es_dk_title" xalign 0.5
            text u"Termina al derrotar al jefe. No guarda récords." style "es_dk_small" xalign 0.5
            for n in range(1, es_practice_max() + 1):
                textbutton (u"Nivel %d - %s" % (n, ES_STAGES[n - 1][0])):
                    style "es_dk_button"
                    xsize 460
                    xalign 0.5
                    action Return(n)
            textbutton u"VOLVER" style "es_dk_button" xalign 0.5 action Return(0)
