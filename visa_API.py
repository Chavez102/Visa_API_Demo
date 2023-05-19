import json
import random
import string
import time
import requests
from jwcrypto import jwe, jwk
import configparser

try:
  import http.client as http_client
except ImportError:
  # Python 2
  import http.client as http_client
http_client.HTTPSConnection.debuglevel = 0


def _get_correlation_id():
  size = 12
  chars = string.digits
  correlationId = ''.join(random.choice(chars) for _ in range(size)) + '_SC'
  return correlationId


def encrypt_jwe(payload, mle_encryption_keyId, encryption_key):
  protected_header = {
    "alg": "RSA-OAEP-256",
    "enc": "A128GCM",
    "typ": "JWE",
    "kid": mle_encryption_keyId,
    "iat": int(round(time.time() * 1000))
  }

  jwe_token = jwe.JWE(json.dumps(payload).encode('utf-8'), recipient=encryption_key, protected=protected_header)
  return {"encData": jwe_token.serialize(compact=True)}


def decrypt_jwe_token(encrypted_payload, decryption_key):
  jwe_token = jwe.JWE()
  jwe_token.deserialize(encrypted_payload, decryption_key)
  return jwe_token.payload


def import_key(pem_file_location):
  with open(pem_file_location, "rb") as pemfile:
    key = jwk.JWK.from_pem(pemfile.read())
  return key


class VisaAPI:

  def __init__(self):

    config = configparser.ConfigParser()
    config.read('configuration.ini')

    # Project Credentials
    self.user_id = config.get('VDP', 'userId')
    self.password = config.get('VDP', 'password')
    self.VDP_cert_path = config.get('VDP', 'cert')
    self.VDP_key_path = config.get('VDP', 'key')

    # Message Level Encryption
    self.mle_encryption_keyId = config.get('MLE', 'keyId')
    self.encryption_key_path = config.get('MLE', 'serverCertificatePath')
    self.decryption_key_path = config.get('MLE', 'privateKeyPath')

    self.input_headers = {'content-type': 'application/json',
                          'accept': 'application/json',
                          'keyId': self.mle_encryption_keyId,
                          'x-correlation-id': _get_correlation_id(),
                          }

  def perform_mutual_auth_request_post(self, body, url):

    try:
      response = requests.post(url,
                               # verify = ('put the CA certificate pem file path here'),
                               cert=(self.VDP_cert_path, self.VDP_key_path),
                               headers=self.input_headers,
                               auth=(self.user_id, self.password),
                               json=body

                               )
      # print(response.content)
      return response
    except Exception as e:
      print("error!!!")
      print(e)

  def send_post_request_CardOnFile(self, request_body):
    encryptor = import_key(self.encryption_key_path)
    encrypted_request_body = encrypt_jwe(request_body, self.mle_encryption_keyId, encryptor)

    response = self.perform_mutual_auth_request_post(encrypted_request_body,
                                                     "https://sandbox.api.visa.com/cofds-web/v1/datainfo")
    print("Response Status:", response.status_code)
    encrypted_content = json.loads(response.content)['encData']

    decryptor = import_key(self.decryption_key_path)
    decrypted_content = decrypt_jwe_token(encrypted_content, decryptor)

    return json.loads(decrypted_content)

  def send_post_VisaDirect_pushfunds(self, request_body):
    encryptor = import_key(self.encryption_key_path)
    encrypted_request_body = encrypt_jwe(request_body, self.mle_encryption_keyId, encryptor)

    response = self.perform_mutual_auth_request_post(encrypted_request_body,
                                                     "https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pushfundstransactions")
    print("Response Status:", response.status_code)
    encrypted_content = json.loads(response.content)['encData']

    decryptor = import_key(self.decryption_key_path)
    decrypted_content = decrypt_jwe_token(encrypted_content, decryptor)

    return json.loads(decrypted_content)

  def send_hello_world(self):
    url = 'https://sandbox.api.visa.com/vdp/helloworld'
    response = requests.get(url,
                            # verify = ('put the CA certificate pem file path here'),
                            cert=(self.VDP_cert_path, self.VDP_key_path),
                            # headers = headers,
                            auth=(self.user_id, self.password),
                            # data = body,
                            # json = payload,
                            timeout=10
                            # if DEBUG: print (response.text)
                            )
    print("Response Status:", response.status_code)
    print(response.content)
    return response
