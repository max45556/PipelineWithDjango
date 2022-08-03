import groovy.json.*

access_token = ''
refresh_token = ''
user_id = ''
logged = false
snippet = ''
body = ''

Map login(username, password) {
    def post_login = new URL("http://django:8000/login/").openConnection()
    def body_login = '{"username":' + '"' + username + '"' + "," + '"password":' + '"' + password + '"}'
    post_login.setRequestMethod("POST")
    post_login.setDoOutput(true)
    post_login.setRequestProperty("Content-Type", "application/json")
    post_login.setRequestProperty("Accept", "application/json")
    post_login.getOutputStream().write(body_login.getBytes("UTF-8"))
    def response = post_login.getInputStream().getText()
    if (post_login.getResponseCode() == 200) {
      Map parsedJson = new JsonSlurper().parseText(response)
      access_token = parsedJson.access
      refresh_token = parsedJson.refresh
      user_id = parsedJson.user_id
      return [isClear:true, reason:"Login successfull"]
    } else {
        return [isClear:false, reason: "Login error"]
    }
}

def get_user_snippets() {
  def get_request = new URL("http://django:8000/snippets/").openConnection();
  get_request.setRequestMethod("GET")
  get_request.setRequestProperty("Content-Type", "application/json")
  get_request.setRequestProperty("Accept", "application/json")
  get_request.setRequestProperty("Authorization", "Bearer " + access_token)
  def getRC = get_request.getResponseCode();
  def response = get_request.getInputStream().getText()
  if(getRC.equals(200)) {
    def pretty = JsonOutput.prettyPrint(jsonsnippets)
    println "User snippets found: \n" + pretty
    } else {
    println "Error happened while trying to get user snippets: " + response
  }
}

def language_identification() {
  def post_language = new URL("http://127.0.0.1:8000/snippets/detect/").openConnection()
  post_language.setRequestMethod("POST")
  post_language.setDoOutput(true)
  post_language.setRequestProperty("Content-Type", "application/json")
  post_language.setRequestProperty("Authorization", "Bearer " + access_token)
  post_language.getOutputStream().write(body.getBytes("UTF-8"))
  def getRC_lan = post_language.getResponseCode()
  String response = post_language.getInputStream().getText()
  if (getRC_lan == 200) {
    Map parsedJson = new JsonSlurper().parseText(response) as Map
    println "Language is " + parsedJson.language + "\n"
  } else {
    print "Error in language " + response
  }
}

def reindent_code() {
  def post_reindent = new URL("http://127.0.0.1:8000/snippets/reindent/").openConnection()
  post_reindent.setRequestMethod("POST")
  post_reindent.setDoOutput(true)
  post_reindent.setRequestProperty("Content-Type", "application/json")
  post_reindent.setRequestProperty("Authorization", "Bearer " + access_token)
  post_reindent.getOutputStream().write(body.getBytes("UTF-8"))
  def getRC_reindent = post_reindent.getResponseCode()
  def response = post_reindent.getInputStream().getText()
  if (getRC_rein == 200) {
    Map parsedJson = new JsonSlurper().parseText(response) as Map
    print("Correct file is " + parsedJson.code_modified + "\n\n")
    } else {
      print "Error in reindet code " + response
    }
  }

def order_import() {
  def post_order_import = new URL("http://127.0.0.1:8000/snippets/order/").openConnection()
  post_order_import.setRequestMethod("POST")
  post_order_import.setDoOutput(true)
  post_order_import.setRequestProperty("Content-Type", "application/json")
  post_order_import.setRequestProperty("Authorization", "Bearer " + access_token)
  post_order_import.getOutputStream().write(body.getBytes("UTF-8"))
  def getRC_order = post_order_import.getResponseCode()
  String response = post_order_import.getInputStream().getText()
  if (getRC_order == 200) {
      Map parsedJson = new JsonSlurper().parseText(response_lan) as Map
      print("Correct file after ordering of imports is " + parsedJson.code_modified + "\n\n")
  } else {
    print "Error in order import " + response
  }
}

def pylint() {
  def post_pylint = new URL("http://127.0.0.1:8000/snippets/pylint/").openConnection()
  post_pylint.setRequestMethod("POST")
  post_pylint.setDoOutput(true)
  post_pylint.setRequestProperty("Content-Type", "application/json")
  post_pylint.setRequestProperty("Authorization", "Bearer " + access_token)
  post_pylint.getOutputStream().write(body.getBytes("UTF-8"))
  def getRC_pylint = post_pylint.getResponseCode()
  String response = post_pylint.getInputStream().getText()
  if (getRC_pylint == 200) {
      Map parsedJson = new JsonSlurper().parseText(response) as Map
      print("Pylint output is: " + parsedJson.pylint_output + "\n\n")
  } else {
    print "Error using pylint " + response
  }
}

