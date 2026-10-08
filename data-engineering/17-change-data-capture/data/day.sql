-- One day of writes to the orders table, in the order they happen.
INSERT INTO orders VALUES (3, 'new');
UPDATE orders SET status='paid' WHERE id=1;
UPDATE orders SET status='cancelled' WHERE id=2;
UPDATE orders SET status='shipped' WHERE id=1;
UPDATE orders SET status='delivered' WHERE id=1;
DELETE FROM orders WHERE id=2;
