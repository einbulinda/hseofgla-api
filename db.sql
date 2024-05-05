CREATE SCHEMA IF NOT EXISTS dev;
CREATE SCHEMA IF NOT EXISTS aud;


-- Creating the Staff table
CREATE TABLE dev.staff (
    staff_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    mobile_number VARCHAR(15),
	email VARCHAR(255),
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id),
    ADD SEQUENCE staff_staff_id_seq RESTART WITH 1001
);

-- Staff ID to start from 1001
-- ALTER SEQUENCE dev.staff_staff_id_seq RESTART WITH 1001;

INSERT INTO dev.staff (name, role) 
VALUES ('hseofgla','system');

-- Creating the Categories table with a self-referencing parent_category_id
CREATE TABLE dev.categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    parent_category_id INT NULL,
    created_by INT,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_date TIMESTAMP,
    FOREIGN KEY (parent_category_id) REFERENCES dev.categories(category_id),
    FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);

-- Creating the Products table
CREATE TABLE dev.products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category_id INT,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id),
	FOREIGN KEY (category_id) REFERENCES dev.categories(category_id)
);

-- Creating the Product Variants table
CREATE TABLE dev.product_variants (
    variant_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    sku VARCHAR(255) UNIQUE NOT NULL,
    price NUMERIC NOT NULL,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES dev.products (product_id),
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);

-- Creating the Inventory table
CREATE TABLE dev.inventory (
    inventory_id SERIAL PRIMARY KEY,
    variant_id INT NOT NULL,
    warehouse_stock INT NOT NULL,
    shop_stock INT NOT NULL,
    reorder_level INT NOT NULL,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
    FOREIGN KEY (variant_id) REFERENCES dev.product_variants(variant_id),
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);

-- Creating the Customers table
CREATE TABLE dev.customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
	mobile_number VARCHAR(15),
	email VARCHAR(255),
    credit_balance NUMERIC DEFAULT 0,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);


-- Creating the Orders table
CREATE TABLE dev.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,    
    total_items_count INT NOT NULL,
	total_order_amount NUMERIC NOT NULL,
    order_status VARCHAR(50) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES dev.customers (customer_id),
    --FOREIGN KEY (variant_id) REFERENCES dev.product_variants (variant_id),
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);

-- Creating the Order Items table
CREATE TABLE dev.order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    variant_id INT NOT NULL,
    quantity INT NOT NULL,
	discount_rate NUMERIC DEFAULT 0,
	discount_amount NUMERIC DEFAULT 0,
    price_at_purchase NUMERIC NOT NULL,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES dev.orders (order_id),
    FOREIGN KEY (variant_id) REFERENCES dev.product_variants (variant_id),
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);

-- Creating the Discounts table
CREATE TABLE dev.discounts (
    discount_id SERIAL PRIMARY KEY,
    discount_name VARCHAR(255) NOT NULL,
	product_id INT NULL,
	variant_id INT NULL,
    discount_rate NUMERIC,
    discount_amount NUMERIC,
    start_date DATE NOT NULL,
    expiry_date DATE,
    description TEXT,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
	FOREIGN KEY (product_id) REFERENCES dev.products(product_id),
	FOREIGN KEY (variant_id) REFERENCES dev.product_variants(variant_id),
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);


-- Creating the Payments table
CREATE TABLE dev.payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    amount_paid NUMERIC NOT NULL,
    payment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(255) NOT NULL,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES dev.orders (order_id),
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);

-- Creating the shipping addresses table
CREATE TABLE dev.shipping_addresses (
    address_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
	county VARCHAR(100) NOT NULL,
	town VARCHAR(100) NOT NULL,
    landmark VARCHAR(255) NOT NULL,
    additional_info VARCHAR(255),
    is_default BOOLEAN DEFAULT FALSE,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES dev.customers (customer_id),
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);

-- Creating the Inventory History table
CREATE TABLE dev.inventory_history (
    history_id SERIAL PRIMARY KEY,
    variant_id INT NOT NULL,
    warehouse_stock_before INT NOT NULL,
    warehouse_stock_after INT NOT NULL,
    shop_stock_before INT NOT NULL,
    shop_stock_after INT NOT NULL,
    change_reason TEXT,
    change_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    staff_id INT NOT NULL,
	created_by INT,
	created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by INT,
	updated_date TIMESTAMP,
    FOREIGN KEY (variant_id) REFERENCES dev.product_variants (variant_id),
    FOREIGN KEY (staff_id) REFERENCES dev.staff (staff_id),
	FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);

--Creating the Images Table
CREATE TABLE dev.product_images (
    image_id SERIAL PRIMARY KEY,
    variant_id INT NOT NULL,
    image_name VARCHAR(255) NOT NULL,
    image_url TEXT NOT NULL,
    created_by INT,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_date TIMESTAMP,
    FOREIGN KEY (variant_id) REFERENCES dev.product_variants (variant_id),
    FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);

