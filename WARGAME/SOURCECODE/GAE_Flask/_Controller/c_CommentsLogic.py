from _SQLite import s_DB as DB
from _Controller import c_Utils as Help
import Constants as GLOBAL
import datetime as Date

class cComments(object):
    def __init__(self):
        pass
    @staticmethod
    def broadcastComment(p_userId, p_Comment):
        var_str = "%s, '%s', %s, NULL, '%s'" % (p_userId, p_Comment, GLOBAL.COMMENT_TYPES["Alliance"], Date.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        DB.DBCalls.insert("_user_id_fk, _comment, _comment_type_id_fk, _in_entity_fk, _commented_on", var_str, "user_comments")
        # no exception
        var_Ret = {
           "id": p_userId,
           "name": GLOBAL.USERNAME,
           "comment": p_Comment,
           "commentType": GLOBAL.COMMENT_TYPES["Alliance"],
           "commentedOn": Help.helpUtil.getTimeFloat(Date.datetime.now())
        }
        return var_Ret
        
    @staticmethod
    def commentOnBattle(p_userId, p_Comment, p_EntityId):
        var_str = "%s, '%s', %s, %s, '%s'" % (p_userId, p_Comment, GLOBAL.COMMENT_TYPES["Battle"], p_EntityId, Date.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        DB.DBCalls.insert("_user_id_fk, _comment, _comment_type_id_fk, _in_entity_fk, _commented_on", var_str, "user_comments")
        # no exception
        var_Ret = {
           "id": p_userId,
           "name": GLOBAL.USERNAME,
           "comment": p_Comment,
           "commentType": GLOBAL.COMMENT_TYPES["Battle"],
           "commentedOn": Help.helpUtil.getTimeFloat(Date.datetime.now())
        }
        return var_Ret