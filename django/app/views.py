from urllib import request

import pytz
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection
from datetime import datetime
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.conf import settings
from .models import User, Orders, Place, Type
from .models import Cinema
from .models import Hall
from .models import FilmArrangement
from .models import Movie
from .models import SeatModel
from datetime import datetime, timedelta
import os
import glob


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # 获取前端传递的字段
        username = data.get('username')
        password = data.get('password')
        gender = data.get('gender')
        phone = data.get('phone')
        print(username, password, gender, phone)

        if not username:
            return JsonResponse({"error": "用户名不能为空"}, status=400)
        if not password:
            return JsonResponse({"error": "密码不能为空"}, status=400)
        if not phone:
            return JsonResponse({"error": "手机号不能为空"}, status=400)

        # 检查用户名和手机号是否已被注册
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "用户名已存在"}, status=400)

        if User.objects.filter(uphone=phone).exists():
            return JsonResponse({"error": "手机号已被注册"}, status=400)

        # 创建新用户
        user = User.objects.create(
            username=username,
            upassword=password,
            ugender=gender,
            uphone=phone,
            utype="normal"
        )

        return JsonResponse({"message": "注册成功"}, status=201)

    return JsonResponse({"error": "请求方法错误"}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        print(username, password, role)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(uphone=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "用户名或手机号不存在"}, status=400)

        if user.upassword != password:
                    return JsonResponse({"error": "密码错误"}, status=400)

        if role == "admin" and user.utype != "admin":
            return JsonResponse({"error": "您不是管理员","uid": user.uid}, status=403)



        return JsonResponse({"message": "登录成功","uid": user.uid}, status=201)

