team = {
    "table_name" : "team",
    "columns" : {
        "id":{
            "type" : "INT",
            "not_null" : True,
            "primary_key" : True
        },
        "name":{
            "type" : "VARCHAR(50)",
            "not_null" : True,
            "primary_key" : False
        },
        "short_name":{
            "type" : "VARCHAR(50)",
            "not_null" : True,
            "primary_key" : False
        },
        "league":{
            "type" : "VARCHAR(50)",
            "not_null" : True,
            "primary_key" : False
        }
    }
}