class Encryptor:
    @staticmethod
    def encrypt(msg, key):
        return ''.join([chr(ord(sym) + key) for sym in msg])

    @staticmethod
    def decrypt(msg, key):
        return ''.join([chr(ord(sym) - key) for sym in msg])
