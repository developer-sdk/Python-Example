import re

html_str = """
var wait_paging = null;
var img_list = ["https:\/\/cdnwowmax.xyz\/upload\/2ecb7116ffbad01dd160c96135ac98de.jpg","https:\/\/cdnwowmax.xyz\/upload\/a4f03cc7438c27e1868b4218fe295f8c.jpg","https:\/\/cdnwowmax.xyz\/upload\/718e2c633694071b809f79ddb8370c31.jpg","https:\/\/cdnwowmax.xyz\/upload\/da79cced1c08e715908c15655656b75a.jpg","https:\/\/cdnwowmax.xyz\/upload\/a4e72303abdc73c804bb4724914aba48.jpg","https:\/\/cdnwowmax.xyz\/upload\/bf664d310c18d27eed1b207c5b8d8f24.jpg","https:\/\/cdnwowmax.xyz\/upload\/6625c612bcb62278f80fa090d1114891.jpg","https:\/\/cdnwowmax.xyz\/upload\/dbe247c089831231136774c8275ab804.jpg","https:\/\/cdnwowmax.xyz\/upload\/5df77d49a8f9077144e0d67616e97237.jpg","https:\/\/cdnwowmax.xyz\/upload\/95a5087cf9e1f4095e3f02ee81be570f.jpg","https:\/\/cdnwowmax.xyz\/upload\/3abe0bb687fc9f548e311e3009fd80da.jpg","https:\/\/cdnwowmax.xyz\/upload\/8e04a220ad912bbe4b2302baf9c06222.jpg","https:\/\/cdnwowmax.xyz\/upload\/c0134327f68cbbd60a2d9da5bd650ed7.jpg","https:\/\/cdnwowmax.xyz\/upload\/4c86c9591a13d9363aa65035297d2f6c.jpg","https:\/\/cdnwowmax.xyz\/upload\/4b00fa819d74db8c0776641e568e577a.jpg","https:\/\/cdnwowmax.xyz\/upload\/93e0d643075807319fa55a3cb6199732.jpg","https:\/\/cdnwowmax.xyz\/upload\/6cd8b55095d0b7ca9005f3b90ee36121.jpg","https:\/\/cdnwowmax.xyz\/upload\/e9b4e63cd0ca8c91710d98e651c22571.jpg","https:\/\/cdnwowmax.xyz\/upload\/aae5ea306df1c02d8d81bbd43a6214f6.jpg","https:\/\/cdnwowmax.xyz\/upload\/fda66f1db0191e40634a34a7e9fdac62.jpg","https:\/\/cdnwowmax.xyz\/upload\/a63e891019997dad184410a82adcd613.jpg"];
var img_list1 = [];
"""

p = re.compile("(https:....cdnwowmax.xyz..upload..[a-z0-9-]+.jpg)")
m = p.findall(html_str)

print(m)
