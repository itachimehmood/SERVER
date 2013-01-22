from _SQLite import s_DB as DB
from _Controller import c_Utils as Help
import Constants as GLOBAL

class cUsers(object):
    def __init__(self):
        pass
    @staticmethod
    def getUserScore(p_lstParams):
        
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        var_Return = DB.DBCalls.executeProcedure("udf_get_user", p_lstParams)
        var_Cursor = var_Return["Cursor"]
        
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        # your processing begins here
        from Mapping import MAP_SP_USER_SCORES, MAP_TABLE_USER_UNITS, MAP_TABLE_USER_MISSIONS, MAP_TABLE_USER_COMMENTS, MAP_SP_USER_BATTLES
        
        var_List = Help.helpUtil.loadCursorData(var_Cursor, MAP_SP_USER_SCORES)
        var_Cursor.nextset()
        var_Units = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_UNITS)
        var_Cursor.nextset()
        var_Missions = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_MISSIONS)
        var_Cursor.nextset()
        var_Battles = Help.helpUtil.loadCursorData(var_Cursor, MAP_SP_USER_BATTLES)
        var_Cursor.nextset()
        var_Comments = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_COMMENTS)
        
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.commit()
        var_Connection.close()
        
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        return {
            "Scores": var_List,
            "Units": var_Units,
            "Missions": var_Missions,
            "Battles": var_Battles,
            "Comments": var_Comments
        }
    @staticmethod
    def getUserById(p_userId):
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        from Mapping import MAP_TABLE_USERS
        var_Return = DB.DBCalls.select("_id, _user_game_token, _last_activity, _user_code, _alliances", "users", "where _id = " + p_userId)
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        # var_User = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USERS)
        var_User = Help.helpUtil.createObjectJsonDirectly(var_Cursor, MAP_TABLE_USERS, "_id", 0)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.close()
        
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        return var_User
    @staticmethod
    def makeUserAliance(p_userId, p_AllianceCode):
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        var_Return = DB.DBCalls.executeProcedure("udf_make_alliance", [p_userId, p_AllianceCode])
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        var_Message = ""
        for row in var_Cursor.fetchall():
            var_Message = row[0]
            pass
        # processing ends here
        var_Connection = var_Return["Connection"]
        if var_Message == "Success":
            var_Connection.commit()
        var_Connection.close()
        
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        
        if var_Message != "Success":
            GLOBAL.STATUSKEY = var_Message
            raise Exception(var_Message)
        return var_Message
    @staticmethod
    def getUserAlliance(p_userId):
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        from Mapping import MAP_SP_USER_ALLIANCES_INVITES
        var_Return = DB.DBCalls.executeProcedure("udf_alliances_list", [p_userId])
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        var_List = Help.helpUtil.loadCursorData(var_Cursor, MAP_SP_USER_ALLIANCES_INVITES)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.close()
        
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        return var_List
    @staticmethod
    def getUserAllianceInvites(p_userId):
        
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        from Mapping import MAP_SP_USER_ALLIANCES_INVITES
        var_Return = DB.DBCalls.executeProcedure("udf_alliances_invites", [p_userId])
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        var_List = Help.helpUtil.loadCursorData(var_Cursor, MAP_SP_USER_ALLIANCES_INVITES)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.close()
        
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        
        return var_List
    @staticmethod
    def deleteUserAlliance(p_userId, p_AllianceId):
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        var_Return = DB.DBCalls.executeProcedure("udf_alliances_delete", [p_userId, p_AllianceId])
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        var_Message = ""
        for row in var_Cursor.fetchall():
            var_Message = row[0]
        # processing ends here
        var_Connection = var_Return["Connection"]
        if var_Message == "Success":
            var_Connection.commit()
        var_Connection.close()
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        
        if var_Message == "Success":
            return var_Message
        else:
            GLOBAL.STATUSKEY = var_Message
            raise Exception("Error")
    @staticmethod
    def acceptAllianceRequest(p_userId, p_AllianceId):
        
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        var_Return = DB.DBCalls.executeProcedure("udf_alliances_accept", [p_userId, p_AllianceId])
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        var_Message = ""
        for row in var_Cursor.fetchall():
            var_Message = row[0]
            
        # processing ends here
        var_Connection = var_Return["Connection"]
        if var_Message == "Success":
            var_Connection.commit()
        var_Connection.close()
        
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        if var_Message == "Success":
            return var_Message
        else:
            GLOBAL.STATUSKEY = var_Message
            raise Exception("Error")
    