import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        category=self._view._ddcategory.value
        starDate=self._view._dp1.value
        endDate=self._view._dp1.value

        #cotnrollo dei parametri

        #controllo cateogoria
        if category is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona una categoria", color="red"))
            self._view.update_page()


        if starDate is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona una data di inizio", color="red"))
            self._view.update_page()


        if endDate is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona una  data di fine", color="red"))
            self._view.update_page()

        if starDate > endDate:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"la data di inizio deve precedere la data di fine", color="red"))
            self._view.update_page()

        #creo grafo
        self._model.creaGrafo(category,starDate,endDate)
        n, m = self._model.getGrafoDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(
            f"Date selezionate: "))
        self._view.txt_result.controls.append(ft.Text(
            f"Start Date: {starDate} \n"
            f"End Date: {endDate}"))


        self._view.txt_result.controls.append(ft.Text(
            f"Grafo creato correttamente\n "
            f"Numero di nodi: {n} \n"
            f"Numero di acrhi: {m}  "))


        self._view.update_page()


    def handleBestProdotti(self, e):
        pass

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)


    def _fillDDCategory(self):

        categories= self._model.getAllCategory()
        categoriesDD= list(map(lambda x: ft.dropdown.Option(x), categories)) #ogni anno diventa una voce del dropdown
        self._view._ddcategory.options = categoriesDD
        self._view.update_page()
