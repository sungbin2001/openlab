import seaborn as sns
import pandas as pd
import numpy as np
import requests
import json
import sqlite3
import url_arrival 
### 지하철 다니는 시간에만 코드 가능 실시간 도착 정보 open api에서 에러 ### 
def get_arrival_Data(): # 실시간 도착 정보 데이터 얻기
    response=[0]*100
    result=[0]*100
    loc=1
    df=pd.DataFrame(columns=['역이름','호선','방향','도착메세지','열차번호'])
    for i in range(53):
        response[i] = requests.get(url_arrival.url[i])
        result[i]=response[i].json()
        for j in range(result[i]['realtimeArrivalList'][0]['totalCount']): # 값 이해하기 쉽도록 변환
            if(result[i]['realtimeArrivalList'][j]['subwayId']=='1001'):
                result[i]['realtimeArrivalList'][j]['subwayId']='1호선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1002'):
                result[i]['realtimeArrivalList'][j]['subwayId']='2호선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1003'):
                result[i]['realtimeArrivalList'][j]['subwayId']='3호선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1004'):
                result[i]['realtimeArrivalList'][j]['subwayId']='4호선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1005'):
                result[i]['realtimeArrivalList'][j]['subwayId']='5호선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1006'):
                result[i]['realtimeArrivalList'][j]['subwayId']='6호선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1007'):
                result[i]['realtimeArrivalList'][j]['subwayId']='7호선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1009'):
                result[i]['realtimeArrivalList'][j]['subwayId']='9호선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1063'):
                result[i]['realtimeArrivalList'][j]['subwayId']='경의중앙선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1067'):
                result[i]['realtimeArrivalList'][j]['subwayId']='경춘선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1075'):
                result[i]['realtimeArrivalList'][j]['subwayId']='수인분당선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1077'):
                result[i]['realtimeArrivalList'][j]['subwayId']='신분당선'
            elif(result[i]['realtimeArrivalList'][j]['subwayId']=='1093'):
                result[i]['realtimeArrivalList'][j]['subwayId']='서해선'
            df.loc[loc]=result[i]['realtimeArrivalList'][j]['statnNm'],result[i]['realtimeArrivalList'][j]['subwayId'],result[i]['realtimeArrivalList'][j]['trainLineNm'],result[i]['realtimeArrivalList'][j]['arvlMsg2'],result[i]['realtimeArrivalList'][j]['btrainNo']
            loc +=1    
    return df
get_arrival_Data()
def connect_arrival_db(): # 실시간 도착 정보 데이터 데이터베이스에 값 입력
    df=get_arrival_Data()
    con=sqlite3.connect("D:/Users/a/db_project/project.db") 
    cur=con.cursor()
    cur.execute("delete from Realtime_arrival ") 
    for row in df.itertuples(): 
        sql="insert into Realtime_arrival (역이름,호선,방향,도착메세지,열차번호) values (?,?,?,?,?)" 
        cur.execute(sql,(row[1],row[2],row[3],row[4],row[5]))
    con.commit()

def get_telnum_Data(): # 지하철역 전화번호,주소 데이터 얻기
    url = 'http://openapi.seoul.go.kr:8088/6f67437066706a7339387243484368/json/StationAdresTelno/1/42/7/'
    res = requests.get(url)
    response_telnum=res
    if(response_telnum.status_code==200):
        result_telnum=response_telnum.json()
    
    df_telnum=pd.DataFrame(columns=['역이름','도로명주소','전화번호'])
    for i in range(42):
        df_telnum.loc[i+1]=[result_telnum['StationAdresTelno']['row'][i]['STATN_NM'],result_telnum['StationAdresTelno']['row'][i]['RDNMADR'],result_telnum['StationAdresTelno']['row'][i]['TELNO']]
    return df_telnum

def connect_telnum_db(): # 지하철역 전화번호, 주소 데이터베이스에 값 입력
    df=get_telnum_Data()
    con=sqlite3.connect("D:/Users/a/db_project/project.db") 
    cur=con.cursor()
    cur.execute("delete from Station_info ") 
    for row in df.itertuples(): 
        sql="insert into Station_info (역이름,도로명주소,전화번호) values (?,?,?)" 
        cur.execute(sql,(row[1],row[2],row[3]))
    con.commit()

def Get_weekday_data(): # 평일 첫차,막차 데이터
    url_weekday_up='http://openapi.seoul.go.kr:8088/504d435a45706a73313034454e504d78/json/SearchFirstAndLastTrainbyLineServiceNew/1/52/07호선/1/1/'
    response_weekday_up=requests.get(url_weekday_up)
    result_weekday_up=response_weekday_up.json()

    url_weekday_down='http://openapi.seoul.go.kr:8088/504d435a45706a73313034454e504d78/json/SearchFirstAndLastTrainbyLineServiceNew/1/52/07호선/2/1/'
    response_weekday_down=requests.get(url_weekday_down)
    result_weekday_down=response_weekday_down.json()
    loc=0
    df=pd.DataFrame(columns=['역이름','요일','방향','첫차시간','첫차출발역','첫차종착역','막차시간','막차출발역','막차종착역'])
    for i in range(52):
        result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG']='평일'
        result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG']='상행'
        df.loc[loc]=result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['STATION_NM'],result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG'],result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG'],result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['FIRST_TIME'],result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYSNAME'],result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYENAME'],result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['LAST_TIME'],result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYSNAME'],result_weekday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYENAME']
        loc +=1   
    for i in range(52):
        result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG']='평일'
        result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG']='하행'
        df.loc[loc]=result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['STATION_NM'],result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG'],result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG'],result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['FIRST_TIME'],result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYSNAME'],result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYENAME'],result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['LAST_TIME'],result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYSNAME'],result_weekday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYENAME']
        loc +=1    
    return df

