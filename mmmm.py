import tkinter as tk
from PIL import Image, ImageTk
import cv2
import webbrowser

from memorama import iniciar_memorama_1
import memorama

from Jumpy_Game import jumpy_game

import sys
# Se añade el path del juego Jumpy_Game por si se requiere cargar recursos internos
sys.path.append(r"E:/cecy/Proyecto_PEC/VSCode_1/Jumpy_Game")

# ----------------- CONFIGURACIÓN DE VENTANA PRINCIPAL -----------------
ventana = tk.Tk()  # Ventana principal de la aplicación
ventana.title("App IA")  # Título de la ventana
ventana.geometry("500x400")  # Tamaño fijo de la ventana (ancho x alto)

# ----------------- RUTAS DE VIDEOS -----------------
video_intro = "videos_de_fondo/video_empresa_nova.mp4"  # Video de introducción al iniciar la app
video_post_login = "videos_de_fondo/pantalla_carga.mp4"  # Video que aparece tras login exitoso
video_juego = "videos_de_fondo/video_carga_juego.mp4"  # Video de introducción antes de iniciar juegos

# ----------------- CREDENCIALES DE USUARIO -----------------
usuario_correcto = "Nova"  # Usuario válido
contrasena_correcta = "12345"  # Contraseña válida
intentos_fallidos = 0  # Contador de intentos incorrectos de login

# ----------------- CARGA DE ICONO ------------------
try:
    imagen_pil = Image.open("fondos/cecyto_icono.jpeg")  # Carga imagen para icono
    icono_tk = ImageTk.PhotoImage(imagen_pil)  # Conversión a formato compatible con tkinter
    ventana.iconphoto(True, icono_tk)  # Establece el icono de la ventana
except Exception as e:
    print(f"Error al cargar el icono: {e}")  # Si falla, se imprime el error

