UPDATE users
SET token = :token,
    updated_at = :updated_at
WHERE email = :email;