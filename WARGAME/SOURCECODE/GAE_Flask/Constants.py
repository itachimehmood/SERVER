from google.appengine.api import memcache as CACHE
MEMCACHE = CACHE.Client()
GSBUCKET = "/gs/azharbgs/"
TOKEN = "X-BGS-GAME-KEY"
TIMESTAMP = "X-BGS-TIMESTAMP"
CHECKSUM = "X-BGS-CHECKSUM"
VERSION = "X-BGS-GAME-VERSION"
ERROR_CODE = "X-BGS-ERROR-CODE"
ERROR_MESSAGE = "X-BGS-ERROR-MESSAGE"
REQUEST_STATUS = "X-BGS-RESPONSE-CODE"
USER_KEY = "X-BGS-USER-KEY"
RESPONSE_CODE_ERR = 0
RESPONSE_CODE_SUC = 1
CATEGORYCODE = "cat"
STORECODE = "store"
PRODUCTCODE = "prods"
ITEMCODE = "items"
DATABASE_NAME = "war_game"
INSTANCE_NAME = "bridgegatestudios.com:gmsreporting:reporting"
X_BRIDGEGATE_GMS_SECRET_SALT="RANDSTRING"

CONNECTION = None
COMMIT = False
CLOSE = False

USERLEVEL = "1"
USERLASTSCOREUPDATE = 0.0
USERNAME = ""

#define kVG_RESPONSE_CODE_FAILED_DATABASE_CONNECTION         10006
#define kVG_RESPONSE_CODE_FAILED_INSERT                      10007
#define kVG_RESPONSE_CODE_FAILED_UPDATE                      10008
#define kVG_RESPONSE_CODE_FAILED_DELETE                      10009
#define kVG_RESPONSE_CODE_FAILED_SELECT                      10010
#define kVG_RESPONSE_CODE_FAILED_PROCEDURE_CALL              10011
#define kVG_RESPONSE_CODE_FAILED_PROCESSING                  10012


#define kVG_RESPONSE_CODE_FAILED_ATTRIBUTE_FORMAT            10013
#define kVG_RESPONSE_CODE_FAILED_CONVERSION                  10014
#define kVG_RESPONSE_CODE_FAILED_MISSING_ATTRIBUTE           10015
#define kVG_RESPONSE_CODE_FAILED_NOT_FOUND_FILE              10016
#define kVG_RESPONSE_CODE_FAILED_NOT_FOUND_COLUMN            10017
#define kVG_RESPONSE_CODE_FAILED_MISSING_METADATA            10018


#define kVG_RESPONSE_CODE_UNKNOWN_USER_TYPE                  10501


