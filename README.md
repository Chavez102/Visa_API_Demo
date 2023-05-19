# Visa_API_Demo
Quick Guide to Start Utilizing Visa API 


## API
* https://developer.visa.com/capabilities/card-on-file-data-inquiry/reference#tag/Card-On-File-Data-Service-API/operation/Card-On-File%20Data%20Service_v1%20-%20Latest

## Prerequisites

##### VISA Developer Center Account, Project
* #####  userID, password, VDP_certificate.pem, VDP_private_key.pem
* ##### MLE: keyID, server_encryption_cert.pem, encryption_csr.pem

##### requests
* ##### from jwcrypto import jwe, jwk
* ##### configparser

## Usage

Card-On-File Data API allows to enable digital control capabilities in Issuer’s online mobile application or web application to provide visibility to the consumers where their card (PAN)/token credentials are stored to initiate Card-On-File Data API/e-commerce transactions and where the credentials are updated in case of a card reissuance or token status updates


