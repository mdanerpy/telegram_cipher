# coding: utf-8

persian_chars = [
    'ا','ب','پ','ت','ث','ج','چ','ح','خ','د','ذ','ر','ز','ژ','س','ش','ص','ض','ط','ظ',
    'ع','غ','ف','ق','ک','گ','ل','م','ن','و','ه','ی',
    '0','1','2','3','4','5','6','7','8','9',
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    ':','،','.','(',')','!','؟','|','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    '$','^','\\','?','>','<',',','"','[',']','_','&','@','#','%',';', 'ة','؛','ـ','«','»','ي','ؤ','ء','آ','إ','أ','ۀ','ً','ٌ','ٍ','َ','ُ','ِ','ّ'
]

chinese_chars = [
    '去','请','钱','前','亲','却','卡','其','求','我','为','玩','问','万','哇','王','网','微','喂','胃','额','饿','俄','噩','齾','鹗','卾',
    '人','日','名','如','猛','肉','入','任','忍','热','让','刃','壬','他','貓','太','天','她','图','听','挺','头','条','题','脱','抬',
    '有','吧','把','用','与','又','也','要','晕','亿','野','油','鱼','雨','雅','壹','啊','阿','吖','嗄','锕','呵','錒','是','说','谁',
    '三','事','率','岁','四','丝','都','的','多','点','但','发','分','放','非','飞','风','方','富','犯','个','给','跟','高','刚',
    '搞','管','和','好','很','会','号','话','回','红','活','在','抱','做','暖','真','最','着','之','只','这','再','总','下','想','小',
    '先','吗','没','么','买','们','忙','拿'
]

def get_mapping(index, direction='+'):
    mapping = {}
    idx = index
    for ch in persian_chars:
        mapping[ch] = chinese_chars[idx % len(chinese_chars)]
        idx = idx + 1 if direction == '+' else idx - 1
    return mapping

def get_reverse_mapping(index, direction='+'):
    mapping = {}
    idx = index
    for ch in persian_chars:
        chinese = chinese_chars[idx % len(chinese_chars)]
        mapping[chinese] = ch
        idx = idx + 1 if direction == '+' else idx - 1
    return mapping

def parse_code_start(code):
    try:
        stripped = code.strip('(){}[]«»')
        if ':' in stripped:
            num, ref = stripped.split(':')
            direction = '+' if '+' in num else '-'
            n = int(num.replace('+', '').replace('-', ''))
            ref_index = persian_chars.index(ref)
            index = (ref_index + n) if direction == '+' else (ref_index - n)
            return index % len(chinese_chars), direction
        elif '+' in stripped or '-' in stripped:
            direction = '+' if '+' in stripped else '-'
            number = int(stripped.replace('+', '').replace('-', ''))
            return number % len(chinese_chars), direction
    except:
        return None
    return None

def process(text, mode='encode'):
    try:
        text = text.strip()
        if text[-1] in ['*', '/']:
            importance = text[-1]
            text = text[:-1]
        else:
            importance = ''

        first_non_brace = ''
        for ch in text:
            if ch in '{}[]()«»':
                break
            first_non_brace += ch

        content = text[len(first_non_brace):]
        code_part = first_non_brace

        brace_count = sum(1 for ch in content if ch in '{}[]()«»')
        if brace_count % 2 != 0:
            return "❗️تعداد آکولادها باید زوج باشد."

        if not any(ch in content for ch in '{}[]()«»'):
            return "❗️خطا: پیام باید داخل آکولاد {...} باشد."

        result = parse_code_start(code_part)
        if not result:
            return "❗️ساختار کد نادرست است."

        index, direction = result
        mapping = get_mapping(index, direction) if mode == 'encode' else get_reverse_mapping(index, direction)

        result = ""
        brace_counter = 0

        for ch in content:
            if ch in '{}[]()«»':
                brace_counter += 1
                result += ch
            else:
                if brace_counter % 2 == 1:
                    result += mapping.get(ch, ch)
                else:
                    result += ch

        return f"{index}{direction}{result}{importance}"

    except:
        return "❌ خطا در پردازش ورودی."