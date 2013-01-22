from _SQLite import s_DB as DB
from _Controller import c_Utils as Help
import Constants as GLOBAL

class cMissions(object):
    def __init__(self):
        pass
    @staticmethod
    def doMission(p_keyM, p_keyC, p_userId, p_missionId):
        var_Mission = Help.helpUtil.getObject(p_keyM, p_missionId, "P")
        
        GLOBAL.STATUSKEY = "MissingAttribute"
        
        var_min = int(var_Mission["revenue_from"])
        var_max = int(var_Mission["revenue_to"])
        import random as Rand
        var_Revenue = Rand.randint(var_min, var_max)
        var_active = Help.helpUtil.boolToInt(var_Mission["_is_active"])
        var_energy = Help.helpUtil.stringIsNullOrEmpty(var_Mission["energy"])
        var_experience = Help.helpUtil.stringIsNullOrEmpty(var_Mission["expereince"])
        var_visible_from = Help.helpUtil.stringIsNullOrEmpty(var_Mission["_visible_from_level"])
        
        var_lstParams = []
        var_lstParams.append(int(p_userId))
        var_lstParams.append(p_missionId)
        var_lstParams.append(var_Mission["units_required"])
        var_lstParams.append(20)
        var_lstParams.append(var_Revenue)
        var_lstParams.append(var_Mission["rewards"])
        var_lstParams.append(int(var_energy))
        var_lstParams.append(int(var_experience))
        var_lstParams.append(int(var_Mission["aliiance"]))
        var_lstParams.append(int(var_visible_from))
        var_lstParams.append(var_active)
        
        var_Level = str(int(GLOBAL.USERLEVEL) + 2)
        var_Config = Help.helpUtil.getObject(p_keyC, "%s_%s" % (GLOBAL.CATEGORY_DEFINITION["Level"], var_Level), "I")
        
        GLOBAL.STATUSKEY = "MissingAttribute"

        var_lstParams.append(var_Config["exp"])


        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False        
        
        var_Return = DB.DBCalls.executeProcedure("udf_do_mission", var_lstParams)
        var_Connection = var_Return["Connection"]
        var_Cursor = var_Return["Cursor"]
        var_Message = ""
        for row in var_Cursor.fetchall():
            var_Message = row[0]
            
        if var_Message == "Success":
            var_Cursor.nextset()
            from Mapping import MAP_TABLE_USER_SCORES
            var_Scores = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_SCORES)
            var_Cursor.nextset()
            from Mapping import MAP_TABLE_USER_MISSIONS
            var_Missions = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_MISSIONS)
            
            var_Connection.commit()
            var_Connection.close()
            
            GLOBAL.CLOSE = False
            GLOBAL.COMMIT = False
            
                        
            return {
                "Missions": var_Missions,
                "Scores": var_Scores
            }
        else:
            GLOBAL.STATUSKEY = var_Message
            raise Exception("Error")
    
    @staticmethod
    def getMissionById(p_userId, p_missionId):
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        var_Return = DB.DBCalls.select("_mission_id, _mission_rank, _mission_completion, _mission_count", "user_missions", "where _user_id_fk = %s and _mission_id = '%s'" % (p_userId, p_missionId))
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        from Mapping import MAP_TABLE_USER_MISSIONS
        var_Mission = Help.helpUtil.createObjectJsonDirectly(var_Cursor, MAP_TABLE_USER_MISSIONS, "_mission_id", 0)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.close()
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        return var_Mission
    @staticmethod
    def getMissions(p_userId):
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        var_Return = DB.DBCalls.select("_mission_id, _mission_rank, _mission_completion, _mission_count", "user_missions", "where _user_id_fk = %s" % (p_userId ,))
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        from Mapping import MAP_TABLE_USER_MISSIONS
        var_Missions = Help.helpUtil.createObjectJsonDirectly(var_Cursor, MAP_TABLE_USER_MISSIONS, "_mission_id", 0)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.close()
        
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        
        return var_Missions