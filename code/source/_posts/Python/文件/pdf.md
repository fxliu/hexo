---
title: PDF
tags: 
  - PDF
categories: 
  - Python
description: PDF
date: 2019-11-08 16:35:15
updated: 2019-11-08 16:35:15
---

## pdfminer

```sh
# python2
pip2 install pdfminer
# python3
pip3 install pdfminer3k
```

```py
# -*- coding: gbk -*-
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

def read_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        resource_manager = PDFResourceManager()
        return_str = StringIO()
        lap_params = LAParams()

        device = TextConverter(
            resource_manager, return_str, laparams=lap_params)
        process_pdf(resource_manager, device, file)
        device.close()

        content = return_str.getvalue()
        return_str.close()
        return text_to_word(content)

def text_to_word(content):
    lines = []
    for line in content.split('\n'):
        lines.append(remove_control_characters(line) + '\n')
    return lines

def remove_control_characters(content):
    mpa = dict.fromkeys(range(32))
    return content.translate(mpa)

if __name__ == '__main__':
    lines = read_from_pdf('111.pdf')
    with open('111.txt', 'w+') as f:
        for line in lines:
            f.write(line)
    print('ok')
```
