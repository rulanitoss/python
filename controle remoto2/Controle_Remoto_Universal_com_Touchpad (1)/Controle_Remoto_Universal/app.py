# -*- coding: utf-8 -*-
"""
Controle Remoto Universal — Windows + telemóvel na rede local.
Uso: executar iniciar.bat, consultar o PIN no terminal e abrir o URL no PC/telemóvel.
"""
import os
import secrets
import socket
import subprocess
import sys
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, render_template, request, session, redirect, url_for, abort

try:
    import pyautogui
except ImportError:
    pyautogui = None

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HOST = "0.0.0.0"
PORT = int(os.environ.get("REMOTE_PORT", "8765"))
PIN = os.environ.get("REMOTE_PIN") or f"{secrets.randbelow(1_000_000):06d}"
SECRET_KEY = secrets.token_hex(32)

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # LAN HTTP; não expor à Internet.
    MAX_CONTENT_LENGTH=16 * 1024,
)

if pyautogui is not None:
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.06

ALLOWED_KEYS = {
    "up", "down", "left", "right", "enter", "esc", "tab", "space",
    "backspace", "delete", "home", "end", "pageup", "pagedown",
    "volumemute", "volumeup", "volumedown", "playpause", "prevtrack",
    "nexttrack", "stop",
}
ALLOWED_HOTKEYS = {
    "alt_tab": ("alt", "tab"),
    "win_d": ("win", "d"),
    "win_s": ("win", "s"),
    "ctrl_c": ("ctrl", "c"),
    "ctrl_v": ("ctrl", "v"),
    "ctrl_x": ("ctrl", "x"),
    "ctrl_z": ("ctrl", "z"),
    "ctrl_y": ("ctrl", "y"),
    "ctrl_a": ("ctrl", "a"),
    "ctrl_shift_esc": ("ctrl", "shift", "esc"),
    "win_e": ("win", "e"),
}
ALLOWED_APPS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "explorer": ["explorer.exe"],
    "keyboard": ["osk.exe"],
}

def local_ip():
    """Descobre o IP IPv4 usado na rede local sem enviar dados para um servidor."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("192.0.2.1", 80))
        ip = sock.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        sock.close()
    return ip

def require_auth(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("authenticated"):
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "error": "Sessão expirada. Entre novamente."}), 401
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped

def require_pyautogui():
    if pyautogui is None:
        return jsonify({"ok": False, "error": "Falta instalar pyautogui. Execute instalar.bat."}), 503
    return None

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        submitted = request.form.get("pin", "")
        if secrets.compare_digest(submitted, PIN):
            session.clear()
            session["authenticated"] = True
            session["csrf"] = secrets.token_urlsafe(24)
            return redirect(url_for("index"))
        error = "PIN incorreto. Confirma o código mostrado no computador."
    return render_template("login.html", error=error)

@app.route("/logout", methods=["POST"])
@require_auth
def logout():
    if request.form.get("csrf") != session.get("csrf"):
        abort(403)
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@require_auth
def index():
    return render_template("index.html", csrf=session.get("csrf", ""))

@app.route("/api/action", methods=["POST"])
@require_auth
def action():
    bad = require_pyautogui()
    if bad:
        return bad
    data = request.get_json(silent=True) or {}
    if not secrets.compare_digest(str(data.get("csrf", "")), str(session.get("csrf", ""))):
        return jsonify({"ok": False, "error": "Pedido inválido. Atualize a página."}), 403

    name = str(data.get("action", ""))
    try:
        if name in ALLOWED_KEYS:
            pyautogui.press(name)
            message = f"Tecla: {name}"
        elif name in ALLOWED_HOTKEYS:
            pyautogui.hotkey(*ALLOWED_HOTKEYS[name])
            message = f"Atalho: {name.replace('_', ' + ')}"
        elif name == "start":
            pyautogui.press("win")
            message = "Menu Iniciar"
        elif name == "screenshot":
            folder = os.path.join(os.path.expanduser("~"), "Pictures", "Capturas")
            os.makedirs(folder, exist_ok=True)
            filename = os.path.join(folder, "captura_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png")
            pyautogui.screenshot().save(filename)
            message = "Captura guardada em Imagens/Capturas"
        elif name in ALLOWED_APPS:
            subprocess.Popen(ALLOWED_APPS[name], shell=False)
            message = "Aplicação aberta"
        elif name == "mouse_move":
            # Movimento relativo limitado para evitar saltos acidentais do cursor.
            dx = data.get("dx", 0)
            dy = data.get("dy", 0)
            if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
                return jsonify({"ok": False, "error": "Coordenadas inválidas."}), 400
            dx = max(-180, min(180, int(dx)))
            dy = max(-180, min(180, int(dy)))
            pyautogui.moveRel(dx, dy, duration=0)
            message = "Cursor movido"
        elif name == "mouse_click":
            pyautogui.click()
            message = "Clique esquerdo"
        elif name == "mouse_double":
            pyautogui.doubleClick(interval=0.12)
            message = "Duplo clique"
        elif name == "mouse_right":
            pyautogui.click(button="right")
            message = "Clique direito"
        elif name == "mouse_down":
            pyautogui.mouseDown()
            message = "Botão do rato pressionado"
        elif name == "mouse_up":
            pyautogui.mouseUp()
            message = "Botão do rato libertado"
        elif name == "mouse_scroll":
            amount = data.get("amount", 0)
            if not isinstance(amount, (int, float)):
                return jsonify({"ok": False, "error": "Valor de rolagem inválido."}), 400
            amount = max(-8, min(8, int(amount)))
            pyautogui.scroll(amount)
            message = "Rolagem executada"
        elif name == "lock":
            # Ação explícita de bloqueio; não desliga nem reinicia o PC.
            subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"], shell=False)
            message = "Sessão bloqueada"
        else:
            return jsonify({"ok": False, "error": "Comando não reconhecido ou não permitido."}), 400
        return jsonify({"ok": True, "message": message})
    except Exception as exc:
        app.logger.exception("Falha ao executar ação")
        return jsonify({"ok": False, "error": f"Não foi possível executar a ação: {type(exc).__name__}"}), 500

@app.route("/api/status")
@require_auth
def status():
    return jsonify({
        "ok": True,
        "computer": socket.gethostname(),
        "pyautogui": pyautogui is not None,
        "network": "rede local",
    })

if __name__ == "__main__":
    print("=" * 58)
    print(" CONTROLE REMOTO UNIVERSAL")
    print("=" * 58)
    print(f"PIN de acesso: {PIN}")
    print(f"No próprio PC: http://127.0.0.1:{PORT}")
    print(f"No telemóvel:  http://{local_ip()}:{PORT}")
    print("PC e telemóvel têm de estar na mesma rede Wi-Fi.")
    print("Não encaminhe esta porta para a Internet.")
    print("Para parar o servidor, pressione Ctrl+C nesta janela.")
    print("=" * 58)
    # Threaded para PC e telemóvel poderem usar a interface; apenas rede local.
    app.run(host=HOST, port=PORT, debug=False, threaded=True)