-- Creating the Staff Login Sessions table
CREATE TABLE aud.staff_login_sessions (
    session_id SERIAL PRIMARY KEY,
    staff_id INT NOT NULL,
    login_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    logout_timestamp TIMESTAMP,
    ip_address VARCHAR(255),
    device_info TEXT,
    FOREIGN KEY (staff_id) REFERENCES dev.staff(staff_id)
);

CREATE TABLE aud.revoked_tokens(
    id SERIAL PRIMARY KEY,
    JTI VARCHAR(120) UNIQUE NOT NULL
);

-- Creating a login details table for both customers and staff.
CREATE TABLE aud.login_details (
	loggin_id SERIAL PRIMARY KEY,
	staff_id INT,
	customer_id INT,
	username VARCHAR(255),
	password VARCHAR (255),
    failed_attempts INT NOT NULL DEFAULT 0,
    is_locked BOOLEAN DEFAULT False,
	created_by INT,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_date TIMESTAMP,
	FOREIGN KEY (staff_id) REFERENCES dev.staff(staff_id),
	FOREIGN KEY (customer_id) REFERENCES dev.customers(customer_id),
    FOREIGN KEY (created_by) REFERENCES dev.staff(staff_id),
    FOREIGN KEY (updated_by) REFERENCES dev.staff(staff_id)
);


-- Creating the Audit Log table
CREATE TABLE aud.audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(255) NOT NULL,
    field_name VARCHAR(255),
    old_value TEXT,
    new_value TEXT,
    operation_type VARCHAR(50) NOT NULL,
    changed_by INT NOT NULL,
    changed_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (changed_by) REFERENCES dev.staff(staff_id)
);

---	TRIGGERS

-- Audit Trail Trigger for Products Table
CREATE OR REPLACE FUNCTION dev.audit_products_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO aud.audit_log(table_name, field_name, old_value, new_value, operation_type, changed_by, changed_date)
        VALUES ('products', 'product_name', OLD.product_name, NEW.product_name, 'UPDATE', NEW.updated_by, NOW()),
				('products', 'category_id', OLD.category_id, NEW.category_id, 'UPDATE', NEW.updated_by, NOW());
        -- Repeat for other fields and operations as necessary
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO aud.audit_log(table_name, operation_type, changed_by, changed_date)
        VALUES ('products', 'INSERT', NEW.created_by, NOW());
        -- No old_value or field_name for INSERT
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO aud.audit_log(table_name, old_value, operation_type, changed_by, changed_date)
        VALUES ('products', OLD.product_name, 'DELETE', OLD.updated_by, NOW());
        -- No new_value for DELETE
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER products_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON dev.products
FOR EACH ROW EXECUTE FUNCTION dev.audit_products_changes();

-- Audit Trail Trigger for Categories Table
CREATE OR REPLACE FUNCTION dev.audit_categories_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO aud.audit_log(table_name, field_name, old_value, new_value, operation_type, changed_by, changed_date)
        VALUES ('categories', 'category_name', OLD.category_name, NEW.category_name, 'UPDATE', NEW.updated_by, NOW()),
				('categories','parent_category_id',OLD.parent_category_id, NEW.parent_category_id,'UPDATE',NEW.updated_by,NOW());
        -- Repeat for other fields and operations as necessary
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO aud.audit_log(table_name, operation_type, changed_by, changed_date)
        VALUES ('categories', 'INSERT', NEW.created_by, NOW());
        -- No old_value or field_name for INSERT
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO aud.audit_log(table_name, old_value, operation_type, changed_by, changed_date)
        VALUES ('categories', OLD.category_name, 'DELETE', OLD.updated_by, NOW());
        -- No new_value for DELETE
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER categories_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON dev.categories
FOR EACH ROW EXECUTE FUNCTION dev.audit_categories_changes();

-- Trigger for Audit Trail on Staff Table
CREATE OR REPLACE FUNCTION dev.audit_staff_changes()
RETURNS TRIGGER AS $$
BEGIN
	IF TG_OP = 'UPDATE' THEN
		INSERT INTO aud.audit_log(table_name,field_name, old_value, new_value, operation_type, changed_by,changed_date)
		VALUES ('staff','name', OLD.name,NEW.name,'UPDATE',NEW.updated_by,NOW()),
				('staff','role', OLD.role,NEW.role,'UPDATE',NEW.updated_by,NOW());	
	ELSIF TG_OP = 'INSERT' THEN
		INSERT INTO aud.audit_log(table_name, operation_type, changed_by,changed_date)
		VALUES ('staff','INSERT',NEW.created_by,NOW());	
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO aud.audit_log(table_name,field_name, old_value, operation_type, changed_by, changed_date)
		VALUES ('staff','name', OLD.name,'DELETE',OLD.updated_by,NOW());
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER staff_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON dev.staff
FOR EACH ROW EXECUTE FUNCTION dev.audit_staff_changes();

