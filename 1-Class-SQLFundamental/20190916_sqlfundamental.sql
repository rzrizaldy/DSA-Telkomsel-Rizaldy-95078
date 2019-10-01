select
sum(transaction_amount)
from
tsel_trx_sample_train
where
transaction_type in ('TOPUP');


 	_c0
1	1100912009


select
sum(transaction_amount)
from
tsel_trx_sample_train
where
transaction_type in ('TOPUP')
and
date_partition in ('20190820');

SELECT
	sum(a.transaction_amount)
from
	tsel_trx_sample_train
where
	(transaction_amount > 5000 and transaction_type='VOiCE')
	OR
	(transaction_amount=10000 and transaction_type='DATA')) a;


select
	city_name,
	transaction_type
	sum(transaction_amount)
	