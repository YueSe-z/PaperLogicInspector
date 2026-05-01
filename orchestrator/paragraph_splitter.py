import re


def split_paragraphs(text: str, max_chars: int = 3000) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    result = []
    for para in paragraphs:
        if len(para) <= max_chars:
            result.append(para)
        else:
            sub_paras = [p.strip() for p in para.split("\n") if p.strip()]
            for sp in sub_paras:
                if len(sp) <= max_chars:
                    result.append(sp)
                else:
                    sentences = re.split(r"(?<=[。.!?！？])\s*", sp)
                    current = ""
                    for sent in sentences:
                        if not sent.strip():
                            continue
                        if len(current) + len(sent) > max_chars and current:
                            result.append(current.strip())
                            current = sent
                        else:
                            current += sent
                    if current.strip():
                        result.append(current.strip())

    return [p for p in result if len(p) >= 20]
