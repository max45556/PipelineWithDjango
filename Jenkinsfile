
String standard_pipeline = 'y'
String custom_pipeline = 'n'
String registration = 'y'

def login(username, password) {
    def post = new URL("http://django:8000/login/").openConnection();
    def message = '{"username":admin, "password": password}'
    post.setRequestMethod("POST")
    post.setDoOutput(true)
    post.setRequestProperty("Content-Type", "application/json")
    post.getOutputStream().write(message.getBytes("UTF-8"));
    def postRC = post.getResponseCode();
    println("Response code" + postRC);
    println("Response" + post.getInputStream().getText());
}

node {
    stage('Preparation') { //
        git branch: 'main', url: 'https://github.com/max45556/PipelineWithDjango.git'
        def file = new File("/var/jenkins_home/workspace/DjangoPipe/snippet.py")
        String fileContent = file.text
        println("Snippet to analyze: \n" + fileContent)
    }
    stage('Login') {
      login('admin', 'admin1212')
    }
    stage('ciccio') {
    def get = new URL("http://django:8000/help").openConnection();
    def getRC = get.getResponseCode();
    println(getRC);
    if(getRC.equals(200)) {
        println(get.getInputStream().getText());
        }
    }
}