# ----------------- CONTENIDO EDUCATIVO -----------------
# Diccionario con títulos como claves y textos explicativos como valores
contenidos = {
    "¿𝐐𝐮é 𝐞𝐬 𝐥𝐚 𝐈𝐀?": (
        "\n"
       "La inteligencia artificial (IA) es una tecnología que permite"
       " a las computadoras y máquinas simular el aprendizaje humano,"
       " la comprensión, la resolución de problemas, la toma de"
       " decisiones, la creatividad y la autonomía."
       "Las aplicaciones y dispositivos equipados con IA pueden ver"
       " e identificar objetos. Pueden entender y responder al"
       " lenguaje humano. Pueden aprender de nueva información"
       " y experiencia. Pueden hacer recomendaciones detalladas"
       " a usuarios y expertos. Pueden actuar de manera independiente,"
       " reemplazando la necesidad de inteligencia o intervención humana"
       " (un ejemplo clásico es un automóvil autónomo)."

    ),
    "¿𝐏𝐨𝐫 𝐪𝐮é 𝐧𝐨 𝐚𝐛𝐮𝐬𝐚𝐫 𝐝𝐞𝐥 𝐮𝐬𝐨 𝐝𝐞 𝐥𝐚 𝐈𝐀?": (
        "\n"
        "\n"
        "El uso adecuado de la inteligencia artificial (IA) puede ser\n"
        " muy beneficioso, ya que nos libera de tareas rutinarias y\n"
        " nos permite centrarnos en actividades más creativas\n"
        " y enriquecedoras. Sin embargo, también presenta riesgos\n"
        " si se utiliza en exceso. La Dra. Mara Dierssen, experta\n"
        " en neurobiología, advierte que confiar demasiado en la IA\n"
        " para escribir, resumir o procesar información puede afectar\n"
        " negativamente nuestras capacidades cognitivas. Al delegar\n"
        " constantemente estas funciones, dejamos de ejercitar la \n"
        "memoria y el pensamiento crítico, lo que a largo plazo puede\n"
        " disminuir nuestra autonomía para resolver problemas y tomar\n"
        " decisiones de forma independiente.\n"
    ),
    "𝐂𝐨𝐧𝐬𝐞𝐜𝐮𝐞𝐧𝐜𝐢𝐚𝐬 𝐝𝐞𝐥 𝐮𝐬𝐨 𝐞𝐱𝐜𝐞𝐬𝐢𝐯𝐨 𝐝𝐞 𝐥𝐚 𝐈𝐀": (
        "\n"
        "\n"
        "La IA no sólo incrementa la productividad a nivel de maquinaria,"
        " sino que también hace que incremente la productividad de los"
        " trabajadores y la calidad del trabajo que realizan. El poder gozar"
        " de mayor información, les permite tener una visión más focalizada"
        " de su trabajo y tomar mejores decisiones.\n"
        "\n"
        "⚠️ Algunas consecuencias son:\n"
        "-Puede causar pérdida de empleos.\n"
        "-Aumenta la desigualdad digital.\n"
        "-Riesgos a la privacidad y vigilancia.\n"
        "-Puede tener sesgos y discriminar.\n"
        "-Genera dependencia tecnológica.\n"
        "-Usos peligrosos en seguridad.\n"
    ),
    "𝐕𝐞𝐧𝐭𝐚𝐣𝐚𝐬 𝐝𝐞 𝐮𝐬𝐚𝐫 𝐥𝐚 𝐈𝐀": (
        "\n"
        "\n"
        "-Automatización de procesos: Reduce tiempos, errores y costos"
        " operativos al optimizar recursos.\n"
        "-Menor intervención humana: Libera a las personas de tareas"
        " repetitivas, permitiéndoles enfocarse en actividades"
        " estratégicas y creativas.\n"
        "-Resultados más precisos: Detecta patrones y procesa información"
        " con alta precisión, mejorando diagnósticos y procesos.\n"
        "-Mejor toma de decisiones: Permite decisiones rápidas y fundamentadas"
        " gracias al análisis en tiempo real.\n"
        "-Mayor control de procesos: Supervisa y corrige desviaciones durante"
        " la producción, mejorando la gestión.\n"
        "-Incremento de la productividad: Automatiza tareas repetitivas,"
        " permitiendo enfocarse en innovación y estrategia.\n"
    ),
    "𝐂𝐮𝐚𝐧𝐝𝐨 𝐒Í 𝐮𝐬𝐚𝐫 𝐥𝐚 𝐈𝐀": (
        "\n"
        "\n"
        "La inteligencia artificial es una súper herramienta,"
        " ¡pero hay que saber cuándo usarla!"
        "\n"
        "✅ Para aprender mejor: cuando necesitas ayuda con tareas"
        " o entender algo difícil."
        "\n"
        "✅ Para inspirarte: si buscas ideas para escribir, dibujar"
        " o crear contenido."
        "\n"
        "✅ Para organizarte: usando apps que te recuerdan cosas"
        " o te ayudan a planear."
        "\n"
        "✅ Para explorar el mundo: traducir idiomas, conocer"
        " culturas o resolver dudas."
        "\n"
        "Usar la IA con responsabilidad y creatividad puede ayudarte"
        " a lograr cosas geniales. Solo recuerda: ¡tú tomas las"
        " decisiones, no la máquina!"
    ),
    "𝐄𝐱𝐩𝐞𝐫𝐢𝐞𝐧𝐜𝐢𝐚𝐬 𝐩𝐨𝐬𝐢𝐭𝐢𝐯𝐚𝐬 𝐝𝐞𝐥 𝐮𝐬𝐨 𝐝𝐞 𝐥𝐚 𝐈𝐀": (
        "\n"
        "\n"
        "La inteligencia artificial está en todas partes y\n"
        " muchas veces ni lo notamos. Nos ayuda a estudiar\n"
        " con apps que explican temas difíciles, a mejorar\n"
        " en los videojuegos con bots inteligentes, y hasta\n"
        " a elegir la mejor ruta en Google Maps. También está\n"
        " en filtros de Instagram, recomendaciones de TikTok\n"
        " y playlists de Spotify.Es como tener un ayudante\n"
        " digital que aprende de lo que te gusta y te hace la\n"
        " vida más fácil (y divertida).La IA también ayuda a\n"
        " cuidar el medio ambiente, prediciendo desastres\n"
        " naturales y monitoreando la contaminación. En la\n"
        " música y el arte, permite crear cosas nuevas y\n"
        " originales con solo unas pocas ideas."
    ),
    "𝐑𝐞𝐟𝐥𝐞𝐱𝐢𝐨𝐧𝐞𝐬 𝐝𝐞𝐥 𝐮𝐬𝐨 𝐝𝐞 𝐥𝐚 𝐈𝐀": (
        "\n"
        "La inteligencia artificial se ha convertido en una\n"
        " herramienta muy útil en distintos ámbitos, como la\n"
        " educación, la salud, la ciencia y hasta en nuestro\n"
        " día a día. Nos permite aprender más rápido, encontrar\n"
        " soluciones creativas y hacer tareas de forma más\n"
        " eficiente. Sin embargo, es importante recordar que\n"
        " no debemos volvernos totalmente dependientes de ella.\n"
        " La IA no está para reemplazarnos, sino para\n"
        " complementarnos. No es una enemiga, sino una aliada\n"
        " que, bien utilizada, puede ayudarnos a crecer, a innovar\n"
        " y a construir un futuro mejor. La clave está en usarla\n"
        " con criterio, ética y responsabilidad, aprovechando sus\n"
        " beneficios sin dejar de pensar por nosotros mismos."
    ),
    "𝐏á𝐠𝐢𝐧𝐚𝐬 ú𝐭𝐢𝐥𝐞𝐬": "",
    "𝐉𝐮𝐞𝐠𝐨 𝐃𝐢𝐝𝐚𝐜𝐭𝐢𝐜𝐨": ""
}

