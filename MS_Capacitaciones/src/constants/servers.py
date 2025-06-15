from os import getenv

SF_SERVER = {
                "USER": getenv("DB_USER"),
                "PWD": getenv("DB_PWD"),
                "SERVER": getenv("DB_SERVER"),
                "DB": getenv("DB_NAME"),
                "DRIVER": getenv("DB_DRIVER"),
            }