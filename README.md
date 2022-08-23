# Snippet Analizer

# Scopo

L'obbiettivo di questo progetto è stato quello di creare, attraverso, [DJANGO REST FRAMEWORK](https://www.django-rest-framework.org/) delle Web API che permettessero di effettuare varie attività su snippet di codice scritti in Python. Le API sono pensate per essere integrate sia all'interno di un applicazione che dentro una pipeline CI/CD e per dimostrare ciò è stato creato:

 - un software con una semplice interfaccia che consente facilmente di operare sugli snippet. Questo
  astrae le modalità di interazione con le API dato che + stato pensato per un utilizzato da utenti non esperti.

- una pipeline CI/CD che presenta come stadi le attività svolte dalle API.

Procederemo quindi ad illustrare quelle che sono le API create, le loro funzionalità e attraverso quali metodi è possibile sfruttarle per poi illustrare il software e la pipeline CI/CD creata.

# Funzionamento delle API

Per utilizzare l'API è necessario registrarsi. Dopo la registrazione un utente può svolgere le seguenti funzioni:
- Gestire il proprio profilo;
- Memorizzare snippet;
- Effettuare delle operazione su snippet memorizzati o non memorizzati.

## Gestione del profilo

Questo elenco comprende una serie di API utilizzate per gestire il profilo utente.

### REGISTRAZIONE
Per utilizzare le funzionalità offerte dalle API è necessario essere registrati. Dopo la fase di registrazione, un utente può effettuare il login utilizzando i dati appena inseriti e può ovviamente decidere di eliminare il proprio profilo in qualsiasi momento. Per la registazione sono necessari tutti i campi successivamente esposti nel body ed al termine delle registrazione vengono riportati i dati dell'utente.

*Richiesta*:

          POST 127.0.0.1:8000/register/  
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
Effettuando il Login un utente può ottenere un token di accesso attraverso il quale sfruttare le API. Insieme ad esso è restituito anche un token di refresh usato per ottenere un nuovo token di accesso e uno user_id. Essendo le API pensate per essere integrate in un ambiente multi-utente tutte le API mostrate successivamente richiedono all'interno del body la specifica dell'Access Token in modo da comprendere quale utente sta effettuando la richiesta.

*Richiesta*:

        POST 127.0.0.1:8000/login/  
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
Viene utilizzato per ottenere un nuovo token di accesso utilizzando il token di refresh fornito al Login. Questa restituisce un nuovo token di accesso.

*Richiesta*:

          POST 127.0.0.1:8000/login/refresh/  
*Header*: Content-Type: application/json  
*Body*:  
- **refresh**: 'refresh token'

*Standard Response Code*: 200 OK  
*Standard Response*:  
- *'access'*: token di accesso' (stringa)

### MODIFICA DELLA PASSWORD UTENTE
Consente a un utente di modificare la password personale utilizzando la sua vecchia password. Specifica se la password è stata correttamente modificata o si è verificato un errore.

*Richiesta*:

          PUT 127.0.0.1:8000  
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
Consente a un utente di aggiornare i dati del proprio profilo. Se la modifica è avvenuta correttamente restiutisce i dati aggiornati dell'utente.

*Richiesta*:

          POST 127.0.0.1:8000  
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
Consente a un utente di visualizzare i propri personali. Restituisci, se la richiesta è stata effettuata correttamente, i dati del profilo.

*Richiesta*:

        GET 127.0.0.1:8000  
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
Consente a un utente di eliminare il proprio profilo. Segnala, se la richiesta è stata effettuata correttamente, la corretta eliminazione.

*Richiesta*:

          DELETE 127.0.0.1:8000  
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
Come detto precedente, gli utenti possono operare su snippet precedentemente creati. Un utente può infatti creare un suo snippet, recuperarlo a piacimento ed effettuare su di esso una serie di operazioni. Per la gestione degli snippet personali sono state create diverse API.

### CREAZIONE DI UN NUOVO SNIPPET
Con questa operazione è possibile memorizzare uno snippet personale. L'unico campo obbligatorio è quello che contiene il codice ma possono essere fornite anche altre informazioni per una migliore gestione dei propri snippet. I campi non precisati assumeranno valori di default. Se la creazione è avvenuta correttamente vengono riportate le informazioni dello snippet assieme ad uno snippet id. Questo sarà utilizzato per selezionare, tra l'elenco degli snippet personali memorizzati, quello su cui effettuare le operazioni.

