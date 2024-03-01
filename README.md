# Web backend

Esta es una aplicación serverless que usa el framework [SAM (Serverless Application Model)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) y expone un backend en forma de API.

## Requisitos

Para levantar esta aplicación se debe tener instalado lo siguiente

* Python `3.11.4`
  * Instalar [pyenv](https://github.com/pyenv/pyenv) y luego
  * `pyenv install -v 3.11.4`
  * `pyernv global 3.11.4`
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
* [Docker](https://docs.docker.com/engine/install/)

## Levantar ambiente local

Para levantar el API de manera local se debe ejecutar el siguiente comando

```shell
sam build && sam local start-api
````

## Comandos útiles

Invocar función localmente

```shell
sam local invoke HealthCheckFunction --debug --event events/health_check.json
````

Levantar API de forma local

```shell
sam local start-api
````

Se puede probar haciendo un request a [http://localhost:3000/health_check](http://localhost:3000/health_check)

```shell
curl http://localhost:3000/health_check
````

## Desarrollando en AWS

Para desarrollar directamente en la nube podemos utilizar un comando que parte por desplegar un stack y luego actualizarlo en medida que vamos guardando cambios en los archivos del proyecto de manera local. Al mismo tiempo en otra consola podemos utilizar un comando que nos muestra directamente todos los logs que genere nuestro stack en AWS Cloudwatch. Los comandos son los siguientes:

Para levantar el stack sincronizado ejecutamos:

```shell
sam sync
```

y luego para obtener los logs en tiempo real:

```shell
sam logs
```

## Despliegue

Luego para hacer build de los últimos cambios y luego desplegar a AWS usamos:

```shell
sam build && sam deploy
```

## Estructura de archivos

```text
src
  api
    functions
    layers
```

## Recursos

* [Lambda docs](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
* [SAM docs](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
  * [SAM reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-reference.html)
  * [SAM CLI reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)
* [SAM Workshop](https://catalog.workshops.aws/complete-aws-sam/en-US)
* [Serverless Patterns Workshop](https://catalog.workshops.aws/serverless-patterns/en-US)
* [Powertools for AWS Lambda](https://docs.powertools.aws.dev/lambda/python/latest/)
* [Serverless Land](https://serverlessland.com/)
# cundaio-web-back
