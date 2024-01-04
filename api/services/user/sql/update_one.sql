UPDATE users
SET token = :token
WHERE email = :email;