from _Startup import app
from _Controller import c_Authentication as Auth
from _Controller import c_UsersLogic as Users
from _Controller import c_CommentsLogic as Comments
from _Controller import c_Utils as Help
from _Controller import c_Base as Common
import Constants as GLOBAL
import Mapping
import traceback

@app.route('/user/me')
@Auth.Authentication.authenticateRequest
def getUser():
    try:
        var_Params = []
        var_UserId = Auth.Request.headers[GLOBAL.USER_KEY]
        var_Token = Auth.Request.headers[GLOBAL.TOKEN]
        var_Params.append(var_Token)
        var_Params.append(var_UserId)
        var_ver2 = Help.helpUtil.getVersion("configs", "1")
        key = "configs_%s_%s" % (var_ver2, "1")
        var_Config = Help.helpUtil.getObject(key, "%s_%s" % (GLOBAL.CATEGORY_DEFINITION["Level"], 2), "I")
        var_Params.append(int(var_Config["exp"]))
        
        var_List = Users.cUsers.getUserScore(var_Params)
        
        var_Units = var_List["Units"]
        var_Scores = var_List["Scores"]
        var_Missions = var_List["Missions"]
        var_Battles = var_List["Battles"]
        var_Comments = var_List["Comments"]
        
        # battle processing starts
        var_Battle_Lst = []
        var_Battle_Comments = []
        var_Index = 0
        while var_Index < len(var_Battles):
            
            if var_Index + 1 < len(var_Battles):
                
                if var_Battles[var_Index].get("_id") == var_Battles[var_Index + 1].get("_id"):
                    commentedOn = var_Battles[var_Index].get("_comment_user_id_fk")
                    if Help.helpUtil.stringIsNullOrEmpty(str(commentedOn)) != "0":
                        commentedOn = Help.helpUtil.getTimeFloat(var_Battles[var_Index].get("_commented_on"))
                        Comment = {
                           "id": var_Battles[var_Index].get("_comment_user_id_fk"),
                           "name": var_Battles[var_Index].get("_comment_display_name"),
                           "comment": var_Battles[var_Index].get("_comment"),
                           "commentType": var_Battles[var_Index].get("_comment_type_id_fk"),
                           "commentedOn": commentedOn
                        }
                        var_Battle_Comments.append(Comment)
                else:
                    
                    if var_Battles[var_Index].get("_battle_type_id_fk") == GLOBAL.BATTLE_TYPES["Battle"]:
                        var_user_ret = Help.helpUtil.parseBattleDetail(var_Battles[var_Index].get("_user_data"))
                        var_battle_ret = Help.helpUtil.parseBattleDetail(var_Battles[var_Index].get("_battle_with_data"))
                        var_user_ret.update({"name": var_Battles[var_Index].get("_user_display_name")})
                        var_battle_ret.update({"name": var_Battles[var_Index].get("_battle_display_name")})
                        var_dict = {
                            "_id": var_Battles[var_Index].get("_id"),
                            var_Battles[var_Index].get("_user_id_fk"): var_user_ret,
                            var_Battles[var_Index].get("_battle_with_id_fk"): var_battle_ret,
                            "Comments": var_Battle_Comments,
                            "victorious": var_Battles[var_Index].get("_victory_id_fk"),
                            "battledOn": Help.helpUtil.getTimeFloat(var_Battles[var_Index].get("_battled_at")),
                            "battleType": var_Battles[var_Index].get("_battle_type_id_fk")
                        }
                    else:
                        var_dict = {
                            "_id": var_Battles[var_Index].get("_id"),
                            var_Battles[var_Index].get("_user_id_fk"): {"Amount": var_Battles[var_Index].get("_user_data"), "name": var_Battles[var_Index].get("_user_display_name")},
                            var_Battles[var_Index].get("_battle_with_id_fk"): {"Amount": 0, "name": var_Battles[var_Index].get("_battle_display_name")},
                            "Comments": var_Battle_Comments,
                            "victorious": var_Battles[var_Index].get("_victory_id_fk"),
                            "battledOn": Help.helpUtil.getTimeFloat(var_Battles[var_Index].get("_battled_at")),
                            "battleType": var_Battles[var_Index].get("_battle_type_id_fk")
                        }
                    var_Battle_Lst.append(var_dict)
                    var_Battle_Comments = []
            else:
                commentedOn = var_Battles[var_Index].get("_comment_user_id_fk")
                if Help.helpUtil.stringIsNullOrEmpty(str(commentedOn)) != "0":
                    commentedOn = Help.helpUtil.getTimeFloat(var_Battles[var_Index].get("_commented_on"))
                    Comment = {
                       "id": var_Battles[var_Index].get("_comment_user_id_fk"),
                       "comment": var_Battles[var_Index].get("_comment"),
                       "name": var_Battles[var_Index].get("_comment_display_name"),
                       "commentType": var_Battles[var_Index].get("_comment_type_id_fk"),
                       "commentedOn": commentedOn
                    }
                    var_Battle_Comments.append(Comment)
                
                if var_Battles[var_Index].get("_battle_type_id_fk") == GLOBAL.BATTLE_TYPES["Battle"]:
                    var_user_ret = Help.helpUtil.parseBattleDetail(var_Battles[var_Index].get("_user_data"))
                    var_battle_ret = Help.helpUtil.parseBattleDetail(var_Battles[var_Index].get("_battle_with_data"))
                    var_user_ret.update({"name": var_Battles[var_Index].get("_user_display_name")})
                    var_battle_ret.update({"name": var_Battles[var_Index].get("_battle_display_name")})
                    var_dict = {
                        "_id": var_Battles[var_Index].get("_id"),
                        var_Battles[var_Index].get("_user_id_fk"): var_user_ret,
                        var_Battles[var_Index].get("_battle_with_id_fk"): var_battle_ret,
                        "Comments": var_Battle_Comments,
                        "victorious": var_Battles[var_Index].get("_victory_id_fk"),
                        "battledOn": Help.helpUtil.getTimeFloat(var_Battles[var_Index].get("_battled_at")),
                        "battleType": var_Battles[var_Index].get("_battle_type_id_fk")
                    }
                else:
                    var_dict = {
                        "_id": var_Battles[var_Index].get("_id"),
                        var_Battles[var_Index].get("_user_id_fk"): {"Amount": var_Battles[var_Index].get("_user_data"), "name": var_Battles[var_Index].get("_user_display_name")},
                        var_Battles[var_Index].get("_battle_with_id_fk"): {"Amount": 0, "name": var_Battles[var_Index].get("_battle_display_name")},
                        "Comments": var_Battle_Comments,
                        "victorious": var_Battles[var_Index].get("_victory_id_fk"),
                        "battledOn": Help.helpUtil.getTimeFloat(var_Battles[var_Index].get("_battled_at")),
                        "battleType": var_Battles[var_Index].get("_battle_type_id_fk")
                    }
                var_Battle_Comments = []
                var_Battle_Lst.append(var_dict)
            
            var_Index = var_Index + 1
        
        # battle processing ends
        
        var_data = {
                        "inviteCode": var_Scores[0].get("_user_code"),
                        "name": var_Scores[0].get("_display_name"),
                        "alliances": var_Scores[0].get("_alliances"),
                        "Scores": Help.helpUtil.createObjectJsonType2(var_Scores, Mapping.MAP_TABLE_USER_SCORES, "_score_type_id_fk"),
                        "Units": Help.helpUtil.createObjectJsonType2(var_Units, Mapping.MAP_TABLE_USER_UNITS, "_unit_id"),
                        "Missions": Help.helpUtil.createObjectJsonType2(var_Missions, Mapping.MAP_TABLE_USER_MISSIONS, "_mission_id"),
                        "BattleNews": var_Battle_Lst,
                        "Comments": Help.helpUtil.createObjectJson(var_Comments, Mapping.MAP_TABLE_USER_COMMENTS)
                    }
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_data, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user')
@Auth.Authentication.authenticateRequest
def getUserById():
    try:
        var_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_userId)
        var_List = Users.cUsers.getUserById(var_userId)
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_List, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)
    
