from PyQt6.QtCore import QTranslator

_current_translator = None

def set_lang(lang_code, app):
    global _current_translator
    if _current_translator is not None:
        app.removeTranslator(_current_translator)

    tr = QTranslator()

    if lang_code == "fa":
        success = tr.load("fa.qm")
        print("fa.qm loaded:", success)

    _current_translator = tr
    app.installTranslator(tr)