*Richiesta*:

          POST 127.0.0.1:8000/snippets/  
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
Con questa operazione è possibile modificare uno snippet precedente salvato. Tutti i campi sono facoltativi e quelli non specificati continueranno ad assumere il valore che avevano precedentemente. È ovviamente necessario specificare lo snippet che si intende modificare e ciò è fatto attraverso lo snippet id. Questo viene fornito al momento della creazione dello snippet ma è visualizzabile anche in un secondo momento.

*Richiesta*:

          POST 127.0.0.1:8000/snippets/snippet_id/  
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

*Richiesta*:

          DELETE 127.0.0.1:8000/snippets/snippet_id/  
*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*: empty  
*Standard Response Code*: 204 NO CONTENT  
{
    "*detail*": "snippet removed"
}


### VISUALIZZAZIONE DI UNO SNIPPET DALL'ID
Con questa operazione è possibile visualizzare uno snippet specifico tra quelli memorizzati. Ciò è fatto attraverso il suo id.

*Richiesta*:

          GET 127.0.0.1:8000/snippets/snippet_id/  
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

*Richiesta*:

          GET 127.0.0.1:8000/snippets/  
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

  i metodi GET vengono utilizzato quando si desidera agire su uno snippet memorizzato. Per questo motivo nelle richieste GET è necessario specificare l'ID dello snippet su cui eseguire l'operazione. Ad esempio, per eseguire l'operazione di individuazione del linguaggio di programmazione dello snippet con id 2 occorre fare la seguente richiesta:

          GET 127.0.0.1:8000/snippets/2/detect/

i metodi POST vengono utilizzati quando si desidera agire su uno snippet *non* memorizzato. Nel body della richiesta è infatti necessario specificare un parametro contenente il codice su affettuare l'attività: 'code': 'codice da analizzare'. Le richieste POST si prestano nel momento in cui si vogliano utilizzare le funzionalità offerte della API senza però preocedere alla memorizzazione degli snippet. All'interno dells pipeline CI/CD si useranno unicamente richieste in POST. Ad esempio, per eseguire l'operazione di individuazione del linguaggio di programmazione su uno snippet occorre fare la seguente richiesta:

          POST 127.0.0.1:8000/snippets/detect/ e specificare nel body il codice da analizzare

I metodi PATCH funzionano in modo quasi identico ai GET. I metodi PATCH servono per eseguire operazioni su uno snippet memorizzato sul server e la differenza rispetto ai metodi GET è che, una volta ottenuto l'output, le modifiche effettuate sul codice (come può essere l'indentazione) vengono salvato nel db. Ad esempio, quando viene eseguita l'operazione di identificazione del linguaggio di programmazione e si ottiene il risultato, questo valore viene memorizzato nel campo linguaggio dello snippet analizzato. Ad esempio, per eseguire l'operazione di individuazione del linguaggio di programmazione dello snippet, che ha id 2, occorre fare la seguente richiesta:

          PATCH 127.0.0.1:8000/snippets/2/detect/

se l'output restituito è Python, il valore Python verrà inserito nel campo language dello snippet 2.

### IDENTIFICAZIONE DEL LINGUAGGIO DELLO SNIPPET
Attraverso questa funzionalità è possibile identificare il linguaggio di programmazione di un particolare snippet. L'identificazione avviene tramite Guesslang, un software di deep learning Open source, che è stato addestrato con oltre un milione di sorgenti. Questo supporta più di 50 linguaggi di programmazione e rileva il linguaggio di programmazione corretto con una precisione superiore al 90%.

*Richiesta*:  

          GET 127.0.0.1:8000/snippets/snippet_id/detect
          PATCH 127.0.0.1:8000/snippets/snippet_id/detect/
          POST 127.0.0.1:8000/snippets/detect/

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

          GET 127.0.0.1:8000/snippets/snippet_id/reindent
          PATCH 127.0.0.1:8000/snippets/snippet_id/reindent/
          POST 127.0.0.1:8000/snippets/reindent/

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

          GET 127.0.0.1:8000/snippets/snippet_id/order
          PATCH 127.0.0.1:8000/snippets/snippet_id/order/
          POST 127.0.0.1:8000/snippets/order/

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

          GET 127.0.0.1:8000/snippets/snippet_id/pylint
          POST 127.0.0.1:8000/snippets/pylint/

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

          GET 127.0.0.1:8000/snippets/snippet_id/pyflakes
          POST 127.0.0.1:8000/snippets/pyflakes/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'pyflakes_output':'output of pyflakes'}

### FLAKE8

