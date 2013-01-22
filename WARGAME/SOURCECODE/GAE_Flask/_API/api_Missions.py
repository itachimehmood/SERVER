from _Startup import app
from _Controller import c_Authentication as Auth
from _Controller import c_Utils as Help
from _Controller import c_MissionsLogic as Mission
from _Controller import c_Base as Common
import Constants as GLOBAL
import traceback

@app.route('/mission')
@Auth.Authentication.authenticateRequest
def getMissions():
    try:
        p_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(p_userId)
        var_data = Mission.cMissions.getMissions(p_userId)
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_data, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/mission/<p_missionId>')
@Auth.Authentication.authenticateRequest
def getMissionById(p_missionId):
    try:
        p_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(p_userId)
        var_data = Mission.cMissions.getMissionById(p_userId, p_missionId)
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_data, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/mission/<p_missionId>', methods=["POST"])
@Auth.Authentication.authenticateRequest
def doMission(p_missionId):
    try:
        import Mapping
        p_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        var_user_type = Auth.Request.headers["X-BGS-USER-TYPE"]
        
        Common.cBase.updateLastActivity(p_userId)
        var_ver1 = Help.helpUtil.getVersion("missions", var_user_type)
        var_ver2 = Help.helpUtil.getVersion("configs", var_user_type)
        var_List = Mission.cMissions.doMission("missions_%s_%s" % (var_ver1, var_user_type), "configs_%s_%s" % (var_ver2, var_user_type), p_userId, p_missionId)    
        var_ListMissions = var_List["Missions"]
        var_ListScores = var_List["Scores"]
        var_objMission = Help.helpUtil.createObjectJsonType2(var_ListMissions, Mapping.MAP_TABLE_USER_MISSIONS, "_mission_id")
        var_objScore = Help.helpUtil.createObjectJsonType2(var_ListScores, Mapping.MAP_TABLE_USER_SCORES, "_score_type_id_fk")
        var_RetData = {
                "Missions": var_objMission,
                "Scores": var_objScore
        }
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_RetData, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)
