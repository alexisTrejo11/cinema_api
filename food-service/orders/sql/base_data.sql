-- Product Categories Insert
INSERT INTO food_orders_product (name, description, price, category, image_url, is_available, stock_quantity, cost_price, created_at)
VALUES
    -- Snacks
    ('Large Popcorn', 'Fresh buttery popcorn, perfect for sharing', 8.99, 'snacks', 'https://example.com/popcorn.jpg', true, 1000, 2.50, NOW()),
    ('Medium Popcorn', 'Classic movie popcorn', 6.99, 'snacks', 'https://example.com/popcorn-medium.jpg', true, 1000, 2.00, NOW()),
    ('Small Popcorn', 'Individual portion of popcorn', 4.99, 'snacks', 'https://example.com/popcorn-small.jpg', true, 1000, 1.50, NOW()),
    ('Nachos', 'Crispy nachos with cheese sauce', 7.99, 'snacks', 'https://example.com/nachos.jpg', true, 500, 3.00, NOW()),
    ('Hot Dog', 'Classic cinema hot dog with condiments', 6.99, 'snacks', 'https://example.com/hotdog.jpg', true, 200, 2.50, NOW()),
    ('Cheese Popcorn', 'Popcorn dusted with premium cheese powder', 9.99, 'snacks', 'https://example.com/cheese-popcorn.jpg', true, 800, 3.00, NOW()),
    ('Caramel Popcorn', 'Sweet caramel-coated popcorn', 9.99, 'snacks', 'https://example.com/caramel-popcorn.jpg', true, 800, 3.00, NOW()),
    ('Mixed Popcorn', 'Half regular, half caramel popcorn', 10.99, 'snacks', 'https://example.com/mixed-popcorn.jpg', true, 800, 3.50, NOW()),
    ('Pretzel Bites', 'Warm soft pretzel bites with salt', 6.99, 'snacks', 'https://example.com/pretzel-bites.jpg', true, 300, 2.50, NOW()),
    ('Mozzarella Sticks', 'Crispy breaded mozzarella sticks with marinara', 8.99, 'snacks', 'https://example.com/mozzarella.jpg', true, 200, 3.50, NOW()),
    ('French Fries', 'Crispy golden fries with salt', 5.99, 'snacks', 'https://example.com/fries.jpg', true, 400, 2.00, NOW()),
    ('Onion Rings', 'Crispy battered onion rings', 6.99, 'snacks', 'https://example.com/onion-rings.jpg', true, 300, 2.50, NOW()),
    

    -- Drinks
    ('Large Coca-Cola', 'Refreshing 32oz cola', 5.99, 'drinks', 'https://example.com/cola-large.jpg', true, 1000, 1.00, NOW()),
    ('Medium Coca-Cola', 'Classic 24oz cola', 4.99, 'drinks', 'https://example.com/cola-medium.jpg', true, 1000, 0.80, NOW()),
    ('Large Sprite', 'Refreshing 32oz lemon-lime soda', 5.99, 'drinks', 'https://example.com/sprite-large.jpg', true, 1000, 1.00, NOW()),
    ('Medium Sprite', 'Classic 24oz lemon-lime soda', 4.99, 'drinks', 'https://example.com/sprite-medium.jpg', true, 1000, 0.80, NOW()),
    ('Bottled Water', 'Pure spring water', 3.99, 'drinks', 'https://example.com/water.jpg', true, 1000, 0.50, NOW()),
    ('Large Dr Pepper', 'Refreshing 32oz Dr Pepper', 5.99, 'drinks', 'https://example.com/drpepper-large.jpg', true, 800, 1.00, NOW()),
    ('Medium Dr Pepper', 'Classic 24oz Dr Pepper', 4.99, 'drinks', 'https://example.com/drpepper-medium.jpg', true, 800, 0.80, NOW()),
    ('Large Fanta', 'Refreshing 32oz orange soda', 5.99, 'drinks', 'https://example.com/fanta-large.jpg', true, 800, 1.00, NOW()),
    ('Medium Fanta', 'Classic 24oz orange soda', 4.99, 'drinks', 'https://example.com/fanta-medium.jpg', true, 800, 0.80, NOW()),
    ('Large Icee - Cherry', 'Frozen cherry-flavored drink', 5.99, 'drinks', 'https://example.com/icee-cherry.jpg', true, 500, 1.20, NOW()),
    ('Large Icee - Blue Raspberry', 'Frozen blue raspberry drink', 5.99, 'drinks', 'https://example.com/icee-blue.jpg', true, 500, 1.20, NOW()),
    ('Fresh Lemonade', 'Freshly squeezed lemonade', 5.99, 'drinks', 'https://example.com/lemonade.jpg', true, 400, 1.50, NOW()),

    -- Sweets
    ('M&Ms', 'Classic chocolate candies', 4.99, 'sweets', 'https://example.com/mms.jpg', true, 500, 2.00, NOW()),
    ('Skittles', 'Fruit-flavored candies', 4.99, 'sweets', 'https://example.com/skittles.jpg', true, 500, 2.00, NOW()),
    ('Sour Patch Kids', 'Sour then sweet gummy candies', 4.99, 'sweets', 'https://example.com/sourpatch.jpg', true, 500, 2.00, NOW()),
    ('Reeses Pieces', 'Peanut butter candies', 4.99, 'sweets', 'https://example.com/reeses.jpg', true, 500, 2.00, NOW()),
    ('Twizzlers', 'Strawberry twisted candy', 4.99, 'sweets', 'https://example.com/twizzlers.jpg', true, 400, 2.00, NOW()),
    ('Snickers', 'Chocolate, caramel and peanut bar', 4.99, 'sweets', 'https://example.com/snickers.jpg', true, 400, 2.00, NOW()),
    ('Raisinets', 'Chocolate covered raisins', 4.99, 'sweets', 'https://example.com/raisinets.jpg', true, 400, 2.00, NOW()),
    ('Milk Duds', 'Chocolate covered caramel balls', 4.99, 'sweets', 'https://example.com/milkduds.jpg', true, 400, 2.00, NOW()),
    ('Junior Mints', 'Dark chocolate covered mints', 4.99, 'sweets', 'https://example.com/juniormints.jpg', true, 400, 2.00, NOW()),
    ('Gummy Bears', 'Assorted fruit flavored gummy bears', 4.99, 'sweets', 'https://example.com/gummybears.jpg', true, 400, 2.00, NOW()),
    

    -- Meals
    ('Chicken Tenders', 'Crispy chicken tenders with sauce', 9.99, 'meals', 'https://example.com/tenders.jpg', true, 200, 4.00, NOW()),
    ('Pizza Slice', 'Fresh cheese pizza slice', 7.99, 'meals', 'https://example.com/pizza.jpg', true, 200, 3.00, NOW()),
    ('Chicken Wings', '6 piece wings with choice of sauce', 11.99, 'meals', 'https://example.com/wings.jpg', true, 150, 5.00, NOW()),
    ('Cheeseburger', 'Quarter-pound burger with cheese', 10.99, 'meals', 'https://example.com/burger.jpg', true, 150, 4.50, NOW()),
    ('Chicken Sandwich', 'Crispy chicken breast sandwich', 9.99, 'meals', 'https://example.com/chicken-sandwich.jpg', true, 150, 4.00, NOW()),
    ('Mini Corn Dogs', '6 piece mini corn dogs', 8.99, 'meals', 'https://example.com/corn-dogs.jpg', true, 200, 3.50, NOW()),
    ('Mac and Cheese', 'Creamy macaroni and cheese', 7.99, 'meals', 'https://example.com/mac-cheese.jpg', true, 200, 3.00, NOW()),

    -- Desserts
    ('Ice Cream', 'Vanilla ice cream cup', 5.99, 'desserts', 'https://example.com/icecream.jpg', true, 200, 2.00, NOW()),
    ('Chocolate Brownie', 'Warm chocolate brownie', 4.99, 'desserts', 'https://example.com/brownie.jpg', true, 200, 1.50, NOW()),
    ('Churros', 'Fresh churros with cinnamon sugar', 5.99, 'desserts', 'https://example.com/churros.jpg', true, 200, 2.00, NOW()),
    ('Cookie Dough Bites', 'Chocolate chip cookie dough pieces', 5.99, 'desserts', 'https://example.com/cookie-dough.jpg', true, 300, 2.50, NOW()),
    ('Dippin Dots', 'Flash-frozen ice cream beads', 6.99, 'desserts', 'https://example.com/dippin-dots.jpg', true, 150, 3.00, NOW()),
    ('Funnel Cake', 'Fresh fried funnel cake with powdered sugar', 7.99, 'desserts', 'https://example.com/funnel-cake.jpg', true, 100, 3.50, NOW()),
    ('Ice Cream Sandwich', 'Vanilla ice cream between chocolate cookies', 4.99, 'desserts', 'https://example.com/ice-cream-sandwich.jpg', true, 200, 2.00, NOW());


