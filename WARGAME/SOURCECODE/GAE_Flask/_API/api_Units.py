from _Startup import app
from _Controller import c_Authentication as Auth
from _Controller import c_UnitsLogic as Units
from _Controller import c_Utils as Help
from _Controller import c_Base as Common
import Constants as GLOBAL
import Mapping
import traceback

@app.route('/unit')
@Auth.Authentication.authenticateRequest
def getUnits():
    try:
        p_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(p_userId)
        var_data = Units.cUnits.getUserUnits(p_userId)
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_data, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/unit/<p_unitId>')
@Auth.Authentication.authenticateRequest
def getUnitById(p_unitId):
    try:
        p_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(p_userId)
        var_data = Units.cUnits.getUnitById(p_userId, p_unitId)
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_data, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/unit/deploy/<p_unitId>', methods=["POST"])
@Auth.Authentication.authenticateRequest
def deployUnit(p_unitId):
    try:
        p_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(p_userId)
        var_ver = Help.helpUtil.getVersion("units", "1")
        var_Return = Units.cUnits.deployUnit("units_%s_%s" % (var_ver, "1"), p_unitId, p_userId)
        var_ListUnits = var_Return["Units"]
        var_ListScores = var_Return["Scores"]
        var_objUnit = Help.helpUtil.createObjectJsonType2(var_ListUnits, Mapping.MAP_TABLE_USER_UNITS, "_unit_id")
        var_objScore = Help.helpUtil.createObjectJsonType2(var_ListScores, Mapping.MAP_TABLE_USER_SCORES, "_score_type_id_fk")
        var_RetData = {
                "Units": var_objUnit,
                "Scores": var_objScore
        }
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_RetData, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)
    
@app.route('/unit/disband/<p_unitId>', methods=["POST"])
@Auth.Authentication.authenticateRequest
def disbandUnit(p_unitId):
    try:
        p_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(p_userId)
        var_ver = Help.helpUtil.getVersion("units", "1")
        var_Return = Units.cUnits.disbandUnit("units_%s_%s" % (var_ver, "1"), p_unitId, p_userId)
        var_ListUnits = var_Return["Units"]
        var_ListScores = var_Return["Scores"]
        var_objUnit = Help.helpUtil.createObjectJsonType2(var_ListUnits, Mapping.MAP_TABLE_USER_UNITS, "_unit_id")
        var_objScore = Help.helpUtil.createObjectJsonType2(var_ListScores, Mapping.MAP_TABLE_USER_SCORES, "_score_type_id_fk")
        var_RetData = {
                "Units": var_objUnit,
                "Scores": var_objScore
        }
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_RetData, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)