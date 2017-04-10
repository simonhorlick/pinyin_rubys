# pinyin_rubys

A tool for generating HTML5 rubys from chinese phrases.

## Example output

```shell
$ python
>>> import ruby
>>> print(ruby.print_rubys(u'我明白了。'))
<ruby><rb>我</rb><rt>wǒ</rt><rb>明白</rb><rt>míngbái</rt><rb>了</rb><rt>le</rt><rb>。</rb><rt></rt></ruby>
```

![HTML as rendered in Safari](/rendered.png)
