UPDATE todos
SET title = '$title',
    details = '$details',
    checked = $checked,
    updated_at = '$updated_at'
WHERE id = $id;