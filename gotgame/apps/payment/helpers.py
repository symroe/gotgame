import requests
import json
import paypalrestsdk

from django.conf import settings

"""
FAKE CREDIT CARD

Card type: VISA
Expiry date (all cards) 05/2015
CVV code (all cards): 000
Number: 4519527907782047


**** REST API ****

**Payment from mobile**

{
    client =     {
        environment = sandbox;
        "paypal_sdk_version" = "1.1.1";
        platform = iOS;
        "product_name" = "PayPal iOS SDK";
    };
    payment =     {
        amount = "9.95";
        "currency_code" = USD;
        "short_description" = "Hipster t-shirt";
    };
    "proof_of_payment" =     {
        "rest_api" =         {
            "payment_id" = "PAY-12A00780VW8313039KIHAGSI";
            state = approved;
        };
    };
}

**Payment from Paypal**
{
    u'update_time': u'2013-08-16T10: 47: 40Z',
    u'links': [
        {
            u'href': u'https: //api.sandbox.paypal.com/v1/payments/payment/PAY-12A00780VW8313039KIHAGSI',
            u'method': u'GET',
            u'rel': u'self'
        }
    ],
    u'payer': {
        u'payment_method': u'credit_card',
        u'funding_instruments': [
            {
                u'credit_card': {
                    u'expire_year': u'2015',
                    u'type': u'visa',
                    u'number': u'xxxxxxxxxxxx2047',
                    u'expire_month': u'3'
                }
            }
        ]
    },
    u'transactions': [
        {
            u'related_resources': [
                {
                    u'sale': {
                        u'update_time': u'2013-08-16T10: 47: 40Z',
                        u'links': [
                            {
                                u'href': u'https: //api.sandbox.paypal.com/v1/payments/sale/2MB69609C8700661H',
                                u'method': u'GET',
                                u'rel': u'self'
                            },
                            {
                                u'href': u'https: //api.sandbox.paypal.com/v1/payments/sale/2MB69609C8700661H/refund',
                                u'method': u'POST',
                                u'rel': u'refund'
                            },
                            {
                                u'href': u'https: //api.sandbox.paypal.com/v1/payments/payment/PAY-12A00780VW8313039KIHAGSI',
                                u'method': u'GET',
                                u'rel': u'parent_payment'
                            }
                        ],
                        u'state': u'completed',
                        u'parent_payment': u'PAY-12A00780VW8313039KIHAGSI',
                        u'amount': {
                            u'currency': u'USD',
                            u'total': u'9.95'
                        },
                        u'create_time': u'2013-08-16T10: 47: 37Z',
                        u'id': u'2MB69609C8700661H'
                    }
                }
            ],
            u'amount': {
                u'currency': u'USD',
                u'total': u'9.95',
                u'details': {
                    u'subtotal': u'9.95'
                }
            },
            u'description': u'Hipstert-shirt'
        }
    ],
    u'state': u'approved',
    u'create_time': u'2013-08-16T10: 47: 37Z',
    u'intent': u'sale',
    u'id': u'PAY-12A00780VW8313039KIHAGSI'
}


****  Adaptive Payments ****

**Payment from mobile**
{
    client =     {
        environment = sandbox;
        "paypal_sdk_version" = "1.1.1";
        platform = iOS;
        "product_name" = "PayPal iOS SDK";
    };
    payment =     {
        amount = "10.95";
        "currency_code" = USD;
        "short_description" = "Hipster t-shirt2";
    };
    "proof_of_payment" =     {
        "adaptive_payment" =         {
            "app_id" = "APP-80W284485P519543T";
            "pay_key" = "AP-75V16544CK059223C";
            "payment_exec_status" = COMPLETED;
            timestamp = "2013-08-16T05:48:10.687-07:00";
        };
    };
}

**Payment from Paypal**
{
    "responseEnvelope": {
        "timestamp": "2013-08-16T06:13:46.217-07:00",
        "ack": "Success",
        "correlationId": "5daf8d1042497",
        "build": "6941298"
    },
    "cancelUrl": "http://www.paypal.com",
    "currencyCode": "USD",
    "paymentInfoList": {
        "paymentInfo": [
            {
                "transactionId": "5UX72565MG371651T",
                "transactionStatus": "COMPLETED",
                "receiver": {
                    "amount": "10.95",
                    "email": "uber.ubiwankenobi-facilitator@gmail.com",
                    "primary": "false",
                    "paymentType": "SERVICE",
                    "accountId": "P8BGSQ8BXMLAQ"
                },
                "refundedAmount": "0.00",
                "pendingRefund": "false",
                "senderTransactionId": "23V45572XB264741W",
                "senderTransactionStatus": "COMPLETED"
            }
        ]
    },
    "returnUrl": "http://www.paypal.com",
    "status": "COMPLETED",
    "payKey": "AP-75V16544CK059223C",
    "actionType": "PAY",
    "feesPayer": "EACHRECEIVER",
    "sender": {
        "accountId": "Z44SEHS9SC294",
        "useCredentials": "true"
    }
}

"""