@app.route('/user/alliances/list/', methods=["GET"])
@Auth.Authentication.authenticateRequest
def getUserAlliance():
    try:
        var_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_userId)
        var_List = Users.cUsers.getUserAlliance(var_userId)    
        # Custom Json
        dAlliance = {}
        for obj in var_List:
            if not dAlliance.has_key(obj.get("_user_id_fk")):
                alliance = Help.helpUtil.createObjectJsonType2([obj], [{"_user_id_fk": 0, 0: "_user_id_fk", "json": "id"}, {"_display_name": 1, 1: "_display_name", "json": "name"}
                                                         ], "_user_id_fk")
                dAlliance.update(alliance)
                dAlliance[obj.get("_user_id_fk")].update({"Scores": {}})    
        
            scores = Help.helpUtil.createObjectJsonType2([obj], [{"_score_type_id_fk": 0, 0: "_score_type_id_fk", "json": "type"},
                                                       {"_score": 1, 1: "_score", "json": "score"}, {"_max": 2, 2: "_max", "json": "max"}], "_score_type_id_fk")
            dAlliance[obj.get("_user_id_fk")]["Scores"].update(scores)
            
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(dAlliance, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/alliances/invites/', methods=["GET"])
@Auth.Authentication.authenticateRequest
def getUserAllianceInvites():
    try:
        var_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_userId)
        var_List = Users.cUsers.getUserAllianceInvites(var_userId)
        # Custom Json
        dAlliance = {}
        for obj in var_List:
            if not dAlliance.has_key(obj.get("_user_id_fk")):
                alliance = Help.helpUtil.createObjectJsonType2([obj], [{"_user_id_fk": 0, 0: "_user_id_fk", "json": "id"}, {"_display_name": 1, 1: "_display_name", "json": "name"} 
                                                                       ], "_user_id_fk")
                dAlliance.update(alliance)
                dAlliance[obj.get("_user_id_fk")].update({"Scores": {}})
        
            elif dAlliance.has_key(obj.get("_user_id_fk")):
                pass    
        
            scores = Help.helpUtil.createObjectJsonType2([obj], [{"_score": 0, 0: "_score", "json": "score"},
                                                    {"_score_type_id_fk": 1, 1: "_score_type_id_fk", "json": "scoreType"}, {"_max": 2, 2: "_max", "json": "max"}], "_score_type_id_fk")
            dAlliance[obj.get("_user_id_fk")]["Scores"].update(scores)
            
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(dAlliance, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/alliances/make/<p_allianceCode>', methods=["POST"])
@Auth.Authentication.authenticateRequest
def makeUserAlliance(p_allianceCode):
    try:
        var_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_userId)
        var_Message = Users.cUsers.makeUserAliance(var_userId, p_allianceCode)
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse({"Message": var_Message}, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/alliances/delete/<p_allianceId>', methods=["DELETE"])
@Auth.Authentication.authenticateRequest
def deleteUserAlliance(p_allianceId):
    try:
        var_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_userId)
        var_Message = Users.cUsers.deleteUserAlliance(var_userId, p_allianceId)
        
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse({"Message": var_Message}, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/alliances/accept/<p_allianceId>', methods=["POST"])
@Auth.Authentication.authenticateRequest
def acceptUserAlliance(p_allianceId):
    try:
        var_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_userId)
        var_Message = Users.cUsers.acceptAllianceRequest(var_userId, p_allianceId)
        
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse({"Message": var_Message}, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)
    
