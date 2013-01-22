import Constants as GLOBAL
import json
import datetime
class customEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return helpUtil.getTimeFloat(obj)
        
        return json.JSONEncoder.default(self, obj)

class helpUtil(object):
    def __init__(self):
        pass
    @staticmethod
    def setCache(p_Key, p_data):    
        var_data = json.loads(p_data)
        GLOBAL.MEMCACHE.set(p_Key, var_data)
    @staticmethod
    def getCache(p_Key):
        return GLOBAL.MEMCACHE.get(p_Key)
    @staticmethod
    def uploadFileInMemcache(p_storeId, p_version, p_dataType):
        GLOBAL.STATUSKEY = "FileNotFound"
        
        from google.appengine.api import files as GSFiles
        fileName = GLOBAL.GSBUCKET + p_storeId + "_" + p_version + "_" + p_dataType + '.json'
        with GSFiles.open(fileName, 'r') as f:
            data = f.read()
        # decide key
        var_cacheKey = GLOBAL.STORE_DEFINITION[p_storeId] + "_" + p_version + "_" + p_dataType
        helpUtil.setCache(var_cacheKey, data)
        GLOBAL.METACONFIG[GLOBAL.STORE_DEFINITION[p_storeId]][p_dataType]["version"] = int(p_version)
        
    @staticmethod
    def getObject(p_Key, p_ref, p_leaf):
        GLOBAL.STATUSKEY = "MetadataKeyMissing"
        
        var_token = p_ref.split('_')
        var_length = len(var_token)
        if var_length == 3:
            if p_leaf == "P":
                return helpUtil.getStoreCategoryProductById(p_Key, var_token[0], var_token[1], var_token[2])
            else: 
                return helpUtil.getStoreCategoryItemById(p_Key, var_token[0], var_token[1], var_token[2])
        elif var_length == 2:
            return helpUtil.getStoreCategoryById(p_Key, var_token[0], var_token[1])
        else:
            return helpUtil.getStoreById(p_Key, var_token[0])
    @staticmethod
    def getStoreById(p_Key, p_StoreId):
        GLOBAL.STATUSKEY = "MetadataKeyMissing"
        var_JSON = GLOBAL.MEMCACHE.get(p_Key)
        return var_JSON[p_StoreId]
    @staticmethod
    def getStoreCategories(p_Key, p_StoreId):
        GLOBAL.STATUSKEY = "MetadataKeyMissing"
        var_JSON = GLOBAL.MEMCACHE.get(p_Key)
        var_Store = var_JSON[p_StoreId]
        return var_Store[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + 's']
    @staticmethod
    def getStoreCategoryById(p_Key, p_StoreId, p_CategoryId):
        GLOBAL.STATUSKEY = "MetadataKeyMissing"
        var_JSON = GLOBAL.MEMCACHE.get(p_Key)
        var_Store = var_JSON[p_StoreId]
        var_Categories = var_Store[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + 's']
        return var_Categories[p_CategoryId]
    @staticmethod
    def getStoreCategoryProducts(p_Key, p_StoreId, p_CategoryId):
        GLOBAL.STATUSKEY = "MetadataKeyMissing"
        var_JSON = GLOBAL.MEMCACHE.get(p_Key)
        var_Store = var_JSON[p_StoreId]
        var_Categories = var_Store[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + 's']
        var_Category = var_Categories[p_CategoryId]
        return var_Category[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + p_CategoryId + GLOBAL.PRODUCTCODE]
    @staticmethod
    def getStoreCategoryItems(p_Key, p_StoreId, p_CategoryId):
        GLOBAL.STATUSKEY = "MetadataKeyMissing"
        var_JSON = GLOBAL.MEMCACHE.get(p_Key)
        var_Store = var_JSON[p_StoreId]
        var_Categories = var_Store[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + 's']
        var_Category = var_Categories[p_CategoryId]
        return var_Category[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + p_CategoryId + GLOBAL.ITEMCODE]
    @staticmethod
    def getStoreCategoryProductById(p_Key, p_StoreId, p_CategoryId, p_ProductId):
        GLOBAL.STATUSKEY = "MetadataKeyMissing"
        var_JSON = GLOBAL.MEMCACHE.get(p_Key)
        var_Store = var_JSON[p_StoreId]
        var_Categories = var_Store[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + 's']
        var_Category = var_Categories[p_CategoryId]
        var_Products = var_Category[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + p_CategoryId + GLOBAL.PRODUCTCODE]
        return var_Products[p_ProductId]
    @staticmethod
    def getStoreCategoryItemById(p_Key, p_StoreId, p_CategoryId, p_ItemId):
        GLOBAL.STATUSKEY = "MetadataKeyMissing"
        var_JSON = GLOBAL.MEMCACHE.get(p_Key)
        var_Store = var_JSON[p_StoreId]
        var_Categories = var_Store[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + 's']
        var_Category = var_Categories[p_CategoryId]
        var_Items = var_Category[GLOBAL.STORECODE + p_StoreId + GLOBAL.CATEGORYCODE + p_CategoryId + GLOBAL.ITEMCODE]
        return var_Items[p_ItemId]
    @staticmethod
    def createConnection():
        GLOBAL.STATUSKEY = "DatabaseConnectionError"
        from google.appengine.api import rdbms as GSQL
        GLOBAL.CONNECTION = GSQL.connect(instance=GLOBAL.INSTANCE_NAME, database=GLOBAL.DATABASE_NAME)
        return GLOBAL.CONNECTION
    @staticmethod
    def parseBuckets(p_str):
        GLOBAL.STATUSKEY = "AttributeFormatError"
        # method returns a dictionary
        token = p_str.split("|")
        index = 0
        lst = []
        while index < len(token) - 1:
            comma = token[index].split(",")
            obj = {
                "cType": comma[0],
                "amount": comma[1],
                "discount": comma[2],
                "active": comma[3]
            }
            lst.append(obj)
            index = index + 1
        return lst
    @staticmethod
    def parseSellBuckets(p_str):
        GLOBAL.STATUSKEY = "AttributeFormatError"
        # method returns a dictionary
        token = p_str.split("|")
        index = 0
        lst = []
        while index < len(token) - 1:
            comma = token[index].split(",")
            obj = {
                "cType": comma[0],
                "amount": comma[1]
            }
            lst.append(obj)
            index = index + 1
        return lst
    @staticmethod
    def parseBattleDetail(p_detail):
        GLOBAL.STATUSKEY = "AttributeFormatError"
        var_user_ret = {"Alliances" : {}}
        var_user_data = p_detail
        if helpUtil.stringIsNullOrEmpty(p_detail) != "0":
            var_alliances = var_user_data.split("|")
            for alliance in var_alliances:
                var_alliance_unit = alliance.split("=")
                if len(var_alliance_unit) > 1:
                    var_dict_alliance = {var_alliance_unit[0]: {"Units": {}}}
                    var_units = var_alliance_unit[1].split(";")
                    for unit in var_units:
                        var_obj = unit.split(",")
                        if len(var_obj) > 1:
                            var_dict = {
                                var_obj[0]: {
                                     "Unitqty": var_obj[1]
                                 }
                            }
                            var_dict_alliance[var_alliance_unit[0]]["Units"].update(var_dict)
                    var_user_ret["Alliances"].update(var_dict_alliance)
        return var_user_ret
    @staticmethod
    def getTimeFloat(obj):
        GLOBAL.STATUSKEY = "ConvertionError"
        import time
        stamp = time.mktime(obj.timetuple())
        return float(stamp)
    @staticmethod
    def createColumnsString(p_colList):
        var_Index = 0
        var_String = ""
        while var_Index < p_colList:
            if p_colList[var_Index][var_Index] != "_id":
                var_String = var_String + p_colList[var_Index][var_Index] + ", "
            var_Index = var_Index + 1
        var_String = var_String + ")"
        var_String = var_String.replace(", )", "")
        return var_String
    @staticmethod
    def createObjectJson(p_ObjectList, p_MAP):
        GLOBAL.STATUSKEY = "ColumnNotFound"
        var_Return = []
        for obj in p_ObjectList:
            var_Index = 0
            var_Obj = {}
            while var_Index < len(p_MAP):
                var_Dict = {
                    p_MAP[var_Index]["json"]: obj.get(p_MAP[var_Index][var_Index])
                }
                var_Obj.update(var_Dict)
                var_Index = var_Index + 1
            var_Return.append(var_Obj)
        return var_Return
    @staticmethod
    def createObjectJsonType2(p_ObjectList, p_MAP, IDCol):
        GLOBAL.STATUSKEY = "ColumnNotFound"
        var_Return = {}
        for obj in p_ObjectList:
            var_Index = 0
            var_Obj = {}
            var_Main = {};
            while var_Index < len(p_MAP):
                var_Dict = {
                    p_MAP[var_Index]["json"]: obj.get(p_MAP[var_Index][var_Index])
                }
                var_Obj.update(var_Dict)
                var_Index = var_Index + 1
    
            var_Main = {obj.get(IDCol): var_Obj}
            var_Return.update(var_Main)
        return var_Return
    @staticmethod
    def createObjectJsonDirectly(p_Cursor, p_MAP, IDCol, IDIndex):
        GLOBAL.STATUSKEY = "ColumnNotFound"
        var_Return = {}
        for row in p_Cursor.fetchall():
            var_Index = 0
            var_Obj = {}
            var_Main = {};
            while var_Index < len(p_MAP):
                var_Dict = {
                    p_MAP[var_Index]["json"]: row[p_MAP[var_Index][p_MAP[var_Index][var_Index]]]
                }
                var_Obj.update(var_Dict)
                var_Index = var_Index + 1

            var_Main = {row[p_MAP[IDIndex][IDCol]]: var_Obj}
            var_Return.update(var_Main)
        return var_Return
    @staticmethod
    def stringIsNullOrEmpty(p_str):
        if(p_str == None):
            return "0"
        elif(p_str == ""):
            return "0"
        else:
            return p_str
    @staticmethod
    def boolToInt(p_val):
        GLOBAL.STATUSKEY = "ConvertionError"
        var_active = 0
        if p_val == True:
            var_active = 1
        else:
            var_active = 0
        return var_active
    @staticmethod
    def loadCursorData(p_Cursor, p_MAPPING):
        GLOBAL.STATUSKEY = "ColumnNotFound"
        from _Models import m_Object as Model
        var_List = []
        for row in p_Cursor.fetchall():
            var_Object = Model.modelObject()
            var_Index = 0
            while var_Index < len(p_MAPPING):
                var_Object.set(p_MAPPING[var_Index][var_Index], row[p_MAPPING[var_Index][p_MAPPING[var_Index][var_Index]]])
                var_Index = var_Index + 1
            var_List.append(var_Object)
        return var_List
    @staticmethod
    def getVersion(p_store, p_dataType):
        GLOBAL.STATUSKEY = "None"
        from Constants import METACONFIG
        return METACONFIG[p_store][p_dataType]["version"]
    @staticmethod
    def generateToken(INIT):
        CHARS = [list("Q12WE34RTYU56IOPLKJ87HGFD8SAZ9XVCBNM0"),
                list("1QAZXSW23EDCVFR45TGBNHY67UJMKI89OLZ0P"),
                list("ZAQ12WSXCDE34RFVBGT56YHNMJU78IKLO9PZ0"),
                list("Q12WE34RTYU56IOPLKJ87HGFD8SAZ9XVCBNM0"),
                list("1QAZXSW23EDCVFR45TGBNHY67UJMKI89OLA0P"),
                list("ZAQ12WSXCDE34RFVBGT56YHNMJU78IKLOAG90")]
    
        ckey = list(INIT)
        ind = len(ckey)
    
        while ind > 0:
            if ckey[ind - 1] != CHARS[ind - 1][len(CHARS[ind - 1]) - 1: ][0]:
                nextChar = CHARS[ind - 1].index(ckey[ind - 1]) + 1
                #import random as Rand
                #nextChar = Rand.randint(0, 37)
                ckey[ind - 1] = CHARS[ind - 1][nextChar]
    
                # Reset Logic
                whileIndex = ind
                while whileIndex < len(ckey):
                    ckey[whileIndex] = CHARS[whileIndex][0]
                    whileIndex = whileIndex + 1
                break
            ind = ind - 1;
    
        return ckey