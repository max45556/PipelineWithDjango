node {
    stage('Preparation') { // for display purposes
        git branch: 'main', url: 'https://github.com/max45556/PipelineWithDjango.git'
        def file = new File("/var/jenkins_home/workspace/DjangoPipe/snippet.py")
        String fileContent = file.text
        return fileContent
    }
}
    }
    stage('Post request') {
    def post = new URL("http://django:8000/login/").openConnection();
    def message = '{"username":"admin", "password": "admin1212"}'
    post.setRequestMethod("POST")
    post.setDoOutput(true)
    post.setRequestProperty("Content-Type", "application/json")
    post.getOutputStream().write(message.getBytes("UTF-8"));
    def postRC = post.getResponseCode();
    println(postRC);
    println(post.getInputStream().getText());
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
