from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.permissions import AllowAny
from user.forms import AccountForm
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountProfileSerializer, FoodSerializer
from django.shortcuts import render
from user.tokens import Token
from .recaptchas import is_recaptcha_correct
from .accounts import UserAccount
from .foods import DailyFood, Food


"""
POST : /api/accounts/
용도 : 회원가입 요청이 들어오면 DB 생성 및 이메일 전송
"""
class APIForAccountRegistration(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        form_data = AccountForm(request.data)

        if not is_recaptcha_correct(request.data['g-recaptcha-response']):
            return Response(status=HTTP_400_BAD_REQUEST)

        if form_data.is_valid():
            AccountInfo = UserAccount(form_data.cleaned_data['username'], form_data.cleaned_data['password'])
            if AccountInfo.already_have_username() or AccountInfo.already_have_email(form_data.cleaned_data['email']):
                return Response(status=HTTP_400_BAD_REQUEST)

            new_account = form_data.save(commit=False)
            new_account.set_password(form_data.cleaned_data['password'])
            new_account.save()

            user = AccountInfo.get_account()
            AccountInfo.send_email(user.email)
            return Response('success', status=HTTP_200_OK)

        else:
            return Response('fail', status=HTTP_400_BAD_REQUEST)


""" 
GET : /api/accounts/verify/<str:id>/
용도 : 아이디에 대한 값이 이미 존재하는지 여부를 리턴

POST : /api/accounts/verify/
용도 : 이메일에 대한 값이 이미 존재하는지 여부를 리턴
"""
class APIForNewAccountCheck(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username):
        AccountInfo = UserAccount(username, None)
        if AccountInfo.already_have_username():
            return Response("이미 사용중인 아이디입니다.", status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_200_OK)

    def post(self, request):
        AccountInfo = UserAccount(None, None)
        email = request.data['email']
        if AccountInfo.already_have_email(email):
            return Response("이미 사용중인 아이디입니다.", status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_200_OK)


"""
GET : (/api/activate/<str:uidb64>/<str:token>)
용도 : 회원가입시 전송되는 이메일을 통해 계정 활성화 여부 결정
"""
class APIForEmailActivation(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        AccountInfo = UserAccount(None, None)
        user = AccountInfo.get_account_by_pk(uidb64)
        res = AccountInfo.check_account_activation(token)
        return render(request, 'emailverifysuccess.html', {'result': res})


"""
GET : user/apis.py -> get_user_profile (/api/accounts/profile/<str:username>)
용도  : 토큰의 사용자 아이디 정보로 프로파일 정보 가져옴
"""
class APIForAccountProfile(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = AccountProfileSerializer

    def get(self, request, username):
        AccountInfo = UserAccount(username, None)
        if AccountInfo.is_account_available():
            serialized = AccountProfileSerializer(AccountInfo.account)
            return Response(serialized.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


"""
POST : user/apis.py -> get_user_token (/api/accounts/login/)
용도  : 사용자 아이디 패스워드 검증 후 token 발급 
"""
class APIForAccountAuthentication(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        if not is_recaptcha_correct(request.data['g-recaptcha-response']):
            return Response("FAIL.", status=HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']
        AccountInfo = UserAccount(username, password)
        if AccountInfo.is_password_correct():
            tk = Token(None)
            token = tk.get_account_token(username, password)
            if token is not None:
                return Response({'token': token}, status=HTTP_200_OK)
            else:
                return Response(status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


"""
POST : user/apis.py -> None (/api/food/)
용도  : 특정 음식에 대한 이미지 정보를 가져옴

GET : food/apis.py -> get_food_detail (/api/food/<str:foodname>) with POST_DATA['foodname']
용도 : 특정 음식에 대한 세부 정보를 가져옴
"""
class APIForFoodDetail(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, foodname):
        if not foodname:
            return Response(status=HTTP_400_BAD_REQUEST)
        UserFood = DailyFood(None)
        try:
            res = UserFood.get_food_info(foodname)
            serialized = FoodSerializer(res)
            return Response(serialized.data, status=HTTP_200_OK)

        except:
            return Response(status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        if not request.data['foodname']:
            return Response(status=HTTP_400_BAD_REQUEST)
        try:
            img = Food.objects.get(menuname=request.data['foodname']).profile
            return HttpResponse(img, content_type='*/*', status=HTTP_200_OK)

        except:
            return Response('fail', status=HTTP_400_BAD_REQUEST)



"""
GET : user/apis.py -> get_user_foodcount (/api/food/user/<str:username>)
용도  : 특정 기간내에 특정 음식을 몇 번 먹었는지 정보 가져옴

POST : food/apis.py -> get_user_food (/api/food/user/<str:username>) with post_data['foodname']
용도 : 특정 음식을 아침/점심/저녁에 각각 몇 번 먹었는지에 대한 정보 가져옴
"""
class APIForUserFoodDetail(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, username):
        if not username:
            return Response(status=HTTP_400_BAD_REQUEST)

        UserFood = DailyFood(username)
        foodlist = UserFood.get_user_food_with_day(9)

        if not foodlist.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        else:
            res = UserFood.get_foodcount_with_date()
            return Response(res, status=HTTP_200_OK)

    def post(self, request, username):
        if not username:
            return Response(status=HTTP_400_BAD_REQUEST)
        if not request.POST.get('foodname'):
            return Response(status=HTTP_400_BAD_REQUEST)

        UserFood = DailyFood(username)
        foodlist = UserFood.get_user_food(request.data['foodname'])

        if not foodlist.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        else:
            res = UserFood.get_user_food_mealkind()
            return Response(res, status=HTTP_200_OK)


"""
GET : user/apis.py -> get_user_preference (/api/food/preference/<str:username>)
용도  : 특정 기간 내의 사용자의 음식 리스트를 조회하여 추천 메뉴 7개를 선정함
"""
class APIForUserFoodChoice(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, username):
        UserFood = DailyFood(username)
        foodlist = UserFood.get_user_food_with_day(9)

        if not foodlist.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        else:
            res = UserFood.get_preference()
            return Response(res, status=HTTP_200_OK)


"""
GET : food/apis.py -> get_user_food_by_date (/api/food/<str:username>/<str:date>)
용도 : 특정 기간 정보를 토대로 사용자의 아침/점심/저녁 리스트를 조회하여 돌려줌

POST : food/apis.py -> update_user_food_by_date (/api/food/<str:username>) with POST_DATA[date, mealkind, foodname]
용도 : 특정 기간 정보를 토대로 사용자의 아침/점심/저녁 리스트를 업데이트함

DELETE : food/apis.py -> delete_user_food_by_date (/api/food/date/<str:username>/<str:date>/<str:mealkind>') 
용도 : 특정 기간 정보를 토대로 사용자의 아침/점심/저녁 리스트를 삭제함
"""
class APIForUserFoodDetailByDate(APIView):
    # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, username, date):
        UserFood = DailyFood(username)
        foodlist = UserFood.get_user_food_by_date(date)
        return Response(foodlist, status=HTTP_200_OK)

    def post(self, request, username):
        UserFood = DailyFood(username)

        date = request.data['date']
        mealkind = request.data['mealkind']
        foodname = request.data['foodname']

        try:
            foodinfo = UserFood.get_food_info(foodname)

        except:
            return Response(status=HTTP_400_BAD_REQUEST)

        mealkind_choice = ['B', 'L', 'D']
        if not mealkind in mealkind_choice:
            return Response(status=HTTP_400_BAD_REQUEST)

        try:
            res = UserFood.get_user_food_by_date_and_mealkind(date, mealkind)
            res.food = foodname
            res.save()
            return Response(status=HTTP_200_OK)

        except:
            UserFood.add_user_food(foodname, mealkind, date)
            return Response(status=HTTP_201_CREATED)

    def delete(self, request, username, date, mealkind):
        try:
            UserFood = DailyFood(username)
            res = UserFood.delete_user_food(date, mealkind)
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

# '''
# GET : None
# 용도 : 특정 메뉴에 대한 사용자들의 댓글 정보를 가져옴
# '''
# class APIForFoodComment(APIView):
#     # FIXME : AUTHENTICATION, PERMISSION LEVEL TO TOKEN
#     authentication_classes = (BasicAuthentication,)
#     permission_classes = (AllowAny,)
#     serializer_class = CommentSerializer
#
#     def get(self, request, foodname):
#         food = Food.objects.get(menuname=foodname)
#         data = FoodComment.objects.select_related('food').filter(food=food, parent=None)
#
#         # serialized = self.get_serializer(data, many=True)
#         serialized = CommentSerializer(data, many=True)
#
#         # for row in data:
#         #     print(row)
#         # FoodComment.objects.filter(food=food)
#         return Response(serialized.data, HTTP_200_OK)