from _Controller import c_Utils as Help
class DBCalls(object):
    def __init__(self):
        pass
    @staticmethod
    def insert(p_columns, p_values, p_table):
        var_Connection = Help.helpUtil.createConnection()
        Help.GLOBAL.STATUSKEY = "InsertFailed"   
        var_Cursor = var_Connection.cursor()
        import logging as Log
        Log.debug("INSERT INTO %s (%s) VALUES (%s)" % (p_table, p_columns, p_values))
        var_Cursor.execute("INSERT INTO %s (%s) VALUES (%s)" % (p_table, p_columns, p_values))
        var_Connection.commit()
        var_Connection.close()
        Help.GLOBAL.CONNECTION = None
    @staticmethod
    def update(p_column, p_value, p_table, p_where):
        var_Connection = Help.helpUtil.createConnection()
        Help.GLOBAL.STATUSKEY = "UpdateFailed"   
        var_Cursor = var_Connection.cursor()
        var_Cursor.execute("UPDATE %s SET %s = %s %s" %(p_table, p_column, p_value, p_where))
        var_Connection.commit()
        var_Connection.close()
        Help.GLOBAL.CONNECTION = None
    @staticmethod
    def delete(p_table, p_where):
        var_Connection = Help.helpUtil.createConnection()
        Help.GLOBAL.STATUSKEY = "DeleteFailed"   
        var_Cursor = var_Connection.cursor()
        var_Cursor.execute('DELETE FROM ' + p_table + ' WHERE' + p_where + ')')
        var_Connection.commit()
        var_Connection.close()
        Help.GLOBAL.CONNECTION = None
    @staticmethod
    def select(p_columns, p_table, p_where):
        var_Connection = Help.helpUtil.createConnection()
        Help.GLOBAL.STATUSKEY = "SelectFailed"   
        var_Cursor = var_Connection.cursor()
        var_Cursor.execute('SELECT ' + p_columns + ' FROM ' + p_table + ' ' + p_where)
        var_Return = {
              "Connection": var_Connection,
              "Cursor": var_Cursor
        }
        return var_Return
    @staticmethod
    def executeProcedure(p_procedureName, p_lstParams):
        Help.GLOBAL.STATUSKEY = "ProcedureCallFailed"
        import logging as Log
        var_Params = ()
        for param in p_lstParams:
            var_Params += (param,)
        var_Connection = Help.helpUtil.createConnection()   
        var_Cursor = var_Connection.cursor()
        Log.debug(p_procedureName)
        Log.debug(str(var_Params))
        var_Cursor.callproc(p_procedureName, var_Params)
        var_Return = {
              "Connection": var_Connection,
              "Cursor": var_Cursor
        }
        return var_Return
    @staticmethod
    def executeProcedureOnSameConn(p_procedureName, p_lstParams, p_Connection):
        Help.GLOBAL.STATUSKEY = "ProcedureCallFailed"
        import logging as Log
        var_Params = ()
        for param in p_lstParams:
            var_Params += (param,)
            
        var_Cursor = p_Connection.cursor()
        Log.debug(p_procedureName)
        Log.debug(str(var_Params))
        var_Cursor.callproc(p_procedureName, var_Params)
        var_Return = {
            "Cursor": var_Cursor
        }
        return var_Return