class PaypalHelper(object):
    def __init__(self):
        self.rest_api_helper = PaypalRestAPIHelper()
        self.adaptive_helper = PaypalAdaptivePaymentHelper()

    def verify_payment(self, mobile_payment):
        proof = mobile_payment['proof_of_payment']

        if 'adaptive_payment' in proof:
            self.adaptive_helper.verify_payment(proof)
        elif 'rest_api' in proof:
            self.rest_api_helper.verify_payment(proof)
        else:
            raise Exception('Cannot verify payment, proof_of_payment not supported')


class PaypalRestAPIHelper(object):
    def __init__(self):
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })

    def get_payment(self, payment_id):
        return paypalrestsdk.Payment.find(payment_id)

    def verify_payment(self, proof):
        payment = self.get_payment(proof['payment_id'])

        if payment['state'] != 'approved':
            raise Exception("The payment hasn't been approved")

        # TODO... https://developer.paypal.com/webapps/developer/docs/integration/mobile/verify-mobile-payment/


class PaypalAdaptivePaymentHelper(object):
    def __init__(self):
        self.user_id = settings.PAYPAL_EMAIL
        self.password = settings.PAYPAL_PASSWORD
        self.signature = settings.PAYPAL_SIGNATURE

        assert settings.PAYPAL_MODE in ['sandbox', 'live']
        if settings.PAYPAL_MODE == 'sandbox':
            self.base_url = 'https://svcs.sandbox.paypal.com/'
        else:
            self.base_url = 'https://svcs.paypal.com/'

    def _request(self, url, method, *args, **kwargs):
        url = '%s%s' % (self.base_url, url)

        # headers
        headers = kwargs.get('headers', {})
        headers.update({
            'X-PAYPAL-SECURITY-USERID': self.user_id,
            'X-PAYPAL-SECURITY-PASSWORD': self.password,
            'X-PAYPAL-SECURITY-SIGNATURE': self.signature,
            'X-PAYPAL-REQUEST-DATA-FORMAT': 'JSON',
            'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON',
        })
        return getattr(requests, method)(url, *args, **kwargs)

    def get_payment(self, app_id, pay_key):
        headers = {
            'X-PAYPAL-APPLICATION-ID': app_id
        }

        data = json.dumps({
            "payKey": pay_key,
            "requestEnvelope": "en_US"
        })
        return self._request(
            'AdaptivePayments/PaymentDetails', 'post', headers=headers, data=data
        ).json()

    def verify_payment(self, proof):
        app_id = proof['app_id']
        pay_key = proof['pay_key']

        payment = self.get_payment(app_id, pay_key)

        if payment['state'] != 'COMPLETED':
            raise Exception("The payment hasn't been completed")

        # TODO... https://developer.paypal.com/webapps/developer/docs/integration/mobile/verify-mobile-payment/
