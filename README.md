# Data_Pirates_challenge
Data Pirates Challenge Resolved!

- Projeto desenvolvido na SO linux 64 bits , utilizando browser  google chrome  versão 84.0.4147.125 64bits.
- Utilizado chromedriver na versão 84.0.4147.30.


## Dependências
* pytest==6.0.1
* selenium==3.141.0


## Instalando dependências
```
python3 -m pip install -r requirements.txt
```
## Argumentos requeridos

- --first / --f  comando requer UF desejada. 
- --second / --s  comando requer UF desejada.
- --quantity / --qtd requer a quantidade de cep a ser baixado

## obs: 
- Consulta minima 50 CEPs. 

## comand to run

```
 python3 correio.py --f "Sao Paulo" --s "Rio de Janeiro" --qtd 300
```