-- Create Combos
WITH popcorn AS (SELECT id FROM food_orders_product WHERE name = 'Large Popcorn' LIMIT 1),
     cola AS (SELECT id FROM food_orders_product WHERE name = 'Large Coca-Cola' LIMIT 1),
     nachos AS (SELECT id FROM food_orders_product WHERE name = 'Nachos' LIMIT 1),
     candy AS (SELECT id FROM food_orders_product WHERE name = 'M&Ms' LIMIT 1)
INSERT INTO food_orders_combo (name, description, price, is_active, image_url, created_at)
VALUES
    ('Movie Night Special', 'Large popcorn and large drink', 12.99, true, 'https://example.com/combo1.jpg', NOW()),
    ('Family Pack', 'Large popcorn, 2 large drinks, and nachos', 24.99, true, 'https://example.com/combo2.jpg', NOW()),
    ('Sweet & Salty Combo', 'Medium popcorn, medium drink, and candy', 14.99, true, 'https://example.com/combo3.jpg', NOW()),
    ('Date Night Bundle', 'Large popcorn, 2 medium drinks, and candy', 19.99, true, 'https://example.com/combo4.jpg', NOW());

-- Link products to combos
WITH combo1 AS (SELECT id FROM food_orders_combo WHERE name = 'Movie Night Special' LIMIT 1),
     combo2 AS (SELECT id FROM food_orders_combo WHERE name = 'Family Pack' LIMIT 1),
     combo3 AS (SELECT id FROM food_orders_combo WHERE name = 'Sweet & Salty Combo' LIMIT 1),
     combo4 AS (SELECT id FROM food_orders_combo WHERE name = 'Date Night Bundle' LIMIT 1),
     large_popcorn AS (SELECT id FROM food_orders_product WHERE name = 'Large Popcorn' LIMIT 1),
     medium_popcorn AS (SELECT id FROM food_orders_product WHERE name = 'Medium Popcorn' LIMIT 1),
     large_cola AS (SELECT id FROM food_orders_product WHERE name = 'Large Coca-Cola' LIMIT 1),
     medium_cola AS (SELECT id FROM food_orders_product WHERE name = 'Medium Coca-Cola' LIMIT 1),
     nachos AS (SELECT id FROM food_orders_product WHERE name = 'Nachos' LIMIT 1),
     mms AS (SELECT id FROM food_orders_product WHERE name = 'M&Ms' LIMIT 1)
