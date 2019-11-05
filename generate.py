from faker import Faker
import csv
import random
import arrow

ACCOUNT_TYPE_INDIVIDUAL = 1
ACCOUNT_TYPE_ORGANISATION = 2
ACCOUNT_PRODUCT_MEMBERSHIP = 1
ACCOUNT_PRODUCT_CAREERS = 2
PAYMENT_TYPE_MONTHLY = 1
PAYMENT_TYPE_YEARLY = 2
TRANSACTION_STATE_SUCCESS = 'success'
TRANSACTION_STATE_FAILED = 'failed'
FAILURE_REASONS = ['card_expired', 'insufficient_funds', 'unknown_error']

n_accounts = 1000
p_accounts_individual = 0.65
n_accounts_individual = int(round(n_accounts * p_accounts_individual))
n_accounts_organisation = n_accounts - n_accounts_individual

price_membership_monthly = 3200
price_membership_yearly = 22000
price_careers_monthly = 11000
price_careers_yearly = 100000

p_membership = 0.75
p_careers = 0.15
p_yearly = 0.75
p_churn = 0.24
p_transaction_success = 0.9
n_days_dunning = 15

def write_to_csv(filename, rows):
  with open('./data/%s.csv' % filename, mode='w') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

    for r in rows:
      writer.writerow(r)

def get_transaction_amount(product_id, payment_period):
  if product_id == ACCOUNT_PRODUCT_MEMBERSHIP and payment_period == PAYMENT_TYPE_YEARLY:
    return price_membership_yearly
  elif product_id == ACCOUNT_PRODUCT_MEMBERSHIP and payment_period == PAYMENT_TYPE_MONTHLY:
    return price_membership_monthly
  elif product_id == ACCOUNT_PRODUCT_CAREERS and payment_period == PAYMENT_TYPE_MONTHLY:
    return price_careers_monthly
  elif product_id == ACCOUNT_PRODUCT_CAREERS and payment_period == PAYMENT_TYPE_YEARLY:
    return price_careers_yearly
  else:
    raise "Unknown combination :("

fake = Faker()

accounts_individual = [[i, fake.name(), ACCOUNT_TYPE_INDIVIDUAL] for i in range(1, n_accounts_individual + 1)]
accounts_organisation = [[i, fake.company(), ACCOUNT_TYPE_ORGANISATION] for i in range(n_accounts_individual + 1, n_accounts_individual + 1 + n_accounts_organisation)]
accounts = accounts_individual + accounts_organisation

account_product_idx = 0
account_products = []

for [account_id, _, account_type_id] in accounts:
  if account_type_id == ACCOUNT_TYPE_INDIVIDUAL:
    account_product_idx = account_product_idx + 1
    account_products.append([account_product_idx, account_id, ACCOUNT_PRODUCT_MEMBERSHIP])
  elif account_type_id == ACCOUNT_TYPE_ORGANISATION:
    has_membership = random.random() <= p_membership
    has_careers = random.random() <= p_careers

    # Make sure account has at least one product.
    if has_membership == False and has_careers == False:
      has_membership = True

    if has_membership:
      account_product_idx = account_product_idx + 1
      account_products.append([account_product_idx, account_id, ACCOUNT_PRODUCT_MEMBERSHIP])

    if has_careers:
      account_product_idx = account_product_idx + 1
      account_products.append([account_product_idx, account_id, ACCOUNT_PRODUCT_CAREERS])

  else:
    raise "Unknown account type :("

epoch_date = arrow.get('2017-01-01')
current_date = arrow.utcnow()

invoices = []
transactions = []
invoice_id = 0
transaction_id = 0
for [account_product_id, _, product_id] in account_products:
  payment_type = PAYMENT_TYPE_YEARLY if random.random() <= p_yearly else PAYMENT_TYPE_MONTHLY
  date = arrow.get(random.randint(epoch_date.timestamp, current_date.timestamp))
  amount = get_transaction_amount(product_id, payment_type)

  while True:
    if date > current_date:
      break

    invoice_id = invoice_id + 1
    is_churned = random.random() <= p_churn

    invoices.append([invoice_id, account_product_id, payment_type, "%d-%d-%d" % (date.year, date.month, date.day)])

    if is_churned:
      failure_reason = random.choice(FAILURE_REASONS)

      for _ in range(n_days_dunning):
        transaction_id = transaction_id + 1
        transactions.append([transaction_id, invoice_id, amount, TRANSACTION_STATE_FAILED, failure_reason, "%d-%d-%d" % (date.year, date.month, date.day)])
        date = date.shift(days=1)

      break
    else:
      # make a successful transaction (can mix with failed ones, but the last one must be success)
      while True:
        transaction_id = transaction_id + 1
        transaction_status = TRANSACTION_STATE_SUCCESS if random.random() <= p_transaction_success else TRANSACTION_STATE_FAILED
        failure_reason = None if transaction_status == TRANSACTION_STATE_SUCCESS else random.choice(FAILURE_REASONS)
        transactions.append([transaction_id, invoice_id, amount, transaction_status, failure_reason, "%d-%d-%d" % (date.year, date.month, date.day)])

        if transaction_status == TRANSACTION_STATE_SUCCESS:
          break
        else:
          date = date.shift(days=1)

    date = date.shift(years=1) if payment_type == PAYMENT_TYPE_YEARLY else date.shift(months=1)

# print transactions
# print invoices

#write_to_csv('account', accounts)
#write_to_csv('account_product', account_products)
write_to_csv('invoice', invoices)
write_to_csv('transaction', transactions)