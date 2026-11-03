TORTOISE_ORM = {
    "connections":{
        "default":{
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "localhost",
                "port": 3306,
                "database": "stu_sys",
                "user": "root",
                "password": "elaina123456",
                "minsize": 1,
                "maxsize": 10,
                "charset": "utf8mb4",
                "echo": True
            }
        },
    },
    "apps":{
        "models":{
            "models":["models"],
            "default_connection": "default"
        }

    },
    "use_tz": True,
    "timezone": "Asia/Shanghai"
    
}