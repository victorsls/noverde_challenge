# Desafio Noverde - Engenheiro de Software Senior

## Requisitos
Para executar a aplicação é necessário ter Docker e Docker Compose instalado no PC.

## Clone do repositório
```bash
git clone https://github.com/victorsls/noverde_challenge.git
```
## Entre no diretório do projeto
```bash
cd noverde_challenge
```

## Execute o docker
```bash
docker-compose up
```

## Criar o Banco de Dados
#### O projeto utiliza a biblioteca django-extensions e vamos utilizar o comando reset_db para criar o banco. (Execute o comando em uma nova aba)
#### OBS: Este comando deleta o banco atual caso ele já exista e depois cria novamente.

```bash
docker-compose exec backend python manage.py reset_db
```

## Volte a aba anterior cancele a execução do docker e rode o comando novamente
```bash
docker-compose up
```

## Na outra aba execute o comando para criar um usuário:
```bash
docker-compose exec backend python manage.py createsuperuser
```

## Endpoint de Autenticação
### **POST** `/obtain-auth-token/`
```json
{
    "username": "",
    "password": ""
}
```

### Todos os Endpoints precisam de autenticação, adicione o Token no Header da requisição
```json
{
   "Authorization": "Token {token}"
}
```

### **POST** `/loan`
#### Request Schema
```json
{
    "name": "Nome do cliente",
    "cpf": "CPF do cliente",
    "birth_date": "Data de nascimento do cliente",
    "amount": "Valor desejado, entre R$ 1.000,00 e R$ 4.000,00",
    "terms": "Quantidade de parcelas desejadas. Valores disponíveis: 6, 9 ou 12",
    "income": "Renda mensal do cliente"
}
```

### **GET** `/loan/:id`
#### Response Schema
```json
{
    "id": "5198cc01-8326-480c-acf2-688c7eedb6d7",
    "status": "completed",
    "result": "approved",
    "refused_policy": null,
    "amount": 5000.0,
    "terms": 12
}
```