CREATE TABLE testday.Account (
    account_id bigint NOT NULL,
    account_title varchar(255) NOT NULL,
    account_type_id int NOT NULL
);

CREATE TABLE testday.AccountProduct (
    account_product_id bigint NOT NULL,
    account_id bigint NOT NULL,
    product_id bigint NOT NULL
);

CREATE TABLE testday.Product (
    product_id bigint NOT NULL,
    product_title varchar(255) NOT NULL
);

CREATE TABLE testday.PaymentPeriod (
    payment_period_id int NOT NULL,
    payment_period_title varchar(255) NOT NULL
);

CREATE TABLE testday.Invoice (
    invoice_id bigint NOT NULL,
    account_product_id bigint NOT NULL,
    payment_period_id int NOT NULL,
    created_datetime date NOT NULL
);

CREATE TABLE testday."Transaction" (
    transaction_id bigint NOT NULL,
    invoice_id bigint NOT NULL,
    transaction_amount_in_cents int NOT NULL,
    transaction_status varchar(50) NOT NULL,
    failure_reason varchar(50) NULL,
    created_datetime date NOT NULL
);