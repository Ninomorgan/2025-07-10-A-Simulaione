import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


        #devo salvare oggetti
        self._prodStart = None
        self._prodEnd = None

    def handleCreaGrafo(self, e):
        category=self._view._ddcategory.value
        starDate=self._view._dp1.value
        endDate=self._view._dp2.value

        #cotnrollo dei parametri

        #controllo cateogoria
        if category is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona una categoria", color="red"))
            self._view.update_page()
            return


        if starDate is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona una data di inizio", color="red"))
            self._view.update_page()
            return


        if endDate is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona una  data di fine", color="red"))
            self._view.update_page()
            return


        if starDate > endDate:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"la data di inizio deve precedere la data di fine", color="red"))
            self._view.update_page()
            return

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

        self._view._btnBestProdotti.disabled = False

        self._fillDDProd()



        self._view.update_page()


    def handleBestProdotti(self, e):
        bestProd= self._model._getBestProdotti()



        self._view.txt_result.controls.append(ft.Text("Top 5 Prodotti Venduti:", color="green"))
        for p,score in bestProd:
            self._view.txt_result.controls.append(ft.Text(f"{p} --> {score}",))

        self._view.update_page()




    def handleCercaCammino(self, e):
        LMax = self._view._txtInLun.value
        partenza = self._prodStart
        arrivo = self._prodEnd

        LMaxINT=0

        #controllo
        if LMax is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare una lunghezza max ", color="red"))
            self._view.update_page()
            return
        if partenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un prodotto di partenza ", color="red"))
            self._view.update_page()
            return
        if arrivo is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un prodotto di fine ", color="red"))
            self._view.update_page()
            return

        try:
            LMaxINT = int(LMax)
        except ValueError:
            self._view.create_alert("Inserire una lunghezza valida")
            return

        cammino, score = self._model.getPath(partenza,arrivo, LMaxINT)

        self._view.txt_result.controls.clear()

        if len(cammino) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun cammino trovato da {partenza} a {arrivo}")
            )
            self._view.update_page()
            return



        self._view.txt_result.controls.append(
            ft.Text(f"Percorso ottimo da {partenza} a {arrivo}:")
        )

        #print NODI E PESO
        for i in range(len(cammino) - 1):
            peso = self._model.getPesoArco(cammino[i], cammino[i + 1])
            self._view.txt_result.controls.append(
                ft.Text(f"{cammino[i]} -> {cammino[i + 1]} | peso: {peso}")
            )

        self._view.txt_result.controls.append(
            ft.Text(f"Peso totale: {score}")
        )

        self._view.update_page()



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

    # si fa sempre così --> PERCHè STO  USSANDO OGGETTIU
    def _fillDDProd(self):
        nodi= self._model.getNodi()
        self._view._ddProdStart.options.clear()
        self._view._ddProdEnd.options.clear()

        for n in nodi:
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(
                    text=str(n),
                    data=n,
                    on_click=self.readDDStart
                )
            )

            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(
                    text=str(n),
                    data=n,
                    on_click=self.readDDEnd
                )
            )

        self._view.update_page()

     # METODO PR LEGGERLI
    def readDDStart(self, e):
        self._prodStart = e.control.data

    def readDDEnd(self, e):
        self._prodEnd = e.control.data