Oltre agli strumenti che consentono di formattare il codice in Python esistono diversi linter e analizzatori statici di codice.
Uno dei più popolari Linter su Python è Flake8 che non cambia il codice, ma fornisce uno strumento di warnings in real time.

*Richiesta*:  

          GET 127.0.0.1:8000/snippets/snippet_id/flake8
          POST 127.0.0.1:8000/snippets/flake8/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'flake8_output':'output of flake8'}

### MYPY

Mypy è un controllore del tipo statico per Python che mira a combinare i vantaggi offerti dal typing statico e dinamico. Mypy combina la potenza espressiva e la comodità di Python con un potente sistema di tipi e un controllo del tipo in fase di compilazione.

*Richiesta*:  

          GET 127.0.0.1:8000/snippets/snippet_id/mypy
          POST 127.0.0.1:8000/snippets/mypy/

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

          GET 127.0.0.1:8000/snippets/snippet_id/execute
          PATCH 127.0.0.1:8000/snippets/snippet_id/execute/
          POST 127.0.0.1:8000/snippets/execute/

*Header*:  
- Content-Type: application/json  
- Authorization: Bearer + Access Token

*Body*:  
- GET REQUEST, empty
- PATCH REQUEST, empty
- POST REQUEST, 'code': 'code_to_analyze'

*Standard Response*: 200 OK  
*Data returned*: {'executable': TRUE or FALSE}

# SOFTWARE PER L'UTILIZZO DELLE API

Come detto in precedenza, è stato sviluppato un software che permette di eseguire le operazioni previste dalle API. Si tratta in particolare di una GUI sviluppata con TKinter e sebbene semplice aiuta a comprendere quella è che la loro utilità all'interno di un software. Procederemo ad analizzare il funzionamento del software attraverso delle immagini.

![alt text](https://github.com/max45556/PipelineWithDjango/blob/main/GUI_image/immagineUI1.png?raw=true)

Nella prima schermata offerta è possibile gestire il profilo utente. Come prima operazione è necessario loggarsi o registrarsi e dopo aver fatto ciò è possibile:  
- Visualizzare i propri dati personali (esclusa la password) attraverso il bottone Get Data.
- Aggiornare i propri dati personali attraverso i form presenti in altro a destra.
- Modificare la propria password personale attraverso i form posti a metà schermata verso destra.
- Eliminare il proprio account attraverso il pulsante Delete.
- Visualizzare un menu di aiuto attraverso il pulsante Help. Questo apre una pagina Web utile per comprendere come le richieste verso svolte.   

Attraverso il pusante con il logo di python è possibile muoversi alla schermata successiva

![alt text](https://github.com/max45556/PipelineWithDjango/blob/main/GUI_image/immagineUI2.png?raw=true)

In questa schermata è possibile specificare su quale snippet effettuare le operazioni ed è possibile:  
- Usare uno snippet personale memorizzato precedentemente
- Caricare uno snippet da file
- Incollare uno snippet copiato

Per usare uno snippet precedentemente memorizzato esiste un bottone apposito Cerca (posizionato in alto a destra), che mostra tutti gli snippet memorizzati. Questi sono mostrati nella finestra presente sulla destra. Ogni snippet ha un id personale e possiamo utilizzarlo per indicare su quale snippet bogliamo agire. Per fare ciò è necessario inserire l'id nel form 'usa questo snippet' e premere, dopo aver fatto ciò, su Select. Lo snippet caricato sarà allora mostrato sulla finestra di sinistra. Sotto il pulsante di selezione è anche presente un form nel quale inserire uno snippet da eliminare. Dopo aver selezioanto lo snippet su cui effettuare le attività è anche possibile modificarlo. Si può, nello specifico, modificare direttamente il codice utilizzando la finestra sulla sinistra nel quale lo snippet è stato caricato e qualora si volessero modificare anche le informazioni ad esso associate sono presenti una serie di form per fare ciò posti sotto la finestra di sinistra. Per quanto riguarda l'analisi di snippet non memorizzati nel db il procedimento è il medesimo.

Attraverso il bottone che presenta una freccia è possibile muoversi alla schermata successiva per effettuare effettivamente le operazioni sullo snippet selezionato.

![alt text](https://github.com/max45556/PipelineWithDjango/blob/main/GUI_image/immagineUI3.png?raw=true)

In questa schermata è possibile. come prima operazione, selezionare la modalità Pipeline o Single Operation. Con la 

# PIPELINE CI/CD

![alt text](https://github.com/max45556/PipelineWithDjango/blob/main/GUI_image/restpipe.png?raw=true)
