1. Sales and Product division want to know 1 what is the most revenue product.


select 
    productname,
    sum(priceeach*quantityordered) rev 
from 
(
    select * from products
)pd 
inner join 
(
    select * from orderdetails
)od on pd.productcode=od.productcode
inner join 
(
    select * from orders where lower(status)='shipped'    
)os on od.ordernumber=os.ordernumber
group by productname
order by rev desc;



2. Finance division want to know GMV (Gross Merchant
Values), Number of Transactions, Unique Users, Average
Order Value and revenue in daily, weekly and Monthly from
each office.


select  date_format(paymentdate, 'yyyyMM') as month,
        date_format(date_sub(paymentdate,5),'Yww') as week,
        date_format(paymentdate,'yyyyMMdd') as day
from payments

3. Head of Sales want to know performance of the employee.


SELECT
	firstname,
	lastname,
	sum(amount) as revenue
FROM 
	employees x
JOIN
	(select
		a.salesrepemployeenumber,
		a.customernumber,
		cast(sum(b.amount) as int) as amount
	FROM
		customers a
	JOIN
		payments b
	ON
		a.customernumber=b.customernumber
	GROUP BY
		a.salesrepemployeenumber,
		a.customernumber) y
ON
	x.employeenumber=y.salesrepemployeenumber
GROUP BY
	firstname,
	lastname;

4. Office Perform


5. Finance Division want to know quarterly data about sales, quantityordered, cusstomers, avg revenue from customers from each office

SELECT
	date,
	countcustomer,
	avgrevenue,
	revenue,
	quantityordered
FROM
	(SELECT
		paymentdate as date,
		count(distinct customernumber) as countcustomer,
		avg(customeramount) as avgrevenue
	FROM
		(SELECT
			y.paymentdate,
			x.customernumber,
			sum(y.amount) as customeramount
		FROM
			customers x
		JOIN
			payments y
		ON
			x.customernumber=y.customernumber
		GROUP BY
			y.paymentdate,
			x.customernumber) x
	GROUP BY
		paymentdate) aa
JOIN
	(SELECT
		shippeddate as date ,
		SUM(revenue) as revenue,
		SUM(quantityordered) as quantityordered
	FROM
		(SELECT
			ordernumber,
			SUM(quantityordered*priceeach) as revenue,
			SUM(quantityordered) as quantityordered
		FROM
			orderdetails
		GROUP BY
			ordernumber) x
	JOIN
		orders y
	ON
		x.ordernumber=y.ordernumber) bb
ON
	aa.date=bb.date;



SELECT ofc.officecode, ofc.city, ofc.state, ofc.country, thn, quarterly, 
format_number(quantity,0) as quantity, 
format_number(uniq_customer,0) as customer, 
format_number((revenue/uniq_customer),2) as avgrevenue
FROM offices ofc 
JOIN
(
    SELECT YEAR(orderdate) AS thn, CONCAT('QUARTER ',(INT((MONTH(orderdate)-1)/3)+1),' ',YEAR(od.orderdate)) as Quarterly, emp.officecode,  
    SUM(ord.priceeach*ord.quantityordered) AS revenue, 
    SUM(ord.quantityordered) AS quantity, 
    COUNT(DISTINCT cst.customernumber) AS uniq_customer 
    FROM employees emp 
    JOIN customers cst 
    ON emp.employeenumber=cst.salesrepemployeenumber 
    JOIN orders od 
    ON cst.customernumber=od.customernumber 
    JOIN orderdetails ord 
    ON od.ordernumber=ord.ordernumber 
    GROUP BY YEAR(orderdate), CONCAT('QUARTER ',(INT((MONTH(orderdate)-1)/3)+1),' ',YEAR(od.orderdate)), emp.officecode
) b
ON ofc.officecode=b.officecode 
ORDER by ofc.officecode ASC, thn ASC, quarterly ASC ;


DATEDIFF()



6. how long on average it takes from order to ship the car 

SELECT
	p.productname,
	AVG(DATEDIFF(o.shippeddate, o.orderdate)) as duration_shipped,
	AVG(DATEDIFF(o.requireddate, o.orderdate)) as duration_req
FROM
	orders o
JOIN
	orderdetails od
ON
	o.ordersnumber=od.ordersnumber
JOIN
	products p
ON o.productcode=p.productcode
GROUP BY
	p.productname;




















