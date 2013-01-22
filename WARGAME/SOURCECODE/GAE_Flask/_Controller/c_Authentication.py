from functools import wraps as Wraps
from flask import request as Request, Response
import Constants as GLOBAL

class Authentication(object):
    def __init__(self):
        pass
    @staticmethod
    def authenticateRequest(f):
        @Wraps(f)
        def decorated(*args, **kwargs):
            import hashlib as Hash
            import datetime
            import c_Utils as Help
            import logging as Log
            var_Message = ""
            try:
                
                var_bgs_game_token = Request.headers[GLOBAL.TOKEN]
                var_bgs_timestamp = Request.headers[GLOBAL.TIMESTAMP]
                var_server_time = Help.helpUtil.getTimeFloat(datetime.datetime.utcnow())
                var_diff = abs(var_server_time - float(var_bgs_timestamp))
                Log.debug(var_diff)
                #if var_diff > 30:
                #    return Authentication.createResponse("{}", 104, "Request Discarded")
                #var_bgs_checksum = Request.headers[GLOBAL.CHECKSUM]
                var_bgs_game_version = Request.headers[GLOBAL.VERSION]
                var_user_game_token = Request.headers[GLOBAL.USER_KEY]
                var_user_type = Request.headers["X-BGS-USER-TYPE"]
                
                from _Controller import c_Base as Common
                var_user_type = Request.headers["X-BGS-USER-TYPE"]
                
                if var_user_type != "0" and var_user_type != "1" and var_user_type != "2":
                    var_Ret = Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["UnknownUserType"])
                    return Authentication.createResponse({}, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_ERR) 
                
                Common.cBase.updateMemcahce(GLOBAL.METACONFIG["units"][var_user_type]["version"], 
                                            GLOBAL.METACONFIG["missions"][var_user_type]["version"],
                                            GLOBAL.METACONFIG["configs"][var_user_type]["version"], var_user_type);
                
            except Exception, e:
                var_Message = str(e)
        
            
            if var_Message == "":
                var_body = ""
                if Request.method == "POST":
                    var_body = str(Request.data)
                var_BigString = var_body + GLOBAL.X_BRIDGEGATE_GMS_SECRET_SALT + var_bgs_game_token + var_bgs_timestamp + var_bgs_game_version + var_user_game_token + var_user_type
                var_ServerSHA = Hash.sha256(var_BigString).hexdigest()
                if True:
                    return f(*args, **kwargs)
                else:
                    var_Ret = Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["PacketTampered"])
                    return Authentication.createResponse({}, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_ERR)
            else:
                var_Ret = Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["MissingHeader"])
                return Authentication.createResponse({}, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_ERR)
        return decorated
    @staticmethod
    def errorReturn(s):
        Authentication.closeConnection()
        if GLOBAL.STATUSKEY == "":
            GLOBAL.STATUSKEY = "None"
        var_Ret = Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS[GLOBAL.STATUSKEY])
        return Authentication.createResponse({}, var_Ret["Code"], var_Ret["Msg"], s, GLOBAL.RESPONSE_CODE_ERR)
    @staticmethod
    def closeConnection():
        import logging as Log
        if GLOBAL.COMMIT:
            Log.debug("Common, Commit")
            GLOBAL.CONNECTION.commit()
        if GLOBAL.CLOSE:
            Log.debug("Common, Connection")
            GLOBAL.CONNECTION.close()
    @staticmethod
    def createCodeMsg(p_Obj):
        GLOBAL.STATUSKEY = "None"
        return {
            "Code": p_Obj["ErrorCode"],
            "Msg": p_Obj["ErrorMsg"]
        }
    @staticmethod
    def createResponse(p_ResponseData, p_ErrorCode, p_Exception, p_Stacktrace, p_Status):
        import c_Utils as Help
        import datetime
        import hashlib as Hash
        var_resp = {
                "Required": {
                     "time": Help.helpUtil.getTimeFloat(datetime.datetime.now()),
                     "status": p_Status, # true or false
                     "statusCode": p_ErrorCode, # 1, 101, 102, 104
                     "statusMsg": p_Exception, # energy rola
                     "stackTrace": p_Stacktrace
                 },
                "Response": p_ResponseData
        }
        var_resp = Help.json.dumps(var_resp, cls=Help.customEncoder)
        p_checkSum = Hash.sha256(GLOBAL.X_BRIDGEGATE_GMS_SECRET_SALT + var_resp).hexdigest()
        var_Response = Response(var_resp, status=200, mimetype='application/json')
        var_Response.headers[GLOBAL.CHECKSUM] = p_checkSum
        return var_Response
    