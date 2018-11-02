signup_schema = {
    "type": "object",
    "properties": {
        "username": {type: "string"},
        "email": {type: "string"},
        "password": {type: "string"},
        "role": {type: "string"}
    },
    "required": ["username", "email", "password", "role"]
}
login_schema = {
    "type": "object",
    "properties": {
        "username": {type: "string"},
        "password": {type: "string"}
    },
    "required": ["username", "password"]
}
login_schema = {
    "type": "object",
    "properties": {
        "username": {type: "string"},
        "password": {type: "string"}
    },
    "required": ["username", "password"]
}
product_schema = {
    "type": "object",
    "properties": {
        "name": {type: "string"},
        "category": {type: "string"},
        "price": {type: "string"},
        "quantity": {type: "string"},
        "lower_inventory": {type: "string"},


    },
    "required": ["name", "category", "price", "quantity", "lower_inventory"]
}

sale_schema = {
"type": "object",
"properties": {
    "id": {type: "string"},
    "user_id": {type: "string"},
    "quantity": {type: "string"},



},
"required": ["id", "user_id", "price", "quantity"]
}
