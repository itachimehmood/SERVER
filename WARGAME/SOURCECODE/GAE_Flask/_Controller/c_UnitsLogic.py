from _SQLite import s_DB as DB
from _Controller import c_Utils as Help
import Constants as GLOBAL

class cUnits(object):
    def __init__(self):
        pass
    @staticmethod
    def getUserUnits(p_userId):
        
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        var_Return = DB.DBCalls.select("_unit_id, _unit_qty", "user_units", "where _user_id_fk = %s" % (p_userId,))
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        from Mapping import MAP_TABLE_USER_UNITS
        var_List = Help.helpUtil.createObjectJsonDirectly(var_Cursor, MAP_TABLE_USER_UNITS, "_unit_id", 0)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.close()
        
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        return var_List
    @staticmethod
    def getUnitById(p_userId, p_unitId):
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        var_Return = DB.DBCalls.select("_unit_id, _unit_qty", "user_units", "where _user_id_fk = %s AND _unit_id = '%s'" % (p_userId, p_unitId))
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        from Mapping import MAP_TABLE_USER_UNITS
        var_Unit = Help.helpUtil.createObjectJsonDirectly(var_Cursor, MAP_TABLE_USER_UNITS, "_unit_id", 0)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.close()
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        return var_Unit
    @staticmethod
    def deployUnit(p_key, p_unitId, p_userId):
        # get unit detail from meta data, expected p_unitId is 1_1_1
        var_Unit = Help.helpUtil.getObject(p_key, p_unitId, "P")
        if var_Unit.has_key("_buy_buckets") and var_Unit.has_key("attack") and var_Unit.has_key("defense"):
            var_buckets = Help.helpUtil.parseBuckets(var_Unit["_buy_buckets"])
            var_active = 0
            if var_Unit["_is_active"] == True:
                var_active = 1
            else:
                var_active = 0
            # required parameters are
            var_lstParams = []
            var_lstParams.append(int(p_userId))
            var_lstParams.append(p_unitId)
            var_lstParams.append(int(var_buckets[0]["amount"]))
            var_lstParams.append(int(var_Unit["attack"]))
            var_lstParams.append(int(var_Unit["defense"]))
            var_lstParams.append(int(var_Unit["upkeep"]))
            var_lstParams.append(int(var_Unit["_visible_from_level"]))
            var_lstParams.append(var_active)
            # make database call, and get the result
            GLOBAL.CLOSE = True
            GLOBAL.COMMIT = False
            var_Return = DB.DBCalls.executeProcedure("udf_unit_deploy", var_lstParams)
            var_Cursor = var_Return["Cursor"]
            # your processing begins here
            var_Message = ""
            for row in var_Cursor.fetchall():
                var_Message = row[0]
                pass
            if var_Message == "Success":
                var_Cursor.nextset()
                from Mapping import MAP_TABLE_USER_UNITS
                var_Units = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_UNITS)
                var_Cursor.nextset()
                from Mapping import MAP_TABLE_USER_SCORES
                var_Scores = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_SCORES)
                # processing ends here
                var_Connection = var_Return["Connection"]
                var_Connection.commit()
                var_Connection.close()
                GLOBAL.CLOSE = False
                GLOBAL.COMMIT = False
                
                return {
                            "Units": var_Units,
                            "Scores": var_Scores
                }
            else:
                GLOBAL.STATUSKEY = var_Message
                raise Exception("Error")
        else:
            GLOBAL.CLOSE = False
            GLOBAL.COMMIT = False
            GLOBAL.STATUSKEY = "MissingAttribute"
            raise Exception("Error")
    @staticmethod
    def disbandUnit(p_key, p_unitId, p_userId):
        # get unit detail from meta data, expected p_unitId is 1_1_1
        var_Unit = Help.helpUtil.getObject(p_key, p_unitId, "P")
        if var_Unit.has_key("_sell_buckets") and var_Unit.has_key("attack") and var_Unit.has_key("defense"):
            var_buckets = Help.helpUtil.parseSellBuckets(var_Unit["_sell_buckets"])
            var_active = 0
            if var_Unit["_is_active"] == True:
                var_active = 1
            else:
                var_active = 0
            # required parameters are
            var_lstParams = []
            var_lstParams.append(int(p_userId))
            var_lstParams.append(p_unitId)
            var_lstParams.append(int(var_buckets[0]["amount"]))
            var_lstParams.append(int(var_Unit["attack"]))
            var_lstParams.append(int(var_Unit["defense"]))
            var_lstParams.append(int(var_Unit["upkeep"]))
            var_lstParams.append(int(var_Unit["_visible_from_level"]))
            var_lstParams.append(var_active)
            # make database call, and get the result
            GLOBAL.CLOSE = True
            GLOBAL.COMMIT = False
            var_Return = DB.DBCalls.executeProcedure("udf_unit_disband", var_lstParams)
            var_Cursor = var_Return["Cursor"]
            # your processing begins here
            var_Message = ""
            for row in var_Cursor.fetchall():
                var_Message = row[0]
                pass
            if var_Message == "Success":
                var_Cursor.nextset()
                from Mapping import MAP_TABLE_USER_UNITS
                var_Units = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_UNITS)
                var_Cursor.nextset()
                from Mapping import MAP_TABLE_USER_SCORES
                var_Scores = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_SCORES)
                # processing ends here
                var_Connection = var_Return["Connection"]
                var_Connection.commit()
                var_Connection.close()
                GLOBAL.CLOSE = False
                GLOBAL.COMMIT = False
                return {
                            "Units": var_Units,
                            "Scores": var_Scores
                }
            else:
                GLOBAL.STATUSKEY = var_Message
                raise Exception("Error")
        else:
            GLOBAL.CLOSE = False
            GLOBAL.COMMIT = False
            GLOBAL.STATUSKEY = "MissingAttribute"
            raise Exception("Error")