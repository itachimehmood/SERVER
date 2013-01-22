from _Startup import app
from _Controller import c_Authentication as Auth, c_Utils as Help
from google.appengine.api import files as GSFiles
import Constants as GLOBAL
from Constants import STORE_DEFINITION

@app.route('/', methods=["GET"])
def api_root():
    return "It Works"

@app.route('/saeed/upload/image', methods=["POST"])
def api_RND():
    
    #from google.appengine.api import images as GSImage
    #var_Image = GSImage.Image(blob_key=blob_key)
    #var_Image.resize(width=80, height=100)
    #thumbnail = var_Image.execute_transforms(output_encoding=GSImage.JPEG)
    #var_Response = Auth.Response(thumbnail, status=200, mimetype='image/jpeg')
    #return var_Response
    
    fileName = GLOBAL.GSBUCKET + "saeed_test.jpg"
    writable_file_name = GSFiles.gs.create(fileName, mime_type='image/jpg', acl='public-read')
    with GSFiles.open(writable_file_name, 'a') as f:
        f.write(Auth.Request.data)
    GSFiles.finalize(writable_file_name)
    
    return "Uploaded Successfully"

@app.route('/upload/dotnet/<p_storeId>/<p_version>/<p_dataType>', methods = ['POST'])
def api_uploadFile(p_storeId, p_version, p_dataType):
    
    from Constants import METACONFIG
    fileName = Auth.GLOBAL.GSBUCKET + str(p_storeId) + "_" + str(p_version) + "_" + str(p_dataType) + '.json'
    
    writable_file_name = GSFiles.gs.create(fileName, mime_type='application/octet-stream', acl='public-read')
    with GSFiles.open(writable_file_name, 'a') as f:
        f.write(Auth.Request.data)
    GSFiles.finalize(writable_file_name)
    
    
    METACONFIG[STORE_DEFINITION[str(p_storeId)]][str(p_dataType)]["version"] = p_version

    return "Uploaded Successfully"
    
@app.route('/update/<p_storeId>/<p_version>/<p_dataType>')
def updateMemCache(p_storeId, p_version, p_dataType):
    
    from Constants import METACONFIG
    fileName = Auth.GLOBAL.GSBUCKET + str(p_storeId) + "_" + str(p_version) + "_" + str(p_dataType) + '.json'
    with GSFiles.open(fileName, 'r') as f:
        data = f.read()
    # decide key
    var_cacheKey = Auth.GLOBAL.STORE_DEFINITION[str(p_storeId)] + "_" + str(p_version) + "_" + str(p_dataType)
    Help.helpUtil.setCache(var_cacheKey, data)
    
    METACONFIG[STORE_DEFINITION[str(p_storeId)]][str(p_dataType)]["version"] = int(p_version)
    
    return "Updated Successfully."

@app.route('/server/config', methods=["GET"])
def getServerConfig():
    
    try:
        var_user_type = Auth.Request.headers["X-BGS-USER-TYPE"]
        if var_user_type != "0" and var_user_type != "1" and var_user_type != "2":
            raise Exception("MissingHeader")
    except Exception:
        import traceback
        GLOBAL.STATUSKEY = "MissingHeader"
        s = traceback.format_exc()
        return Auth.Authentication.errorReturn(s)
    
    import datetime
    from Constants import METACONFIG
    from _SQLite import s_DB as DB
    var_respdata = str(Help.helpUtil.getTimeFloat(datetime.datetime.now()))
    
    var_arabic = DB.DBCalls.select("_text", "arabic", "")
    var_Cursor = var_arabic["Cursor"]
    var_text = ""
    for row in var_Cursor.fetchall():
        var_text = row[0]
    var_Connection = var_arabic["Connection"]
    var_Connection.close()

    var_data = {
        "GlobalConfig": {"time":1357564169,"version":1.3,"analyticsmode":0,"forceupdate":1,"versionupdateinterval":1,
                         "itunesurl":"https://itunes.apple.com/sa/app/khmn-rsmy/id566535292?mt=8",
                        "versionupdatetext": var_text},
        "GameConfig": {
            "time": var_respdata,
            "Stores": {
                STORE_DEFINITION["units"]: {
                      "version": METACONFIG["units"][var_user_type]["version"],
                      "file": "1_%s_%s.sqlite" % (METACONFIG["units"][var_user_type]["version"], var_user_type)
                },
                STORE_DEFINITION["missions"]: {
                      "version": METACONFIG["missions"][var_user_type]["version"],
                      "file": "2_%s_%s.sqlite" % (METACONFIG["missions"][var_user_type]["version"], var_user_type)
                },
                STORE_DEFINITION["configs"]: {
                      "version": METACONFIG["configs"][var_user_type]["version"],
                      "file": "3_%s_%s.sqlite" % (METACONFIG["configs"][var_user_type]["version"], var_user_type)
                }
            }
        },
        "CustomConfig": {
                   
        }
    }
    
    var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
    return Auth.Authentication.createResponse(var_data, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)

@app.route('/masterdata')
@Auth.Authentication.authenticateRequest
def getGameMasterData():
    from Constants import METACONFIG
    var_user_type = Auth.Request.headers["X-BGS-USER-TYPE"]
    from _Controller import c_Base as Common
    
    Common.cBase.updateMemcahce(METACONFIG["units"][var_user_type]["version"], METACONFIG["missions"][var_user_type]["version"]
                                , METACONFIG["configs"][var_user_type]["version"], var_user_type)
    
    var_data = {
           "Stores": {
                STORE_DEFINITION["units"]: {
                      "version": METACONFIG["units"][var_user_type]["version"],
                      "file": "1_%s_%s.sqlite" % (METACONFIG["units"][var_user_type]["version"], var_user_type)
                },
                STORE_DEFINITION["missions"]: {
                      "version": METACONFIG["missions"][var_user_type]["version"],
                      "file": "2_%s_%s.sqlite" % (METACONFIG["missions"][var_user_type]["version"], var_user_type)
                },
                STORE_DEFINITION["configs"]: {
                      "version": METACONFIG["configs"][var_user_type]["version"],
                      "file": "3_%s_%s.sqlite" % (METACONFIG["configs"][var_user_type]["version"], var_user_type)
                }
            }
    }

    var_Ret = Auth.Authentication.createCodeMsg(GLOBAL.STATUS_DETAILS["Success"])
    return Auth.Authentication.createResponse(var_data, var_Ret["Code"], var_Ret["Msg"], "", GLOBAL.RESPONSE_CODE_SUC)    

