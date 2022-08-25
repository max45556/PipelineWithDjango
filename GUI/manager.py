import json

import requests

from user import user_data


class Manager:

    def __init__(self):
        self.options_chosen = None
        self.url = 'http://127.0.0.1:8000/'
        self.token_access = None  # token for operation
        self.token_refresh = None
        self.user_id = None  # user_id
        self.snippet = None  # saved as json -> all data
        self.snippet_code = None
        self.snippet_id = None
        self.headers = {'Content-type': 'application/json'}
        self.write = False  # usato per sapere se si vuole salvare il contenuto delle operazioni in un file
        self.user_with_data = user_data()

    def get_outh_header(self):
        return {'Content-type': 'application/json', 'Authorization': 'Bearer ' + str(self.token_access)}

    def set_snippet(self, snippet):
        self.snippet = snippet

    def get_snippet_code(self):
        return str(self.snippet['code'])

    def login(self, username, pw):
        print("Logging with username {} and password {}".format(username, pw))
        data = {'username': username, 'password': pw}
        response = requests.post(self.url + 'login/', data=json.dumps(data), headers=self.headers)
        print("Status code: ", response.status_code)
        if response.status_code == 200:
            print("Login successfully")
            self.token_access = response.json()["access"]
            self.token_refresh = response.json()["refresh"]
            self.user_id = response.json()["user_id"]
            print("t-access", self.token_access)
            print("t-refresh", self.token_refresh)
            print("user_id", self.user_id)
        sc, rc = self.get_user_data()
        if sc == 200:
            self.user_with_data.save_username(rc["username"])
            self.user_with_data.save_first_name(rc["first_name"])
            self.user_with_data.save_last_name(rc["last_name"])
            self.user_with_data.save_email(rc["email"])
        print("Data of user: ", self.user_with_data.return_values())
        return response.status_code, response.json()

    def register(self, username, pw, pw2, email, fn, ln):
        data = {'username': username, 'password': pw, 'password2': pw2, 'email': email, 'first_name': fn,
                'last_name': ln}
        response = requests.post(self.url + 'register/', data=json.dumps(data), headers=self.headers)
        if response.status_code == 201:
            parsed = json.loads(response.text)
            js = json.dumps(parsed, indent=4, sort_keys=True)
            print("User created: " + js)
        return response.status_code, response.json()

    def update_profile(self, username, firstname, lastname, email):
        if username == "":
            username = self.user_with_data.username
        if firstname == "":
            firstname = self.user_with_data.first_name
        if lastname == "":
            lastname = self.user_with_data.last_name
        if email == "":
            email = self.user_with_data.email
        data = {'username': username, 'first_name': firstname, 'last_name': lastname, 'email': email}
        print("DATA", data)
        response = requests.post(self.url, data=json.dumps(data), headers=self.get_outh_header())
        if response.status_code == 200:
            parsed = json.loads(response.text)
            js = json.dumps(parsed, indent=4, sort_keys=True)
            print("User updated: " + js)
        return response.status_code, response.json()

    def update_password(self, password1, password2, old_password):
        data = {'password': password1, 'password2': password2, 'old_password': old_password}
        response = requests.put(self.url, data=json.dumps(data), headers=self.get_outh_header())
        if response.status_code == 200:
            print("Password updated")
        return response.status_code, response.json()

    def delete(self):
        response = requests.delete(self.url, data='', headers=self.get_outh_header())
        if response.status_code == 200:
            print("User eliminated")
        return response.status_code, response.json()

    def get_user_data(self):
        response = requests.get(self.url, data='', headers=self.get_outh_header())
        if response.status_code == 200:
            parsed = json.loads(response.text)
            js = json.dumps(parsed, indent=4, sort_keys=True)
            print("User data retrieved: " + js)
        return response.status_code, response.json()

    def get_user_snippets(self):
        response = requests.get(self.url + 'snippets/', data='', headers=self.get_outh_header())
        if response.status_code == 200:
            parsed = json.loads(response.text)  # lista di dict
            f_output = ""
            for i in parsed:
                dict_of_value = i  # dict
                output = dict_of_value['code'] + "\n"
                del dict_of_value['code']
                for k, v in dict_of_value.items():
                    output = output + str(k) + ": " + str(v) + '\n'
                f_output += output + "-------------------------------------------------------------------- \n"
            return 200, f_output
        else:
            return response.status_code, response.text.strip()

    def get_snippet_by_id(self, snippet_id):
        response = requests.get(self.url + 'snippets/' + snippet_id, data='', headers=self.get_outh_header())
        dict = {}
        if response.status_code == 200:
            snippet_returned = response.json()
            dict['code'] = snippet_returned['code']
            dict['title'] = snippet_returned['title']
            dict['language'] = snippet_returned['language']
            dict['executable'] = snippet_returned['executable']
        else:
            dict['response'] = response.text
        return response.status_code, dict

    def update_snippet_by_id(self, snippet_id, code, title, language, exec):
        data_body = {'code': code, 'title': title, 'language': language, 'executable': exec}
        response = requests.post(self.url + 'snippets/' + snippet_id + "/", data=json.dumps(data_body),
                                 headers=self.get_outh_header())
        if response.status_code == 200:
            self.snippet = response.json()
            self.snippet_code = self.snippet['code']
            self.snippet_id = self.snippet['id']
            return response.status_code, 'data updated'
        else:
            return response.status_code, response.text.strip()

    def create_snippet(self, code, title, language, exec):
        data = {'code': code, 'executable': exec}
        if title:
            data['title'] = title
        if language:
            data['language'] = language
        response = requests.post(self.url + 'snippets/', data=json.dumps(data), headers=self.get_outh_header())
        if response.status_code == 201:
            self.snippet = response.json()
            self.snippet_code = self.snippet['code']
            self.snippet_id = self.snippet['id']
            return response.status_code, 'Created'
        else:
            return response.status_code, response.text.strip()

    def delete_snippet(self, snippet_id):
        response = requests.delete(self.url + 'snippets/' + snippet_id + "/", data='', headers=self.get_outh_header())
        return response.status_code

    '''//------------------------------------------
    
    
    GET OPERATION ON CODE
    Si usano le get quando si vuole agire su uno snippet esistente. Le get non richiedono quindi il codice passato in input 
    ma può capitare che per ognuna di queste operazioni si voglia salvare l'output in un file. Si controllo allora un parametro 
    write.
    '''

    def get_language_recognition(self):
        response = requests.get(self.url + 'snippets/' + str(self.snippet_id) + '/detect/', data='',
                                headers=self.get_outh_header())
        if response.status_code == 200:
            if self.write:
                file = open("language_recognition_output.txt", "w")
                file.truncate(0)
                file.write(json.dumps(response.json()))
                file.close()
            return response.status_code, response.json()

    def get_reindent_code(self):
        response = requests.get(self.url + 'snippets/' + str(self.snippet_id) + '/reindent/', data='',
                                headers=self.get_outh_header())
        if response.status_code == 200:
            if self.write:
                file = open("reindent_code_output.txt", "w")
                file.truncate(0)
                file.write(json.dumps(response.json()))
                file.close()
            return response.status_code, response.json()

    def get_order_imports(self):
        response = requests.get(self.url + 'snippets/' + str(self.snippet_id) + '/order/', data='',
                                headers=self.get_outh_header())
        if response.status_code == 200:
            if self.write:
                file = open("order_import_output.txt", "w")
                file.truncate(0)
                file.write(json.dumps(response.json()))
                file.close()
            return response.status_code, response.json()

    def get_check_pylint(self):
        response = requests.get(self.url + 'snippets/' + str(self.snippet_id) + '/pylint/', data='',
                                headers=self.get_outh_header())
        if response.status_code == 200:
            if self.write:
                file = open("pylint_output.txt", "w")
                file.truncate(0)
                file.write(json.dumps(response.json()))
                file.close()
            return response.status_code, response.json()

    def get_check_pyflakes(self):
        response = requests.get(self.url + 'snippets/' + str(self.snippet_id) + '/pyflakes/', data='',
                                headers=self.get_outh_header())
        if response.status_code == 200:
            if self.write:
                file = open("pyflakes_output.txt", "w")
                file.truncate(0)
                file.write(json.dumps(response.json()))
                file.close()
            return response.status_code, response.json()

    def get_check_flake8(self):
        response = requests.get(self.url + 'snippets/' + str(self.snippet_id) + '/flake8/', data='',
                                headers=self.get_outh_header())
        if response.status_code == 200:
            if self.write:
                file = open("flake8_output.txt", "w")
                file.truncate(0)
                file.write(json.dumps(response.json()))
                file.close()
            return response.status_code, response.json()

    def get_check_mypy(self):
        response = requests.get(self.url + 'snippets/' + str(self.snippet_id) + '/mypy/', data='',
                                headers=self.get_outh_header())
        if response.status_code == 200:
            if self.write:
                file = open("mypy_output.txt", "w")
                file.truncate(0)
                file.write(json.dumps(response.json()))
                file.close()
            return response.status_code, response.json()

    def get_execute(self):
        response = requests.get(self.url + 'snippets/' + str(self.snippet_id) + '/execute/', data='',
                                headers=self.get_outh_header())
        if response.status_code == 200:
            if self.write:
                file = open("execute_output.txt", "w")
                file.truncate(0)
                file.write(json.dumps(response.json()))
                file.close()
            return response.status_code, response.json()

    # -------------POST OPERATION ON CODE

    def post_language_recognition(self, code):
        response = requests.post(self.url + 'snippets/detect/', data=json.dumps({'code': code}),
                                 headers=self.get_outh_header())
        return response.status_code, response.json()

    def post_reindent_code(self, code):
        response = requests.post(self.url + 'snippets/reindent/', data=json.dumps({'code': code}),
                                 headers=self.get_outh_header())

        return response.status_code, response.json()

    def post_order_imports(self, code):
        response = requests.post(self.url + 'snippets/order/', data=json.dumps({'code': code}),
                                 headers=self.get_outh_header())
        return response.status_code, response.json()

    def post_check_pylint(self, code):
        response = requests.post(self.url + 'snippets/pylint/', data=json.dumps({'code': code}),
                                 headers=self.get_outh_header())
        return response.status_code, response.json()

    def post_check_pyflakes(self, code):
        response = requests.post(self.url + 'snippets/pyflakes/', data=json.dumps({'code': code}),
                                 headers=self.get_outh_header())
        return response.status_code, response.json()

    def post_check_flake8(self, code):
        response = requests.post(self.url + 'snippets/flake8/', data=json.dumps({'code': code}),
                                 headers=self.get_outh_header())
        return response.status_code, response.json()

    def post_check_mypy(self, code):
        response = requests.post(self.url + 'snippets/mypy/', data=json.dumps({'code': code}),
                                 headers=self.get_outh_header())
        return response.status_code, response.json()

    def post_execute(self, code):
        print("Entered into post_execute")
        response = requests.post(self.url + 'snippets/execute/', data=json.dumps({'code': code}),
                                 headers=self.get_outh_header())
        return response.status_code, response.json()

    #######---PATCH -----------------

    def patch_language_recognition(self):
        response = requests.patch(self.url + 'snippets/' + str(self.snippet_id) + '/detect/', data='',
                                  headers=self.get_outh_header())
        if response.status_code == 200:
            return response.status_code, response.json()

    def patch_reindent_code(self):
        response = requests.patch(self.url + 'snippets/' + str(self.snippet_id) + '/reindent/', data='',
                                  headers=self.get_outh_header())
        if response.status_code == 200:
            return response.status_code, response.json()

    def patch_order_imports(self):
        response = requests.patch(self.url + 'snippets/' + str(self.snippet_id) + '/order/', data='',
                                  headers=self.get_outh_header())
        if response.status_code == 200:
            return response.status_code, response.json()

    def patch_execute(self):
        print("Entered into post_execute")
        response = requests.patch(self.url + 'snippets/' + str(self.snippet_id) + '/execute/', data='',
                                  headers=self.get_outh_header())
        if response.status_code == 200:
            return response.status_code, response.json()

    ############################################################################

    def multiple_operation(self, option_choose, write):
        print("MULTIPLE OPERATION")
        self.write = write
        if write:
            print("CREO FILE MULTIPLI")
        option = {
            'language recognition': self.get_language_recognition,
            'reindent code': self.get_reindent_code,
            'order imports': self.get_order_imports,
            'pylint checker': self.get_check_pylint,
            'pyflakes checker': self.get_check_pyflakes,
            'flake8 checker': self.get_check_flake8,
            'mypy checker': self.get_check_mypy,
            'check execution': self.get_execute
        }
        elaborate_response = ""
        for element in option_choose:
            if element in option:
                status_code, output = option[element]()
                if status_code == 200:
                    elaborate_response += "-------> " + element + " operation Successfully \n"
                    elaborate_response += json.dumps(output) + "\n\n"
                else:
                    elaborate_response += "-------> " + element + " operation Not Done \n"
        self.write = False
        return elaborate_response

    '''
    Per restutuire un solo output si passa ogni volta il codice modificato. Quindi invio richiesta in post e salvo il codice. 
    Poi faccio un altra post passando il codice modificato che mi era stato restituito. Per la post e la patch il risultato è il 
    medesimo e quando avviene la patch avviene in più la memorizzazione.  
    '''

    def single_operation(self, option_choose, write, save_value):
        print("Singole operazioni")
        print("Memorizzo file") if write else print("Non memorizzo file")
        print("Salvo i dati") if save_value else print("Non salvo i file")
        code_modified = self.snippet_code
        final_output = ""

        patch_operation_on_code = {
            'reindent code': self.patch_reindent_code,
            'order imports': self.patch_order_imports,
        }

        patch_operation_of_evaluation = {
            'language recognition': self.patch_language_recognition,
            'pylint checker': self.get_check_pylint,
            'pyflakes checker': self.get_check_pyflakes,
            'flake8 checker': self.get_check_flake8,
            'mypy checker': self.get_check_mypy,
            'check execution': self.patch_execute,
        }

        post_operation_on_code = {
            'reindent code': self.post_reindent_code,
            'order imports': self.post_order_imports,
        }

        post_operation_of_evaluation = {
            'language recognition': self.post_language_recognition,
            'pylint checker': self.post_check_pylint,
            'pyflakes checker': self.post_check_pyflakes,
            'flake8 checker': self.post_check_flake8,
            'mypy checker': self.post_check_mypy,
            'check execution': self.post_execute,
        }

        ## I METODI RITORNANO SOLAMENTE LA RISPOSTA, NON FANNO OPERAZIONI DI FILTRAGGIO!!!!
        ## RITORNANO {'CODE', 'CIAO'}
        if not save_value:  # POST
            print("Effettuo richieste in POST")
            for element in option_choose:
                if element in post_operation_on_code:
                    status_code, response = post_operation_on_code[element](code_modified)
                    '''
                    response:
                     {'code_modified': 'import sys\n\nfrom my_lib import Object2, Object3\nfrom third_party import (lib1, lib2, lib3, lib4, lib5, lib6, lib7, lib8, lib9,\n                         lib10, lib11, lib12, lib13, lib14, lib15)\n\nkeys_list = ["A", "B", "C"]\nvalues_list = ["blue", "red", "bold"]'}
                     Starting code: import sys...
                    '''
                    code_modified = response['code_modified']
                    if status_code == 200:
                        final_output += "-------> " + element + " operation Successfully \n"
                    else:
                        final_output += "-------> " + element + " operation Not Done \n"
            final_output += "\n----CODE---- \n"
            final_output += code_modified + "\n"

            for element in option_choose:
                if element in post_operation_of_evaluation:
                    status_code, output = post_operation_of_evaluation[element](code_modified)  # code modified
                    if status_code == 200:
                        initial_ele = next(iter((output.items())))
                        final_output += "-------> " + element + " operation Successfully \n"
                        final_output += initial_ele[1] + "\n\n"
                    else:
                        final_output += "-------> " + element + " operation Not Done \n"
                        final_output += json.dumps(output) + "\n\n"

        else:  # SALVO PATCH
            # i metodi patch ritornano i risultati salvandoli
            for element in option_choose:
                if element in patch_operation_on_code:
                    status_code, code_modified = patch_operation_on_code[element]()  # code modified
                    if status_code == 200:
                        final_output += "-------> " + element + " operation Successfully \n"
                    else:
                        final_output += "-------> " + element + " operation Not Done \n"
            final_output += "\n ----CODE---- \n"
            final_output += code_modified['code_modified'] + "\n\n"

            for element in option_choose:
                if element in patch_operation_of_evaluation:
                    status_code, output = patch_operation_of_evaluation[element]()  # code modified
                    if status_code == 200:
                        initial_ele = next(iter((output.items())))
                        final_output += "-------> " + element + " operation Successfully \n"
                        final_output += initial_ele[1] + "\n\n"
                    else:
                        final_output += "-------> " + element + " operation Not Done \n"
                        final_output += json.dumps(output) + "\n\n"

        if write:
            file = open("Output of operation.txt", "w")
            file.truncate(0)
            file.write(final_output)
            file.close()

            file_code = open("Code_to_execute.py", "w")
            file_code.truncate(0)
            file_code.write(json.dumps(code_modified))
            file_code.close()

        return final_output
