create or replace NONEDITIONABLE TRIGGER PreventCartDeletion
BEFORE DELETE ON Cart_Ecommerce
FOR EACH ROW
DECLARE
    cartCount INT;
BEGIN
    SELECT COUNT(*) INTO cartCount FROM Customers_Ecommerce WHERE Cart_id = :OLD.Cart_id;
    IF cartCount > 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Cannot delete a Cart that is referenced in Customers_Ecommerce.');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER PreventCustomersDeletion
BEFORE DELETE ON Customers_Ecommerce
FOR EACH ROW
DECLARE
    cartCount INT;
BEGIN
    SELECT COUNT(*) INTO cartCount FROM Cart_Ecommerce WHERE Cart_id = :OLD.Cart_id;
    IF cartCount > 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Cannot delete a Customer with associated Cart records.');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER PreventPaymentDeletion
BEFORE DELETE ON Payment_Ecommerce
FOR EACH ROW
DECLARE
    customerCount INT;
BEGIN
    SELECT COUNT(*) INTO customerCount FROM Customers_Ecommerce WHERE Customer_id = :OLD.Customer_id;
    IF customerCount > 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Cannot delete a Payment record associated with a Customer.');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER enforce_customers_update
BEFORE UPDATE ON Customers_Ecommerce
FOR EACH ROW
DECLARE
    v_reference_count NUMBER;
BEGIN
    -- Check if the updated Cart_id exists in the Cart_Ecommerce table
    SELECT COUNT(*)
    INTO v_reference_count
    FROM Cart_Ecommerce
    WHERE Cart_id = :NEW.Cart_id;

    -- If the reference does not exist, raise an exception
    IF v_reference_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Referential integrity violation: Cart_id does not exist in the Cart_Ecommerce table.');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER enforce_product_update
BEFORE UPDATE ON Product_Ecommerce
FOR EACH ROW
DECLARE
    v_reference_count NUMBER;
BEGIN
    -- Check if the updated Seller_id exists in the Seller_Ecommerce table
    SELECT COUNT(*)
    INTO v_reference_count
    FROM Seller_Ecommerce
    WHERE Seller_id = :NEW.Seller_id;

    -- If the reference does not exist, raise an exception
    IF v_reference_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Referential integrity violation: Seller_id does not exist in the Seller_Ecommerce table.');
    END IF;
END;
/

CREATE OR REPLACE TRIGGER enforce_payment_update
BEFORE UPDATE ON Payment_Ecommerce
FOR EACH ROW
DECLARE
    v_reference_count NUMBER;
BEGIN
    -- Check if the updated Customer_id and Cart_id exist in the Customers_Ecommerce and Cart_Ecommerce tables
    SELECT COUNT(*)
    INTO v_reference_count
    FROM Customers_Ecommerce C, Cart_Ecommerce Ca
    WHERE C.Customer_id = :NEW.Customer_id AND Ca.Cart_id = :NEW.Cart_id;

    -- If the reference does not exist, raise an exception
    IF v_reference_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Referential integrity violation: Customer_id or Cart_id does not exist in the referenced tables.');
    END IF;
END;
/



