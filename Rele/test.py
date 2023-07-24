
text = '~220 (+10%), 50 Гц'
# text = '24 DC; 230 AC'
# text = '24 AC/DC'
if ';' in text:
    print(text.strip().replace('~', '').replace('; ', ' ;; Русский ~ '))
elif any(x in text for x in ['~',')', '%','(','cosφ', 'sin']):
    print(text.strip().replace('~', '').split(' ', 1)[0])
else:
    print(text.strip())
