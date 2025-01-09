import base64
from secrets import token_hex
from curl_cffi import requests
from pyamf import remoting, AMF3
from defs.checksumCalc import create_checksum

# Funkcja wysylajaca request do AMF-MSP-api oraz odbierajaca response.
def AmfCall(server: str, method: str, params: list) -> tuple[int, any]:
    server = server.upper() # .upper zapewnia, ze kod serwera jest WIELKIMI literami.

    req = remoting.Request(target=method, body=params)
    event = remoting.Envelope(AMF3)
    event.headers = remoting.HeaderCollection({
        ("sessionID", False, base64.b64encode(token_hex(23).encode()).decode()),
        ("needClassName", False, False),
        ("id", False, create_checksum(params))
    })
    event['/1'] = req
    encoded_req = remoting.encode(event).getvalue()
    full_endpoint = f"https://ws-{server}.mspapis.com/Gateway.aspx?method={method}"

    headerspost = {
        'Content-Type': 'application/x-amf',
        'User-Agent': 'Mozilla/5.0 (Android; U; en-GB) AppleWebKit/533.19.4 (KHTML, like Gecko) AdobeAIR/50.2',
        'x-flash-version': '50,2,3,4',
        'Connection': 'Keep-Alive',
        'Referer': 'app:/MSPMobile.swf',
    }

    post_resp = requests.post(full_endpoint, headers=headerspost, data=encoded_req, verify=False)
    post_resp_content = post_resp.content if post_resp.status_code == 200 else None

    if post_resp.status_code != 200:
        return (post_resp.status_code, post_resp_content)
    return (post_resp.status_code, remoting.decode(post_resp_content)["/1"].body)