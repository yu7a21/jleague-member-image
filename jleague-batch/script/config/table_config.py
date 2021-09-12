table_struct_list = {
    "team":{
        "id":{
            "type" : "INT",
            "not_null" : True,
            "primary_key" : True,
            "auto_increment" : False
        },
        "name":{
            "type" : "VARCHAR(50)",
            "not_null" : True,
            "primary_key" : False,
            "auto_increment" : False
        },
        "short_name":{
            "type" : "VARCHAR(50)",
            "not_null" : True,
            "primary_key" : False,
            "auto_increment" : False
        },
        "league":{
            "type" : "VARCHAR(50)",
            "not_null" : True,
            "primary_key" : False,
            "auto_increment" : False
        }
    },
    "player":{
        "team_id":{
            "type" : "INT",
            "not_null" : True,
            "primary_key" : False,
            "auto_increment" : False
        },
        "name_ja":{
            "type" : "VARCHAR(100)",
            "not_null" : True,
            "primary_key" : False,
            "auto_increment" : False
        },
        "name_en":{
            "type" : "VARCHAR(100)",
            "not_null" : True,
            "primary_key" : False,
            "auto_increment" : False
        },
        "number":{
            "type" : "INT",
            "not_null" : False,
            "primary_key" : False,
            "auto_increment" : False
        },
        "id":{
            "type" : "INT",
            "not_null" : True,
            "primary_key" : True,
            "auto_increment" : True
        },
    }
}