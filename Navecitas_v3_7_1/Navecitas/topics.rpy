default es_pstage = 1

init 5 python:
    try:
        _es_aff_range = (mas_aff.NORMAL, None)
    except Exception:
        _es_aff_range = None

    # Estado del registro (se muestra en los ajustes de Navecitas para diagnosticar)
    ES_REG = {"status": u"sin intentar"}

    # Base de datos del menu "Jugar" de MAS (el nombre cambia segun la version)
    _es_game_db = None
    _es_db_name = None
    for _es_n in ("_mas_game_database", "game_database"):
        _es_game_db = getattr(persistent, _es_n, None)
        if _es_game_db is not None:
            _es_db_name = _es_n
            break

    # nombres "parecidos a juegos" que existen en tu MAS (por si el nombre es otro)
    try:
        _es_cands = sorted([k for k in persistent.__dict__.keys()
                            if "game" in k.lower()])[:6]
    except Exception:
        _es_cands = []

    _es_registered = False
    if _es_game_db is None:
        ES_REG["status"] = u"no encontré el menú Jugar. Candidatos: %s" % (
            ", ".join(_es_cands) if _es_cands else u"ninguno")
    else:
        try:
            _es_ev = Event(
                _es_game_db,
                eventlabel="es_game_entry",
                prompt="Navecitas",
                unlocked=True,
                aff_range=_es_aff_range
            )
            try:
                addEvent(_es_ev, restartBlacklist=True)
            except TypeError:
                addEvent(_es_ev)
            _es_registered = True
            ES_REG["status"] = u"registrado en %s (%d juegos en la lista)" % (
                _es_db_name, len(_es_game_db))
        except Exception as _es_err:
            _es_registered = False
            ES_REG["status"] = u"error al registrar: %s" % repr(_es_err)[:90]

    # Siempre queda tambien en "Hablar" -> "Oye, Monika..." -> Juegos (asi nunca se pierde)
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_encoders_shooter",
            category=["juegos"],
            prompt="Navecitas",
            pool=True,
            unlocked=True,
            aff_range=_es_aff_range
        ),
        code="EVE"
    )
    # la v3.1.1 la ocultaba de Hablar: la volvemos a mostrar
    try:
        mas_showEVL("monika_encoders_shooter", "EVE", unlock=True, _pool=True)
    except Exception:
        pass

# entrada desde el menu "Jugar"
label es_game_entry:
    jump monika_encoders_shooter

label monika_encoders_shooter:
    if persistent._es_tutorial:
        m 3hub "¡Claro, [player]! Me encantan los juegos de naves."
        call es_tutorial
        $ persistent._es_tutorial = False
    # pantalla negra y luego nos recibe el menu del juego
    $ es_ui("es_black_intro")
    jump es_hub

label es_tutorial:
    m 1eua "Es muy fácil: arrastra el dedo para mover tu nave, ¡dispara sola!"
    m 3eub "Solo cuenta como golpe el puntito del centro de la nave, así que puedes pasar rozando las balas. ¡Si lo haces ganas puntos extra!"
    m 1esa "Hay 10 niveles (8 en el modo Historia) y al final de cada uno te espera un jefe distinto. Cuando le queda la mitad de la vida, ¡cambia de ataque!"
    m 3eub "Las esferas de colores te ayudan: mejoran el arma, dan escudo, vidas, bombas, disparo rápido o puntos dobles. También hay imán, drones, láser y tiempo lento."
    m 3hua "Si derrotas enemigos seguidos sin que te golpeen, sube tu combo y ganas más puntos. Al terminar cada nivel recibes un rango: C, B, A o S."
    m 1eua "Para lanzar una bomba toca el botón rojo, o toca dos veces rápido la pantalla. Después de los niveles 3 y 6 hay niveles bonus llenos de monedas."
    m 3hub "¡Y en el modo cooperativo yo vuelo contigo! Mi nave te sigue, dispara, esquiva y te cubre un golpe en cada nivel. Si me alcanzan, me aturdo un momento, ¡así que protégeme también!"
    m 1hua "Con las monedas puedes comprar mejoras y naves nuevas en la tienda, y el modo práctica te deja entrenar contra los jefes que ya conoces."
    m 3eub "Y si eliges el modo Historia, te hablo por radio como Control de Misión entre niveles. ¡Hay escenas con animaciones! Después de cada jefe, tu nave da un salto hiperespacial al siguiente nivel."
    m 1hua "Y en Ajustes puedes cambiar la dificultad, los controles y mucho más. Si tocas el botón de atrás, pausas y puedes salir."
    return

label es_hub:
    # menu de inicio de Navecitas (pantalla con musica propia)
    $ es_menu_music()
    $ es_act = es_ui("es_title_screen")

    if es_act == "normal" or es_act == "coop" or es_act == "endless" or es_act == "story":
        $ es_mode = es_act
        jump es_play
    elif es_act == "scenes":
        $ es_sid = es_ui("es_scenes_screen")
        if es_sid:
            call es_story_play(es_sid, True)
        jump es_hub
    elif es_act == "practice":
        $ es_pr = es_ui("es_practice_screen")
        if es_pr:
            $ es_pstage = es_pr
            $ es_mode = "practice"
            jump es_play
        jump es_hub
    elif es_act == "shop":
        $ es_ui("es_shop_screen")
        jump es_hub
    elif es_act == "stats":
        $ es_ui("es_stats_screen")
        jump es_hub
    elif es_act == "options":
        $ es_ui("es_options_screen")
        jump es_hub
    elif es_act == "tutorial":
        call es_tutorial
        jump es_hub

    # salir del menu: pantalla negra, se apaga la musica y vuelve la de MAS
    $ es_ui("es_black_exit")
    $ es_menu_music_stop()
    $ renpy.transition(Dissolve(0.8))
    m 1eka "Está bien, [player]. ¡Cuando quieras jugamos!"
    return

