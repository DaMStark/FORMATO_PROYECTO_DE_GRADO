import re
with open('C:\\Users\\Benjo\\OneDrive\\Desktop\\FORMATO_PROYECTO_DE_GRADO\\FORMATOLATEX_DOC\\5_Introduccion.tex', 'r', encoding='utf-8') as f:
    text = f.read()

def split_long_paragraphs(match):
    lines = match.group(0).split('\n')
    if len(lines) > 4:
        # Split paragraph into two parts roughly by sentence boundary
        para = match.group(0)
        sentences = re.split(r'(?<=\.)\s+', para)
        mid = len(sentences) // 2
        if mid > 0:
            p1 = ' '.join(sentences[:mid])
            p2 = ' '.join(sentences[mid:])
            return p1 + '\n\n' + p2
    return match.group(0)

# We only want to touch the Antecedentes section
# Let's find Antecedentes and Identificación del problema
start_idx = text.find('\\subsection*{Antecedentes}')
end_idx = text.find('\\subsection*{Identificación del problema}')

if start_idx != -1 and end_idx != -1:
    antecedentes = text[start_idx:end_idx]
    
    # Process paragraphs
    # Paragraphs are separated by \n\n
    paragraphs = antecedentes.split('\n\n')
    new_paragraphs = []
    for p in paragraphs:
        if p.strip() == '':
            continue
        # Split if too long
        lines = p.split('\n')
        if len(lines) > 5:
            # Let's split by sentence roughly
            sentences = re.split(r'(?<=\.)\s+(?=[A-Z])', p)
            if len(sentences) >= 2:
                mid = len(sentences) // 2
                p1 = ' '.join(sentences[:mid])
                p2 = ' '.join(sentences[mid:])
                # Replace internal newlines with spaces to avoid weird formatting
                p1 = p1.replace('\n', ' ')
                p2 = p2.replace('\n', ' ')
                new_paragraphs.append(p1)
                new_paragraphs.append(p2)
            else:
                new_paragraphs.append(p.replace('\n', ' '))
        else:
            new_paragraphs.append(p.replace('\n', ' '))
            
    new_antecedentes = '\n\n'.join(new_paragraphs)
    
    # Format line lengths to 80 chars
    final_antecedentes = []
    for p in new_antecedentes.split('\n\n'):
        words = p.split(' ')
        lines = []
        current_line = []
        for w in words:
            if len(' '.join(current_line + [w])) > 80:
                lines.append(' '.join(current_line))
                current_line = [w]
            else:
                current_line.append(w)
        if current_line:
            lines.append(' '.join(current_line))
        final_antecedentes.append('\n'.join(lines))
        
    final_antecedentes_str = '\n\n'.join(final_antecedentes) + '\n\n'
    
    new_text = text[:start_idx] + final_antecedentes_str + text[end_idx:]
    with open('C:\\Users\\Benjo\\OneDrive\\Desktop\\FORMATO_PROYECTO_DE_GRADO\\FORMATOLATEX_DOC\\5_Introduccion.tex', 'w', encoding='utf-8') as f:
        f.write(new_text)
