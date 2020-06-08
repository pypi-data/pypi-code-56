from datetime import datetime, timedelta, timezone
import time
import calendar
import re
import pytz


class Pnp_Datetime:
    """
    Date time functions for easy use
    """
    
    @classmethod
    def datetime_to_str(cls, pi_datetime:datetime, out_format="ISO8601", sep="T") -> str:
        """
        Convert datatime to string

        default format: ISO8601
            2001-01-01T06:28:22.199000+00:00
            2001-01-01 06:28:22.199000+00:00
        """
        if isinstance(pi_datetime, datetime):
            if out_format == "ISO8601":
                return str(pi_datetime.isoformat(sep=sep))


    @classmethod
    def str_to_datetime(cls, pi_str_datetime:str) -> datetime:
        """
        Convert string type datetime to datetime type

        Support format: 
            2001-01-01T06:28:22.199000+00:00
            2001-01-01 06:28:22.199000+00:00

            2001-01-01T06:28:22.198+00:00
            2001-01-01T06:28:22.198+0000

            2001-01-01T06:28:22+00:00
            2001-01-01T06:28:22+0000

            2001-01-01 06:28:22+00:00
            2001-01-01 06:28:22+0000

            2001-01-01T16:41:24Z 
            2001-01-01 16:41:24Z 

        """
        if isinstance(pi_str_datetime, datetime):
            return pi_str_datetime

        re_ISO8601_pattern = r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}'  #2001-01-01T06:41:22.698000+00:00
                                                                                            #2001-01-01 06:41:22.698000+00:00

        re_pattern_11 = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{2}:{0,1}\d{2}'     #2001-01-01T05:28:22.198+00:00
                                                                                            #2001-01-01T05:28:22.198+0000

        re_pattern_21 = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:{0,1}\d{2}'            #2001-01-01T05:28:22+00:00
                                                                                            #2001-01-01T05:28:22+0000
        re_pattern_22 = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{2}:{0,1}\d{2}'            #2001-01-01 05:28:22+00:00
                                                                                            #2001-01-01 05:28:22+0000
        re_pattern_31 = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'                             #2001-01-01T16:41:24Z
        re_pattern_32 = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}Z'                             #2001-01-01 16:41:24Z

        if re.fullmatch(re_ISO8601_pattern, pi_str_datetime):
            return datetime.fromisoformat(pi_str_datetime)

        elif re.fullmatch(re_pattern_11, pi_str_datetime):
            return datetime.strptime(pi_str_datetime, "%Y-%m-%dT%H:%M:%S.%f%z")

        elif re.fullmatch(re_pattern_21, pi_str_datetime):
            return datetime.strptime(pi_str_datetime, "%Y-%m-%dT%H:%M:%S%z")

        elif re.fullmatch(re_pattern_22, pi_str_datetime):
            return datetime.strptime(pi_str_datetime, "%Y-%m-%d %H:%M:%S%z")

        elif re.fullmatch(re_pattern_31, pi_str_datetime):
            return datetime.strptime(pi_str_datetime, "%Y-%m-%dT%H:%M:%S%z")

        elif re.fullmatch(re_pattern_32, pi_str_datetime):
            return datetime.strptime(pi_str_datetime, "%Y-%m-%d %H:%M:%S%z")
        else:
            raise ValueError("Invalid time format:{}, not support now.".format(pi_str_datetime))



    @classmethod
    def utcnow(cls) -> datetime:
        """
        current UTC time, with timezone
        """
        return pytz.utc.localize(datetime.utcnow())

    @classmethod
    def now_of_tz(cls, pi_timezone:str) -> datetime:
        """
        current time of timezone <pi_timezone>, 

        pi_timezone: timezone name, valid timezone name in pytz.all_timezones, like 'US/Alaska', 'Australia/Sydney'
                     https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

        Return datetime with timezone
        """
        dt_utcnow = cls.utcnow()
        tz = pytz.timezone(pi_timezone)
        return dt_utcnow.astimezone(tz)
        

    @classmethod
    def datetime_plus_months(cls, pi_datetime:datetime, pi_months:int) -> datetime:
        """
        Only add from month, if input: Dec, then Jan of next year
        """
        v_month = pi_datetime.month - 1 + pi_months
        v_year = pi_datetime.year + v_month // 12
        v_month = v_month % 12 + 1
        v_day = min(pi_datetime.day, calendar.monthrange(v_year, v_month)[1])

        return pi_datetime.replace(year=v_year, month=v_month, day=v_day)


    @classmethod
    def datetime_minus_months(cls, pi_datetime:datetime, pi_months:int) -> datetime:
        """
        Only minus from month, if input: Jan, then Dec of last year
        """
        if pi_datetime.month > pi_months:
            new_month = pi_datetime.month - pi_months
            new_year = pi_datetime.year
        else:
            new_month = 12 + pi_datetime.month - pi_months
            new_year = pi_datetime.year - 1
            
        new_day = min(pi_datetime.day, calendar.monthrange(new_year, new_month)[1])

        return pi_datetime.replace(year=new_year, month=new_month, day=new_day)


    @classmethod
    def datetime_plus(cls, pi_datetime:datetime, **kwargs) -> datetime:
        """
        datetime plus given years, months, days, hours, minutes, seconds

        example:
            datetime_plus(before_plus, days=3, hours=2, minutes=10, seconds=10)
            before plus: 2001-01-01 10:10:01.000001
             after plus: 2001-01-04 12:20:11.000001

        **kwargs: years=0, months=0, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0
        """
        sub_kwargs = {k:kwargs.get(k) for k in kwargs.keys() if k not in ['years', 'months']}
        v_datetime = pi_datetime + timedelta(**sub_kwargs)

        # add months
        v_months = kwargs.get("months") 
        if v_months and v_months > 0:
            v_datetime = cls.datetime_plus_months(v_datetime, v_months)

        # add years
        v_years = kwargs.get("years") 
        if v_years and v_years > 0:
            v_new_year = v_datetime.year + v_years
            v_datetime = v_datetime.replace(year=v_new_year) 
           
        return v_datetime


    @classmethod
    def datetime_minus(cls, pi_datetime:datetime, **kwargs) -> datetime:
        """
        datetime minus given years, months, days, hours, minutes, seconds

        example:
            datetime_minus(before_minus, days=3, hours=2, minutes=10, seconds=10)
            before minus: 2001-01-04 12:20:11.000001
             after minus: 2001-01-01 10:10:01.000001

        **kwargs:
            days
            hours
            seconds
        """
        sub_kwargs = {k:kwargs.get(k) for k in kwargs.keys() if k not in ['years', 'months']}

        v_time_delta = timedelta(**sub_kwargs)
        v_new_datetime = pi_datetime - v_time_delta

        # minus months
        v_months = kwargs.get("months") 
        if v_months and v_months > 0:
            v_new_datetime = cls.datetime_minus_months(v_new_datetime, v_months)

        # minus years
        v_years = kwargs.get("years") 
        if v_years and v_years > 0:
            v_new_datetime = v_new_datetime.replace(year=(v_new_datetime.year - v_years)) 
           
        return v_new_datetime


    @classmethod
    def local_current_month_begin_time(cls) -> datetime:
        """
        Local current month begin time 
        like: 
            2018-02-01T00:00:00+00:00
        """
        v_local_now = cls.local_now()
        #v_year = v_now.year
        #v_month = v_now.month
        #v_tz_info = v_now.tzinfo

        return v_local_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


    @classmethod
    def current_month_begin_time_of_tz(cls, pi_timezone:str) -> datetime:
        """
        current month begin time of timezone <pi_timezone>
        like: 
            2018-02-01T00:00:00Z
        """
        v_now = cls.now_of_tz(pi_timezone)

        v_year = v_now.year
        v_month = v_now.month
        v_tz_info = v_now.tzinfo

        return datetime(year=v_year, month=v_month, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=v_tz_info)


    @classmethod
    def is_local_daylight_saving(cls) -> bool:
        """
        Check if local system time is in Daylight Saving

        tm_isdst: 1: when daylight savings time is in effect, 
                  0: when it is not. 
                 -1: indicates that this is not known
        """
        v_isdst = time.localtime().tm_isdst
        if v_isdst == 1:
            return True
        elif v_isdst == 0:
            return False
        else:
            raise ValueError("Unknown DST or not")

    is_local_dst = is_local_daylight_saving


    @classmethod
    def local_timezone_offset_seconds(cls) -> int:
        """
        Get The offset (seconds) of the local timezone
        """
        if time.daylight == 1:
            # Get The offset of the local DST timezone, This is negative if the local DST timezone is east of UTC 
            return  time.altzone
        elif time.daylight == 0:
            # Get The offset of the local timezone, This is negative if the local DST timezone is east of UTC 
            return  time.timezone
        else:
            raise ValueError("Invalid time.daylight: {}".format(time.daylight))


    @classmethod
    def local_now(cls) -> datetime:
        """
        Local datetime with timezone 

        Return format:
            2019-02-27 22:35:16.162488+11:00
        """
        utc_now = cls.utcnow()

        v_offset_seconds = cls.local_timezone_offset_seconds()

        tz = timezone(- timedelta(0, v_offset_seconds))
        return utc_now.astimezone(tz)




    @classmethod
    def pytz_timezones(cls) -> list:
        """
        """
        return pytz.all_timezones
