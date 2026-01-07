CREATE DATABASE price_tracker;
USE price_tracker;

CREATE TABLE platforms (
    platform_id INT PRIMARY KEY,
    platform_name VARCHAR(50) NOT NULL
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    brand VARCHAR(50)
);
CREATE TABLE price_history (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    platform_id INT,
    mrp DECIMAL(10,2),
    selling_price DECIMAL(10,2),
    discount_percent DECIMAL(5,2),
    price_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (platform_id) REFERENCES platforms(platform_id)
);
INSERT INTO platforms VALUES
(1, 'Amazon'),
(2, 'Flipkart'),
(3, 'Myntra');
SELECT * FROM platforms;
INSERT INTO products VALUES
(1,'Boat Rockerz 450 Headphones','Electronics','Boat'),
(2,'JBL Tune 510BT Headphones','Electronics','JBL'),
(3,'Sony WH-1000XM4 Headphones','Electronics','Sony'),
(4,'Apple AirPods 2','Electronics','Apple'),
(5,'Samsung Galaxy Buds','Electronics','Samsung'),
(6,'Nike Revolution Shoes','Footwear','Nike'),
(7,'Adidas Ultraboost Shoes','Footwear','Adidas'),
(8,'Puma Smash V2 Shoes','Footwear','Puma'),
(9,'Reebok Running Shoes','Footwear','Reebok'),
(10,'Skechers Go Walk','Footwear','Skechers'),
(11,'Amazon Echo Dot','Electronics','Amazon'),
(12,'Fire TV Stick','Electronics','Amazon'),
(13,'Mi Smart Band 6','Electronics','Xiaomi'),
(14,'Samsung Galaxy M14','Electronics','Samsung'),
(15,'Realme Narzo 60','Electronics','Realme'),
(16,'HP Wireless Mouse','Accessories','HP'),
(17,'Logitech Keyboard','Accessories','Logitech'),
(18,'Dell Laptop Backpack','Accessories','Dell'),
(19,'Canon EOS 1500D','Electronics','Canon'),
(20,'Nikon D3500','Electronics','Nikon'),
(21,'Lenovo IdeaPad Slim 3','Computers','Lenovo'),
(22,'Asus VivoBook 15','Computers','Asus'),
(23,'Acer Aspire 5','Computers','Acer'),
(24,'HP Pavilion 14','Computers','HP'),
(25,'Apple MacBook Air M1','Computers','Apple'),
(26,'OnePlus Nord CE 3','Electronics','OnePlus'),
(27,'Samsung Galaxy S21 FE','Electronics','Samsung'),
(28,'iQOO Z7','Electronics','iQOO'),
(29,'Sony Bravia 43 TV','Electronics','Sony'),
(30,'LG Washing Machine','Home Appliances','LG');

SELECT COUNT(*) FROM products;

INSERT INTO price_history
(product_id, platform_id, mrp, selling_price, discount_percent, price_date)
SELECT
    p.product_id,
    pl.platform_id,
    ROUND(2000 + p.product_id * 300, 2) AS mrp,
    ROUND(
        (2000 + p.product_id * 300) *
        (1 - CASE pl.platform_id
            WHEN 1 THEN 0.10
            WHEN 2 THEN 0.15
            WHEN 3 THEN 0.08
        END),
        2
    ) AS selling_price,
    CASE pl.platform_id
        WHEN 1 THEN 10.00
        WHEN 2 THEN 15.00
        WHEN 3 THEN 8.00
    END AS discount_percent,
    d.price_date
FROM products p
CROSS JOIN platforms pl
CROSS JOIN (
    SELECT DATE('2025-01-01') AS price_date
    UNION ALL SELECT DATE('2025-01-05')
    UNION ALL SELECT DATE('2025-01-10')
    UNION ALL SELECT DATE('2025-01-15')
    UNION ALL SELECT DATE('2025-01-20')
) d;
SELECT COUNT(*) FROM price_history;
SELECT COUNT(DISTINCT product_id) FROM price_history;
DELETE FROM price_history;
INSERT INTO price_history
(product_id, platform_id, mrp, selling_price, discount_percent, price_date)
SELECT
    p.product_id,
    pl.platform_id,

    -- base MRP
    ROUND(2000 + p.product_id * 300, 2) AS mrp,

    -- selling price with date fluctuation
    ROUND(
        (2000 + p.product_id * 300) *
        (1 - CASE pl.platform_id
            WHEN 1 THEN 0.10
            WHEN 2 THEN 0.15
            WHEN 3 THEN 0.08
        END)
        *
        (1 + (
            CASE d.price_date
                WHEN '2025-01-01' THEN -0.03
                WHEN '2025-01-05' THEN -0.06
                WHEN '2025-01-10' THEN  0.02
                WHEN '2025-01-15' THEN  0.05
                WHEN '2025-01-20' THEN  0.01
            END
        )),
        2
    ) AS selling_price,

    -- discount %
    CASE pl.platform_id
        WHEN 1 THEN 10.00
        WHEN 2 THEN 15.00
        WHEN 3 THEN 8.00
    END AS discount_percent,

    d.price_date