def Get_sat_data(): # 토요일 첫차,막차 데이터
    url_sat_up='http://openapi.seoul.go.kr:8088/504d435a45706a73313034454e504d78/json/SearchFirstAndLastTrainbyLineServiceNew/1/52/07호선/1/2/'
    response_sat_up=requests.get(url_sat_up)
    result_sat_up=response_sat_up.json()

    url_sat_down='http://openapi.seoul.go.kr:8088/504d435a45706a73313034454e504d78/json/SearchFirstAndLastTrainbyLineServiceNew/1/52/07호선/2/2/'
    response_sat_down=requests.get(url_sat_down)
    result_sat_down=response_sat_down.json()
    loc=0
    df=pd.DataFrame(columns=['역이름','요일','방향','첫차시간','첫차출발역','첫차종착역','막차시간','막차출발역','막차종착역'])
    for i in range(52):
        result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG']='토요일'
        result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG']='상행'
        df.loc[loc]=result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['STATION_NM'],result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG'],result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG'],result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['FIRST_TIME'],result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYSNAME'],result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYENAME'],result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['LAST_TIME'],result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYSNAME'],result_sat_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYENAME']
        loc +=1   
    for i in range(52):
        result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG']='토요일'
        result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG']='하행'
        df.loc[loc]=result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['STATION_NM'],result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG'],result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG'],result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['FIRST_TIME'],result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYSNAME'],result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYENAME'],result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['LAST_TIME'],result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYSNAME'],result_sat_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYENAME']
        loc +=1    
    return df

def Get_holiday_data(): # 공휴일 첫차,막차 데이터
    url_holiday_up='http://openapi.seoul.go.kr:8088/504d435a45706a73313034454e504d78/json/SearchFirstAndLastTrainbyLineServiceNew/1/52/07호선/1/3/'
    response_holiday_up=requests.get(url_holiday_up)
    result_holiday_up=response_holiday_up.json()

    url_holiday_down='http://openapi.seoul.go.kr:8088/504d435a45706a73313034454e504d78/json/SearchFirstAndLastTrainbyLineServiceNew/1/52/07호선/2/3/'
    response_holiday_down=requests.get(url_holiday_down)
    result_holiday_down=response_holiday_down.json()
    loc=0
    df=pd.DataFrame(columns=['역이름','요일','방향','첫차시간','첫차출발역','첫차종착역','막차시간','막차출발역','막차종착역'])
    for i in range(52):
        result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG']='공휴일'
        result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG']='상행'
        df.loc[loc]=result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['STATION_NM'],result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG'],result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG'],result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['FIRST_TIME'],result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYSNAME'],result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYENAME'],result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['LAST_TIME'],result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYSNAME'],result_holiday_up['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYENAME']
        loc +=1   
    for i in range(52):
        result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG']='공휴일'
        result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG']='하행'
        df.loc[loc]=result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['STATION_NM'],result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['WEEK_TAG'],result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['INOUT_TAG'],result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['FIRST_TIME'],result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYSNAME'],result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['F_SUBWAYENAME'],result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['LAST_TIME'],result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYSNAME'],result_holiday_down['SearchFirstAndLastTrainbyLineServiceNew']['row'][i]['L_SUBWAYENAME']
        loc +=1    
    return df
    
def connect_time_db():
    df=Get_weekday_data()
    df_sat=Get_sat_data()
    df_holiday=Get_holiday_data()
    con=sqlite3.connect("D:/Users/a/db_project/project.db") # 
    cur=con.cursor()
    cur.execute("delete from Time ") 
    # 평일 정보 DB에 값 입력
    for row in df.itertuples():
        sql="insert into Time (역이름,요일,방향,첫차시간,첫차출발역,첫차종착역,막차시간,막차출발역,막차종착역) values (?,?,?,?,?,?,?,?,?)" # 테이블 이름 바꾸기
        cur.execute(sql,(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
        
    # 토요일 정보 DB에 값 입력
    for row in df_sat.itertuples(): 
        sql="insert into Time (역이름,요일,방향,첫차시간,첫차출발역,첫차종착역,막차시간,막차출발역,막차종착역) values (?,?,?,?,?,?,?,?,?)" # 테이블 이름 바꾸기
        cur.execute(sql,(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
        
    # 공휴일 정보 DB에 값 입력
    for row in df_holiday.itertuples():
        sql="insert into Time (역이름,요일,방향,첫차시간,첫차출발역,첫차종착역,막차시간,막차출발역,막차종착역) values (?,?,?,?,?,?,?,?,?)" # 테이블 이름 바꾸기
        cur.execute(sql,(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
    con.commit()
    
connect_arrival_db()
# 주소, 전화번호, 첫차,막차 시간은 자주 바뀌지 않으므로 갱신 필요할 때 주석 풀어서 업데이트
#connect_telnum_db()
#connect_time_db()

