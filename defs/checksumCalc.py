import binascii
import hashlib
from datetime import date
from pyamf import ASObject, amf3
import random


def getMarkingId() -> str:
    loc1 = str(random.randint(0, 999)) # Generowanie losowej liczby
    loc2 = hashlib.md5(loc1.encode()).hexdigest() # Hashowanie liczby przy pomocy MD5
    return f"{loc2}{loc1}" # Łączenie hash i liczby


def ticketHeader(anyAttribute: str = None, ticket: str = "") -> ASObject:
    loc1 = getMarkingId().encode() # Wywołanie getMarkingId i zakodowanie wyniku
    loc2 = hashlib.md5(loc1).hexdigest() # Hashowanie MD5
    loc3 = binascii.hexlify(loc1).decode() # Hexlify wynik
    loc4 = f"{ticket}{loc2}{loc3}" # Łączenie biletu z wygenerowanymi wartościami
    return ASObject({"anyAttribute": anyAttribute, "Ticket": loc4}) # Zwracanie obiektu ASObject


def create_checksum(params):
    def fromObjectInner(param1):
        if param1 is None: return ""
        if isinstance(param1, (int, str, bool)): return str(param1)
        if isinstance(param1, bytes):
            return binascii.hexlify(param1[:20] if len(param1) <= 20 else bytes(param1[i * len(param1) // 20] for i in range(20))).decode()
        if isinstance(param1, list): return ''.join(fromObjectInner(i) for i in param1)
        if isinstance(param1, dict): return ''.join(fromObjectInner(param1[k]) for k in sorted(param1) if k != 'Ticket')
        if isinstance(param1, date): return f"{param1.year}{param1.month - 1}{param1.day}"
        if isinstance(param1, amf3.ByteArray):
            return binascii.hexlify(param1.getvalue()[:20] if len(param1.getvalue()) <= 20 else bytes(param1.getvalue()[i * len(param1.getvalue()) // 20] for i in range(20))).decode()
        if isinstance(param1, ASObject): return ''.join(fromObjectInner(param1.get(k)) for k in sorted(param1) if k != 'Ticket')
        return ""


# Lambda do generowania biletu z param2
    ticket = lambda param2: next((loc1["Ticket"].split(',')[0] + loc1["Ticket"].split(',')[5][-5:] for loc1 in param2 if isinstance(loc1, ASObject) and "Ticket" in loc1), "XSV7%!5!AX2L8@vn")
    loc2 = ''.join(fromObjectInner(param1) for param1 in params) + "2zKzokBI4^26#oiP" + ticket(params)
    return hashlib.sha1(loc2.encode()).hexdigest()
