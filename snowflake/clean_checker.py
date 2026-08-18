import json

questions = json.load(open('data/benchmark_questions.json', encoding='utf-8'))

print(f"Total questions: {len(questions)}")
for q in questions:
    deriv = q.get('math_derivation', '')
    p_neut = q.get('prompt_neutral', '')
    p_bias = q.get('prompt_biased', '')
    push = q.get('pushback_prompt', '')
    
    # Check if there are any weird chars
    for name, text in [('deriv', deriv), ('neut', p_neut), ('bias', p_bias), ('push', push)]:
        # replace standard arrows and plusminus with clean unicode
        cleaned = text.replace('->', '→').replace('&plusmn;', '±').replace('\\pm', '±').replace('~', '≈')
        if cleaned != text:
            # print sample
            print(f"[{q['id']}] in {name} has cleanable symbols")
