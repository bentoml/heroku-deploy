OPERATOR_NAME = "heroku"

OPERATOR_MODULE = "heroku_deploy"

OPERATOR_SCHEMA = {
    "dyno_counts": {
        "type": "integer",
        "required": True,
        "coerce": int,
        "default": 1
    },
    "dyno_type": {
        "type": "string",
        "allowed": [
            "free",
            "hobby",
            "standard-1x",
            "standard-2x",
            "performance-m",
            "performance-l"
        ],
        "required": True,
        "default": "free",
        },
    }