# ----------------- CARGA DE FONDOS -----------------
fondos = {}  # Diccionario de imágenes de fondo
fondos_rutas = {
    "login": "fondos/cecyto_login.png",  # Fondo para la pantalla de login
    "menu": "fondos/cecyto_menu.png",  # Fondo para el menú principal
    "contenido": "fondos/cecyto_opciones.png",  # Fondo para los contenidos educativos
    "intro": "fondos/cecyto_intro.png",  # Fondo para la pantalla de introducción
}

# Carga de imágenes y redimensionamiento a 500x400 px
for nombre, ruta in fondos_rutas.items():
    try:
        img = Image.open(ruta).resize((500, 400))
        fondos[nombre] = ImageTk.PhotoImage(img)  # Se guarda la imagen en el diccionario
    except:
        fondos[nombre] = None  # Si falla la carga, se asigna None

# ----------------- FRAMES PRINCIPALES -----------------
# Marcos (frames) que representan diferentes secciones de la app
frame_video = tk.Frame(ventana)  # Frame para reproducir los videos
frame_login = tk.Frame(ventana)  # Frame para la pantalla de acceso con usuario y contraseña
frame_intro = tk.Frame(ventana)  # Frame de introducción del proyecto tras login exitoso
frame_menu = tk.Frame(ventana)  # Frame que contiene los botones de navegación del menú principal
frame_contenido = tk.Frame(ventana)  # Frame donde se muestran los textos educativos al seleccionar una opción
frame_opciones_memorama = tk.Frame(ventana)  # Frame con botones para seleccionar versiones del memorama

# Se colocan todos los frames en la ventana principal (ocultos inicialmente)
for frame in [frame_video, frame_login, frame_intro, frame_menu, frame_contenido, frame_opciones_memorama]:
    frame.pack(fill="both", expand=True)  # Se llenan completamente pero solo se muestra uno a la vez

# ----------------- FUNCIONES AUXILIARES -----------------
def abrir_enlace(url):
    """Abre un enlace en el navegador predeterminado del sistema"""
    webbrowser.open_new_tab(url)

def mostrar_frame(frame):
    """Muestra el frame deseado y oculta los demás"""
    for f in (frame_video, frame_login, frame_intro, frame_menu, frame_contenido, frame_opciones_memorama):
        f.pack_forget()
    frame.pack(fill="both", expand=True)

