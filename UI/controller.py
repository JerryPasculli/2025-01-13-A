import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def riempi(self):
        lista = self._model.getLocal()
        for element in lista:
            opzione = ft.dropdown.Option(element[0])
            self._view.dd_localization.options.append(opzione)
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        local = self._view.dd_localization.value
        if local is None:
            stringa = ft.Text("NON HAI SCELTO UNA LOCALIZATION", color ="red")
            self._view.txt_result.controls.append(stringa)
            self._view.update_page()
            return
        t1 = self._model.creaGrafo(local)
        stringa = ft.Text(t1)
        self._view.txt_result.controls.append(stringa)
        self._view.btn_analizza_grafo.disabled=False
        self._view.update_page()

    def analyze_graph(self, e):
        self._view.txt_result.controls.clear()
        t1 = self._model.dettagli()
        stringa = ft.Text(t1)
        self._view.txt_result.controls.append(stringa)
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result.controls.clear()
        t1 = self._model.setMinimo()
        stringa = ft.Text(t1)
        self._view.txt_result.controls.append(stringa)
        self._view.update_page()

