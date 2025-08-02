# backend/app/utils/email_merge_tags.py
def merge_tags(template: str, data: dict) -> str:
    for key, value in data.items():
        template = template.replace(f"[{key}]", value)
    return template

