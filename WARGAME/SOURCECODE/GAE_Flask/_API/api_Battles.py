from _Startup import app
from _Controller import c_Authentication as Auth
from _Controller import c_BattlesLogic as Battles
from _Controller import c_Utils as Help
from _Controller import c_Base as Common
import Constants as GLOBAL
import Mapping
import traceback

@app.route('/battle/list')
@Auth.Authentication.authenticateRequest
def getBattleList():
    try:
        var_Params = []
        var_UserId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_UserId)
        var_Token = Auth.Request.headers[GLOBAL.TOKEN]
        var_Params.append(var_Token)
        var_Params.append(var_UserId)
        var_List = Battles.cBattles.getBattleList(var_UserId)
        var_List = Help.helpUtil.createObjectJson(var_List, Mapping.MAP_SP_USER_SCORES_SAME)
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_List, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/sanction/<p_sanctionedId>/<p_amount>')
@Auth.Authentication.authenticateRequest
def sanctionAlliance(p_sanctionedId, p_amount):
    try:
        var_Params = []
        var_UserId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_UserId)
        var_Token = Auth.Request.headers[GLOBAL.TOKEN]
        var_Params.append(var_Token)
        var_Params.append(var_UserId)
        var_List = Battles.cBattles.sanctionAlliance(var_UserId, p_sanctionedId, p_amount)
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_List, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/battle/attack/<p_battleUserId>')
@Auth.Authentication.authenticateRequest
def attackUser(p_battleUserId):
    try:
        var_UserId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_UserId)
        var_user_type = Auth.Request.headers["X-BGS-USER-TYPE"]
        var_ver = Help.helpUtil.getVersion("configs", var_user_type)
        key = "configs_%s_%s" % (var_ver, var_user_type)
        unitKey = "units_%s_%s" % (var_ver, var_user_type)
        var_Data = Battles.cBattles.attack(key, var_UserId, p_battleUserId, unitKey)
        
        var_List = var_Data["Battle"]

        var_user_ret = Help.helpUtil.parseBattleDetail(var_List[0].get("_user_data"))
        var_battle_ret = Help.helpUtil.parseBattleDetail(var_List[0].get("_battle_with_data"))
        
        var_user_ret.update({"Scores": var_Data["Score1"]})
        var_battle_ret.update({"Scores": var_Data["Score2"]})
        var_user_ret.update({"name": var_List[0].get("_user_display_name")})
        var_battle_ret.update({"name": var_List[0].get("_battle_display_name")})
        
        var_List = {
            "_id": var_List[0].get("_id"),
            var_List[0].get("_user_id_fk"): var_user_ret,
            var_List[0].get("_battle_with_id_fk"): var_battle_ret,
            "Victorious": var_List[0].get("_victory_id_fk"),
            "battledOn": Help.helpUtil.getTimeFloat(var_List[0].get("_battled_at")),
            "battleType": var_List[0].get("_battle_type_id_fk")
        }
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_List, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/sanction/attack/<p_battleUserId>')
@Auth.Authentication.authenticateRequest
def attackSanction(p_battleUserId):
    try:
        var_Params = []
        var_UserId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_UserId)
        var_Token = Auth.Request.headers[GLOBAL.TOKEN]
        var_Params.append(var_Token)
        var_Params.append(var_UserId)
        var_List = Battles.cBattles.attackSanction(var_UserId, p_battleUserId)
        
        #var_List = Help.helpUtil.createObjectJson(var_List, Mapping.MAP_TABLE_USER_BATTLES)
        var_Json = {
            "_id": var_List[0].get("_id"),
            var_List[0].get("_user_id_fk"): {"Amount": var_List[0].get("_user_data"), "name": var_List[0].get("_user_display_name")},
            var_List[0].get("_battle_with_id_fk"):{"Amount": 0, "name": var_List[0].get("_user_display_name")},
            "Victorious": var_List[0].get("_victory_id_fk"),
            "battledOn": Help.helpUtil.getTimeFloat(var_List[0].get("_battled_at")),
            "battleType": var_List[0].get("_battle_type_id_fk")
        }
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_Json, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/battle/sanction')
@Auth.Authentication.authenticateRequest
def sanctionList():
    try:
        var_Params = []
        var_UserId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_UserId)
        var_Token = Auth.Request.headers[GLOBAL.TOKEN]
        var_Params.append(var_Token)
        var_Params.append(var_UserId)
        var_List = Battles.cBattles.getSanctionList()
        var_List = Help.helpUtil.createObjectJson(var_List, Mapping.MAP_VIEW_USER_SANCTIONS)
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_List, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)
