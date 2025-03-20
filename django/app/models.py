from django.db import models

# 用户表
class User(models.Model):
    utype = models.CharField(max_length=255, verbose_name="用户等级")
    uid = models.BigAutoField(primary_key=True, verbose_name="用户编号")
    username = models.CharField(max_length=255, verbose_name="用户名")
    ugender = models.CharField(max_length=255, verbose_name="用户性别")
    uphone = models.CharField(max_length=255, verbose_name="用户手机号")
    upassword = models.CharField(max_length=255, verbose_name="密码")

    class Meta:
        db_table = "user"

# 类型表
class Type(models.Model):
    tid = models.BigAutoField(primary_key=True, verbose_name="类型编号")
    tname = models.CharField(max_length=255, verbose_name="类型名称")

    class Meta:
        db_table = "type"

# 来源地表
class Place(models.Model):
    pid = models.BigAutoField(primary_key=True, verbose_name="来源地编号")
    pname = models.CharField(max_length=255, verbose_name="来源地")

    class Meta:
        db_table = "place"

# 电影院表
class Cinema(models.Model):
    cid = models.BigAutoField(primary_key=True, verbose_name="电影院编号")
    cname = models.CharField(max_length=255, verbose_name="电影院名称")

    class Meta:
        db_table = "cinema"

# 座位布局模板表
class SeatModel(models.Model):
    sid = models.BigAutoField(primary_key=True, verbose_name="布局模板编号")
    smodel = models.TextField(verbose_name="座位布局")

    class Meta:
        db_table = "seat_model"

# 电影表
class Movie(models.Model):
    mid = models.BigAutoField(primary_key=True, verbose_name="电影编号")
    mtime = models.BigIntegerField(verbose_name="影片时长(分钟)")
    mname = models.CharField(max_length=255, verbose_name="电影名称")
    tid = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="类型编号")
    mhot = models.BigIntegerField(verbose_name="影片热度")
    mscore = models.FloatField(verbose_name="影片评分")
    myear = models.DateField(verbose_name="上线时间")
    mtext = models.CharField(max_length=255, verbose_name="简介")
    pid = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="来源地编号")
    m_active = models.BooleanField(default=True)

    class Meta:
        db_table = "movie"

# 影厅表
class Hall(models.Model):
    hid = models.BigAutoField(primary_key=True, verbose_name="影厅编号")
    cid = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name="所属影院编号")
    hname = models.CharField(max_length=255, verbose_name="影厅名称")
    sid = models.ForeignKey(SeatModel, on_delete=models.CASCADE, verbose_name="座位布局编号")
    h_active = models.BooleanField(default=True)

    class Meta:
        db_table = "hall"

# 座位表
class Seat(models.Model):
    seatid = models.BigAutoField(primary_key=True, verbose_name="布局编号")
    sid = models.ForeignKey(SeatModel, on_delete=models.CASCADE, verbose_name="布局模板编号")
    seats = models.TextField(verbose_name="座位情况")

    class Meta:
        db_table = "seat"


# 排片表
class FilmArrangement(models.Model):
    fid = models.BigIntegerField(primary_key=True, verbose_name="排片编号")
    cid = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name="所在影院")
    hid = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name="所在影厅")
    mid = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="所播电影")
    fstarttime = models.DateTimeField(verbose_name="开播时间")
    fendtime = models.DateTimeField(verbose_name="结束时间")
    seatid = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name="布局编号")
    fcost = models.BigIntegerField(verbose_name="定价")
    f_active = models.BooleanField(default=True)

    class Meta:
        db_table = "film_arrangement"

# 订单表
class Orders(models.Model):
    oid = models.BigIntegerField(primary_key=True, verbose_name="订单编号")
    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="下单用户编号")
    fid = models.ForeignKey(FilmArrangement, on_delete=models.CASCADE, verbose_name="下单排片编号")
    otime = models.DateTimeField(verbose_name="下单时间")
    oseats = models.TextField(verbose_name="所定座位", default='0')
    oprice = models.BigIntegerField(verbose_name="花费金额", default=0)

    class Meta:
        db_table = "orders"
