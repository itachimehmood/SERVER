MAP_TABLE_USERS = [
    {"_id": 0, 0: "_id", "json": "id"},
    {"_user_game_token": 1, 1: "_user_game_token", "json": "gameToken"},
    {"_last_activity": 2, 2: "_last_activity", "json": "lastActivity"},
    {"_user_code": 3, 3: "_user_code", "json": "inviteCode"},
    {"_alliances": 4, 4: "_alliances", "json": "alliances"},
    {"_display_name": 5, 5: "_display_name", "json": "name"}
]

MAP_TABLE_USER_SCORES = [
   {"_score_type_id_fk": 0, 0: "_score_type_id_fk", "json": "scoreType"},
   {"_score": 1, 1: "_score", "json": "score"},
   {"_max": 2, 2: "_max", "json": "max"}
]

MAP_TABLE_USER_UNITS = [
   {"_unit_id": 0, 0: "_unit_id", "json": "id"},
   {"_unit_qty": 1, 1: "_unit_qty", "json": "qty"}
]

MAP_TABLE_USER_MISSIONS = [
   {"_mission_id": 0, 0: "_mission_id", "json": "id"},
   {"_mission_rank": 1, 1: "_mission_rank", "json": "rank"},
   {"_mission_completion": 2, 2: "_mission_completion", "json": "percentage"},
   {"_mission_count": 3, 3: "_mission_count", "json": "takes"}
   
]
MAP_TABLE_USER_BATTLES = [
    {"_user_id_fk": 0, 0: "_user_id_fk", "json": "userId"},
    {"_battle_with_id_fk": 1, 1: "_battle_with_id_fk", "json": "battleWithId"},
    {"_battle_type_id_fk": 2, 2: "_battle_type_id_fk", "json": "battleType"},
    {"_user_data": 3, 3: "_user_data", "json": "userData"},
    {"_battle_with_data": 4, 4: "_battle_with_data", "json": "battleWithData"},
    {"_battled_at": 5, 5: "_battled_at", "json": "battledAt"},
    {"_victory_id_fk": 6, 6: "_victory_id_fk", "json": "victorious"},
    {"_id": 7, 7: "_id", "json": "id"},
    {"_user_display_name": 8, 8: "_user_display_name", "json": "userName"},
    {"_battle_display_name": 9, 9: "_battle_display_name", "json": "battleName"}
]

MAP_TABLE_USER_COMMENTS = [
    {"_user_id_fk": 0, 0: "_user_id_fk", "json": "id"},
    {"_comment": 1, 1: "_comment", "json": "comment"},
    {"_comment_type_id_fk": 2, 2: "_comment_type_id_fk", "json": "commentType"},
    {"_commented_on": 3, 3: "_commented_on", "json": "commentedOn"},
    {"_display_name": 4, 4: "_display_name", "json": "name"}
]

MAP_SP_USER_BATTLES = [
    {"_id": 0, 0: "_id", "json": "id"},                   
    {"_user_id_fk": 1, 1: "_user_id_fk", "json": "userId"},
    {"_battle_with_id_fk": 2, 2: "_battle_with_id_fk", "json": "battleWithId"},
    {"_battle_type_id_fk": 3, 3: "_battle_type_id_fk", "json": "battleType"},
    {"_user_data": 4, 4: "_user_data", "json": "userData"},
    {"_battle_with_data": 5, 5: "_battle_with_data", "json": "battleWithData"},
    {"_battled_at": 6, 6: "_battled_at", "json": "battledAt"},
    {"_victory_id_fk": 7, 7: "_victory_id_fk", "json": "victorious"},
    {"_comment_user_id_fk": 8, 8: "_comment_user_id_fk", "json": "userCommentId"},
    {"_comment": 9, 9: "_comment", "json": "_comment"},
    {"_comment_type_id_fk": 10, 10: "_comment_type_id_fk", "json": "type"},
    {"_commented_on": 11, 11: "_commented_on", "json": "_commented_on"},
    {"_user_display_name": 12, 12: "_user_display_name", "json": "userName"},
    {"_battle_display_name": 13, 13: "_battle_display_name", "json": "battleName"},
    {"_comment_display_name": 14, 14: "_comment_display_name", "json": "commentName"}
]

MAP_VIEW_USER_SANCTIONS = [
    {"_user_id_fk": 0, 0: "_user_id_fk", "json": "id"},
    {"_amount": 1, 1: "_amount", "json": "amount"},
    {"_score_type_id_fk": 2, 2: "_score_type_id_fk", "json": "scoreType"},
    {"_score": 3, 3: "_score", "json": "score"},
    {"_display_name": 4, 4: "_display_name", "json": "name"}
]

MAP_TABLE_USER_ALLIANCES = [
   {"_alliance_id_fk": 0, 0: "_alliance_id_fk", "json": "allianceId"},
   {"_score_type_id_fk": 1, 1: "_score_type_id_fk", "json": "scoreType"},
   {"_score": 2, 2: "_score", "json": "score"},
   {"_display_name": 3, 3: "_display_name", "json": "name"}
]

MAP_SP_USER_SCORES = [
   {"_user_id_fk": 0, 0: "_user_id_fk", "json": "userId"},
   {"_user_code": 1, 1: "_user_code", "json": "inviteCode"},
   {"_alliances": 2, 2: "_alliances", "json": "alliances"},
   {"_score_type_id_fk": 3, 3: "_score_type_id_fk", "json": "scoreType"},
   {"_score": 4, 4: "_score", "json": "score"},
   {"_max": 5, 5: "_max", "json": "max"},
   {"_display_name": 6, 6: "_display_name", "json": "name"}
]

MAP_SP_USER_SCORES_SAME = [
   {"_user_id_fk": 0, 0: "_user_id_fk", "json": "id"},
   {"_user_code": 1, 1: "_user_code", "json": "inviteCode"},
   {"_score_type_id_fk": 2, 2: "_score_type_id_fk", "json": "scoreType"},
   {"_score": 3, 3: "_score", "json": "score"},
   {"_display_name": 4, 4: "_display_name", "json": "name"}
]

MAP_SP_USER_ALLIANCES_INVITES = [
   {"_user_id_fk": 0, 0: "_user_id_fk", "json": "id"},
   {"_score": 1, 1: "_score", "json": "score"},
   {"_score_type_id_fk": 2, 2: "_score_type_id_fk", "json": "scoreType"},
   {"_max": 3, 3: "_max", "json": "max"},
   {"_display_name": 4, 4: "_display_name", "json": "name"}
]