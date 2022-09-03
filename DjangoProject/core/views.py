import ast
import os
import subprocess

from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from guesslang import Guess
from rest_framework import status, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import Snippet
from core.serializers import SnippetSerializer, MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer, \
    UpdateUserSerializer, ChangePasswordSerializer


@csrf_exempt
def home(request):
    return render(request, 'home.html')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserOperationAPI(APIView):

    def post(self, request):
        user = User.objects.get(pk=self.request.user.id)
        serializer = UpdateUserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = User.objects.get(pk=self.request.user.id)
        serializer = ChangePasswordSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response("Data correctly Modified", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.request.user
        user.delete()
        return Response({"result": "user delete"})

    def get(self, request):
        print("Entered")
        serializer = UserSerializer(request.user)
        print("DATA: ", serializer.data)
        return Response(serializer.data)


"""
Login Class.
post 127.0.0.1:8000/login/
- For this operation is required to set in the body the username and the password. The server response with
refresh token, access token and user_id
"""


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class SnippetList(APIView):
    permission_classes = (IsAuthenticated,)

    """
    List all user snippets
    get 127.0.0.1:8000/snippets/
    - For this operation is required the authentication so is necessary to enter the access token in the header.
    The username of the requesting user is retrieved through access token and this is set in the owner field of the snippet.
    """

    def get(self, request):  # request necessary
        print("entered into get: get 127.0.0.1:8000/snippets/")
        snippet = Snippet.objects.filter(owner=self.request.user.username)
        serializer = SnippetSerializer(snippet, many=True)
        return Response(serializer.data)

    """
    create new Snippet
    post 127.0.0.1:8000/snippets/ -> required code in the body -> code:value
    - For this operation is required the authentication so is necessary to enter the access token in the header.
    The username of the requesting user is retrieved through access token and this is set in the owner field of the snippet.
    """

    def post(self, request):
        serializer = SnippetSerializer(data=request.data, context={'owner': request.user.username})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    permission_classes = (IsAuthenticated,)

    """
    Retrieve, update or delete a snippet instance. The snippet is identified throw the id.
    """

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object(pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def post(self, request, pk):
        snippet = self.get_object(pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        serializer = SnippetSerializer(snippet,
                                       partial=True,  # senno modifica tutti i campi
                                       data=request.data,
                                       context={'owner': request.user.username})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        snippet.delete()
        return Response(data={'detail': 'snippet removed'}, status=status.HTTP_204_NO_CONTENT)


'''
DETECT the language of a snippet.
GET 127.0.0.1:8000/snippets/1/detect/ to use a stored snippet into db, so require a valid identifier to locate the snippet (id -> 1)
POST 127.0.0.1:8000/snippets/detect/ to pass a snippet to elaborate -> require code specification into the body (code: 'code')
GET 127.0.0.1:8000/snippets/1/detect/ to use a stored snippet into db, so require a valid identifier to locate the snippet (id -> 1)
the only difference with get is that this store the value into db
'''


class SnippetDetect(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        print("Identificazione lingua dello snippet... GET\n")
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        language = self.identify_language(code)
        return Response(status=status.HTTP_200_OK, data={"language": language})

    def post(self, request):
        print("Identificazione lingua dello snippet... POST\n")
        print(request.data)
        if not request.data.get('code'):
            return Response(status=status.HTTP_200_OK, data="You must specify the code into body (code: 'code') ")
        code = request.data.get('code')
        print(code)
        language = self.identify_language(code)
        return JsonResponse(status=status.HTTP_200_OK, data={"language": language})

    def patch(self, request, pk):
        print("Identificazione lingua dello snippet... PATCH\n")
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        language = self.identify_language(code)
        snippet.language = language
        snippet.save()
        return Response(status=status.HTTP_200_OK, data={"language": language})

    def identify_language(self, code):
        guess = Guess()
        language = guess.language_name(code)
        print("LANGUAGE FOUND IS : " + language + "\n")
        return language


def operation(code, command):
    if os.path.exists("file.py"):
        os.remove("file.py")
    file = open("file.py", "a")
    file.write(code)
    file.close()
    pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    std_out, std_err = pipes.communicate()
    if pipes.returncode == 123:
        print("Errore rilevato, ritorno il codice originario...\n")
        return code
    else:
        f = open("file.py", "r")
        contents = f.read()
        f.close()
        print("Modifica effettuata, ritorno il nuovo codice...:\n " + contents + "\n")
        return contents


'''
Reindent code
'''


class SnippetReindent(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        print("Eseguendo black...GET\n")
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        code_modified = operation(code, ["black", "file.py"])
        return JsonResponse(status=status.HTTP_200_OK, data={"code_modified": code_modified})

    def post(self, request):
        print("Eseguendo black...POST\n")
        if not request.data.get('code'):
            return Response(status=status.HTTP_200_OK, data="You must specify the code into body (code: 'code') ")
        code = request.data.get('code')
        code_modified = operation(code, ["black", "file.py"])
        return JsonResponse(status=status.HTTP_200_OK, data={"code_modified": code_modified})

    def patch(self, request, pk):
        print("Eseguendo black...PATCH\n")
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        code_modified = operation(code, ["black", "file.py"])
        snippet.code = code_modified
        snippet.save()
        return JsonResponse(status=status.HTTP_200_OK, data={"code_modified": code_modified})


'''
Order Import
'''


class SnippetOrderImport(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        print("Ordinando le importazioni...GET\n")
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        code_modified = operation(code, ["isort", "file.py"])
        return JsonResponse(status=status.HTTP_200_OK, data={"code_modified": code_modified})

    def post(self, request):
        print("Ordinando le importazioni...POST\n")
        if not request.data.get('code'):
            return Response(status=status.HTTP_200_OK, data="You must specify the code into body (code: 'code') ")
        code = request.data.get('code')
        code_modified = operation(code, ["isort", "file.py"])
        return JsonResponse(status=status.HTTP_200_OK, data={"code_modified": code_modified})

    def patch(self, request, pk):
        print("Ordinando le importazioni...PATCH\n")
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        code_modified = operation(code, ["isort", "file.py"])
        snippet.code = code_modified
        snippet.save()
        return JsonResponse(status=status.HTTP_200_OK, data={"code_modified": code_modified})

#---------------------------------------------------

def check_operation(code, command):
    if os.path.exists("file.py"):
        os.remove("file.py")
    file = open("file.py", "a")
    file.write(code)
    file.close()
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    return output


class SnippetPylint(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        pylint_output = check_operation(code, "pylint file.py")
        return JsonResponse(status=status.HTTP_200_OK, data={"pylint_output": pylint_output})

    def post(self, request):
        if not request.data.get('code'):
            return Response(status=status.HTTP_200_OK, data="You must specify the code into body (code: 'code') ")
        code = request.data.get('code')
        pylint_output = check_operation(code, "pylint file.py")
        return JsonResponse(status=status.HTTP_200_OK, data={"pylint_output": pylint_output})


class SnippetPyflakes(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        pyflakes_output = check_operation(code, "pyflakes file.py")
        return JsonResponse(status=status.HTTP_200_OK, data={"pyflakes_output": pyflakes_output})

    def post(self, request):
        if not request.data.get('code'):
            return Response(status=status.HTTP_200_OK, data="You must specify the code into body (code: 'code') ")
        code = request.data.get('code')
        pyflakes_output = check_operation(code, "pyflakes file.py")
        return JsonResponse(status=status.HTTP_200_OK, data={"pyflakes_output": pyflakes_output})


class SnippetFlake8(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        flake8_output = check_operation(code, "flake8 file.py")
        return JsonResponse(status=status.HTTP_200_OK, data={"flake8_output": flake8_output})

    def post(self, request):
        if not request.data.get('code'):
            return Response(status=status.HTTP_200_OK, data="You must specify the code into body (code: 'code') ")
        code = request.data.get('code')
        flake8_output = check_operation(code, "flake8 file.py")
        return JsonResponse(status=status.HTTP_200_OK, data={"flake8_output": flake8_output})


class SnippetMypy(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        mypy_output = check_operation(code, "mypy file.py")
        return JsonResponse(status=status.HTTP_200_OK, data={"mypy_output": mypy_output})

    def post(self, request):
        if not request.data.get('code'):
            return Response(status=status.HTTP_200_OK, data="You must specify the code into body (code: 'code') ")
        code = request.data.get('code')
        mypy_output = check_operation(code, "mypy file.py")
        return JsonResponse(status=status.HTTP_200_OK, data={"mypy_output": mypy_output})


class SnippetExecute(APIView):
    permission_classes = (IsAuthenticated,)

    def operation(self, code):
        if os.path.exists("file.py"):
            os.remove("file.py")
        file = open("file.py", "a")
        file.write(code)
        file.close()
        with open("file.py") as f:
            source = f.read()
        valid = True
        try:
            ast.parse(source)
        except SyntaxError:
            valid = False
            # traceback.print_exc()  # Remove to silence any errros
        return valid

    def get(self, request, pk):
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        executable_output = self.operation(code)
        return JsonResponse(status=status.HTTP_200_OK, data={"executable": str(executable_output)})

    def post(self, request):
        if not request.data.get('code'):
            return Response(status=status.HTTP_200_OK, data="You must specify the code into body (code: 'code') ")
        code = request.data.get('code')
        executable_output = self.operation(code)
        return JsonResponse(status=status.HTTP_200_OK, data={"executable": str(executable_output)})

    def patch(self, request, pk):
        snippet = Snippet.objects.get(pk=pk)
        if snippet.owner != self.request.user.username:
            raise PermissionDenied
        code = SnippetSerializer(snippet).data.get('code')
        executable_output = self.operation(code)
        snippet.executable = executable_output  # true or false
        snippet.save()
        return Response(status=status.HTTP_200_OK, data={"executable": str(executable_output)})
