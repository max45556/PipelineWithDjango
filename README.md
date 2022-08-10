```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```

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


<span style="color: green"> Some green text </span>

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
In caso di accesso riuscito, vengono restituite le seguenti informazioni:

  - *access*: token di accesso (stringa)
  - *refresh*: Aggiorna di refresh (stringa)
  - *user_id*: ID dell'utente che si è autenticato (int)  
*Richiesta*: POST 127.0.0.1:8000/login/  
*Header*: Content-Type: application/json  
*Body*:  
- **username**: 'username'
- **password**: 'password'

*Standard Response*: 200 OK

### REFRESH TOKEN
Viene utilizzato per ottenere un nuovo token di accesso utilizzando il token di aggiornamento fornito all'accesso. Restituisce un nuovo token di accesso.

*Richiesta*: POST 127.0.0.1:8000/login/refresh/  
*Header*: Content-Type: application/json  
*Body*:  
- **refresh**: 'refresh token'

*Standard Response*: 200 OK  

### CHANGE PASSWORD
Consente a un utente di modificare la password utilizzando la vecchia password

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
Consente a un utente di aggiornare il proprio profilo. Restituire dati utente aggiornati

*Richiesta*: POST 127.0.0.1:8000  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token  

*Body*:  
- **username**: 'username'
- **first_name**: 'first_name'
- **last_name**: 'last_name'
- **email**: 'email'

*Standard Response*: 200 OK

### GET USER DATA
Consente a un utente di vedere il suo profilo. Restituisci i dati del profilo

*Richiesta*: GET 127.0.0.1:8000  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token  
*Body*: empty  
*Standard Response*: 200 OK

### DELETE PROFILE
Consente a un utente di eliminare il proprio profilo. Nessun dato viene restituito

*Richiesta*: DELETE 127.0.0.1:8000  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*: empty  
*Standard Response*: 200 OK

## Gestione degli snippet

### CREA NUOVO SNIPPET
Con questa operazione è possibile creare uno snippet. L'unico campo obbligatorio è quello del codice ma potrebbero essere fornite altre informazioni per una migliore gestione dello snippet personale.

*Richiesta*: POST 127.0.0.1:8000/snippets/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- code: 'code' REQUIRED
- title: 'title' FACULTATIVE
- language: 'code language' FACULTATIVE
- executable: 'bool' FACULTATIVE

*Standard Response*: 200 OK

### AGGIORNA UNO SNIPPET ESISTENTE
Con questa operazione è possibile modificare uno snippet esistente. Non sono obbligatori i campi obbligatori e verranno modificati solo i campi superati. È necessario specificare lo snippet tramite l'id.

*Richiesta*: POST 127.0.0.1:8000/snippets/snippet_id/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- code: 'code' FACULTATIVE
- title: 'title' FACULTATIVE
- language: 'code language' FACULTATIVE
- executable: 'bool' FACULTATIVE

*Standard Response*: 200 OK

### ELIMINA UNO SNIPPET ESISTENTE
Con questa operazione è possibile eliminare uno snippet esistente. Non sono obbligatori i campi in budy ma è necessario specificare lo snippet da eliminare tramite l'id.

*Richiesta*: DELETE 127.0.0.1:8000/snippets/snippet_id/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*: empty  
*Standard Response*: 200 OK

### OTTIENI SNIPPET DALL'ID
Con questa operazione è possibile vedere uno snippet specificato attraverso il suo id

*Richiesta*: GET 127.0.0.1:8000/snippets/snippet_id/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*: empty  
*Standard Response*: 200 OK

### OTTIENI GLI SNIPPET DELL'UTENTE
Con questa operazione è possibile vedere gli snippet salvati dagli utenti

*Richiesta*:GET 127.0.0.1:8000/snippets/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*: empty  
*Standard Response*: 200 OK

## Operazioni sugli snippet

Di seguito sono riportati alcuni uri utilizzati per eseguire operazioni sul codice. Ad esempio, puoi chiedere al server di re-indentare il codice o verificare che sia eseguibile. Per implementare le funzioni sono state utilizzate varie librerie che verranno spiegate in dettaglio in seguito. Quasi tutte le funzionalità sono accessibili tramite tre tipi di richieste: una richiesta GET, una richiesta POST e una richiesta PATCH.

GET viene utilizzato quando si desidera agire su uno snippet archiviato sul server. Per questo motivo, nella URI è necessario specificare l'ID dello snippet su cui eseguire l'operazione. Ad esempio, per eseguire l'operazione di individuazione del linguaggio di programmazione dello snippet, che ha id uguale a 2, occorre fare la seguente richiesta:

          GET 127.0.0.1:8000/snippets/2/detect/

Il POST viene utilizzato quando si vuole agire su uno snippet che però non è memorizzato sul server e che viene passato al server. Per questo, quando la richiesta viene effettuata tramite l'uri è necessario specificare nel body un parametro che contiene il codice su cui agire, 'codice': 'codice da analizzare'. Ad esempio, per identificare il linguaggio di programmazione dello snippet passato al server, è necessario fare:

          POST 127.0.0.1:8000/snippets/detect/ and in the body you need to insert the snippet

