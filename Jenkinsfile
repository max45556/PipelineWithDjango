String standard_pipeline = 'y'
String custom_pipeline = 'n'
String registration = 'y'
String acc_token = ''
String ref_token = ''
String user_id = ''

def login(username, password) {
    def post = new URL("http://django:8000/login/").openConnection();
    def message = '{"username":' + '"' + username + '"' + "," + '"password":' + '"' + password + '"}'
    post.setRequestMethod("POST")
    post.setDoOutput(true)
    post.setRequestProperty("Content-Type", "application/json")
    post.setRequestProperty("Accept", "application/json")
    post.getOutputStream().write(message.getBytes("UTF-8"));
    if (100 <= post.getResponseCode() && post.getResponseCode() <= 399) {
      print(connection.getInputStream());
        }
    }

node {
    stage('Preparation') {
        git branch: 'main', url: 'https://github.com/max45556/PipelineWithDjango.git'
        def file = new File("/var/jenkins_home/workspace/DjangoPipe/snippet.py")
        String fileContent = file.text
        println("Snippet to analyze: \n" + fileContent)
    }
    stage('Login') {
      login('admin', 'admin1212')
    }
    stage('ciccio') {
    }
}