def pyflakes() {
  def post_pyflakes = new URL("http://127.0.0.1:8000/snippets/pyflakes/").openConnection()
  post_pyflakes.setRequestMethod("POST")
  post_pyflakes.setDoOutput(true)
  post_pyflakes.setRequestProperty("Content-Type", "application/json")
  post_pyflakes.setRequestProperty("Authorization", "Bearer " + access_token)
  post_pyflakes.getOutputStream().write(body.getBytes("UTF-8"))
  def getRC_pyflake = post_pyflakes.getResponseCode()
  String response = post_pyflakes.getInputStream().getText()
  if (getRC_pyflake == 200) {
      Map parsedJson = new JsonSlurper().parseText(response) as Map
      print("Pyflake output is: " + parsedJson.pyflakes_output + "\n\n")
  } else {
    print "Error using pyflakes " + response
  }
}

def flake8() {
  def post_flake8 = new URL("http://127.0.0.1:8000/snippets/flake8/").openConnection()
  post_flake8.setRequestMethod("POST")
  post_flake8.setDoOutput(true)
  post_flake8.setRequestProperty("Content-Type", "application/json")
  post_flake8.setRequestProperty("Authorization", "Bearer " + access_token)
  post_flake8.getOutputStream().write(body.getBytes("UTF-8"))
  def getRC_flake8 = post_flake8.getResponseCode()
  String response = post_flake8.getInputStream().getText()
  if (getRC_flake8 == 200) {
      Map parsedJson = new JsonSlurper().parseText(response) as Map
      print("flake8 output is: " + parsedJson.flake8_output + "\n\n")
  } else {
    print "Error using flake8 " + response
  }
}

def mypy() {
  def post_mypy = new URL("http://127.0.0.1:8000/snippets/mypy/").openConnection()
  post_mypy.setRequestMethod("POST")
  post_mypy.setDoOutput(true)
  post_mypy.setRequestProperty("Content-Type", "application/json")
  post_mypy.setRequestProperty("Authorization", "Bearer " + access_token)
  post_mypy.getOutputStream().write(body.getBytes("UTF-8"))
  def getRC_mypy = post_mypy.getResponseCode()
  String response = post_mypy.getInputStream().getText()
  if (getRC_flake8 == 200) {
      Map parsedJson = new JsonSlurper().parseText(response) as Map
      print("mypy output is: " + parsedJson.mypy_output + "\n\n")
  } else {
    print "Error using mypy " + response
  }
}

def execute() {
  def post_execute = new URL("http://127.0.0.1:8000/snippets/execute/").openConnection()
  post_execute.setRequestMethod("POST")
  post_execute.setDoOutput(true)
  post_execute.setRequestProperty("Content-Type", "application/json")
  post_execute.setRequestProperty("Authorization", "Bearer " + access_token)
  post_execute.getOutputStream().write(body.getBytes("UTF-8"))
  def getRC_execute = post_execute.getResponseCode()
  String response = post_execute.getInputStream().getText()
  if (getRC_execute == 200) {
      Map parsedJson = new JsonSlurper().parseText(response) as Map
      print("File is executable: " + parsedJson.executable + "\n\n")
  } else {
    print "Error with executable " + response
  }
}


node {
    stage('Get snippet') {
        git branch: 'main', url: 'https://github.com/max45556/PipelineWithDjango.git'
        def file = new File("/var/jenkins_home/workspace/DjangoPipe/snippet.py")
        snippet = file.text
        body = snippet.replaceAll("(\\r|\\n|\\r\\n)+", "\\\\n")
        println("Snippet to analyze: \n\n" + snippet)
    }
    stage('Logging') {
      def result = login('admin', 'admin1212')
      println(result.reason)
      if (result.isClear) {
        logged = true
        println("Access: " + access_token)
        println("Refresh: " + refresh_token)
        println("user_id: " + user_id)
        }
      }
      if (logged) {
        stage('Getting user Snippet') {
          get_user_snippets()
        }
        stage('Identify language') {
          language_identification()
        }
        stage('Reindent code') {
          reindent_code()
        }
        stage('Ordering import') {
          order_import()
        }
        stage('Pylint') {
          pylint()
        }
        stage('PyFlakes') {
          pyflakes()
        }
        stage('Flake8') {
          flake8()
        }
        stage('Mypy') {
          mypy()
        }
        stage('Execute') {
          execute()
        }
      }

  }
