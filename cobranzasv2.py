import os
import json
from datetime import datetime

## Abre el archivo donde dejará los logs
with open('logs.txt', 'w') as archivo:
    print('---Logs Fx de cobranzas---', file=archivo)
# Carga las variables de entorno desde el archivo .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
with open(env_path, 'r') as file:
    for line in file:
        if line.strip() and not line.strip().startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

# Ahora puedes acceder a las variables de entorno cargadas
ZOHO_CLIENT_ID = os.getenv('ZOHO_CLIENT_ID')
ZOHO_CLIENT_SECRET = os.getenv('ZOHO_CLIENT_SECRET')
ZOHO_REFRESH_TOKEN = os.getenv('ZOHO_REFRESH_TOKEN')



# Muestra las variables en pantalla
#print("Contenido de .env:")
#print(f"ZOHO_CLIENT_ID: {ZOHO_CLIENT_ID}")
#print(f"ZOHO_CLIENT_SECRET: {ZOHO_CLIENT_SECRET}")
#print(f"ZOHO_REFRESH_TOKEN: {ZOHO_REFRESH_TOKEN}")




import requests

## Trae auth Token
url = f"https://accounts.zoho.com/oauth/v2/token?client_id={ZOHO_CLIENT_ID}&client_secret={ZOHO_CLIENT_SECRET}&refresh_token={ZOHO_REFRESH_TOKEN}&grant_type=refresh_token"


response = requests.post(url)

if response.status_code == 200:
    # La solicitud fue exitosa
    data = response.json()  
    # Acceder al token de acceso
    access_token = data['access_token']

    # Imprimir el token de acceso
    ##print("Token de acceso:", access_token)
else:
    print("Error al traer el access token de zoho:", response.status_code)
    
###############


