import requests
import base64

url_access = "https://openapi.seatalk.io/webhook/group/PlnZSbixS2OvsHKvcgefUg"

def send_message_custom(mensagem):
    fmessage = {"tag": "markdown",
                "markdown": {"content": f"__{mensagem}__", "at_all": False}}

    result = requests.post(url_access, json=fmessage)

    return result.status_code

def send_photo(path_file_image):

    with open(path_file_image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    fmessage = {"tag": "image",
                "image_base64": {"content": encoded_string}}
    
    result = requests.post(url_access, json= fmessage)

    return result.status_code
