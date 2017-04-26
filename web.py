
#import socketserver este no sirve, solo en server.py
#poner todos los import juntos y ordenados alfabeticamente

# HTTPRequestHandler class
import http.client
import http.server
import json


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL="api.fda.gov" #si en algun momento tengo q cambiar el º
    OPENFDA_API_EVENT="/drug/event.json"



    def get_event(self):

        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT+'?limit=10')
        r1=conn.getresponse()
        data1=r1.read()
        data=data1.decode('utf8')
        eventos=json.loads(data)
        return eventos

    def get_buscar_medicamento(self,medicamento):

        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT+'?limit=10'+ '&search=patient.drug.medicinalproduct:'+medicamento)
        r1=conn.getresponse()
        data1=r1.read()
        data=data1.decode('utf8')
        eventos_medicamentos=json.loads(data)
        return eventos_medicamentos

    def get_buscar_empresa(self,empresa):

        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT+'?limit=10'+ '&search=companynumb:' + empresa)
        r1=conn.getresponse()
        data1=r1.read()
        data=data1.decode('utf8')
        eventos_empresas=json.loads(data)
        return eventos_empresas

    def get_medicamentos(self,eventos):
        medicamentos=[]
        results=eventos["results"]
        for event in results:
            patient=event["patient"]
            drug=patient["drug"]
            medicinalproduct=drug[0]["medicinalproduct"]
            medicamentos += [medicinalproduct]
        return medicamentos

    def get_empresas(self,eventos):
        empresas=[]
        results=eventos["results"]
        for event in results:
            empresas+=[event['companynumb']]
        return empresas

    def conseguir_empresas_desde_medicamentos(self,eventos_medicamentos):
        empresas=[]
        results=eventos_medicamentos["results"]
        for empresa in results:
            empresas+=[empresa['companynumb']]
        return empresas

    def conseguir_medicamentos_desde_empresa(self,eventos_empresas):
        medicamentos=[]
        results=eventos_empresas["results"]
        for event in results:
            patient=event["patient"]
            drug=patient["drug"]
            medicinalproduct=drug[0]["medicinalproduct"]
            medicamentos += [medicinalproduct]
        return medicamentos

    def get_main_page(self):
        html="""
        <html>
            <head>
            </head>
            <body>
                <form method="get" action="listDrugs">
                    <input type="submit" value="listDrugs">
                    </input>
                </form>
                <form method "get" action="listCompanies">
                    <input type="submit" value="listCompanies">
                    </input>
                </form>

                <form method="get" action="searchDrug">
                    <input type="submit" value="searchDrug">
                    </input>
                    <input type= "text" name="drug">
                    </input>
                </form>

                <form method="get" action="searchCompany">
                    <input type="submit" value="searchCompany">
                    </input>
                    <input type= "text" name="company">
                    </input>
                </form>
            </body>
        </html>
        """
        return html

    def get_html(self,componentes):
        print (componentes)

        html="""
            <html>
                <head>
                </head>
                <body>
                    <ul>
        """
        for componente in componentes:
            html+= "<li>" +componente+ "</li>"
        html+="""
                    </ul>
                </body>
            </html>

            """
        return html


    def do_GET(self):

        main_page= False
        is_medicamentos= False
        is_empresas=False
        is_empresas_en_medicamento=False
        is_medicamentos_en_empresa=False
        if self.path=='/':
            main_page=True
        elif 'listDrugs' in self.path:
            is_medicamentos=True
        elif 'listCompanies' in self.path:
            is_empresas=True
        elif 'searchDrug' in self.path:
            is_empresas_en_medicamento=True
        elif 'searchCompany' in self.path:
            is_medicamentos_en_empresa=True

        #Send response status code
        self.send_response(200)

        #Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        if main_page:
            html=self.get_main_page()
            self.wfile.write(bytes(html,"utf8"))
        elif is_medicamentos:
            event=self.get_event()
            medicamentos=self.get_medicamentos(event)
            html=self.get_html(medicamentos)
            self.wfile.write(bytes(html,"utf8"))
        elif is_empresas:
            event=self.get_event()
            empresas=self.get_empresas(event)
            html=self.get_html(empresas)
            self.wfile.write(bytes(html,"utf8"))

        elif is_empresas_en_medicamento:
            medicamento=self.path.split('=')[1]
            event=self.get_buscar_medicamento(medicamento)
            empresas=self.conseguir_empresas_desde_medicamentos(event)
            html=self.get_html(empresas)
            self.wfile.write(bytes(html,"utf8"))

        elif is_medicamentos_en_empresa:
            empresa=self.path.split('=')[1]
            event=self.get_buscar_empresa(empresa)
            empresas=self.conseguir_medicamentos_desde_empresa(event)
            html=self.get_html(empresas)
            self.wfile.write(bytes(html,"utf8"))
