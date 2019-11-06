CREATE VIEW rz_dw_customer_transaction
AS
SELECT
	ord.ordernumber,
	ord.orderdate,
	ord.status,
	emp.employeenumber,
	emp.jobtitle,
	cust.customernumber,
	cust.creditlimit,
	prod.productcode,
	prod.productname,
	prod.productline,
	prod.productvendor,
	emp.officecode,
	cust.country,
	cust.state,
	cust.city,
	cust.phone
FROM
	orders ord
JOIN
	customers cust on ord.customernumber=cust.customernumber
JOIN
	employees emp on cust.salesrepemployeenumber=emp.employeenumber
JOIN
	orderdetails orddet on ord.ordernumber=orddet.ordernumber
JOIN
	products prod on orddet.productcode=prod.productcode;

---


SELECT
	*
FROM
	(SELECT
		orderdate,
		ordernumber,
		case when a.ordernumber=b.last_trans then 'Last Transaction' when a.ordernumber=b.first_trans then 'First Transaction' end as Transaction_Class,
		a.customernumber,
		productname,
		productline,
		productvendor,
		country,
		city
	FROM
		rz_dw_customer_transaction a
	JOIN
		(SELECT
			max(ordernumber) as last_trans,
			min(ordernumber) as first_trans,
			customernumber
		FROM
			rz_dw_customer_transaction
		GROUP BY
			customernumber) b
	ON
		a.customernumber=b.customernumber
	WHERE
		a.status in ('Shipped')) x
WHERE
	Transaction_Class is not null
ORDER BY
	customernumber ASC, orderdate ASC, ordernumber ASC;




