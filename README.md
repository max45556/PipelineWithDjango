# Snippet Analizer

[![Build](https://github.com/WebGoat/WebGoat/actions/workflows/build.yml/badge.svg?branch=develop)](https://github.com/WebGoat/WebGoat/actions/workflows/build.yml)
[![java-jdk](https://img.shields.io/badge/java%20jdk-17-green.svg)](https://jdk.java.net/)
[![OWASP Labs](https://img.shields.io/badge/OWASP-Lab%20project-f7b73c.svg)](https://owasp.org/projects/)
[![GitHub release](https://img.shields.io/github/release/WebGoat/WebGoat.svg)](https://github.com/WebGoat/WebGoat/releases/latest)
[![Gitter](https://badges.gitter.im/OWASPWebGoat/community.svg)](https://gitter.im/OWASPWebGoat/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Discussions](https://img.shields.io/github/discussions/WebGoat/WebGoat)](https://github.com/WebGoat/WebGoat/discussions)

# Scopo

L'obbiettivo di questo progetto è stato quello di creare, attraverso, [DJANGO REST FRAMEWORK](https://www.django-rest-framework.org/) delle Web API che permettano di effettuare varie attività su snippet di codice scritti in Python. Procederemo quindi ad illustrare quelle che sono le API create, le loro funzionalità e attraverso quali metodi accerdervi.Le API sono pensate per essere integrate sia all'interno di un applicazione che dentro una pipeline CI/CD e per dimostrare ciò è stato creato:

 - un software con una semplice interfaccia e che fornisci degli automatismi per agire sugli snippet. Questo
  astrae le modalità di interazione con le API essendo pensato per un pubblico non esperto.

- una pipeline CI/CD che presenta come stadi le attività svolte dalle API.

# Funzionamento delle API

Per utilizzare l'API è necessario registrarsi. Dopo la registrazione un utente può svolgere le seguenti funzioni:
- Gestire il profilo
- Gestire gli snippet personali che ha memorizzato
- Effettuare delle operazione sugli snippet

## Gestione del profilo

Questo elenco comprende una serie di API create per la gestione del profilo utente. Le API sono pensate per essere integrate in un ambiente multi-utente e posso quindi gestire l'esecuzione discrimando tra diversi i diversi attori che interagiscono con i servizi.

### REGISTRAZIONE

Per utilizzare le funzionalità offerte dalle API è necessario essere registrati. Dopo la fase di registrazione, un utente può effettuare il login utilizzando i dati appena inseriti e può ovviamente decidere di eliminare il proprio profilo in qualsiasi momento.Per la registazione sono necessari tutti i campi successivamente esposti nel body ed al termine delle registrazione vengono riportati i dati dell'utente.

*Richiesta*: POST 127.0.0.1:8000/register/  
*Header*: Content-Type: application/json    
*Body*:  
- **username**: 'username'
- **password**: 'password'
- **password2**: 'password2'
- **email**: 'email'
- **first_name**: 'first_name'
- **last_name**: 'last_name'

*Standard Response Code*: 201 Created
*Standard Response*:  
{
    '*username*': 'username',
    '*email*': 'email',
    '*first_name*': 'first name',
    '*last_name*': 'last name'
}

### LOGIN
Effettuando il login un utente può ottenere un token di accesso attraverso il quale sfruttare le API. Insieme ad esso è restituito anche un token di refresh usato per ottenere un nuovo token di accesso e uno user_id che vedremo successivamente come sarà utilizzato.

*Richiesta*: POST 127.0.0.1:8000/login/  
*Header*: Content-Type: application/json  
*Body*:  
- **username**: 'username'
- **password**: 'password'

*Standard Response Code*: 200 OK  
*Standard Response*:
{
  *'access'*: 'token di accesso' (stringa)
  *'refresh'*: 'token di refresh' (stringa)
  *'user_id'*: 'ID dell'utente che si è autenticato' (int)
}

### TOKEN DI REFRESH
Viene utilizzato per ottenere un nuovo token di accesso utilizzando il token di refresh fornito al login. Questa restituisce un nuovo token di accesso.

*Richiesta*: POST 127.0.0.1:8000/login/refresh/  
*Header*: Content-Type: application/json  
*Body*:  
- **refresh**: 'refresh token'

*Standard Response Code*: 200 OK  
*Standard Response*:  
- *'access'*: ìtoken di accesso' (stringa)

### MODIFICA DELLA PASSWORD UTENTE
Consente a un utente di modificare la password utilizzando la vecchia password. Specifica se la password è stata correttamente modificata.

*Richiesta*: PUT 127.0.0.1:8000  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token  
*Body*:  
- **password**: 'password'
- **password2**: 'password2'
- **old_password**: 'old_password'

*Standard Response Code*: 200 OK  
*Standard Response*: "Data correctly Modified"

### AGGIORNAMENTO DEL PROFILO
Consente a un utente di aggiornare il proprio profilo. Se la modifica è avvenuta correttamente restiutisce i dati aggiornati di un utente.

*Richiesta*: POST 127.0.0.1:8000  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token  

*Body*:  
- **username**: 'username'
- **first_name**: 'first_name'
- **last_name**: 'last_name'
- **email**: 'email'

*Standard Response Code*: 200 OK
*Standard Response*:  
{
  *'username'*: 'username'
  *'first_name'*: 'first_name'
  *'last_name'*: 'last_name'
  *'email'*: 'email'
}

### VISUALIZZAZIONE DEI DATI PERSONALI
Consente di visualizzare i dati riguardanti il suo profilo. Restituisci se la richiesta è stata effettuata correttamente i dati del profilo.

*Richiesta*: GET 127.0.0.1:8000  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token  
*Body*: empty  
*Standard Response Code*: 200 OK
*Standard Response*:  
{
  *'username'*: 'username'
  *'first_name'*: 'first_name'
  *'last_name'*: 'last_name'
  *'email'*: 'email'
}

### ELIMINAZIONE DEL PROFILO
Consente a un utente di eliminare il proprio profilo. Qualora l'operazione fosse stata effettuata con successo viene segnalato ciò.

*Richiesta*: DELETE 127.0.0.1:8000  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*: empty  
*Standard Response Code*: 200 OK  
*Standard Response*:
{
  *'result'*: 'user delate'
}

## Gestione degli snippet

Come detto le API sono pensate per essere utilizzate da più utenti e questi possono anche operare su snippet precedentemente creati. Un utente può infatti creare un suo snippet, recuperarlo a piacimento dal db ed effettuare su di esso una serie di operazioni. Per la gestione degli snippet 'personali' sono state creare diverse API.

### CREAZIONE DI UN NUOVO SNIPPET
Con questa operazione è possibile creare uno snippet personale. L'unico campo obbligatorio è quello che contiene il codice ma potrebbero essere fornite altre informazioni per una migliore gestione dello stesso. I campi non precisati assumeranno valori di default.

*Richiesta*: POST 127.0.0.1:8000/snippets/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- code: 'code' REQUIRED
- title: 'title' FACULTATIVE
- language: 'code language' FACULTATIVE
- executable: 'bool' FACULTATIVE

*Standard Response Code*: 200 OK  
*Standard Response*:
{
      "*id*": 13,
      "*title*": "Mutable Argoument",
      "*code*": "def    append(n,  l = None):\n  if l is None:\n    l = [     ]\n  l.append(    n)\n  return l\n\nappend(0) # [0]\nappend(     1) # [1]",
      "*owner*": "admin"        -> non era stato specificato
      "*language": "unknown",   -> non era stato specificato
      "*executable*": false,    -> non era stato specificato
}

### MODIFICA DI UNO SNIPPET ESISTENTE
Con questa operazione è possibile modificare uno snippet esistente. Tutti i campi sono facoltativi e quelli non specificati continueranno ad avere il valore precedente. È necessario specificare lo snippet che si intende modificare attraverso il suo id. Questo viene fornito al momento della creazione dello snippet o è possibile ottenerlo in un secondo momento.

*Richiesta*: POST 127.0.0.1:8000/snippets/snippet_id/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- code: 'code' FACULTATIVE
- title: 'title' FACULTATIVE
- language: 'code language' FACULTATIVE
- executable: 'bool' FACULTATIVE

*Standard Response Code*: 200 OK   
*Standard Response*:  
{
      "*id*": 13,
      "*title*": "Mutable Argoument",
      "*code*": "def    append(n,  l = None):\n  if l is None:\n    l = [     ]\n  l.append(    n)\n  return l\n\nappend(0) # [0]\nappend(     1) # [1]",
      "*owner*": "admin"       
      "*language": "unknown",   
      "*executable*": false,    
}

### ELIMINARE UNO SNIPPET ESISTENTE
Con questa operazione è possibile eliminare uno snippet esistente. Non è richiesto alcun campo all'interno del body ma è necessario specificare lo snippet da eliminare tramite il suo id.

*Richiesta*: DELETE 127.0.0.1:8000/snippets/snippet_id/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*: empty  
*Standard Response Code*: 204 NO CONTENT  
{
    "*detail*": "snippet removed"
}


### VISUALIZZAZIONE DI UNO SNIPPET DALL'ID
Con questa operazione è visualizzare uno snippet personale specificato il suo id.

*Richiesta*: GET 127.0.0.1:8000/snippets/snippet_id/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*: empty  
*Standard Response Code*: 200 OK  
*Standard Response*:  
{
    "id": 8,
    "title": "difference",
    "code": "def difference(a, b):\n    set_a = set(a)\n    set_b = set(b)\n    comparison = set_a.difference(set_b)\n    return list(comparison)\n\n\ndifference([1,2,3], [1,2,4]) # [3]",
    "language": "Python",
    "executable": false,
    "owner": "admin"
}

### VISUALIZZAZIONE DI TUTTI GLI SNIPPET MEMORIZZATI
Con questa operazione è possibile vedere tutti gli snippet che un utente ha memorizzato.

*Richiesta*:GET 127.0.0.1:8000/snippets/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*: empty  
*Standard Response*: 200 OK
*Standard Response*:  
...
{
    "id": 8,
    "title": "difference",
    "code": "def difference(a, b):\n    set_a = set(a)\n    set_b = set(b)\n    comparison = set_a.difference(set_b)\n    return list(comparison)\n\n\ndifference([1,2,3], [1,2,4]) # [3]",
    "language": "Python",
    "executable": false,
    "owner": "admin"
}
...

## Operazioni sugli snippet

Di seguito sono riportati le API utilizzate per eseguire delle operazioni sugli snippet. Per eseguire le attività previste sono state utilizzate varie librerie che verranno illustrate in seguito. Quasi tutte le funzionalità sono accessibili tramite tre tipi di richieste: GET, POST e PATCH.

i metodi GET vengono utilizzato quando si desidera agire su uno snippet memorizzato sul server. Per questo motivo nelle richieste GET è necessario specificare l'ID dello snippet su cui eseguire l'operazione. Ad esempio, per eseguire l'operazione di individuazione del linguaggio di programmazione dello snippet con id 2 occorre fare la seguente richiesta:

          GET 127.0.0.1:8000/snippets/2/detect/

i metodi POST vengono utilizzati quando si desidera agire su uno snippet *non* memorizzato sul server. Nel body della richiesta è infatti necessario specifiacare un parametro contenente il codice su affettuare l'attività: 'code': 'codice da analizzare'. Le richieste post si prestano nel momento in cui si voglione utilizzare le funzionalità su snippet che non si vuole vengano memorizzati nel db. Ad esempio, per eseguire l'operazione di individuazione del linguaggio di programmazione su uno snippet occorre fare la seguente richiesta:

          POST 127.0.0.1:8000/snippets/detect/ e specificare nel body il codice da analizzare

I metodi PATCH funzionano in modo quasi identico ai GET. I metodi PATCH servono per eseguire operazioni su uno snippet memorizzato sul server e la differenza rispetto ai metodi GET è che, una volta ottenuto l'output, le modifiche effettaute vengono salvato nel db. Ad esempio, quando viene eseguita l'operazione di identificazione del linguaggio di programmazione e si ottiene il risultato, questo valore viene memorizzato nel campo linguaggio di questo snippet. Ad esempio, per eseguire l'operazione di individuazione del linguaggio di programmazione dello snippet, che ha id 2, occorre fare la seguente richiesta:

          PATCH 127.0.0.1:8000/snippets/2/detect/

se l'output restituito è Python, il valore Python verrà inserito nel campo della lingua dello snippet 2.

### IDENTIFICAZIONE DEL LINGUAGGIO DELLO SNIPPET

Attraverso questa funzionalità è possibile identificare il linguaggio di programmazione di un particolare snippet. L'identificazione avviene tramite Guesslang, un software di deep learning Open source, che è stato addestrato con oltre un milione di sorgenti. Questo supporta più di 50 linguaggi di programmazione e rileva il linguaggio di programmazione corretto con una precisione superiore al 90%.

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

Attraverso questa operazione è possibile indentare il codice dello snippet. Per fare ciò è stata utilizzata una libreria chiamata Black che offre un formattatore di codice Python molto veloce. L'API restituisce i codice formattato come risposta.

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
*Data returned*: {'code_modified':'code modified'}

### ORDINAMENTO DELLE IMPORTAZIONI DELLO SNIPPET

Tramite questa operazione è possibile ordinare le importazioni all'interno del codice. Per fare ciò è stata utilizzata una libreria chiamata Isort. Isort è un'utility/libreria Python che permette di ordinare le importazioni in ordine alfabetico e separarle automaticamente in sezioni e a seconda del tipo.

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
*Data returned*: {'code_modified':'code with ordered imports'}

### PYLINT

Tramite questa funzione è possibile controllare eventuali errori presenti dentro codice Python. Per fare ciò è stato utilizzato Pylint che cerca di identificare errori dentro il codice imponendo uno standard di codifica. Questo può anche cercare determinate tipologie di errori e consigliare su come eseguire il refactoring di determinati blocchi offrendo anche dettagli sulla complessità del codice.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/pylint
- POST 127.0.0.1:8000/snippets/pylint/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'pylint_output':'output of pylint'}

### PYFLAKES

Tramite questa funzione è possibile controllare eventuali errori presenti dentro codice Python. Per fare ciò è stato utilizzato Pyflakes il quale analizza i programmi e rileva eventuali errori. Funziona analizzando il file sorgente, non importandolo, quindi è più sicuro e veloce.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/pyflakes
- POST 127.0.0.1:8000/snippets/pyflakes/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'pyflakes_output':'output of pyflakes'}

### FLAKE8

Flake8 è un wrapper attorno a questi strumenti: lo script McCabe di PyFlakes e pycodestyle di Ned Batchelder. Flake8 esegue tutti gli strumenti lanciando il singolo comando flake8. Visualizza gli avvisi in un output unito per file.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/flake8
- POST 127.0.0.1:8000/snippets/flake8/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'flake8_output':'output of flake8'}

### MYPY

Mypy è un controllore del tipo statico per Python che mira a combinare i vantaggi offerti dal typing statico e dinamico. Mypy combina la potenza espressiva e la comodità di Python con un potente sistema di tipi e un controllo del tipo in fase di compilazione. Il tipo Mypy controlla i programmi Python standard.

*Richiesta*:  
- GET 127.0.0.1:8000/snippets/snippet_id/mypy
- POST 127.0.0.1:8000/snippets/mypy/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'mypy_output':'output of mypy'}

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
