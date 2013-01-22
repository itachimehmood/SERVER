class cBase(object):
    def __init__(self):
        pass
    @staticmethod
    def updateLastActivity(p_userId):
        
        from _SQLite import s_DB as DB
        import Constants as GLOBAL
        import datetime as Date
        
        GLOBAL.CLOSE = True
        GLOBAL.COMMIT = False
        
        var_Return = DB.DBCalls.executeProcedure("udf_update_scores", [p_userId, 5])
        var_Cursor = var_Return["Cursor"]
        var_Connection = var_Return["Connection"]
        
        var_Message = ""
        for row in var_Cursor.fetchall():
            var_Message = row[0]
            GLOBAL.USERLEVEL = row[1]
            GLOBAL.USERLASTSCOREUPDATE = row[2]
            GLOBAL.USERNAME = row[3]
        
        if var_Message != "Success":
            GLOBAL.STATUSKEY = var_Message
            raise Exception("Error")
        
        import logging as Log
        var_diff = (DB.Help.helpUtil.getTimeFloat(Date.datetime.now()) - GLOBAL.USERLASTSCOREUPDATE) / 60
        Log.debug(var_diff)
        if var_diff > 5:
            var_upkeep = 0
            var_Cursor.close()
            var_Cursor = var_Connection.cursor()
            var_Cursor.execute("select _unit_id, _unit_qty from user_units where _user_id_fk = %s" % (p_userId, ))
            for row in var_Cursor.fetchall():
                var_Product = DB.Help.helpUtil.getObject("units_1_1", row[0], "P")
                var_upkeep = var_upkeep + (int(var_Product["upkeep"]) * int(row[1]))
            Log.debug(var_upkeep)
            var_Cursor.close()
            var_Cursor = var_Connection.cursor()
            var_Cursor.execute("update user_scores set _score = _score - %s where _user_id_fk = %s and _score_type_id_fk = %s" % (var_upkeep, p_userId, GLOBAL.SCORE_TYPES["Cash"]))
            
        var_Connection.commit()
        var_Connection.close()
        
        GLOBAL.CLOSE = False
        GLOBAL.COMMIT = False
        
    @staticmethod
    def updateMemcahce(p_ver1, p_ver2, p_ver3, p_user):
        from Constants import MEMCACHE
        from Constants import STORE_DEFINITION
        from _Controller import c_Utils as Help
        try:
            var_JSON = MEMCACHE.get("configs_%s_%s" % (str(p_ver3), p_user))
            var_JSON[STORE_DEFINITION["configs"]]
        except:
            Help.helpUtil.uploadFileInMemcache(STORE_DEFINITION["configs"], str(p_ver3), p_user)
            
        try:
            var_JSON = MEMCACHE.get("missions_%s_%s" % (str(p_ver2), p_user))
            var_JSON[STORE_DEFINITION["missions"]]
        except:
            Help.helpUtil.uploadFileInMemcache(STORE_DEFINITION["missions"], str(p_ver2), p_user)
            
        try:
            var_JSON = MEMCACHE.get("units_%s_%s" % (str(p_ver1), p_user))
            var_JSON[STORE_DEFINITION["units"]]
        except:
            Help.helpUtil.uploadFileInMemcache(STORE_DEFINITION["units"], str(p_ver1), p_user)