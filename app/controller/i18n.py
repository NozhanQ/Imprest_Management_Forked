import os
import sys
from PyQt6.QtCore import QTranslator

_current_translator = None

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def set_lang(lang_code, app):
    global _current_translator
    if _current_translator is not None:
        app.removeTranslator(_current_translator)

    tr = QTranslator()

    if lang_code == "fa":
        qm_path = os.path.join(get_base_path(), "fa.qm")
        loaded = tr.load(qm_path)
        print("fa.qm loaded:", loaded, "from", qm_path)

    _current_translator = tr
    app.installTranslator(tr)