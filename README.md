# O que é
Implementação da API do algoritmo de ML para regulação médica.

# Como utilizar
## Passo-a-passo
- Clonar o repositório:
git clone https://github.com/ajuricabense/tele-regula-ML.git

- Colocar os arquivos **model.hdf5** na pasta webapp/app/weights e **tokenizer.pkl.z** na pasta webapp/app/tokenizer.  
- Construir a imagem do container:
```
cd telessauders-regulacao`
docker-compose build
```
- Iniciar o container
```
docker-compose up -d
```

## Testes
O algoritmo precisa de 2 entradas solicitacao_id e quadro_clinico. O resultado será um objeto com as variaveis: SOLICITACAOID, PROBABILIDADE, DECISAO, DATA e ASSINATURA. Para realizar a solicitação é necessario fazer uma requisição POST no endereço [http://localhost:8080/regular](http://localhost:8080/regular).

A imagem teste.png mostra um teste utilizando a ferramenta Postman. O input são tres textos a ser regulados com seu respectivo id. O output e o conjunto dos 3 objetos com seu respectivo resultado.
![GitHub Logo](/images/example.png)
