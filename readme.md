# Bias Expire Dict 偏差过期字典

*An incomplete and imperfect solution for expiring dict.*

``` python
>>> d = BiasExpireDict(expire=4, bias=1)
>>> d['BiasExpireDict'] = 'foo'
>>> time.sleep(2)
>>> d
{'BiasExpireDict': 'foo'}
>>> time.sleep(3)
>>> d['BiasExpireDict']
Traceback (most recent call last):
...
KeyError: 'BiasExpireDict'
>>> d.update({'ExpireDict': 'foo'}, ExpireDict='foo_', BiasDict='foo_')
{'ExpireDict': 'foo_', 'BiasDict': 'foo_'}
```

The final key expiring time is between **'expire'** and **'expire'+'bias'**

Smaller bias means more accurate expire time but more resources consumption

Usages that might be malfunctioning:
> - big data
> - tiny bias