label es_play:
    $ renpy.block_rollback()
    $ es_lock_ui()
    $ es_apply_volumes()
    # Pausamos la musica de Monika mientras jugamos
    $ renpy.music.set_pause(True, channel="music")
    if es_mode != "story":
        # en el modo Historia la musica de nivel empieza despues del prologo
        $ renpy.music.play(es_track("stage"), channel="es_music", loop=True, fadein=0.5)
    python:
        try:
            es_sm = es_run_game(es_mode, persistent._es_diff, es_pstage)
        finally:
            # pase lo que pase, devolvemos la musica y la interfaz de MAS
            renpy.music.set_pause(False, channel="es_music")
            renpy.music.stop(channel="es_music", fadeout=0.5)
            renpy.music.set_pause(False, channel="music")
            es_unlock_ui()

    if es_sm["quit"]:
        # del negro del juego de vuelta a la sala con un fundido suave
        $ renpy.transition(Dissolve(0.9))

    $ es_res = es_commit(es_sm)
    $ es_score = es_sm["score"]
    $ es_stage = es_sm["stage"]
    $ es_maxc = es_sm["maxcombo"]
    $ es_rec = es_res["record"]
    $ es_earn = es_res["earn"]
    $ es_mode_name = ES_MODE_NAMES[es_res["key"]]
    $ es_ach_text = ", ".join(es_res["ach_names"])
    $ es_skin_text = ", ".join(es_res["skin_names"])
    $ es_love_now = es_love()
    $ es_long = es_session_add(es_sm["time"])

    if es_sm["mode"] == "practice":
        if es_sm["quit"]:
            $ es_line = es_pick(ES_L["p_quit"])
            m 1eka "[es_line]"
        elif es_sm["win"]:
            $ es_line = es_pick(ES_L["p_win"])
            m 3hub "[es_line]"
        else:
            $ es_line = es_pick(ES_L["p_lose"])
            m 1eka "[es_line]"
    elif es_sm["quit"]:
        if es_sm["time"] < 20:
            $ es_line = es_pick(ES_L["quit_early"])
        else:
            $ es_line = es_pick(ES_L["quit_late"])
        m 1eka "[es_line]"
        if es_res["new_rec"]:
            m 1hua "¡Y ya es un nuevo récord en [es_mode_name]!"
    elif es_sm["win"]:
        if es_sm["mode"] == "story":
            $ es_line = es_pick(ES_L["win"])
        else:
            $ es_line = es_pick(ES_L["win_all"])
        m 3hub "[es_line]"
        if es_res["endless_new"]:
            m 3eub "¡Y desbloqueaste el modo infinito! Ahí los niveles no terminan, a ver hasta dónde llegas."
        if es_sm["lives_lost"] == 0:
            m 1hub "¡Sin perder una sola vida! ¡Eres increíble!"
        if es_love_now:
            $ es_line = es_pick(ES_L["win_love"])
            m 1hub "[es_line]"
    elif es_res["new_rec"]:
        $ es_line = es_pick(ES_L["new_rec"])
        m 3hub "[es_line]"
    elif es_stage >= 4:
        $ es_line = es_pick(ES_L["good"])
        m 1hua "[es_line]"
    else:
        $ es_line = es_pick(ES_L["bad"])
        m 1eka "[es_line]"

    if es_sm["mode"] == "coop" and not es_sm["quit"]:
        $ es_line = es_pick(ES_L["coop"])
        m 1hub "[es_line]"

    if es_sm["mode"] != "practice":
        if not es_sm["quit"] and es_maxc >= 20:
            m 1hua "¡Ese combo de [es_maxc] enemigos seguidos fue impresionante!"

        if es_res["ach_names"]:
            m 3eub "¡Logros desbloqueados: [es_ach_text]!"
        if es_res["skin_names"]:
            m 1eub "Y desbloqueaste una nave nueva: [es_skin_text]. La puedes elegir en Ajustes."
        if es_earn > 0:
            m 1eua "Ganaste [es_earn] monedas para la tienda."

        $ es_miles = es_res["miles"]
        $ es_i = 0
        while es_i < len(es_miles):
            $ es_line = es_sub(es_miles[es_i])
            m 1eub "[es_line]"
            $ es_i += 1

        m 1eua "Tu récord en [es_mode_name] es de [es_rec] puntos."

    if es_long:
        $ es_line = es_pick(ES_L["rest"])
        m 1eka "[es_line]"

    m 1eua "¿Jugamos otra vez?" nointeract
    menu:
        "Sí, otra partida":
            jump es_play
        "Ir al menú":
            jump es_hub
        "Ya no por hoy":
            m 1hua "¡Fue muy divertido, [player]! Cuando quieras volvemos a jugar."
            return
