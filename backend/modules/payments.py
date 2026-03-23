import stripe
import paypalrestsdk
import requests
import json
from pathlib import Path

class PaymentGateway:
    def __init__(self, config):
        self.config = config
        if config.get('STRIPE_SECRET_KEY'):
            stripe.api_key = config['STRIPE_SECRET_KEY']
        if config.get('PAYPAL_CLIENT_ID'):
            paypalrestsdk.configure({
                'mode': 'sandbox' if config.get('PAYPAL_MODE') != 'live' else 'live',
                'client_id': config['PAYPAL_CLIENT_ID'],
                'client_secret': config['PAYPAL_SECRET']
            })

    def stripe_payment(self, amount_cents, currency='zar', description='Stormy Subscription'):
        try:
            charge = stripe.Charge.create(
                amount=amount_cents,
                currency=currency,
                source='tok_visa',  # In production, use token from frontend
                description=description
            )
            return {'success': True, 'id': charge.id}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def paypal_payment(self, amount, currency='ZAR', return_url='https://stormy.com/success', cancel_url='https://stormy.com/cancel'):
        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {'payment_method': 'paypal'},
            'transactions': [{
                'amount': {'total': str(amount), 'currency': currency},
                'description': 'Stormy Subscription'
            }],
            'redirect_urls': {'return_url': return_url, 'cancel_url': cancel_url}
        })
        if payment.create():
            for link in payment.links:
                if link.rel == 'approval_url':
                    return {'success': True, 'approval_url': link.href, 'payment_id': payment.id}
        return {'success': False, 'error': payment.error}

    def payfast_payment(self, amount, item_name='Stormy Subscription'):
        # PayFast sandbox/live integration
        data = {
            'merchant_id': self.config.get('PAYFAST_MERCHANT_ID'),
            'merchant_key': self.config.get('PAYFAST_MERCHANT_KEY'),
            'return_url': 'https://stormy.com/success',
            'cancel_url': 'https://stormy.com/cancel',
            'notify_url': 'https://stormy.com/api/payments/payfast-webhook',
            'amount': amount,
            'item_name': item_name,
            'email_confirmation': '1'
        }
        # Generate signature
        import hashlib
        pf_string = '&'.join([f'{k}={v}' for k, v in sorted(data.items()) if v])
        if self.config.get('PAYFAST_PASSPHRASE'):
            pf_string += f"&passphrase={self.config['PAYFAST_PASSPHRASE']}"
        data['signature'] = hashlib.md5(pf_string.encode()).hexdigest()
        # Return URL and data to POST
        base_url = 'https://sandbox.payfast.co.za/eng/process' if self.config.get('PAYFAST_MODE') != 'live' else 'https://www.payfast.co.za/eng/process'
        return {'success': True, 'url': base_url, 'data': data}

    def direct_eft(self, amount, account_type='fnb'):
        # Return bank details for manual EFT
        if account_type == 'fnb':
            details = {
                'bank': 'FNB',
                'account_name': self.config.get('FNB_ACCOUNT_NAME'),
                'account_number': self.config.get('FNB_ACCOUNT_NUMBER'),
                'branch_code': self.config.get('FNB_BRANCH_CODE'),
                'reference': f'STORMY-{amount}-{int(time.time())}'
            }
        else:
            details = {
                'bank': 'African Bank',
                'account_name': self.config.get('AFRICAN_BANK_ACCOUNT_NAME'),
                'account_number': self.config.get('AFRICAN_BANK_ACCOUNT_NUMBER'),
                'branch_code': self.config.get('AFRICAN_BANK_BRANCH_CODE'),
                'reference': f'STORMY-{amount}-{int(time.time())}'
            }
        return {'success': True, 'method': 'direct_eft', 'details': details}
