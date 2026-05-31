-- 1. Insert a user (note: no id given, Postgres assigns it)
INSERT INTO users (username, password_hash) VALUES ('test_user', 'fake_hash_for_now');

-- 2. Read back, confirm id auto-assigned
SELECT * FROM users;

-- 3. Insert calculation linked to that user (use the id from step 2, likely 1)
INSERT INTO calculation_history (user_id, expression, result) VALUES (1, '5+10', 15);

-- 4. Read calculations
SELECT * FROM calculation_history;

-- 5. TRY TO BREAK FK — insert calculation for non-existent user
INSERT INTO calculation_history (user_id, expression, result) VALUES (999, '1+1', 2);
-- MUST fail with: violates foreign key constraint

-- 6. Test CASCADE — delete user, watch their history die too
DELETE FROM users WHERE id = 1;
SELECT * FROM calculation_history;
-- Should return 0 rows (CASCADE wiped it)
