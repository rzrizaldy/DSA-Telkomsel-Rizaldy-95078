Berdasarkan ERD tersebut, tuliskan query yang akan menghasilkan daftar karyawan yang berasal dari kota di kantor ‘Boston’ dengan menampilkan Nama (firstname) karyawan, kota, negara bagian dan negara.



SELECT
	a.firstName,
	b.city,
	b.state,
	b.country
FROM
	employees a
JOIN
	offices b
ON
	a.officeCode=b.officeCode
WHERE
	b.city in ('Boston');


Berdasarkan ERD tersebut, tampilkan jumlah customer di setiap kantor dengan menampilkan office Code, city, state, country, jumlah customer.

SELECT
	c.officeCode,
	c.city,
	c.state,
	c.country,
	count(distinct a.customerNumber) as count_customer
FROM
	customers a
JOIN
	employees b
ON
	a.salesrepemployeenumber=b.employeenumber
JOIN
	offices c
ON
	b.officeCode=c.officeCode
GROUP BY
	c.officeCode,
	c.city,
	c.state,
	c.country;