INSERT INTO food_orders_comboproduct (combo_id, product_id, quantity)
SELECT combo1.id, large_popcorn.id, 1 FROM combo1, large_popcorn
UNION ALL
SELECT combo1.id, large_cola.id, 1 FROM combo1, large_cola
UNION ALL
SELECT combo2.id, large_popcorn.id, 1 FROM combo2, large_popcorn
UNION ALL
SELECT combo2.id, large_cola.id, 2 FROM combo2, large_cola
UNION ALL
SELECT combo2.id, nachos.id, 1 FROM combo2, nachos
UNION ALL
SELECT combo3.id, medium_popcorn.id, 1 FROM combo3, medium_popcorn
UNION ALL
SELECT combo3.id, medium_cola.id, 1 FROM combo3, medium_cola
UNION ALL
SELECT combo3.id, mms.id, 1 FROM combo3, mms
UNION ALL
SELECT combo4.id, large_popcorn.id, 1 FROM combo4, large_popcorn
UNION ALL
SELECT combo4.id, medium_cola.id, 2 FROM combo4, medium_cola
UNION ALL
SELECT combo4.id, mms.id, 1 FROM combo4, mms;

-- Create some promotions
INSERT INTO food_orders_promotion (name, description, discount_type, discount_value, 
                      start_date, end_date, min_purchase_amount, usage_limit, current_usage)
VALUES
    ('Happy Hour Discount', 
     'Get 20% off on all combos between 2 PM and 5 PM', 
     'percentage', 20.00, 
     CURRENT_DATE, CURRENT_DATE + INTERVAL '3 months',
     0.00, 1000, 0),
    
    ('Student Tuesday', 
     'Students get $5 off on purchases over $20', 
     'fixed', 5.00, 
     CURRENT_DATE, CURRENT_DATE + INTERVAL '6 months',
     20.00, NULL, 0),
    
    ('Family Weekend Special', 
     'Buy any family pack and get a free large popcorn', 
     'fixed', 8.99, 
     CURRENT_DATE, CURRENT_DATE + INTERVAL '2 months',
     24.99, 500, 0),
    
    ('Member Monday', 
     'Cinema members get 15% off all purchases', 
     'percentage', 15.00, 
     CURRENT_DATE, CURRENT_DATE + INTERVAL '12 months',
     0.00, NULL, 0);

-- Link promotions to eligible products/combos
WITH happy_hour AS (SELECT id FROM food_orders_promotion WHERE name = 'Happy Hour Discount' LIMIT 1),
     student_promo AS (SELECT id FROM food_orders_promotion WHERE name = 'Student Tuesday' LIMIT 1),
     family_special AS (SELECT id FROM food_orders_promotion WHERE name = 'Family Weekend Special' LIMIT 1),
     member_monday AS (SELECT id FROM food_orders_promotion WHERE name = 'Member Monday' LIMIT 1),
     family_pack AS (SELECT id FROM food_orders_combo WHERE name = 'Family Pack' LIMIT 1)
INSERT INTO food_orders_promotion_combos (promotion_id, combo_id)
SELECT happy_hour.id, food_orders_combo.id 
FROM happy_hour, food_orders_combo
UNION ALL
SELECT family_special.id, family_pack.id 
FROM family_special, family_pack;

-- Link member monday promotion to all products
INSERT INTO food_orders_promotion_combos (promotion_id, combo_id)
SELECT member_monday.id, food_orders_combo.id
FROM (SELECT id FROM food_orders_promotion WHERE name = 'Member Monday' LIMIT 1) member_monday
CROSS JOIN food_orders_combo;