@app.route('/user/comment/broadcast', methods=["POST"])
@Auth.Authentication.authenticateRequest
def broadcastComment():
    try:
        var_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_userId)
        var_Comment = Help.json.loads(Auth.Request.data)
        var_Comment = var_Comment["Comment"]
        var_Data = Comments.cComments.broadcastComment(var_userId, var_Comment)
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_Data, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/comment/broadcast/<p_battleId>', methods=["POST"])
@Auth.Authentication.authenticateRequest
def commentOnBattle(p_battleId):
    try:
        var_userId = Auth.Request.headers[GLOBAL.USER_KEY]
        Common.cBase.updateLastActivity(var_userId)
        var_Comment = Help.json.loads(Auth.Request.data)
        var_Comment = var_Comment["Comment"]
        var_Data = Comments.cComments.commentOnBattle(var_userId, var_Comment, p_battleId)
        var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
        return Auth.Authentication.createResponse(var_Data, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)
    
@app.route('/user/buy/health', methods=["POST"])
@Auth.Authentication.authenticateRequest
def buyHealth():
    try:
        pass
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)
    
@app.route('/user/buy/energy', methods=["POST"])
@Auth.Authentication.authenticateRequest
def buyEnergy():
    try:
        pass
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/buy/amo', methods=["POST"])
@Auth.Authentication.authenticateRequest
def buyAmo():
    try:
        pass
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/buy/skillpoints', methods=["POST"])
@Auth.Authentication.authenticateRequest
def buySkillpoints():
    try:
        pass
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/upgrade/energy', methods=["POST"])
@Auth.Authentication.authenticateRequest
def upgradeEnergy():
    try:
        pass
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/upgrade/health', methods=["POST"])
@Auth.Authentication.authenticateRequest
def upgradeHealth():
    try:
        pass
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)

@app.route('/user/upgrade/amo', methods=["POST"])
@Auth.Authentication.authenticateRequest
def upgradeAmo():
    try:
        pass
    except Exception:
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)
