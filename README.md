# Snippet Analizer

[![Build](https://github.com/WebGoat/WebGoat/actions/workflows/build.yml/badge.svg?branch=develop)](https://github.com/WebGoat/WebGoat/actions/workflows/build.yml)
[![java-jdk](https://img.shields.io/badge/java%20jdk-17-green.svg)](https://jdk.java.net/)
[![OWASP Labs](https://img.shields.io/badge/OWASP-Lab%20project-f7b73c.svg)](https://owasp.org/projects/)
[![GitHub release](https://img.shields.io/github/release/WebGoat/WebGoat.svg)](https://github.com/WebGoat/WebGoat/releases/latest)
[![Gitter](https://badges.gitter.im/OWASPWebGoat/community.svg)](https://gitter.im/OWASPWebGoat/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Discussions](https://img.shields.io/github/discussions/WebGoat/WebGoat)](https://github.com/WebGoat/WebGoat/discussions)

# Scopo

L'obbiettivo di questo progetto è stato quello di creare, attraverso, [DJANGO REST FRAMEWORK](https://www.django-rest-framework.org/) delle Web API che permettano di effettuare varie attività su snippet di codice scritti in Python. Procederemo quindi
ad illustrare quelle che sono le API create, le loro funzionalità e attraverso quali metodi accerdervi.Le API sono pensate per
essere integrate sia all'interno di un applicativo che dentro una pipeline CI/CD e per dimostrare ciò è stato creato:

 - un software con una semplice interfaccia e che fornisci degli automatismi per agire sugli snippet. Questo
  astrae le modalità di interazione con le API essendo pensato per un pubblico non geek.

- una pipeline CI/CD che presenta come stadi le attività svolte dalle API

# Funzionamento della API

Per utilizzare l'API è necessario registrarsi. Dopo la registrazione un utente può svolgere le seguenti funzioni:
- Gestire il profilo
- Gestire gli snippet personali che ha memorizzato
- Effettuare delle operazione sugli snippet

## Gestione del profilo

### REGISTRAZIONE
Per utilizzare le funzionalità offerte dall'applicazione è necessario essere registrati. Dopo la fase di registrazione, un utente può effettuare il login. Un utente può decidere di eliminare il proprio profilo, dopo averlo creato, in qualsiasi momento.

*Richiesta*: POST 127.0.0.1:8000/register/  
*Header*: Content-Type: application/json    
*Body*:  
- **username**: 'username'
- **password**: 'password'
- **password2**: 'password2'
- **email**: 'email'
- **first_name**: 'first_name'
- **last_name**: 'last_name'

*Standard Response*: 201 Created

### LOGIN
Effettuando il login, un utente può ottenere un token di accesso attraverso il quale sfruttare le funzioni del server.
In caso di accesso riuscito, vengono restituite le seguenti informazioni:<br/>
  - *access*: token di accesso (stringa)
  - *refresh*: Aggiorna di refresh (stringa)
  - *user_id*: ID dell'utente che si è autenticato (int)

*Richiesta*: POST 127.0.0.1:8000/login/<br/>
*Header*: Content-Type: application/json<br/>
*Body*:<br/>
- **username**: 'username'
- **password**: 'password'

*Standard Response*: 200 OK

### REFRESH TOKEN
Viene utilizzato per ottenere un nuovo token di accesso utilizzando il token di aggiornamento fornito all'accesso. Restituisce un nuovo token di accesso.<br/>
*Richiesta*: POST 127.0.0.1:8000/login/refresh/<br/>
*Header*: Content-Type: application/json<br/>
*Body*:
- **refresh**: 'refresh token'

*Standard Response*: 200 OK

### CHANGE PASSWORD
Consente a un utente di modificare la password utilizzando la vecchia password<br/>
*Richiesta*: PUT 127.0.0.1:8000

*Header*:
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- **password**: 'password'
- **password2**: 'password2'
- **old_password**: 'old_password'

*Standard Response*: 200 OK

### UPDATE PROFILE
Consente a un utente di aggiornare il proprio profilo. Restituire dati utente aggiornati.<br/>
*Richiesta*: POST 127.0.0.1:8000<br/>
*Header*:
- Content-Type: application/json  
- Authorization: Bearer + Access Token<br/>
*Body*:  
- **username**: 'username'
- **first_name**: 'first_name'
- **last_name**: 'last_name'
- **email**: 'email'<br/>
*Standard Response*: 200 OK

### GET USER DATA
Consente a un utente di vedere il suo profilo. Restituisci i dati del profilo<br/>
*Richiesta*: GET 127.0.0.1:8000<br/>
*Header*:
- Content-Type: application/json  
- Authorization: Bearer + Access Token<br/>
*Body*: empty<br/>
*Standard Response*: 200 OK

### DELETE PROFILE
Consente a un utente di eliminare il proprio profilo. Nessun dato viene restituito<br/>
*Richiesta*: DELETE 127.0.0.1:8000<br/>
*Header*:
- Content-Type: application/json  
- Authorization: Bearer + Access Token<br/>
*Body*: empty<br/>
*Standard Response*: 200 OK