def reproducir_video(path, siguiente_accion):
    """Reproduce un video desde la ruta dada y luego ejecuta una función"""
    cap = cv2.VideoCapture(path)  # Se carga el video
    label = tk.Label(frame_video)  # Etiqueta donde se mostrará el video
    label.pack()

    def mostrar():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (500, 400))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            label.imgtk = img
            label.configure(image=img)
            ventana.after(30, mostrar)
        else:
            cap.release()  # Se libera el recurso
            label.destroy()
            if callable(siguiente_accion):
                siguiente_accion()

    mostrar_frame(frame_video)  # Se muestra el frame del video
    mostrar()  # Se inicia la reproducción

# ----------------- FUNCIÓN PARA VERIFICAR LOGIN -----------------
def verificar_login():
    global intentos_fallidos
    usuario = entrada_usuario.get()
    contrasena = entrada_contra.get()
    if usuario == usuario_correcto and contrasena == contrasena_correcta:
        reproducir_video(video_post_login, frame_intro)
    else:
        intentos_fallidos += 1
        if intentos_fallidos < 3:
            error_label.config(text=f"Intento {intentos_fallidos}/3: Usuario o contraseña incorrectos")
        else:
            error_label.config(text="Acceso denegado")
            ventana.after(2000, ventana.quit)


# ----------------- FUNCIÓN PARA INICIAR VIDEO DE INTRODUCCIÓN -----------------
def iniciar_intro():
    mostrar_frame(frame_intro)  # Muestra la pantalla de introducción

# ----------------- FUNCIÓN PARA MOSTRAR EL MENÚ -----------------
def mostrar_menu():
    mostrar_frame(frame_menu)  # Muestra el menú principal

# ----------------- FUNCIÓN PARA MOSTRAR CONTENIDO EDUCATIVO -----------------
def mostrar_texto(titulo, texto):
    if titulo == "𝐉𝐮𝐞𝐠𝐨 𝐃𝐢𝐝𝐚𝐜𝐭𝐢𝐜𝐨":
        mostrar_frame(frame_video)
        ventana.after(100, lambda: reproducir_video(video_juego, mostrar_opciones_memorama))
        return

    frame = frame_contenido
    for widget in frame.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(frame, width=500, height=400)
    canvas.pack(fill="both", expand=True)

    if fondos["contenido"]:
        canvas.create_image(0, 0, image=fondos["contenido"], anchor="nw")

    canvas.create_text(250, 50, text=titulo, font=("Arial", 16, "bold"), fill="black")

    if titulo == "𝐏á𝐠𝐢𝐧𝐚𝐬 ú𝐭𝐢𝐥𝐞𝐬":
        botones_info = [
            ("Khan Academy", "https://www.khanacademy.org"),
            ("Socratic by Google", "https://socratic.org"),
            ("Quillbot", "https://quillbot.com"),
            ("Querium", "https://www.querium.com"),
            ("ScribeHow", "https://scribehow.com")
        ]

        y = 100
        for nombre, url in botones_info:
            boton = tk.Button(canvas, text=f"Abrir: {nombre}", bg="#87CEEB", command=lambda u=url: abrir_enlace(u))
            canvas.create_window(250, y, window=boton)
            y += 40
    else:
        canvas.create_text(250, 190, text=texto, font=("Arial", 12), width=440, fill="black", justify=tk.LEFT)

    tk.Button(frame, text="Volver al menú", bg="#87CEEB", command=mostrar_menu).place(x=190, y=350)

    mostrar_frame(frame)

