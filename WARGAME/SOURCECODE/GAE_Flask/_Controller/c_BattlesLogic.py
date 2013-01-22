from _SQLite import s_DB as DB
from _Controller import c_Utils as Help
import Constants

class cBattles(object):
    def __init__(self):
        pass
    @staticmethod
    def getBattleList(p_userId):
        Constants.CLOSE = True
        Constants.COMMIT = False
        var_Return = DB.DBCalls.executeProcedure("udf_get_user_on_same_score", [p_userId, Constants.SCORE_TYPES["Level"]])
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        from Mapping import MAP_SP_USER_SCORES_SAME
        var_List = Help.helpUtil.loadCursorData(var_Cursor, MAP_SP_USER_SCORES_SAME)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.close()
        Constants.CLOSE = False
        Constants.COMMIT = False
        
        return var_List
    @staticmethod
    def sanctionAlliance(key, p_userId, p_allianceId, p_amount):
        
        var_Level1 = Help.helpUtil.getObject(key, Constants.CATEGORY_DEFINITION["Level"] + "_" + str(Constants.USERLEVEL), "I")
        var_percent = float(var_Level1["sanction_percent"]) / 100
        
        Constants.CLOSE = True
        Constants.COMMIT = False
        var_Return = DB.DBCalls.executeProcedure("udf_sanction_alliance", [p_userId, p_allianceId, p_amount, var_percent])
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        var_Message = ""
        for row in var_Cursor.fetchall():
            var_Message = row[0]
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.commit()
        var_Connection.close()
        Constants.CLOSE = False
        Constants.COMMIT = False
        if var_Message != "Success":
            Constants.STATUSKEY = var_Message
            raise Exception("Error")
        
        return { "Message": var_Message}
    @staticmethod
    def getSanctionList():
        Constants.CLOSE = True
        Constants.COMMIT = False
        var_Return = DB.DBCalls.select("*", "vw_sanction_list", "where _score_type_id_fk = %s" % (Constants.SCORE_TYPES["Level"]))
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        from Mapping import MAP_VIEW_USER_SANCTIONS
        var_List = Help.helpUtil.loadCursorData(var_Cursor, MAP_VIEW_USER_SANCTIONS)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.close()
        Constants.CLOSE = False
        Constants.COMMIT = False
        return var_List
    @staticmethod
    def attack(key, p_userId, p_attackUserId, unitKey):
        
        if p_userId == p_attackUserId:
            Constants.STATUSKEY = "ProcessingError"
            raise Exception("Same")
        
        var_params = []
        # get user level
        var_Users = DB.DBCalls.select("_user_id_fk, _score", "user_scores", "where _user_id_fk in (%s, %s) and _score_type_id_fk = %s" % (p_userId, p_attackUserId, Constants.SCORE_TYPES["Level"]))
        var_User_Score = 0
        var_BattleUser_Score = 0
        var_Cursor = var_Users["Cursor"]
        var_Connection = var_Users["Connection"]
        for row in var_Cursor.fetchall():
            if p_userId == str(row[0]):
                var_User_Score = row[1] + 2
            else:
                var_BattleUser_Score = row[1] + 2
        
        var_Cursor.close()
        # changed var_Connection.close()
        # getting user level information done
        
        var_Config = Help.helpUtil.getObject(key, Constants.CATEGORY_DEFINITION["Configurations"], "I")
        
        var_Level1_Exp = Help.helpUtil.getObject(key, Constants.CATEGORY_DEFINITION["Level"] + "_" + str(var_User_Score), "I")
        var_Level2_Exp = Help.helpUtil.getObject(key, Constants.CATEGORY_DEFINITION["Level"] + "_" + str(var_BattleUser_Score), "I")
        var_Level1_All = Help.helpUtil.getObject(key, Constants.CATEGORY_DEFINITION["Level"] + "_" + str(var_User_Score - 2), "I")
        var_Level2_All = Help.helpUtil.getObject(key, Constants.CATEGORY_DEFINITION["Level"] + "_" + str(var_BattleUser_Score - 2), "I")
        
        var_alliances_1 = var_Level1_All["alliances"]
        var_alliances_2 = var_Level2_All["alliances"]
        var_exp_1 = var_Level1_Exp["exp"]
        var_exp_2 = var_Level2_Exp["exp"]
        
        # making random policies
        import random as Rand
        import logging as Log
        var_unit_tok = var_Config["unit_usage_policy"].split("-")
        var_unit_tok_percent = float(Rand.randint(int(var_unit_tok[0]), int(var_unit_tok[1]))) / 100
        
        var_cash_win_tok = var_Config["cash_win_percent"].split("-")
        var_cash_win_percent = float(Rand.randint(int(var_cash_win_tok[0]), int(var_cash_win_tok[1]))) / 100
        
        var_cash_loss_tok = var_Config["cash_loss_percent"].split("-")
        var_cash_loss_percent = float(Rand.randint(int(var_cash_loss_tok[0]), int(var_cash_loss_tok[1]))) / 100
        
        var_damage_win_tok = var_Config["damage_on_win_percent"].split("-")
        var_damage_win_percent = float(Rand.randint(int(var_damage_win_tok[0]), int(var_damage_win_tok[1]))) / 100
        
        var_damage_loss_tok = var_Config["damage_on_loss_percent"].split("-")
        var_damage_loss_percent = float(Rand.randint(int(var_damage_loss_tok[0]), int(var_damage_loss_tok[1]))) / 100
        
        # parameters for first call
        var_params.append(p_userId)
        var_params.append(p_attackUserId)
        var_params.append(var_alliances_1)
        var_params.append(var_alliances_2)
        var_params.append(var_unit_tok_percent)
        var_params.append(var_damage_loss_percent)
        
        Constants.CLOSE = True
        Constants.COMMIT = False
        
        var_Return = DB.DBCalls.executeProcedureOnSameConn("udf_get_rand_alliances", var_params, var_Connection)
        # changed var_Return = DB.DBCalls.executeProcedure("udf_get_rand_alliances", var_params)
        var_Cursor = var_Return["Cursor"]
        # changed var_Connection = var_Return["Connection"]
        
        var_Message = ""
        for row in var_Cursor.fetchall():
            var_Message = row[0]
            
        if var_Message == "Success":
            var_Cursor.nextset()
            for row in var_Cursor.fetchall():
                var_Text_1 = row[0]
                Log.debug(var_Text_1)
            
            var_Cursor.nextset() # Unit List Users
            var_user_attack = 0
            var_user_defense = 0
            for row in var_Cursor.fetchall():
                var_Product = Help.helpUtil.getObject(unitKey, row[1], "P")
                var_user_attack = var_user_attack + int(var_Product["attack"]) * row[2]
                var_user_defense = var_user_defense + int(var_Product["defense"]) * row[2]
            
            var_Cursor.nextset() # Unit List Alliances
            for row in var_Cursor.fetchall():
                var_Product = Help.helpUtil.getObject(unitKey, row[1], "P")
                var_user_attack = var_user_attack + int(var_Product["attack"]) * row[2]
                var_user_defense = var_user_defense + int(var_Product["defense"]) * row[2]
            
            var_Cursor.nextset()
            for row in var_Cursor.fetchall():
                var_Text_2 = row[0]
                Log.debug(var_Text_2)
    
            var_Cursor.nextset() # Unit List BAttle
            var_battle_attack = 0
            var_battle_defense = 0
            for row in var_Cursor.fetchall():
                var_Product = Help.helpUtil.getObject(unitKey, row[1], "P")
                var_battle_attack = var_battle_attack + int(var_Product["attack"]) * row[2]
                var_battle_defense = var_battle_defense + int(var_Product["defense"]) * row[2]
            
            var_Cursor.nextset() # Unit List Alliances BAttle
            for row in var_Cursor.fetchall():
                var_Product = Help.helpUtil.getObject(unitKey, row[1], "P")
                var_battle_attack = var_battle_attack + int(var_Product["attack"]) * row[2]
                var_battle_defense = var_battle_defense + int(var_Product["defense"]) * row[2]
            
            #Log.debug(var_user_attack)
            #Log.debug(var_user_defense)
            #Log.debug(var_battle_attack)
            #Log.debug(var_battle_defense)
            
            var_Cursor.close()
            # changed var_Connection.close()
            Constants.CLOSE = True
            Constants.COMMIT = False
            
            var_params = []
            var_params.append(p_userId)
            var_params.append(p_attackUserId)
            var_params.append(var_user_attack)
            var_params.append(var_user_defense)
            var_params.append(var_battle_attack)
            var_params.append(var_battle_defense)
            var_params.append(var_Text_1)
            var_params.append(var_Text_2)
            var_params.append(var_cash_win_percent)
            var_params.append(var_cash_loss_percent)
            var_params.append(var_damage_win_percent)
            var_params.append(var_damage_loss_percent)
            var_params.append(4)
            var_params.append(2)
            var_params.append(var_exp_1)
            var_params.append(var_exp_2)
            var_params.append(int(Constants.BATTLE_TYPES["Battle"]))
            
            Constants.CLOSE = True
            Constants.COMMIT = False
            var_Return = DB.DBCalls.executeProcedureOnSameConn("udf_do_battle", var_params, var_Connection)
            # changedvar_Return = DB.DBCalls.executeProcedure("udf_do_battle", var_params)
            var_Cursor = var_Return["Cursor"]
            # changed var_Connection = var_Return["Connection"]
            
            from Mapping import MAP_TABLE_USER_BATTLES, MAP_TABLE_USER_SCORES
            var_List = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_BATTLES)
            var_Cursor.nextset()
            var_Score1 = Help.helpUtil.createObjectJsonDirectly(var_Cursor, MAP_TABLE_USER_SCORES, "_score_type_id_fk", 0)
            var_Cursor.nextset()
            var_Score2 = Help.helpUtil.createObjectJsonDirectly(var_Cursor, MAP_TABLE_USER_SCORES, "_score_type_id_fk", 0) 
            # processing ends here
            var_Connection.commit()
            var_Connection.close()
            Constants.CLOSE = False
            Constants.COMMIT = False
            return {
                "Battle": var_List,
                "Score1": var_Score1,
                "Score2": var_Score2
            }
        else: # not successful means requirement does not meet
            Constants.STATUSKEY = var_Message
            raise Exception("Error")
        
    @staticmethod
    def attackSanction(p_userId, p_attackUserId):
        Constants.CLOSE = True
        Constants.COMMIT = False
        var_Return = DB.DBCalls.executeProcedure("udf_attack_sanction", [p_userId, p_attackUserId, Constants.BATTLE_TYPES["Sanction"]])
        var_Cursor = var_Return["Cursor"]
        # your processing begins here
        from Mapping import MAP_TABLE_USER_BATTLES
        var_List = Help.helpUtil.loadCursorData(var_Cursor, MAP_TABLE_USER_BATTLES)
        # processing ends here
        var_Connection = var_Return["Connection"]
        var_Connection.commit()
        var_Connection.close()
        Constants.CLOSE = False
        Constants.COMMIT = False
        return var_List