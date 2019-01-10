<div dir="rtl" align="right">

## حذف چپ گردی آشکار (Explicit Left Recursion)
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

<div dir="rtl" align="right">

بنابراین قواعد پس از حذف چپ‌گردی آشکار به صورت زیر خواهد بود.

</div>

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
29. term → factor term-a
30. term-a → * factor term-a | **ε**
31. factor → **(** expression **)** | var | call | **NUM**
32. call → **ID (** args **)**
33. args → arg-list | **ε**
34. arg-list → expression arg-list-a 
35. arg-list-a → **,** expression arg-list-a | **ε**

<div dir="rtl" align="right">
## حذف چپ گردی ضمنی (Implicit Left Recursion)

ورودی الگوریتم گرامر G با این شرط که قاعده اپسیلون نداشته باشد و هیچ دوری نیز در گرامر موجود نباشد. یعنی بسط‌هایی به صورت `A → +A` در گرامر نباشد. خروجی الگوریتم، گرامری معادل گرامر G، اما فاقد چپ‌گردی است. ابتدا غیر‌پایانه‌های گرامر را به ترتیب دلخواه A1, A2, ..., An مرتب می‌کنیم. سپس اعمال زیر را به صورت مشخص شده در حلقه‌های تکرار اجرا می‌کنیم:

</div>

```
For i := 1 to n do begin
  For j := 1 to i - 1 do begin
    replace each production of the form Ai → AjY
    by the productions Ai → δ1Y|δ2Y|...|δkY
    where Aj → δ1|δ2|...|δk are all current Aj productions;
  end
end
```

| Non-terminal           | Alternative non-terminal  |
|:-------------| :-----|
| program | A1 |
| declaration-list | A2 |
| declaration | A3 |
| var-declaration | A4 |
| fun-declaration | A5 |
| params | A6 |
| param-list | A7 |
| param | A8 |
| statement-list | A9 |
| statement | A10 |
| expression-stmt | A11 | 
| case-stmts | A12 |
| expression | A13 |
| simple-expression | A14 |
| additive-expression | A15 |
| additive-expression-a | A16 |
| term | A17 |
| term-a | A18 |
| args | A18 |
| arg-list | A19 |
| type-specifier | A20 |
| param-list-a | A21 |
| compound-stms | A22 |
| selection-stmt | A23 |
| iteration-stmt | A24 |
| return-stmt | A25 |
| switch-stmt | A26 |
| case-stmt | A27 |
| default-stmt | A28 |
| var | A29 | 
| relop | A30 | 
| addop | A31 | 
| term | A32 | 
| factor | A33 |
| call | A34 |
| arg-list-a | A35 |
 

1. A1 → A2 **EOF**
2. A2 → A3 A2 | A3
3. A3 → A4 | A5
4. A4 → A20 **ID ;** | A20 **ID [ NUM ] ;**
5. A20 → **int** | **void**
6. A5 → A20 **ID (** A6 **)** compound-stmt
7. A6 → A7 | **void**
8. A7 → A8 A21 
9. A21 → **,** A8 A21 | **ε** 
10. A8 → A20 **ID** | A20 **ID []**
11. A22 → **{** A2 A9 **}**
12. A9 → A10 A9 | **ε** 
13. A10 → A11 | compound-stmt | A23 | A24 | A25 | A26
14. A11 → A13 **;** | **continue ;** | **break ;** | **;**
15. A23 → **if (** A13 **)** A10 **else** A10
16. A24 → **return ;** | **return** A13 **;**
17. A25 → **return ;** | **return** A13 **;**
18. A26 → **switch (** A13 **) {** A12 A28 **}**
19. A12 → A27 A12 | **ε**
20. A27 → **case NUM :** A9
21. A28 → **default :** A9 | **ε**
22. A13 → A29 **=** A13 | A14
23. A29 → **ID** | **ID [** A13 **]**
24. A14 → A15 A30 A15 | A15
25. A30 → **<** | **==**
26. A15 → A32 A16 
27. A16 → A31 A32 A16 | **ε** 
28. A31 → **+** | **-**
29. A32 → A33 A18
30. A18 → * A33 A18 | **ε**
31. A33 → **(** A13 **)** | A29 | A34 | **NUM**
32. A34 → **ID (** A18 **)**
33. A18 → A19 | **ε**
34. A19 → A13 A35 
35. A35 → **,** A13 A35 | **ε**