FROM products p
CROSS JOIN platforms pl
CROSS JOIN (
    SELECT DATE('2025-01-01') AS price_date
    UNION ALL SELECT DATE('2025-01-05')
    UNION ALL SELECT DATE('2025-01-10')
    UNION ALL SELECT DATE('2025-01-15')
    UNION ALL SELECT DATE('2025-01-20')
) d;
DELETE FROM price_history;
SET SQL_SAFE_UPDATES = 0;
DELETE FROM price_history;
INSERT INTO price_history
(product_id, platform_id, mrp, selling_price, discount_percent, price_date)
SELECT
    p.product_id,
    pl.platform_id,

    -- base MRP varies by product
    ROUND(3000 + p.product_id * 400 + (RAND(p.product_id) * 500), 2) AS mrp,

    -- selling price with product + date randomness
    ROUND(
        (
            3000
            + p.product_id * 400
            + (RAND(p.product_id) * 500)
        )
        * (1 - CASE pl.platform_id
            WHEN 1 THEN 0.08 + (RAND(pl.platform_id) * 0.05)
            WHEN 2 THEN 0.12 + (RAND(pl.platform_id) * 0.06)
            WHEN 3 THEN 0.06 + (RAND(pl.platform_id) * 0.04)
        END)
        * (1 + (
            CASE d.price_date
                WHEN '2025-01-01' THEN (RAND(p.product_id + 1) * 0.06 - 0.03)
                WHEN '2025-01-05' THEN (RAND(p.product_id + 2) * 0.08 - 0.04)
                WHEN '2025-01-10' THEN (RAND(p.product_id + 3) * 0.10 - 0.05)
                WHEN '2025-01-15' THEN (RAND(p.product_id + 4) * 0.07 - 0.03)
                WHEN '2025-01-20' THEN (RAND(p.product_id + 5) * 0.09 - 0.04)
            END
        )),
        2
    ) AS selling_price,

    -- approximate discount %
    ROUND(
        (
            CASE pl.platform_id
                WHEN 1 THEN 10 + (RAND() * 5)
                WHEN 2 THEN 15 + (RAND() * 6)
                WHEN 3 THEN 8 + (RAND() * 4)
            END
        ),
        2
    ) AS discount_percent,

    d.price_date
FROM products p
CROSS JOIN platforms pl
CROSS JOIN (
    SELECT DATE('2025-01-01') AS price_date
    UNION ALL SELECT DATE('2025-01-05')
    UNION ALL SELECT DATE('2025-01-10')
    UNION ALL SELECT DATE('2025-01-15')
    UNION ALL SELECT DATE('2025-01-20')
) d;
SELECT
    p.product_name,
    ph.price_date,
    ph.selling_price
FROM price_history ph
JOIN products p ON ph.product_id = p.product_id
WHERE p.product_id IN (1, 5, 10)
ORDER BY p.product_name, ph.price_date;
DELETE FROM price_history;
INSERT INTO price_history
(product_id, platform_id, mrp, selling_price, discount_percent, price_date)
SELECT
    p.product_id,
    pl.platform_id,

    -- base MRP per product
    ROUND(3000 + p.product_id * 400 + (RAND(p.product_id) * 600), 2) AS mrp,

    -- selling price with independent platform + date behavior
    ROUND(
        (
            3000
            + p.product_id * 400
            + (RAND(p.product_id) * 600)
        )
        * (1 - (
            CASE pl.platform_id
                WHEN 1 THEN 0.10 + RAND(pl.platform_id) * 0.05
                WHEN 2 THEN 0.15 + RAND(pl.platform_id) * 0.06
                WHEN 3 THEN 0.08 + RAND(pl.platform_id) * 0.04
            END
        ))
        * (1 + (
            CASE d.price_date
                WHEN '2025-01-01' THEN (RAND(p.product_id + pl.platform_id + 1) * 0.08 - 0.04)
                WHEN '2025-01-05' THEN (RAND(p.product_id + pl.platform_id + 2) * 0.10 - 0.05)
                WHEN '2025-01-10' THEN (RAND(p.product_id + pl.platform_id + 3) * 0.12 - 0.06)
                WHEN '2025-01-15' THEN (RAND(p.product_id + pl.platform_id + 4) * 0.09 - 0.045)
                WHEN '2025-01-20' THEN (RAND(p.product_id + pl.platform_id + 5) * 0.11 - 0.055)
            END
        )),
        2
    ) AS selling_price,

    -- discount %
    ROUND(
        CASE pl.platform_id
            WHEN 1 THEN 10 + RAND(pl.platform_id) * 5
            WHEN 2 THEN 15 + RAND(pl.platform_id) * 6
            WHEN 3 THEN 8  + RAND(pl.platform_id) * 4
        END,
        2
    ) AS discount_percent,

    d.price_date
FROM products p
CROSS JOIN platforms pl
CROSS JOIN (
    SELECT DATE('2025-01-01') AS price_date
    UNION ALL SELECT DATE('2025-01-05')
    UNION ALL SELECT DATE('2025-01-10')
    UNION ALL SELECT DATE('2025-01-15')
    UNION ALL SELECT DATE('2025-01-20')
) d;
