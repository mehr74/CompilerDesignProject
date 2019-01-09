<div dir="rtl" align="right">

## حذف چپ گردی (Left Recursion)
همانطور که می‌دانیم گرامری را چپ‌گرد می‌گویند، که غیر‌پایانه سمت چپ یک قاعده آن به عنوان به عنوان اولین علامت سمت راست آن قاعده ظاهر شده باشد، به عبارت دیگر، قاعده‌ای به صورت `A → Aα` داشته باشیم.

روش‌های پارس بالا به پایین را نمی‌توان برای گرامری که چپ‌گردی داشته باشد، به کار برد. از این رو باید چپ‌گردی گرامر را حذف کنیم. یعنی گرامر را به گرامری معادل تبدیل کنیم که در آن چپ‌گردی وجود نداشته باشد. برای مثال، گرامر چپ‌گرد  `A → Aα|β` را می‌توان به فرم زیر که چپ‌گردی ندارد، تبدیل نمود:
</div>

```
A → βA'
A' → αA'|ε
```

<div dir="rtl" align="right">
هر دو گرامر فوق رشته‌های به فرم `*βα` توصیف می‌کند.

روش کلی حذف چپ‌گردی به صورت زیر است، توجه کنید که اهمیتی ندارد که چه تعداد از قواعد چپ باشند. به طور کلی، اگر داشته باشیم: 
</div>

```
A → Aα1|Aα2|...|Aαm|β1|β2|...|βn
```

<div dir="rtl" align="right">
  
در قواعد فوق، فرض بر این است که `βi` نباید با `A` شروع شوند و هیچ کدام از `αi` نباید `ε` باشند. در این صورت می‌توان قواعد زیر را به جای قواعد چپ‌گرد فوق به کار برد:

</div>

```
A → β1A'|β2A'|...|βnA'
A' → α1A'|α2A'|...|αmA'|ε
```

<div dir="rtl" align="right">
  
این گونه چپ گردی‌ها را چپ‌گردی آشکار `(Explicit Left Recursion)` می‌گویند. 

ممکن است، چپ‌گردی در بیش از یک قدم ظاهر شود، به آن چپ‌گردی ضمنی گویند. به عنوان مثال، گرامر زیر دارای چپ‌گردی ضمنی است. 

</div>


| Left-recursion rule           | Alternative non-left recursion rule  |
|:-------------| :-----|
| declaration-list → declaration-list declaration \| declaration | declaration-list → declaration declaration-list \| declaration |
| param-list → param-list **,** param \| param | param-list → param param-list-a <br> param-list-a → **,** param param-list-a \| **ε** |
| statement-list → statement-list statement \| **ε** | statement-list → statement statement-list \| **ε**  |
| case-stmts → case-stmts case-stmt \| **ε** | case-stmts → case-stmt case-stmts \| **ε**|
| additive-expression → additive-expression addop term \| term | additive-expression → term additive-expression-a <br> additive-expression-a → addop term additive-expression-a \| **ε** |
| term → term * factor \| factor | term → factor term-a <br> term-a → * factor term-a \| **ε** |
| arg-list → arg-list **,** expression \| expression | arg-list → expression arg-list-a <br> arg-list-a → **,** expression arg-list-a \| **ε** |

بنابراین قواعد پس از حذف چپ‌گردی آشکار به صورت زیر خواهد بود.

1. program → declaration-list **EOF**
2. declaration-list → declaration declaration-list | declaration
3. declaration → var-declaration | fun-declaration
4. var-declaration → type-specifier **ID ;** | type-specifier **ID [ NUM ] ;**
5. type-specifier → **int** | **void**
6. fun-declaration → type-specifier **ID (** params **)** compound-stmt
7. params → param-list | **void**
8. param-list → param param-list-a 
9. param-list-a → **,** param param-list-a | **ε** 
10. param → type-specifier **ID** | type-specifier **ID []**
11. compound-stms → **{** declaration-list statement-list **}**
12. statement-list → statement statement-list | **ε** 
13. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | switch-stmt
14. expression-stmt → expression **;** | **continue ;** | **break ;** | **;**
15. selection-stmt → **if (** expression **)** statement **else** statement
16. iteration-stmt → **return ;** | **return** expression **;**
17. return-stmt → **return ;** | **return** expression **;**
18. switch-stmt → **switch (** expression **) {** case-stmts default-stmt **}**
19. case-stmts → case-stmt case-stmts | **ε**
20. case-stmt → **case NUM :** statement-list
21. default-stmt → **default :** statement-list | **ε**
22. expression → var **=** expression | simple-expression
23. var → **ID** | **ID [** expression **]**
24. simple-expression → additive-expression relop additive-expression | additive-expression
25. relop → **<** | **==**
26. additive-expression → term additive-expression-a 
27. additive-expression-a → addop term additive-expression-a | **ε** 
28. addop → **+** | **-**
29. term → term * factor | factor
30. term → factor term-a
31. term-a → * factor term-a \| **ε**
32. call → **ID (** args **)**
33. args → arg-list | **ε**
34. arg-list → expression arg-list-a 
35. arg-list-a → **,** expression arg-list-a | **ε**