-- Trigger for Audit Trail on Customers Table
CREATE OR REPLACE FUNCTION dev.audit_customer_changes()
RETURNS TRIGGER AS $$
BEGIN
	IF TG_OP = 'UPDATE' THEN
		INSERT INTO aud.audit_log(table_name,field_name, old_value, new_value, operation_type, changed_by,changed_date)
		VALUES ('customers','name', OLD.name,NEW.name,'UPDATE',NEW.updated_by,NOW()),
				('customers','mobile_number', OLD.role,NEW.role,'UPDATE',NEW.updated_by,NOW()),
				('customers','email', OLD.role,NEW.role,'UPDATE',NEW.updated_by,NOW()),
				('customers','credit_balance', OLD.role,NEW.role,'UPDATE',NEW.updated_by,NOW());	
	ELSIF TG_OP = 'INSERT' THEN
		INSERT INTO aud.audit_log(table_name, operation_type, changed_by,changed_date)
		VALUES ('customers','INSERT',NEW.created_by,NOW());	
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO aud.audit_log(table_name,field_name, old_value, operation_type, changed_by, changed_date)
		VALUES ('customers','name', OLD.name,'DELETE',OLD.updated_by,NOW()),
                ('customers','mobile_number', OLD.name,'DELETE',OLD.updated_by,NOW()),
                ('customers','email', OLD.name,'DELETE',OLD.updated_by,NOW()),
                ('customers','credit_balance', OLD.name,'DELETE',OLD.updated_by,NOW());
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER customers_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON dev.customers
FOR EACH ROW EXECUTE FUNCTION dev.audit_customer_changes();


-- Trigger for Audit Trail on Discounts Table
CREATE OR REPLACE FUNCTION dev.audit_discounts_changes()
RETURNS TRIGGER AS $$
BEGIN
	IF TG_OP = 'UPDATE' THEN
		INSERT INTO aud.audit_log(table_name,field_name, old_value, new_value, operation_type, changed_by,changed_date)
		VALUES ('discounts','discount_name', OLD.discount_name,NEW.discount_name,'UPDATE',NEW.updated_by,NOW()),
				('discounts','discount_rate', OLD.discount_rate,NEW.discount_rate,'UPDATE',NEW.updated_by,NOW());
	ELSIF TG_OP = 'INSERT' THEN
		INSERT INTO aud.audit_log(table_name, operation_type, changed_by,changed_date)
		VALUES ('discounts','INSERT',NEW.changed_by,NOW());	
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO aud.audit_log(table_name,field_name, old_value, operation_type, changed_by, changed_date)
		VALUES ('discounts','discount_name', OLD.discount_name,'DELETE',OLD.updated_by,NOW());
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER discounts_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON dev.discounts
FOR EACH ROW EXECUTE FUNCTION dev.audit_discounts_changes();

-- Trigger for Audit Trail on Orders Table
CREATE OR REPLACE FUNCTION dev.audit_orders_changes()
RETURNS TRIGGER AS $$
BEGIN
	IF TG_OP = 'UPDATE' THEN
		INSERT INTO aud.audit_log(table_name,field_name, old_value, new_value, operation_type, changed_by,changed_date)
		VALUES ('orders','order_status', OLD.order_status,NEW.order_status,'UPDATE',NEW.updated_by,NOW()),
				('orders','order_status', OLD.order_status,NEW.order_status,'UPDATE',NEW.updated_by,NOW());
	ELSIF TG_OP = 'INSERT' THEN
		INSERT INTO aud.audit_log(table_name, operation_type, changed_by,changed_date)
		VALUES ('orders','INSERT',NEW.changed_by,NOW());	
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO aud.audit_log(table_name,field_name, old_value, operation_type, changed_by, changed_date)
		VALUES ('orders','order_id', OLD.order_id,'DELETE',OLD.updated_by,NOW());
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER orders_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON dev.orders
FOR EACH ROW EXECUTE FUNCTION dev.audit_orders_changes();

-- Trigger for locking user on multiple attempts
CREATE OR REPLACE FUNCTION update_lock_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.failed_attempts >= 5 THEN
        NEW.is_locked := TRUE;
    ELSIF NEW.failed_attempts = 0 THEN
        NEW.is_locked := FALSE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_lock_status
BEFORE UPDATE OF failed_attempts ON aud.login_details
FOR EACH ROW
EXECUTE FUNCTION update_lock_status();
