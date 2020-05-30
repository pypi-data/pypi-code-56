"""
## chinese
适用于中文、英文和中英混合的音素，其中汉字拼音采用清华大学的音素，英文字符分字母和英文。

中文音素简介：

声母：
aa b c ch d ee f g h ii j k l m n oo p q r s sh t uu vv x z zh

韵母：
a ai an ang ao e ei en eng er i ia ian iang iao ie in ing iong iu ix iy iz o ong ou u ua uai uan uang ueng ui un uo v van ve vn ng uong

声调：
1 2 3 4 5

字母：
Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz

英文：
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

标点：
! ? . , ; : " # ( )
注：!=!！|?=?？|.=.。|,=,，、|;=;；|:=:：|"="“|#= 　\t|(=(（[［{｛【<《|)=)）]］}｝】>》

预留：
w y 0 6 7 8 9

其他：
_ ~  - *
"""
from .convert import fan2jian, jian2fan, quan2ban, ban2quan
from .number import say_digit, say_decimal, say_number
from .pinyin import text2pinyin, split_pinyin
from .sequence import text2sequence, text2phoneme, pinyin2phoneme, phoneme2sequence, sequence2phoneme
from .sequence import symbol_chinese, ph2id_dict, id2ph_dict
