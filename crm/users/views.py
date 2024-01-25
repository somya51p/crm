from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.models import User

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from . serializer import UserSerializer
# Create your views here.

class SignUpAPI(APIView):
    def post(self, request, format = None):
        data_get = request.data
        value_set = {
            'message' : '',
            'error' : '',
            'user' : '',   
            'keys' : '',   
        }
        if 'login' in request.path or 'sign' in request.path:
            if 'email' not in data_get:
                value_set['message'] = 'Error occur Keys missing'
                value_set['keys'] = 'email'
                value_set['status'] = '0'
                return Response(data = value_set , status= status.HTTP_400_BAD_REQUEST)
            
            elif not data_get['email']:
                value_set['message'] = 'Error occur Data missing email empty'
                value_set['keys'] = ''
                value_set['status'] = '0'
                return Response(data = value_set , status= status.HTTP_400_BAD_REQUEST)
            
            elif data_get['email']:
                email  = data_get['email']
                user = User.objects.filter(email = email)
                if user.exists():
                    user = user[0]
                    value_set['message'] = 'User Exist we Login him'
                    if not user.login_type:
                        if user.check_password(data_get['password']):
                            serialize_data = UserSerializer(user).data
                            value_set['user'] = serialize_data
                            user_token,created = Token.objects.get_or_create(user = user)
                            value_set['user']['Token'] = user_token.key
                            value_set['status'] = '1'
                            return Response(data = value_set , status= status.HTTP_200_OK)
                        else:
                            value_set['message'] = "Password didn't match"
                            value_set['keys'] = ''
                            value_set['status'] = '0'

                            return Response(data = value_set , status= status.HTTP_400_BAD_REQUEST)

                    else: 
                        if 'login_type' in  data_get:
                            if  data_get['login_type'] == user.login_type :
                                serialize_data = UserSerializer(user).data
                                value_set['user'] = serialize_data
                                user_token,created = Token.objects.get_or_create(user = user)
                                value_set['user']['Token'] = user_token.key
                                value_set['status'] = '1'
                                return Response(data = value_set , status= status.HTTP_200_OK)
                            else:
                                value_set['message'] = "Login type did not match"
                                value_set['keys'] = ''
                                value_set['status'] = '0'

                                return Response(data = value_set , status= status.HTTP_400_BAD_REQUEST)
                        else:
                            print(request.POST)
                            value_set['message'] = "there is not password / login_type"
                            value_set['keys'] = ''
                            value_set['status'] = '0'

                            return Response(data = value_set , status= status.HTTP_400_BAD_REQUEST)
                    
                elif not 'login' in request.path:
                    user = User()
                    user.email = data_get['email']
                    if 'first_name' in data_get:
                        user.first_name = data_get['first_name']

                    if 'gender' in data_get:
                        user.gender = data_get['gender']

                    if 'role' in data_get:
                        user.role = data_get['role']

                    if 'birth_date' in data_get:
                        if data_get['birth_date']:
                            user.birth_date = data_get['birth_date']

                    if 'mobile' in data_get:
                        user.mobile = data_get['mobile']

                    if 'password' in data_get:
                        user.password = data_get['password']
                        user.set_password = data_get['password']

                    elif'login_type' in data_get:
                        user.login_type = data_get['login_type']
                    else:
                        value_set['message'] = 'password / login_type, Both key available but there is no data inside'
                        value_set['keys'] = ''
                        value_set['status'] = '0'
                        return Response(data = value_set , status= status.HTTP_400_BAD_REQUEST)
                    
                    user.save()
                    serialize_data = UserSerializer(user).data
                    value_set['message'] = 'Account has been created'
                    value_set['user'] = serialize_data
                    user_token,created = Token.objects.get_or_create(user = user)
                    value_set['user']['Token'] = user_token.key
                    value_set['status'] = '1'
                    return Response(data = value_set , status= status.HTTP_200_OK)

                else:
                    value_set['message'] = 'You are using worng api.'
                    value_set['error'] = 'User not exist'
                    value_set['status'] = '0'
                    return Response(data = value_set , status= status.HTTP_400_BAD_REQUEST)
            