@csrf_exempt
def cinemascontroller(request):
    try:
        # 获取所有影院记录
        cinemas = Cinema.objects.all()

        # 构造一个字典，存储影院信息
        cinema_list = []
        for cinema in cinemas:
            cinema_list.append({
                'cid': cinema.cid,
                'cname': cinema.cname
            })

        # 返回 JSON 格式的响应
        return JsonResponse(cinema_list, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def get_cinema(request):
    if request.method == 'POST':
        try:
            cid = int(request.body.decode('utf-8'))
            cinema = Cinema.objects.get(cid=cid)
            data = {
                'cid': cinema.cid,
                'cname': cinema.cname,
            }
            return JsonResponse(data)
        except Cinema.DoesNotExist:
            return JsonResponse({'error': 'Cinema not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def get_halls(request):
    if request.method == 'POST':
        try:
            # 获取请求体中的影院ID（cid）
            cid = int(request.body.decode('utf-8'))
            cinema = Cinema.objects.get(cid=cid)
            halls = Hall.objects.filter(cid=cinema)
            hall_data = []
            for hall in halls:
                if hall.h_active == False:
                    continue
                hall_data.append({
                    'hid': hall.hid,
                    'hname': hall.hname,
                })
            return JsonResponse(hall_data, safe=False)
        except Cinema.DoesNotExist:
            return JsonResponse({'error': 'Cinema not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def get_hall_arrangement_today(request):
    if request.method == 'POST':
        try:
            hid = int(request.body.decode('utf-8'))
            #print('第一行:',hid)

            arrangements = FilmArrangement.objects.filter(hid=hid)
            #print('第三行:',arrangements)

            arrangement_data = []
            for arrangement in arrangements:
                #print('第四行:',arrangement.mid)
                #print('第五行:',int(arrangement.mid.mid))
                the_movie = Movie.objects.get(mid=int(arrangement.mid.mid))
                #print('第六行:',the_movie.mid,the_movie.mname,the_movie.mtime,arrangement.fstarttime,arrangement.fendtime,arrangement.fid)

                if arrangement.f_active == False:
                    continue

                arrangement_data.append({
                    'mid': the_movie.mid,
                    'mname': the_movie.mname,
                    'mtime': the_movie.mtime,
                    'fstarttime': arrangement.fstarttime,
                    'fendtime': arrangement.fendtime,
                    'fid': arrangement.fid
                })
            return JsonResponse(arrangement_data, safe=False)
        except FilmArrangement.DoesNotExist:
            return JsonResponse({'error': 'Film Arrangement not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def get_hall_seatmodel(request):
    if request.method == 'POST':
        try:
            hallid = int(request.body.decode('utf-8'))
            seatmodel = Hall.objects.get(hid=hallid)
            #print(seatmodel.sid)
            seatmodel_data = SeatModel.objects.get(sid=seatmodel.sid)
            return JsonResponse(seatmodel_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def get_hall_details(request):
    if request.method == 'POST':
        try:
            # 获取影厅ID
            hid = int(request.body.decode('utf-8'))
            #print(hid)

            # 获取影厅名称
            hall = Hall.objects.get(hid=hid)
            #print(1,hall)
            hallname = hall.hname
            #print(2,hallname)

            # 获取影厅的座位布局
            seat_model = hall.sid
            #print(3,seat_model)
            seat_layout = seat_model.smodel  # 座位布局字符串
            #print(seat_layout)

            # 解析座位布局字符串，获取最大的列数
            seat_array = seat_layout.split(',')
            max_column = 0  # 初始化最大列数
            #print(max_column)
            #print(seat_array)
            for i in range(1, len(seat_array), 4):
                col = seat_array[i]
                # 解析列信息，更新最大列数
                if col != '':
                    col = int(str(seat_array[i])[1:])  # 解析列号，去掉 "c" 并转换为整数
                    #print(col)
                    if col > max_column:
                        max_column = col
            #print(max_column)

            # 获取影厅的排片安排
            arrangements_original = FilmArrangement.objects.filter(hid=hid)
            #print(5,arrangements_original)
            arrangements = []
            for arrangement in arrangements_original:
                movie = Movie.objects.get(mid=arrangement.mid.mid)

                if arrangement.f_active == False:
                    continue
                if movie.m_active == False:
                    continue

                # 将排片信息加入到列表中
                arrangements.append({
                    'fid': arrangement.fid,
                    'mname': movie.mname,
                    'fstarttime': arrangement.fstarttime,
                    'fendtime': arrangement.fendtime,
                    'fcost': arrangement.fcost,
                })

            # 返回影厅详细信息
            data = {
                'hname': hallname,
                'smodel': seat_layout,
                'arrangements': arrangements,
                'maxcolumn': max_column
            }

            return JsonResponse(data)

        except Hall.DoesNotExist:
            return JsonResponse({'error': 'Hall not found'}, status=404)
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Movie not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def now_playing(request):
    try:
        movies = Movie.objects.all().order_by('-mhot')[:5]  # 获取热度前5的电影
        movie_data = []
        for movie in movies:

            # 封面图片存放在 media/movies/ 目录下，文件名与电影名称相同
            cover_filename = os.path.join(settings.MEDIA_ROOT, 'movies', f'{movie.mname}.*')
            cover_files = glob.glob(cover_filename)

            if cover_files:
                # 如果找到了对应的封面文件，获取第一个文件的路径
                cover_url = f"{settings.MEDIA_URL}movies/{os.path.basename(cover_files[0])}"
            else:
                # 如果没有找到封面文件，可以返回一个默认封面
                cover_url = f"{settings.MEDIA_URL}movies/default_cover.jpg"

            #print(cover_url)

            if movie.m_active == False:
                continue

            movie_data.append({
                'mid': movie.mid,
                'mname': movie.mname,
                'mtime': movie.mtime,
                'mhot': movie.mhot,
                'mscore': movie.mscore,
                'myear': movie.myear,
                'cover': cover_url,
            })
        return JsonResponse(movie_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def getmovies(request):
    try:
        movies = Movie.objects.all().order_by('-mhot')
        movie_data = []
        for movie in movies:

            # 封面图片存放在 media/movies/ 目录下，文件名与电影名称相同
            cover_filename = os.path.join(settings.MEDIA_ROOT, 'movies', f'{movie.mname}.*')
            cover_files = glob.glob(cover_filename)

            if cover_files:
                # 如果找到了对应的封面文件，获取第一个文件的路径
                cover_url = os.path.join(settings.MEDIA_URL, 'movies', os.path.basename(cover_files[0]))
            else:
                # 如果没有找到封面文件，可以返回一个默认封面
                cover_url = os.path.join(settings.MEDIA_URL, 'movies', 'default_cover.jpg')

            #print(cover_url)
            if movie.m_active == False:
                continue

            movie_data.append({
                'mid': movie.mid,
                'mname': movie.mname,
                'mtime': movie.mtime,
                'mhot': movie.mhot,
                'mscore': movie.mscore,
                'myear': movie.myear,
                'cover': cover_url,  # 假设封面字段为 'cover'
            })
        return JsonResponse(movie_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def movie_details(request):
    try:
        # 获取请求中的 movieId
        movie_id = int(request.body.decode('utf-8'))
        #print(movie_id)

        if not movie_id:
            return JsonResponse({'error': 'Movie ID is required'}, status=400)

        movie = Movie.objects.get(mid=movie_id)
        #print(movie)

        # 获取封面图片的 URL
        cover_filename = os.path.join(settings.MEDIA_ROOT, 'movies', f'{movie.mname}.*')
        cover_files = glob.glob(cover_filename)

        if cover_files:
            # 如果找到了对应的封面文件，获取第一个文件的路径
            cover_url = os.path.join(settings.MEDIA_URL, 'movies', os.path.basename(cover_files[0]))
        else:
            # 如果没有找到封面文件，可以返回一个默认封面
            cover_url = os.path.join(settings.MEDIA_URL, 'movies', 'default_cover.jpg')
        #print(cover_url)

        # 获取电影的类型和来源地
        movie_type = movie.tid.tname if movie.tid else None
        movie_place = movie.pid.pname if movie.pid else None
        #print(movie.mid,movie.mname,movie.mtime,movie.mhot,movie.mscore,movie.myear,movie.mtext,movie_type,movie_place,)

        # 构建电影详情数据
        movie_data = {
            'mid': movie.mid,
            'mname': movie.mname,
            'mtime': movie.mtime,
            'mhot': movie.mhot,
            'mscore': movie.mscore,
            'myear': movie.myear,
            'mtext': movie.mtext,
            'cover': cover_url,
            'type': movie_type,
            'place': movie_place,
        }

        return JsonResponse(movie_data)

    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_movie_halls(request):
    try:
        movie_id = int(request.body.decode('utf-8'))
        #print(movie_id)
        # 获取电影排片安排
        arrangements = FilmArrangement.objects.filter(mid=movie_id)
        #print(arrangements)
        hall_data = []
        #print(1)

        for arrangement in arrangements:
            #print(arrangement.hid)
            hall = Hall.objects.get(hid=arrangement.hid.hid)
            cinema = Cinema.objects.get(cid=arrangement.cid.cid)
            #print(hall.hid,hall.hname,arrangement.fstarttime,arrangement.fendtime,arrangement.fcost,cinema.cname)

            if hall.h_active == False:
                continue

            hall_data.append({
                'hid': hall.hid,
                'hname': hall.hname,
                'fstarttime': arrangement.fstarttime,
                'fendtime': arrangement.fendtime,
                'fcost': arrangement.fcost,
                'cinema': cinema.cname,
            })

        return JsonResponse(hall_data, safe=False)

    except FilmArrangement.DoesNotExist:
        return JsonResponse({'error': 'Film arrangements not found'}, status=404)
    except Hall.DoesNotExist:
        return JsonResponse({'error': 'Hall not found'}, status=404)
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def purchase(request):
    if request.method == 'POST':
        try:
            fid = int(request.body.decode('utf-8'))
            film = FilmArrangement.objects.get(fid=fid)

            hallname = film.hid.hname
            seat_model = film.seatid
            seat_layout = seat_model.seats
            cinemaname = film.cid.cname
            filmname = film.mid.mname

            # 解析座位布局字符串，获取最大的列数
            seat_array = seat_layout.split(',')
            max_column = 0
            for i in range(1, len(seat_array), 4):
                col = seat_array[i]
                # 解析列信息，更新最大列数
                if col != '':
                    col = int(str(seat_array[i])[1:])  # 解析列号，去掉 "c" 并转换为整数
                    #print(col)
                    if col > max_column:
                        max_column = col

            # 获取影厅的排片安排
            starttime = film.fstarttime
            endtime = film.fendtime
            price = film.fcost

            # 获取封面图片的 URL
            cover_filename = os.path.join(settings.MEDIA_ROOT, 'movies', f'{filmname}.*')
            cover_files = glob.glob(cover_filename)

            if cover_files:
                # 如果找到了对应的封面文件，获取第一个文件的路径
                cover_url = os.path.join(settings.MEDIA_URL, 'movies', os.path.basename(cover_files[0]))
            else:
                # 如果没有找到封面文件，可以返回一个默认封面
                cover_url = os.path.join(settings.MEDIA_URL, 'movies', 'default_cover.jpg')

            # 返回影厅详细信息
            data = {
                'filmname': filmname,
                'cinemaname': cinemaname,
                'hname': hallname,
                'smodel': seat_layout,
                'maxcolumn': max_column,
                'starttime': starttime,
                'endtime': endtime,
                'price': price,
                'cover': cover_url,
            }

            return JsonResponse(data)

        except Hall.DoesNotExist:
            return JsonResponse({'error': 'Hall not found'}, status=404)
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Movie not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def updateSeatLayout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fid = data.get('fid')
            updatedLayout = data.get('updatedSeatLayout')
            occupiedSeats = data.get('occupiedSeats')
            uid = str(data.get('uid'))


            the_arrangement = FilmArrangement.objects.get(fid=fid)
            the_seats = the_arrangement.seatid

            # 读取现有的座位布局
            currentLayout = the_seats.seats  # seats 是一个字符串格式 'r1,c1,t1,o0,r1,c2,t2,o1,...'
            seatArray = currentLayout.split(',')

            # 过滤出所有已经被占用的座位 (t2)，返回的结果是所有状态为 t2 的座位信息
            occupiedSeatArray = []
            for i in range(0, len(seatArray), 4):  # 每个座位4个元素
                status = seatArray[i + 2]  # 座位状态在数组的第三个位置
                o = seatArray[i + 3]
                #print(status)
                if status == 't2' and o != "o" + uid:  # 如果状态是 t2 (已占座)
                    occupiedSeatArray.append({
                        'row': int(seatArray[i].strip('r')),  # 获取行号
                        'col': int(seatArray[i + 1].strip('c')),  # 获取列号
                    })


            # 检查当前用户选择的座位是否已经被其他用户占用
            for seat in occupiedSeats:
                row = seat['row']
                col = seat['col']

                # 如果前端发送的座位已经被占用，返回错误
                if any(occupiedSeat['row'] == row and occupiedSeat['col'] == col for occupiedSeat in
                       occupiedSeatArray):
                    return JsonResponse(
                        {'message': 'seats already been taken'},
                        status=200)

            the_seats.seats = updatedLayout
            the_seats.save()

            return JsonResponse({'message': "Seat layout updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def createOrder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            fid = data.get('fid')
            selectedseats = data.get('selectedSeatData')
            tickets = data.get('tickets')
            #print(selectedseats)
            #print(tickets)


            # 将 selectedSeatData 转换成字符串格式
            seat_str = ''.join(
                [f"r{seat['row']},c{seat['col']}," for seat in selectedseats])
            #print(seat_str)

            # 获取相关的外键对象实例
            user = User.objects.get(uid=uid)  # 获取指定的用户
            film_arrangement = FilmArrangement.objects.get(fid=fid)  # 获取指定的排片
            cost1 = film_arrangement.fcost
            cost2 = cost1 * tickets
            #print(cost2)

            utc_now = datetime.now(pytz.utc)
            shanghai_tz = pytz.timezone('Asia/Shanghai')
            shanghai_time = utc_now.astimezone(shanghai_tz)
            #print(shanghai_time)

            true_fid = film_arrangement.fid
            true_uid = user.uid

            ordersorders = Orders.objects.filter()
            maxoid = 0
            for ordero in ordersorders:
                if ordero.oid > maxoid:
                    maxoid = ordero.oid

            Orders.objects.create(oid=maxoid+1,uid_id=true_uid, fid_id=true_fid, otime=shanghai_time, oseats=seat_str, oprice=cost2)

            return JsonResponse({'message': 'Order created successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def myorders(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            orders = Orders.objects.filter(uid_id=uid)
            data = []
            for order in orders:
                arrangement = order.fid
                film_name = arrangement.mid.mname
                starttime = arrangement.fstarttime
                hname = arrangement.hid.hname
                cname = arrangement.cid.cname
                mtime = arrangement.mid.mtime


                data.append({
                    'otime': order.otime,
                    'oseats': order.oseats,
                    'oprice': order.oprice,
                    'mname': film_name,
                    'starttime': starttime,
                    'hname': hname,
                    'cname': cname,
                    'mtime': mtime,
                })

            return JsonResponse({'data': data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def adminorders(request):
    if request.method == 'POST':
        try:
            orders = Orders.objects.filter()

            data = []
            for order in orders:
                arrangement = order.fid
                film_name = arrangement.mid.mname
                starttime = arrangement.fstarttime
                hname = arrangement.hid.hname
                cname = arrangement.cid.cname
                mtime = arrangement.mid.mtime
                yonghuid = order.uid.uid
                yonghuming = order.uid.username


                data.append({
                    'otime': order.otime,
                    'oseats': order.oseats,
                    'oprice': order.oprice,
                    'mname': film_name,
                    'starttime': starttime,
                    'hname': hname,
                    'cname': cname,
                    'mtime': mtime,
                    'yonghuid': yonghuid,
                    'yonghuming': yonghuming,
                })

            return JsonResponse({'data': data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def admingetmovies(request):
    if request.method == 'POST':
        try:
            movies = Movie.objects.filter()
            data = []
            for movie in movies:
                mid = movie.mid
                mname = movie.mname
                mtime = movie.mtime
                mscore = movie.mscore
                mhot = movie.mhot
                tname = movie.tid.tname
                pname = movie.pid.pname
                m_active = movie.m_active
                mtext = movie.mtext
                myear = movie.myear

                # 获取封面图片的 URL
                cover_filename = os.path.join(settings.MEDIA_ROOT, 'movies', f'{mname}.*')
                cover_files = glob.glob(cover_filename)
                if cover_files:
                    # 如果找到了对应的封面文件，获取第一个文件的路径
                    cover_url = os.path.join(settings.MEDIA_URL, 'movies', os.path.basename(cover_files[0]))
                else:
                    # 如果没有找到封面文件，可以返回一个默认封面
                    cover_url = os.path.join(settings.MEDIA_URL, 'movies', 'default_cover.jpg')


                data.append({
                    'mid': mid,
                    'mname': mname,
                    'mscore': mscore,
                    'mhot': mhot,
                    'mtime': mtime,
                    'tname': tname,
                    'pname': pname,
                    'm_active': m_active,
                    'cover': cover_url,
                    'mtext': mtext,
                    'myear': myear,
                })

            return JsonResponse({'data': data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def adminsubmovie(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            movieform = data.get('movie')
            print(data)
            if action == 'edit':
                mid = movieform.get('mid')
                new_mname = movieform.get('mname')
                new_mtime = movieform.get('mtime')
                new_mscore = movieform.get('mscore')
                new_mhot = movieform.get('mhot')
                new_tname = movieform.get('tname')
                new_pname = movieform.get('pname')
                new_mtext = movieform.get('mtext')
                new_myear = movieform.get('myear')

                the_movie = Movie.objects.get(mid=mid)

                the_place = Place.objects.get(pname=new_pname)
                the_movie_pid = the_place.pid
                the_type = Type.objects.get(tname=new_tname)
                the_movie_type = the_type.tid

                the_movie.mname = new_mname
                the_movie.mtime = new_mtime
                the_movie.mscore = new_mscore
                the_movie.mhot = new_mhot
                the_movie.tid_id = the_movie_type
                the_movie.mtext = new_mtext
                the_movie.pid_id = the_movie_pid
                the_movie.myear = new_myear
                the_movie.save()
            if action == 'create':
                new_mname = movieform.get('mname')
                new_mtime = movieform.get('mtime')
                new_mscore = movieform.get('mscore')
                new_mhot = movieform.get('mhot')
                new_tname = movieform.get('tname')
                new_pname = movieform.get('pname')
                new_mtext = movieform.get('mtext')
                new_myear = movieform.get('myear')
                print(new_mname,new_pname)

                the_place = Place.objects.get(pname=new_pname)
                the_movie_pid = the_place.pid
                print(the_movie_pid)
                the_type = Type.objects.get(tname=new_tname)
                the_movie_type = the_type.tid
                print(the_movie_type)

                new_movie = Movie.objects.create(
                    mname=new_mname,
                    mtime=new_mtime,
                    tid=the_movie_type,
                    mhot=new_mhot,
                    mscore=new_mscore,
                    myear=new_myear,
                    mtext=new_mtext,
                    pid=the_movie_pid,
                    m_active=True  # 激活该电影
                )

            return JsonResponse({'action': action}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def admindisablemovie(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mid = data.get('mid')
            the_movie = Movie.objects.get(mid=mid)
            if the_movie.m_active == True:
                the_movie.m_active = False
            elif the_movie.m_active == False:
                the_movie.m_active = True

            the_movie.save()

            arrangements = FilmArrangement.objects.filter(mid_id=mid)
            for ar in arrangements:
                if ar.f_active == False:
                    ar.f_active = True
                elif ar.f_active == True:
                    ar.f_active = False
                ar.save()


            return JsonResponse({'data': mid}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def admingetschedules(request):
    if request.method == 'POST':
        try:
            arrangements = FilmArrangement.objects.filter()
            data = []
            for ar in arrangements:
                fid = ar.fid
                cname = ar.cid.cname
                hname  = ar.hid.hname
                mname = ar.mid.mname
                fstarttime = ar.fstarttime
                fendtime = ar.fendtime
                fcost = ar.fcost
                f_active = ar.f_active

                data.append({
                    'sid': fid,
                    'cinema': cname,
                    'hall': hname,
                    'movie': mname,
                    'start_time': fstarttime,
                    'end_time': fendtime,
                    'price': fcost,
                    'f_active': f_active
                })

            return JsonResponse({'data': data}, status=200)


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def adminsubschedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            form = data.get('schedule')

            if action == 'edit':
                fid = form.get('sid')
                cname = form.get('cinema')
                fstarttime = form.get('start_time')
                fendtime = form.get('end_time')
                fcost = form.get('price')

                fstarttime = fstarttime.replace('T', ' ')
                fendtime = fendtime.replace('T', ' ')
                time_format = '%Y-%m-%d %H:%M'

                # 将时间字符串转换为 datetime 对象
                start_time_obj = datetime.strptime(fstarttime, time_format)
                end_time_obj = datetime.strptime(fendtime, time_format)

                # 使用 timedelta 加 8 小时
                start_time_obj += timedelta(hours=8)
                end_time_obj += timedelta(hours=8)

                # 将 datetime 对象转回字符串
                fstarttime_new = start_time_obj.strftime(time_format)
                fendtime_new = end_time_obj.strftime(time_format)

                start_time_aware = timezone.make_aware(start_time_obj, timezone.get_current_timezone())
                end_time_aware = timezone.make_aware(end_time_obj, timezone.get_current_timezone())


                cid = Cinema.objects.get(cname=cname).cid

                ar = FilmArrangement.objects.get(fid=fid)
                ar.cid_id = cid
                ar.fstarttime = start_time_aware
                ar.fendtime = end_time_aware
                ar.fcost = fcost
                ar.save()

            if action == 'create':
                #print(form)
                cname = form.get('cinema')
                fstarttime = form.get('start_time')
                fendtime = form.get('end_time')
                fcost = form.get('price')
                hname = form.get('hall')
                mname = form.get('movie')



                fstarttime = fstarttime.replace('T', ' ')
                fendtime = fendtime.replace('T', ' ')
                time_format = '%Y-%m-%d %H:%M'

                # 将时间字符串转换为 datetime 对象
                start_time_obj = datetime.strptime(fstarttime, time_format)
                end_time_obj = datetime.strptime(fendtime, time_format)

                # 使用 timedelta 加 8 小时
                start_time_obj += timedelta(hours=8)
                end_time_obj += timedelta(hours=8)

                # 将 datetime 对象转回字符串
                fstarttime_new = start_time_obj.strftime(time_format)
                fendtime_new = end_time_obj.strftime(time_format)

                start_time_aware = timezone.make_aware(start_time_obj, timezone.get_current_timezone())
                end_time_aware = timezone.make_aware(end_time_obj, timezone.get_current_timezone())
                #print(start_time_aware, end_time_aware)

                cid = Cinema.objects.get(cname=cname).cid
                #print(cid)
                hid = Hall.objects.get(hname=hname,cid_id=cid).hid
                #print(hid)
                mid = Movie.objects.get(mname=mname).mid
                #print(mid)
                seatid = Hall.objects.get(hid=hid).sid_id
                #print(seatid)

                filmfilm = FilmArrangement.objects.filter()
                maxfid = 0
                for filmfi in filmfilm:
                    if filmfi.fid > maxfid:
                        maxfid = filmfi.fid

                print(cid, hid, mid,start_time_aware,end_time_aware,seatid,fcost)
                FilmArrangement.objects.create(
                    fid=maxfid+1,
                    cid_id=cid,
                    hid_id=hid,
                    mid_id=mid,
                    fstarttime=start_time_aware,
                    fendtime=end_time_aware,
                    seatid_id=seatid,
                    fcost=fcost,
                    f_active=True
                )


            return JsonResponse({'action': action}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def admindisableschedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fid = data.get('sid')
            ar = FilmArrangement.objects.get(fid=fid)
            if ar.f_active == False:
                ar.f_active = True
            elif ar.f_active == True:
                ar.f_active = False
            ar.save()

            return JsonResponse({'action': 'disable'}, status=200)


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def admingetcinemas(request):
    if request.method == 'POST':
        try:
            halls = Hall.objects.filter()
            data = []
            for hall in halls:
                cname = hall.cid.cname
                hname = hall.hname
                hid = hall.hid
                h_active = hall.h_active

                data.append({
                    'cname': cname,
                    'hall_name': hname,
                    'cid': hid,
                    'h_active': h_active
                })

            return JsonResponse({'data':data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def admindelcinema(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hid = data.get('cid')
            hall = Hall.objects.get(hid=hid)
            if hall.h_active == False:
                hall.h_active = True
            elif hall.h_active == True:
                hall.h_active = False
            hall.save()

            return JsonResponse({'action': 'delete'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