url = 'https://www.zohoapis.com/crm/v2/RDAsetup'
headers = {
    'Authorization': f'Zoho-oauthtoken {access_token}'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # La solicitud fue exitosa
    data = response.json()  
    rdaSetups = data['data']
    
    ## Conseguir la data para acceder a la API de Finnegans
    # Lista para almacenar los registros que comienzan con 'Finnegans_'
    filtered_objects = []

   # Iterar sobre cada objeto en la lista
    for obj in rdaSetups:
        # Verificar si el valor de la clave 'name' comienza con 'Finnegans'
        if obj.get("Name", "").startswith("Finnegans"):
            filtered_objects.append(obj)
            
    # Get de Zoho las credenciales para acceder a Finnegans
    for obj in filtered_objects:
        if obj.get("Name", "") == "Finnegans_Client_ID":
            Finnegans_Client_ID =  obj["Valor"]
            #print("Finnegans_Client_ID", Finnegans_Client_ID)
        if obj.get("Name", "") == "Finnegans_Client_Secret":
            Finnegans_Client_Secret =  obj["Valor"]
            #print("Finnegans_Client_Secret", Finnegans_Client_Secret)
        if obj.get("Name", "") == "Finnegans_Url":
            Finnegans_Url =  obj["Valor"]
            #print("Finnegans_Url", Finnegans_Url)
        if obj.get("Name", "") == "Finnegans_EmpresaCodigo":
            Finnegans_EmpresaCodigo =  obj["Valor"]
            #print("Finnegans_EmpresaCodigo", Finnegans_EmpresaCodigo)
    
    ## Trae authenticate de Finnegans
    url_finnegs = f"https://api.teamplace.finneg.com/api/oauth/token?grant_type=client_credentials&client_id={Finnegans_Client_ID}&client_secret={Finnegans_Client_Secret}"


    response = requests.get(url_finnegs)

    if response.status_code == 200:
        # La solicitud fue exitosa
        authenticate_response = response.text 
        ##print("authenticate_response", authenticate_response)
        
        
        ##Fecha actual 
        fecha = datetime.now()        
        #print("Fecha actual:", fecha)
        with open('logs.txt', 'a') as archivo:
            print(f'Fecha de ejecución: {fecha}', file=archivo)
        
        ## Trae registros de Finnegans
        url_finnegs_records = f"https://api.teamplace.finneg.com/api/reports/RDACOMPOSICIONSALDOSCLIENTESAPI?ACCESS_TOKEN={authenticate_response}&PARAMWEBREPORT_Fecha={fecha}&PARAMWEBREPORT_Empresa={Finnegans_EmpresaCodigo}"


        response = requests.get(url_finnegs_records)

        if response.status_code == 200:
        # La solicitud fue exitosa
            finnegs_records = response.json()  
            ##print("finnegs_records", finnegs_records)
            
            ##TO DO
            ##El siguiente proceso marca como cobradas las facturas de zoho que ya no existen en finnegans
            ## Search records a zoho con el numero de cuit 
            url_zoho_search_composiciones = f'https://www.zohoapis.com/crm/v2/Composici_n_Saldo_Cliente/search?criteria=Cobrada:equals:false'
            headers = {
                'Authorization': f'Zoho-oauthtoken {access_token}'
            }

            response_comp_falta_pagar = requests.get(url_zoho_search_composiciones, headers=headers)
            
            

            
            if response_comp_falta_pagar.status_code == 200:
                    print("Recorriendo las composiciones ya existentes en busca de las cobradas")
                    # La solicitud fue exitosa
                    composiciones_faltas_de_pago = response_comp_falta_pagar.json() 
                    ##print( "ESTAS COMPOSICIONES FALTAN PAGAR")
                    ##print( composiciones_faltas_de_pago["data"])
                    for record in composiciones_faltas_de_pago["data"]:
                        print(record)
                        ##REVISAR
                        id=record["id"]
                        print(id)
                        Identificacion_Externa = record["Identificacion_Externa"]
                        sinPago = any(item["IDENTIFICACIONEXTERNA"] == Identificacion_Externa for item in finnegs_records )
                        print(sinPago)
                        
                        if (sinPago == False): 
                            ##QUIERE DECIR QUE ESTA PAGA
                            ##UPDATEA EL REGISTRO EN ZOHO Y LO MARCA COMO PAGO
                            
                            body = { "data": [{
                                                
                                                "Estado":"Pago completo",
                                                "Cobrada": True,
                                                "Importe_Secundario": 0
                                                
                                            }]}
                            url_update_composicion = f'https://www.zohoapis.com/crm/v2/Composici_n_Saldo_Cliente/{id}'
                            headers = {
                                'Authorization': f'Zoho-oauthtoken {access_token}'
                            }

                            responseUpdate = requests.put(url_update_composicion, headers=headers, data=json.dumps(body).encode('utf-8'))

                            if responseUpdate.status_code == 200:
                                # La solicitud fue exitosa
                                update_composicion = responseUpdate.json()
                                print("El Registro ",id, " fue marcado como pago: ", update_composicion) 
                                with open('logs.txt', 'a') as archivo:
                                    print(f'- El registro: {id} fue MARCADO COMO PAGO: {str(update_composicion)}', file=archivo)
                            else:
                                print("Error en el registro id: ", id ," responseUpdate:", responseUpdate) 
                                with open('logs.txt', 'a') as archivo:
                                    print(f'- Error en el registro id: {id} NO PUDO MARCARSE COMO PAGO -responseUpdate: {str(responseUpdate)}', file=archivo)   
                            
                            
            else:
                    print("Error en la busqueda de cobranzas ya existentes en zoho:", response_comp_falta_pagar.status_code)
            
            ####
            ##El siguiente proceso actualiza los montos y estados de  las facturas en ZOHO si existen
            for record in finnegs_records:
                client_cuit = record["CUIT"]
                
                
                ## Search records a zoho con el numero de cuit 
                url_zoho_search = f'https://www.zohoapis.com/crm/v2/Accounts/search?criteria=CUIT:equals:{client_cuit}'
                headers = {
                    'Authorization': f'Zoho-oauthtoken {access_token}'
                }

                response = requests.get(url_zoho_search, headers=headers)
                
                

                
                if response.status_code == 200:
                    # La solicitud fue exitosa
                    zoho_record = response.json() 
                    #print( record["data"])
                    array_length = len(zoho_record["data"]) 
                    if array_length  > 0 :
                        cliente_id =  zoho_record["data"][0]["id"]
                        #print(cliente_id)
                        composicion_de_saldo = {
                            "Cuenta": cliente_id
                        }
                    id_comprobante_finnegans = record["COMPROBANTE"]    
                    ## Revisa si la composición ya existe y actualiza
                    url_composicion_search = f'https://www.zohoapis.com/crm/v2/Composici_n_Saldo_Cliente/search?criteria=Name:equals:{id_comprobante_finnegans}'
                    headers = {
                        'Authorization': f'Zoho-oauthtoken {access_token}'
                    }

                    response = requests.get(url_composicion_search, headers=headers)

                    if response.status_code == 200:
                        # La solicitud fue exitosa
                        composicion_already_exist_record = response.json()
                        composicion = composicion_already_exist_record["data"][0]
                        identificacion_externa = composicion["Identificacion_Externa"]
                        
                        if identificacion_externa.startswith("FAC"):
                            composicion_id = composicion["id"]
                            composicion_importe_ppal = composicion["Importe_Principal"]
                            composicion_pago_parcial = composicion["Pago_parcial"]
                            
                            print("id comp a updatear: ",composicion_id )
                            
                            ## Mapeo de campos para la modificación de registros en Zoho
                            fecha_vto = datetime.strptime(record["FECHAVTO"], '%Y-%m-%d').strftime('%Y-%m-%d')
                            fecha_formateada = datetime.strptime(record["FECHA"], '%Y-%m-%d').strftime('%Y-%m-%d')
                            fecha_compr = datetime.strptime(record["FECHACOMPROBANTE"], '%Y-%m-%d').strftime('%Y-%m-%d')
                            
                            
                                
                            composicion_de_saldo["Vencimiento"] = fecha_vto
                            composicion_de_saldo["Fecha"] = fecha_formateada
                            composicion_de_saldo["Fecha_de_Comprobante"] = fecha_compr
                            composicion_de_saldo["Name"] = id_comprobante_finnegans
                            composicion_de_saldo["Organizacion"] = record["ORGANIZACION"]
                            composicion_de_saldo["CUIT"] = record["CUIT"]
                            composicion_de_saldo["Importe_Principal"] = int(record["IMPORTEMONPPAL"])
                            composicion_de_saldo["Importe_Secundario"] = int(record["IMPORTEMONSECUNDARIA"])
                            composicion_de_saldo["Identificacion_Externa"] = record["IDENTIFICACIONEXTERNA"]
                            composicion_de_saldo["Dias_Mora"] = record["DIASMORA"]

                            if record["DIASMORA"] > 0 and record["DIASMORA"] < 31:
                                composicion_de_saldo["Estado"] = "Deuda 1 a 30"
                            elif record["DIASMORA"] > 30 and record["DIASMORA"] < 61:
                                composicion_de_saldo["Estado"] = "Deuda 31 a 60"
                            elif record["DIASMORA"] > 60 and record["DIASMORA"] < 91:
                                composicion_de_saldo["Estado"] = "Deuda 61 a 90"
                            elif record["DIASMORA"] > 90:
                                composicion_de_saldo["Estado"] = "Alerta deuda +90"
                            elif record["DIASMORA"] == 0:
                                composicion_de_saldo["Estado"] = "Por vencer"
                            
                            
                            #if composicion_importe_ppal < record["IMPORTEMONPPAL"] or composicion_pago_parcial == True:
                            #    ##Si el saldo es menor se tilda como pago parcial
                            #    composicion_de_saldo["Pago_parcial"] = True
                            #    composicion_de_saldo["Estado"] = "Pago parcial"
                            
                                
                            #if composicion_de_saldo["Importe_Principal"] == 0:
                            #    composicion_de_saldo["Pago_parcial"] = False    
                            #    composicion_de_saldo["Estado"] = "Pago completo"
                            
                                
                            
                            body = { "data": [composicion_de_saldo]}
                    
                            #print("objeto a updatear: ", body )
                            
                            ##UPDATEA EL REGISTRO EN ZOHO
                            url_update_composicion = f'https://www.zohoapis.com/crm/v2/Composici_n_Saldo_Cliente/{composicion_id}'
                            headers = {
                                'Authorization': f'Zoho-oauthtoken {access_token}'
                            }

                            responseUpdate = requests.put(url_update_composicion, headers=headers, data=json.dumps(body).encode('utf-8'))

                            if responseUpdate.status_code == 200:
                                # La solicitud fue exitosa
                                update_composicion = responseUpdate.json()
                                print("El Registro ",composicion_id, " fue actualizado correctamente: ", update_composicion) 
                                with open('logs.txt', 'a') as archivo:
                                    print(f'- El registro: {composicion_id} fue actualizado correctamente: {str(update_composicion)}', file=archivo)
                            else:
                                print("Error en el registro id: ", composicion_id ," responseUpdate:", responseUpdate) 
                                with open('logs.txt', 'a') as archivo:
                                    print(f'- Error en el registro id: {composicion_id} responseUpdate: {str(responseUpdate)}', file=archivo)   
                            
                    else:
                        print("Error en la busqueda de una composición ya existente:", response.status_code)    

                else:
                    print("Error en la busqueda de una cuenta ya existente:", response.status_code)    
        
        else:
            print("Error en traer registros de finnegans:", response.status_code)
        
        
    else:
        print("Error al traer el authenticate de finnegans:", response.status_code)
    
else:
    print("Error al traer los datos del modulo RDA SETUP de zoho:", response.status_code)