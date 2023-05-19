# #!/usr/bin/env python
import datetime
import json
from visa_API import VisaAPI

api = VisaAPI()


def demo_get_helloWorld():
  print("Hello World API")
  api.send_hello_world()
  print()


demo_get_helloWorld()


def demo_post_request_CardOnFile():
  cardOnFile_body_request = json.loads('''{
  "requestHeader": {
  "requestMessageId": "6da6b8b024532a2e0eacb1af58581",
  "messageDateTime": "2019-02-35 05:25:12.327"
  },
  "requestData": {
  "pANs": [
  4072208010000000
  ],
  "group": "STANDARD"
  }
  }''')

  print("Card On File API")
  cardOnFile_response = api.send_post_request_CardOnFile(cardOnFile_body_request)
  print(cardOnFile_response, '\n')


demo_post_request_CardOnFile()


def demo_post_VisaDirect_pushfunds():
  date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
  push_funds_request = json.loads('''{
    "amount": "124.05",
    "senderAddress": "901 Metro Center Blvd",
    "localTransactionDateTime": "''' + date + '''",
    "pointOfServiceData": {
      "panEntryMode": "90",
      "posConditionCode": "00",
      "motoECIIndicator": "0"
    },
    "recipientPrimaryAccountNumber": "4060320000000127",
    "colombiaNationalServiceData": {
      "addValueTaxReturn": "10.00",
      "taxAmountConsumption": "10.00",
      "nationalNetReimbursementFeeBaseAmount": "20.00",
      "addValueTaxAmount": "10.00",
      "nationalNetMiscAmount": "10.00",
      "countryCodeNationalService": "170",
      "nationalChargebackReason": "11",
      "emvTransactionIndicator": "1",
      "nationalNetMiscAmountType": "A",
      "costTransactionIndicator": "0",
      "nationalReimbursementFee": "20.00"
    },
    "cardAcceptor": {
      "address": {
        "country": "USA",
        "zipCode": "94404",
        "county": "San Mateo",
        "state": "CA"
      },
      "idCode": "CA-IDCode-77765",
      "name": "Visa Inc. USA-Foster City",
      "terminalId": "TID-9999"
    },
    "senderReference": "",
    "transactionIdentifier": "883916196354773",
    "acquirerCountryCode": "840",
    "acquiringBin": "408999",
    "retrievalReferenceNumber": "412770452025",
    "senderCity": "Foster City",
    "senderStateCode": "CA",
    "systemsTraceAuditNumber": "451018",
    "senderName": "Mohammed Qasim",
    "businessApplicationId": "AA",
    "settlementServiceIndicator": "9",
    "merchantCategoryCode": "6012",
    "transactionCurrencyCode": "USD",
    "recipientName": "rohan",
    "senderCountryCode": "124",
    "sourceOfFundsCode": "05",
    "senderAccountNumber": "4060320000000126"
  }''')
  print("pushfundstransactions Visa Direct API")
  a = api.send_post_VisaDirect_pushfunds(push_funds_request)
  print(a)


demo_post_VisaDirect_pushfunds()