STATUSKEY = "None"
STATUS_DETAILS = {
      
      "Success": {"ErrorCode": 1, "ErrorMsg": "Request processed successfully", "Parameters": ""},
      "PacketTampered": {"ErrorCode": 10001, "ErrorMsg": "Packet tampered, checksum not matched", "Parameters": ""},
      "RequestTimeout": {"ErrorCode": 10002, "ErrorMsg": "Request timeout", "Parameters": ""},
      "MissingHeader": {"ErrorCode": 10003, "ErrorMsg": "Required header is missing", "Parameters": ""},
      "None": {"ErrorCode": 10004, "ErrorMsg": "Internal Server Error", "Parameters": ""},
      "Checksum": {"ErrorCode": 10005, "ErrorMsg": "Checksum not matched", "Parameters": ""},
      
      "DatabaseConnectionError": {"ErrorCode": 10006, "ErrorMsg": "Cannot connect to the database", "Parameters": ""},
      "InsertFailed": {"ErrorCode": 10007, "ErrorMsg": "Query: Insertion failed", "Parameters": ""},
      "UpdateFailed": {"ErrorCode": 10008, "ErrorMsg": "Query: Update failed", "Parameters": ""},
      "DeleteFailed": {"ErrorCode": 10009, "ErrorMsg": "Query: Delete failed", "Parameters": ""},
      "SelectFailed": {"ErrorCode": 10010, "ErrorMsg": "Query: Select failed", "Parameters": ""},
      "ProcedureCallFailed": {"ErrorCode": 10011, "ErrorMsg": "Database: Business layer exception", "Parameters": ""},
      "ProcessingError": {"ErrorCode": 10012, "ErrorMsg": "Controller: Business layer exception", "Parameters": ""},
      
      "AttributeFormatError": {"ErrorCode": 10013, "ErrorMsg": "Attribute not formated properly", "Parameters": ""},
      "ConvertionError": {"ErrorCode": 10014, "ErrorMsg": "Cannot convert the data", "Parameters": ""},
      "MissingAttribute": {"ErrorCode": 10015, "ErrorMsg": "Attribute is missing", "Parameters": ""},
      "FileNotFound": {"ErrorCode": 10016, "ErrorMsg": "File not found", "Parameters": ""},
      "ColumnNotFound": {"ErrorCode": 10017, "ErrorMsg": "Column not found", "Parameters": ""},
      "MetadataKeyMissing": {"ErrorCode": 10018, "ErrorMsg": "Meta data key missing", "Parameters": ""},
      
      "NotAccessibleAtLevel": {"ErrorCode": 10401, "ErrorMsg": "You need to rise to the higher level to fulfill this request", "Parameters": ""},
      "LessCash": {"ErrorCode": 10402, "ErrorMsg": "You do not have enough cash", "Parameters": ""},
      "LowEnergy": {"ErrorCode": 10403, "ErrorMsg": "You do not have enough energy", "Parameters": ""},
      "LessAlliance": {"ErrorCode": 10404, "ErrorMsg": "More alliances are required", "Parameters": ""},
      "LessUnit": {"ErrorCode": 10405, "ErrorMsg": "More units are required", "Parameters": ""},
      "AllianceExists": {"ErrorCode": 10406, "ErrorMsg": "This alliance already exists", "Parameters": ""},
      "UserHealthLow": {"ErrorCode": 10407, "ErrorMsg": "You do not have enough health", "Parameters": ""},
      "BattleRetreat": {"ErrorCode": 10408, "ErrorMsg": "The player is retreating right now", "Parameters": ""},
      "SanctionExists": {"ErrorCode": 10409, "ErrorMsg": "Alliance have already been sanctioned", "Parameters": ""},
      
      "AllianceNotFound": {"ErrorCode": 13404, "ErrorMsg": "Alliance not found", "Parameters": ""},
      "InviteCodeNotFound": {"ErrorCode": 14404, "ErrorMsg": "Invite code not found", "Parameters": ""},
      "UnitNotFound": {"ErrorCode": 15404, "ErrorMsg": "Unit not found", "Parameters": ""},
      "UserNotFound": {"ErrorCode": 16404, "ErrorMsg": "User not found", "Parameters": ""},
      "UnitDataTampered": {"ErrorCode": 18404, "ErrorMsg": "Data tampered", "Parameters": ""},
      
      "UnknownUserType": {"ErrorCode": 10501, "ErrorMsg": "User type unknown", "Parameters": ""}
}

SCORE_TYPES = {
   "Energy": 1,
   "Amo": 2,
   "Health": 3,
   "Experience": 4,
   "Level": 5,
   "Cash": 6,
   "Attack": 7,
   "Defense": 8,
   "Skillpoints": 9
}

BATTLE_TYPES = {
   "Battle": 1,
   "Sanction": 2
}

COMMENT_TYPES = {
   "Alliance": 1,
   "Battle": 2
}

METACONFIG = {
      "units": {
                    "0": {
                            "version": 1
                    },
                    "1": {
                            "version": 1
                    },
                    "2": {
                            "version": 1
                    }
        },
      "missions":{
                  "0": {
                            "version": 1
                    },
                    "1": {
                            "version": 1
                    },
                    "2": {
                            "version": 1
                    }
      },
      "configs": {
                  "0": {
                            "version": 1
                    },
                    "1": {
                            "version": 1
                    },
                    "2": {
                            "version": 1
                    }
      }
}
STORE_DEFINITION = { 
    '1': 'units',
    '2': 'missions', 
    '3': "configs",
    'units': '1',
    'missions': '2',
    'configs': '3' 
}
CATEGORY_DEFINITION = {
   "Level" : "3_1",
   "Configurations": "3_4_1"
}
