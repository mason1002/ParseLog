import re
# recognizer
recognizer = ""
# pattern define
class RegexPattern:
    def __init__(self):
        self.pattern_name = ""
        self.pattern_value = ""
# 定义日志拆分模块数据结构
class WordPattern:
    def __init__(self,word_str):
        self.str = word_str  #该结构的字符串，必须有值
        self.is_static = True  #是否为静态，静态表示不需要解析的内容，即该日志格式中的固定内容
        self.regex_pattern = '' #该结构的正则pattern,可为SIEM系统定义的全局pattern或自定义pattern
        self.regex = '' #该结构的正则表达式，当regex_pattern有值时可为空
        self.event_attribution = '' #该部分结构映射的SIEM的event attribution, 可为空
        self.var = '' #该部分结构被定义的临时变量，可为空
        self.next = None #指向下一个结构体
        self.default_split_regex = r"([;,\|\s+])"
        self.default_match_regex = r"^[;,\|\s+]$"
        self.tk_static_value = None
        self.tk_regex_choose_value = None
        self.tk_regex_value = None
        self.tk_frame = None
    def split(self,split_str=''):
        pat_list = []
        if split_str == '':
            syslog_start_regex = re.compile('^(<\d+>).*$')   #syslog标识
            syslog_result = syslog_start_regex.findall(self.str)
            if len(syslog_result) > 0:
                split_str = self.str.split(syslog_result[0],1)
                self.str = syslog_result[0]
                self.is_static = False
                self.regex_pattern = "gPatSyslogPRI"
                new_patt = WordPattern(split_str[1])
                self.next = new_patt
                next_pat_list = new_patt.split()
                next_pat_list.insert(0, self)
                return next_pat_list                            
            words = re.split(self.default_split_regex,self.str)
            '''
            default_split_str_array = [';','|',' ',',']
            split_count = []
            for i in range(len(default_split_str_array)):
                words = self.str.split(default_split_str_array[i])
                split_count.append(len(words))
            max_index = split_count.index(max(split_count))
            words = self.str.split(default_split_str_array[max_index])
            '''
            if len(words) > 1:
                self.str = words[0]
                self.preParse()
                pat_list.append(self)
                for i in range(1, len(words)):
                    new_patt = WordPattern(words[i])
                    new_patt.preParse()
                    pat_list[i-1].next = new_patt
                    pat_list.append(new_patt)
                return pat_list
            else:
                return None
        else:
            words = self.str.split(split_str)
            if len(words) > 1:
                self.str = words[0]
                self.preParse()
                if words[0] == split_str:
                    new_patt.is_static = True
                else:
                    new_patt.is_static = False                
                pat_list.append(self)
                for i in range(1, len(words)):
                    new_patt = WordPattern(words[i])
                    new_patt.preParse()
                    if words[i] == split_str:
                        new_patt.is_static = True
                    else:
                        new_patt.is_static = False
                    pat_list[i-1].next = new_patt
                    pat_list.append(new_patt)
                return pat_list
            else:
                return None
    def preParse(self):
        result = re.match(self.default_match_regex,self.str)
        if result is None:
            self.is_static = False
        else:
            self.is_static = True
        march_regex = r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$"
        result = re.match(march_regex,self.str)
        if result != None:
            self.regex_pattern = "gPatMon"
            self.var = "_mon"
        march_regex = r"^[0-3]{1}[0-9]{1}$"
        result = re.match(march_regex,self.str)
        if result != None:
            self.regex_pattern = "gPatDay"
            self.var = "_day" 
        march_regex = r"^[0-9]{4}$"
        result = re.match(march_regex,self.str)
        if result != None:
            self.regex_pattern = "gPatYear"
            self.var = "_year"
        march_regex = r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$"
        result = re.match(march_regex,self.str)
        if result != None:
            self.regex_pattern = "gPatTime"
            self.var = "_time"
        march_regex = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        result = re.match(march_regex,self.str)
        if result != None:
            self.regex = r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
            self.var = "_date"
        march_regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        result = re.match(march_regex,self.str)
        if result != None:
            self.regex_pattern = "gPatIpAddr"
        

    def group(self):
        if self != None and self.next != None:
            self.str += self.next.str
            self.next = self.next.next
        return self
    def getKeyInclude(self, with_split=True):
        key_value_split = r"([=:])"
        words = re.split(key_value_split, self.str)
        if len(words) > 1 and len(words) < 4:
            if with_split:
                return words[0]+words[1]
            else:
                return words[0]
        else:
            return None
    def getMapKey(self):
        if self.event_attribution != '':
            return self.event_attribution
        elif self.var != '':
            return self.var
        else:
            return None
    def getMapValue(self):
        if self.regex_pattern != '':
            return  self.regex_pattern
        else:
            return None
# 定义单个属性设置模块数据结构  
class AttriSetting:
    def __init__(self):
        self.event_attribute = "eventType"
        self.value = ""
        self.isConditionNeed = False
        self.condition = ""
class LogParserOneFormat:
    def __init__(self,logStr):
        self.orig_log = logStr
        self.word_patterns:list[WordPattern] = [] #class WordPattern ArrayList
        self.attr_settings:list[AttriSetting] = [] #class AttriSetting ArrayList
class LogParser:
    def __init__(self):
        self.recognizer = ""
        self.regex_patterns:list[RegexPattern] = [] #class RegexPattern ArrayList
        self.parser_formats:list[LogParserOneFormat] = [] #class LogParserOneFormat ArrayList
#test_str = "<51>Mar 23 07:18:55 8.10.1.199 id=S2XE142RV6PXCF|service=guioper server=20.35.130.201(20.35.130.201-跳板机),account=jiahui_wang"
#pat = WordPattern(test_str)
#resutl = pat.split()

#print(resutl)





        