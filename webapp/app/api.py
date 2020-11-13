import pandas as pd
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from classifier import classify

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('solicitacao_id', type = str, action='append')
parser.add_argument('quadro_clinico', type = str, action='append')

# Requisição parametros solicitacao_id e texto.
class TodoList(Resource):
    def post(self):
        args = parser.parse_args() # HERE IS ALL THE INFORMATION THAT IS SEND FROM THE USER.
        solicitacao_df = pd.DataFrame(args['solicitacao_id'], columns=['SOLICITACAOID'])
        text_df = pd.DataFrame(args['quadro_clinico'], columns=['QUADROCLINICO'])
        solicitacaoid = solicitacao_df['SOLICITACAOID'].values
        texts = text_df['QUADROCLINICO'].values
        preds = classify(solicitacaoid, texts)
        return preds
api.add_resource(TodoList, '/regular')

if __name__ == '__main__':
    app.run(debug=True)