def mostrar_opciones_memorama():
    frame = frame_opciones_memorama
    for widget in frame.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(frame, width=500, height=400)
    canvas.pack(fill="both", expand=True)

    if fondos["contenido"]:
        canvas.create_image(0, 0, image=fondos["contenido"], anchor="nw")

    canvas.create_text(250, 50, text="Seleccione un juego", font=("Arial", 16, "bold"), fill="#000000")

    tk.Button(canvas, text="Memorama", width=20, bg="#87CEEB", command=iniciar_memorama_1).place(x=170, y=150)
    tk.Button(canvas, text="Juego de saltos", width=20, bg="#87CEEB", command=ejecutar_juego_saltos).place(x=170, y=200)
    tk.Button(canvas, text="Volver al menú", bg="#87CEEB", command=mostrar_menu).place(x=190, y=350)

    mostrar_frame(frame)

# ----------------- FUNCIÓN PARA INICIAR MEMORAMA -----------------
def iniciar_memorama():
    reproducir_video(video_juego, memorama.iniciar_memorama_1)  # Se reproduce video y luego inicia el juego

# ----------------- FUNCIÓN PARA INICIAR JUEGO DE SALTOS -----------------
def ejecutar_juego_saltos():
    reproducir_video(video_juego, jumpy_game)  # Se reproduce video y luego inicia el juego

def salir_con_creditos():
    """
    Función para mostrar una pantalla final con los créditos y luego salir de la aplicación.
    """
    # Limpiar el contenido actual del frame de contenido
    frame = frame_contenido
    for widget in frame.winfo_children():
        widget.destroy()

    # Crear un Canvas para mostrar los créditos
    canvas = tk.Canvas(frame, width=500, height=400)
    canvas.pack(fill="both", expand=True)

    # Establecer la imagen de fondo si está disponible
    if fondos["contenido"]:
        canvas.create_image(0, 0, image=fondos["contenido"], anchor="nw")

    # Título de los créditos
    canvas.create_text(250, 50, text="=== Créditos ===", font=("Arial", 16, "bold"), fill="black")

    # Texto con los integrantes del equipo y el nombre de la empresa
    canvas.create_text(250, 190,
                       text="Grupo 205\nEquipo 3 - Empresa: Nova\n- Gabriela Baez\n- Jesus Gael Garcia\n"
                            "- Franco Dominic Mojica\n- Rafael Arturo Leon",
                       font=("Arial", 12), width=440, fill="black", justify=tk.LEFT)

    # Mostrar el frame de créditos
    mostrar_frame(frame)

    # Cerrar la ventana automáticamente después de 4 segundos
    ventana.after(4000, ventana.quit)


# ----------------- LOGIN -----------------
# Crear un canvas para la pantalla de inicio de sesión
canvas_login = tk.Canvas(frame_login, width=500, height=400)
canvas_login.pack(fill="both", expand=True)

# Establecer la imagen de fondo para la pantalla de login si existe
if fondos["login"]:
    canvas_login.create_image(0, 0, image=fondos["login"], anchor="nw")

# Título de la pantalla de inicio de sesión
canvas_login.create_text(250, 40, text="Inicio de Sesión", font=("Arial", 16, "bold"))

# Etiqueta y campo de entrada para el usuario
canvas_login.create_text(180, 120, text="Usuario:")
entrada_usuario = tk.Entry(frame_login)
canvas_login.create_window(300, 120, window=entrada_usuario)

# Etiqueta y campo de entrada para la contraseña
canvas_login.create_text(180, 160, text="Contraseña:")
entrada_contra = tk.Entry(frame_login, show="*")
canvas_login.create_window(300, 160, window=entrada_contra)

# Botón para iniciar sesión que llama a la función verificar_login
btn_login = tk.Button(frame_login, text="Ingresar", bg="#87CEEB", command=verificar_login)
canvas_login.create_window(250, 200, window=btn_login)

# Etiqueta para mostrar errores de inicio de sesión
error_label = tk.Label(frame_login, text="", fg="red", bg="white")
canvas_login.create_window(250, 240, window=error_label)


# ----------------- INICIO -----------------
# Iniciar la aplicación mostrando primero el frame de video introductorio
mostrar_frame(frame_video)

# Reproducir el video de introducción y luego mostrar la pantalla de inicio de sesión
reproducir_video(video_intro, lambda: mostrar_frame(frame_login))

# Mantener la ventana principal corriendo
ventana.mainloop()


print("key")