import json
import requests

from importlib.resources import Resource
from flask_restful import Resource, Api
from flask import Flask, render_template, request, jsonify, Response
from json import dumps
app = Flask(__name__)

api = Api(app)

@app.route('/')
def hello():
    return render_template("index.html")

class Zip(Resource):
    def get(self, zip):
        request = requests.get("https://viacep.com.br/ws/"+zip+"/json/")
        if request.status_code == 200:
            zipData = request.json()
            if zipData['uf'] == 'SP':
                if zipData['localidade'] == "São Bernardo do Campo":
                    return Response(json.dumps({"situacao": "OK"}), status=200, headers={"content-type": "application/json"})       
                if zipData['localidade'] == "São Caetano do Sul":
                    return Response(json.dumps({"situacao": "OK"}), status=200, headers={"content-type": "application/json"})       
                if zipData['localidade'] == "Santo André":
                    return Response(json.dumps({"situacao": "OK"}), status=200, headers={"content-type": "application/json"})         
                if zipData['localidade'] == "São Paulo":
                    return Response(json.dumps({"situacao": "OK"}), status=200, headers={"content-type": "application/json"})       
                if zipData['localidade'] == "Diadema":
                    return Response(json.dumps({"situacao": "OK"}), status=200, headers={"content-type": "application/json"})        
            return Response(json.dumps({"situacao": "Não atendida"}), status = 400, headers={"content-type": "application/json"})
        return Response(json.dumps({"situacao": "Não encontrado"}), status = 404, headers={"content-type": "application/json"})

api.add_resource(Zip, '/zip/<zip>') 

class Cpf(Resource):
    def get(self, cpf):
        # Remover caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))

        # Verificar se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return Response(json.dumps({"situacao": f"O CPF número: {cpf} é inválido."}), status = 400, headers={"content-type": "application/json"})

        # Verificar se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return Response(json.dumps({"situacao": f"O CPF número: {cpf} é inválido."}), status = 400, headers={"content-type": "application/json"})

        # Calcular o primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        # Verificar o primeiro dígito verificador
        if digito1 != int(cpf[9]):
            return Response(json.dumps({"situacao": f"O CPF número: {cpf} é inválido."}), status = 400, headers={"content-type": "application/json"})

        # Calcular o segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        # Verificar o segundo dígito verificador
        if digito2 != int(cpf[10]):
            return Response(json.dumps({"situacao": f"O CPF número: {cpf} é inválido."}), status = 400, headers={"content-type": "application/json"})

        # Se passar por todas as verificações, o CPF é válido
        return Response(json.dumps({"situacao": "OK"}), status=200, headers={"content-type": "application/json"})


api.add_resource(Cpf, '/cpf/<cpf>') 

class Bbq(Resource):
    def get(self, menCount, womenCount, childrenCount, hasDrink, time):
        kgmen = (float(menCount) * 0.6)/(4.0/float(time)) 
        kgwomen = (float(womenCount) * 0.5)/(4.0/float(time)) 
        kgchildren = (float(childrenCount) * 0.4)/(4.0/float(time)) 
        
        totalPerson = int(menCount) + int(womenCount) + int(childrenCount)
        
        drink = 0
        if (hasDrink == "true"):
            totalPerson = totalPerson - int(float(menCount) + float(womenCount) * 0.4)
            drink = ((float(menCount) + float(womenCount)*.4) * 0.6)/(4.0/float(time)) 
        
        softdrink = (float(totalPerson) * 0.5)/(4.0/float(time)) 
        
        bbq = {
            "total_convidados":  int(menCount) + int(womenCount) + int(childrenCount),
            "carnes": {
                "frango": f'{(kgmen + kgwomen + kgchildren) * 0.1:.2f}',
                "linguica": f'{(kgmen + kgwomen + kgchildren) * 0.3:.2f}',
                "porco": f'{(kgmen + kgwomen + kgchildren) * 0.2:.2f}',
                "bovino":f'{(kgmen + kgwomen + kgchildren) * 0.4:.2f}',
            },
            "bebidas": {
                "cervejas_litros": f'{drink:.2f}',
                "refrigerante_litros": f'{softdrink:.2f}'
            }
        }
        
        return Response(json.dumps(bbq), status=200, headers={"content-type": "application/json"})
    
class BbqPost(Resource):
    def post(self):
        menCount = request.json['menCount']
        womenCount = request.json['womenCount']
        childrenCount = request.json['childrenCount']
        hasDrink = request.json['hasDrink']
        time = request.json['time']
        
        kgmen = (float(menCount) * 0.6)/(4.0/float(time)) 
        kgwomen = (float(womenCount) * 0.5)/(4.0/float(time)) 
        kgchildren = (float(childrenCount) * 0.4)/(4.0/float(time)) 
        
        totalPerson = int(menCount) + int(womenCount) + int(childrenCount)
        
        drink = 0
        if (hasDrink == "true"):
            totalPerson = totalPerson - int(float(menCount) + float(womenCount) * 0.4)
            drink = ((float(menCount) + float(womenCount)*.4) * 0.6)/(4.0/float(time)) 
        
        softdrink = (float(totalPerson) * 0.5)/(4.0/float(time)) 
        
        bbq = {
            "total_convidados":  int(menCount) + int(womenCount) + int(childrenCount),
            "carnes": {
                "frango": f'{(kgmen + kgwomen + kgchildren) * 0.1:.2f}',
                "linguica": f'{(kgmen + kgwomen + kgchildren) * 0.3:.2f}',
                "porco": f'{(kgmen + kgwomen + kgchildren) * 0.2:.2f}',
                "bovino":f'{(kgmen + kgwomen + kgchildren) * 0.4:.2f}',
            },
            "bebidas": {
                "cervejas_litros": f'{drink:.2f}',
                "refrigerante_litros": f'{softdrink:.2f}'
            }
        }
        
        return Response(json.dumps(bbq), status=200, headers={"content-type": "application/json"})
    
api.add_resource(Bbq, '/bbq/<menCount>/<womenCount>/<childrenCount>/<hasDrink>/<time>') 
api.add_resource(BbqPost, '/bbq')

#if __name__ == "__main__":
#    print("iniciado")
#    app.run(port=5000,debug=True)