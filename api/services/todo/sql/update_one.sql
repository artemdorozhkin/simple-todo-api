UPDATE todos
SET title = :title,
    details = :details,
    checked = :checked,
    file_path = :file_path,
    updated_at = :updated_at
WHERE id = :id;