Il PATCH funziona quasi identico a Get. La patch serve per eseguire operazioni su uno snippet salvato sul server e la differenza rispetto a get è che quando si ottiene l'output, il valore ottenuto viene salvato nel db. Ad esempio, quando viene eseguita l'operazione di identificazione del linguaggio di programmazione snippet e si ottiene il risultato, questo valore viene memorizzato nel campo della lingua dell'istanza di questo snippet sul db. Ad esempio, per eseguire l'operazione di individuazione del linguaggio di programmazione dello snippet, che ha id uguale a 2, occorre fare la seguente richiesta:

          PATCH 127.0.0.1:8000/snippets/2/detect/

se l'output restituito è Python, il valore Python verrà inserito nel campo della lingua dello snippet 2.

### RILEVA LA LINGUA DEGLI SNIPPET

Attraverso questa funzionalità è possibile identificare il linguaggio di programmazione di un particolare snippet. L'identificazione avviene tramite Guesslang, un software di deep learning open source che è stato addestrato con oltre un milione di file di codice sorgente. Questo supporta più di 50 linguaggi di programmazione e rileva il linguaggio di programmazione corretto con una precisione superiore al 90%. Guesslang può essere utilizzato come strumento di interfaccia a riga di comando o come modulo Python.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/detect
- PATCH 127.0.0.1:8000/snippets/snippet_id/detect/
- POST 127.0.0.1:8000/snippets/detect/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- PATCH REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'language':'language of the snippet'}

### REINDENTAZIONE DEL CODICE

Attraverso questa operazione è possibile indentare il codice. Per fare ciò è stata utilizzata una libreria chiamata Black. Il nero è il formattatore di codice Python senza compromessi. Usandolo, accetti di cedere il controllo sulle minuzie della formattazione manuale. In cambio, Black ti dà velocità, determinismo e libertà dal fastidioso stile pycode sulla formattazione. Il codice annerito ha lo stesso aspetto indipendentemente dal progetto che stai leggendo. La formattazione diventa trasparente dopo un po' e puoi invece concentrarti sul contenuto. Il nero rende la revisione del codice più veloce producendo le differenze più piccole possibili.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/reindent
- PATCH 127.0.0.1:8000/snippets/snippet_id/reindent/
- POST 127.0.0.1:8000/snippets/reindent/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- PATCH REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'code':'code modified'}

### ORDINAMENTO DELLE IMPORTAZIONI DEL CODICE

tramite questa operazione è possibile ordinare le importazioni all'interno del codice. Per fare ciò è stata utilizzata una libreria chiamata Isort. Isort è un'utilità / libreria Python per ordinare le importazioni in ordine alfabetico e separate automaticamente in sezioni e per tipo.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/order
- PATCH 127.0.0.1:8000/snippets/snippet_id/order/
- POST 127.0.0.1:8000/snippets/order/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- PATCH REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'code':'code with ordered imports'}

### PYLINT

Pylint è uno strumento che controlla gli errori nel codice Python, cerca di imporre uno standard di codifica e cerca gli odori del codice. Può anche cercare determinati errori di tipo, può consigliare suggerimenti su come eseguire il refactoring di determinati blocchi e può offrire dettagli sulla complessità del codice.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/pylint
- PATCH 127.0.0.1:8000/snippets/snippet_id/pylint/
- POST 127.0.0.1:8000/snippets/pylint/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- PATCH REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'output':'output of pylint'}

### PYFLAKES

Un semplice programma che controlla gli errori dei file sorgente Python. Pyflakes analizza i programmi e rileva vari errori. Funziona analizzando il file sorgente, non importandolo, quindi è sicuro da usare su moduli con effetti collaterali. È anche molto più veloce.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/pyflakes
- PATCH 127.0.0.1:8000/snippets/snippet_id/pyflakes/
- POST 127.0.0.1:8000/snippets/pyflakes/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- PATCH REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'output':'output of pyflakes'}

### FLAKE8

Flake8 è un wrapper attorno a questi strumenti: lo script McCabe di PyFlakes pycodestyle di Ned Batchelder. Flake8 esegue tutti gli strumenti lanciando il singolo comando flake8. Visualizza gli avvisi in un output unito per file.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/flake8
- PATCH 127.0.0.1:8000/snippets/snippet_id/flake8/
- POST 127.0.0.1:8000/snippets/flake8/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- PATCH REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'output':'output of flake8'}

### MYPY

Mypy è un controllo del tipo statico opzionale per Python che mira a combinare i vantaggi della digitazione dinamica (o "anatra") e della digitazione statica. Mypy combina la potenza espressiva e la comodità di Python con un potente sistema di tipi e un controllo del tipo in fase di compilazione. Il tipo Mypy controlla i programmi Python standard; eseguili usando qualsiasi VM Python praticamente senza sovraccarico di runtime.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/mypy
- PATCH 127.0.0.1:8000/snippets/snippet_id/mypy/
- POST 127.0.0.1:8000/snippets/mypy/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- PATCH REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'output':'output of mypy'}

### ESECUZIONE DEL CODICE

L'esecuzione del codice consente di testare l'esecuzione di uno snippet. Il server risponde True o False a seconda che sia eseguibile o meno.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/execute
- PATCH 127.0.0.1:8000/snippets/snippet_id/execute/
- POST 127.0.0.1:8000/snippets/execute/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- PATCH REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'executable': TRUE or FALSE}
