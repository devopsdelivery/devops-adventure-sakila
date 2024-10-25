CREATE TABLE User_Products (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(id),
    product_id INT REFERENCES Products(id)
);
