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

</div>


| Left-recursion rule           | Alternative non-left recursion rule  |
|:-------------| :-----|
| declaration-list → declaration-list declaration \| declaration | declaration-list → declaration declaration-list-a <br> declaration-list-a → declaration declaration-list-a \| **ε** |
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
2. declaration-list → declaration declaration-list-a 
3. declaration-list-a → declaration declaration-list-a | **ε** 
4. declaration → var-declaration | fun-declaration
5. var-declaration → type-specifier **ID ;** | type-specifier **ID [ NUM ] ;**
6. type-specifier → **int** | **void**
7. fun-declaration → type-specifier **ID (** params **)** compound-stmt
8. params → param-list | **void**
9. param-list → param param-list-a 
10. param-list-a → **,** param param-list-a | **ε** 
11. param → type-specifier **ID** | type-specifier **ID [ ]**
12. compound-stmt → **{** declaration-list statement-list **}**
13. statement-list → statement statement-list | **ε** 
14. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | switch-stmt
15. expression-stmt → expression **;** | **continue ;** | **break ;** | **;**
16. selection-stmt → **if (** expression **)** statement **else** statement
17. iteration-stmt → **while (** expression **)** statement
18. return-stmt → **return ;** | **return** expression **;**
19. switch-stmt → **switch (** expression **) {** case-stmts default-stmt **}**
20. case-stmts → case-stmt case-stmts | **ε**
21. case-stmt → **case NUM :** statement-list
22. default-stmt → **default :** statement-list | **ε**
23. expression → var **=** expression | simple-expression
24. var → **ID** | **ID [** expression **]**
25. simple-expression → additive-expression relop additive-expression | additive-expression
26. relop → **<** | **==**
27. additive-expression → term additive-expression-a 
28. additive-expression-a → addop term additive-expression-a | **ε** 
29. addop → **+** | **-**
30. term → factor term-a
31. term-a → * factor term-a | **ε**
32. factor → **(** expression **)** | var | call | **NUM**
33. call → **ID (** args **)**
34. args → arg-list | **ε**
35. arg-list → expression arg-list-a 
36. arg-list-a → **,** expression arg-list-a | **ε**

<div dir="rtl" align="right">

## حذف چپ گردی ضمنی (Implicit Left Recursion)

ورودی الگوریتم گرامر G با این شرط که قاعده`ε` نداشته و هیچ دوری نیز در گرامر موجود نباشد. یعنی بسط‌هایی به صورت `A → +A` در گرامر نباشد. خروجی الگوریتم، گرامری معادل گرامر G، اما فاقد چپ‌گردی است. ابتدا غیر‌پایانه‌های گرامر را به ترتیب دلخواه A1, A2, ..., An مرتب می‌کنیم. سپس اعمال زیر را به صورت مشخص شده در حلقه‌های تکرار اجرا می‌کنیم:

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
|  declaration-list-a | A0 | 
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
| args | A13 |
| simple-expression | A14 |
| additive-expression | A15 |
| additive-expression-a | A16 |
| term | A17 |
| term-a | A18 |
| arg-list | A19 |
| expression | A20 |
| type-specifier | A21 |
| param-list-a | A22 |
| compound-stmt | A23 |
| selection-stmt | A24 |
| iteration-stmt | A25 |
| return-stmt | A26 |
| switch-stmt | A27 |
| case-stmt | A28 |
| default-stmt | A29 |
| var | A30 | 
| relop | A31 | 
| addop | A32 | 
| factor | A33 |
| call | A34 |
| arg-list-a | A35 |

1. A1 → A2 **EOF**
2. A2 → A3 A0
3. A0 → A3 A0 | **ε** 
4. A3 → A4 | A5
5. A4 → A21 **ID ;** | A21 **ID [ NUM ] ;**
6. A21 → **int** | **void**
7. A5 → A21 **ID (** A6 **)** A23
8. A6 → A7 | **void**
9. A7 → A8 A22 
10. A22 → **,** A8 A22 | **ε** 
11. A8 → A21 **ID** | A21 **ID [ ]**
12. A23 → **{** A2 A9 **}**
13. A9 → A10 A9 | **ε** 
14. A10 → A11 | A23 | A24 | A25 | A26 | A27
15. A11 → A20 **;** | **continue ;** | **break ;** | **;**
16. A24 → **if (** A20 **)** A10 **else** A10
17. A25 → **while (** A20 **)** A10
18. A26 → **return ;** | **return** A20 **;**
19. A27 → **switch (** A20 **) {** A12 A29 **}**
20. A12 → A28 A12 | **ε**
21. A28 → **case NUM :** A9
22. A29 → **default :** A9 | **ε**
23. A20 → A30 **=** A20 | A14
24. A30 → **ID** | **ID [** A20 **]**
25. A14 → A15 A31 A15 | A15
26. A31 → **<** | **==**
27. A15 → A17 A16 
28. A16 → A32 A17 A16 | **ε** 
29. A32 → **+** | **-**
30. A17 → A33 A18
31. A18 → * A33 A18 | **ε**
32. A33 → **(** A20 **)** | A30 | A34 | **NUM**
33. A34 → **ID (** A13 **)**
34. A13 → A19 | **ε**
35. A19 → A20 A35 
36. A35 → **,** A20 A35 | **ε**


<div dir="rtl" align="right">


## فاکتور گیری از چپ (Left Factoring)
با استفاده از فاکتورگیری از چپ، می‌توان گرامر‌هایی که در آن ها برای غیرپایانه `A` دو قاعده به صورت ?? و ?? وجود دارد طوری تغییر داد که بتوان پارس بالا به پایین را برای این گرامر‌ها استفاده کرد.
مشکل این قبیل گرامر‌ها در این است که روشن نیست که از کدام یک از قواعد باید برای بسط غیرپایانه A استفاده کرد.

</div>


| Left-factor rule           | Alternative non-left-factor rule  |
|:-------------| :-----|
| var-declaration → type-specifier **ID ;** \| type-specifier **ID [ NUM ] ;** | var-declaration → type-specifier **ID** var-declaration-a <br> var-declaration-a → **;** \| **[ NUM ] ;** |
| param → type-specifier **ID** \| type-specifier **ID [ ]** | param → type-specifier **ID** param-a <br> param-a → **ε** \| **[ ]**  | 
| return-stmt → **return ;** \| **return** expression **;** | return-stmt → **return** return-stmt-a <br> return-stmt-a → **;** \| expression **;** | 
| var → **ID** \| **ID [** expression **]** | var → **ID** var-a <br> var-a → **ε** \| **[** expression **]** |
| simple-expression → additive-expression relop additive-expression \| additive-expression | simple-expression → additive-expression simple-expression-a <br> simple-expression-a → relop additive-expression \| **ε** |


بنابراین قواعد پس از فاکتورگیری از چپ به صورت زیر خواهد بود.


1. program → declaration-list **EOF**
2. declaration-list → declaration declaration-list-a 
3. declaration-list-a → declaration declaration-list-a | **ε** 
4. declaration → var-declaration | fun-declaration
5. var-declaration → type-specifier **ID** var-declaration-a 
6. var-declaration-a → **;** | **[ NUM ] ;** 
7. type-specifier → **int** | **void**
8. fun-declaration → type-specifier **ID (** params **)** compound-stmt
9. params → param-list | **void**
10. param-list → param param-list-a 
11. param-list-a → **,** param param-list-a | **ε** 
12. param → type-specifier **ID** param-a
13. param-a → **ε** \| **[ ]**
14. compound-stmt → **{** declaration-list statement-list **}**
15. statement-list → statement statement-list | **ε** 
16. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | switch-stmt
17. expression-stmt → expression **;** | **continue ;** | **break ;** | **;**
18. selection-stmt → **if (** expression **)** statement **else** statement
19. iteration-stmt → **while (** expression **)** statement
20. return-stmt → **return** return-stmt-a 
21. return-stmt-a → **;** \| expression **;**
22. switch-stmt → **switch (** expression **) {** case-stmts default-stmt **}**
23. case-stmts → case-stmt case-stmts | **ε**
24. case-stmt → **case NUM :** statement-list
25. default-stmt → **default :** statement-list | **ε**
26. expression → var **=** expression | simple-expression
27. var → **ID** var-a 
28. var-a → **ε** | **[** expression **]**
29. simple-expression → additive-expression simple-expression-a
30. simple-expression-a → relop additive-expression \| **ε**
31. relop → **<** | **==**
32. additive-expression → term additive-expression-a 
33. additive-expression-a → addop term additive-expression-a | **ε** 
34. addop → **+** | **-**
35. term → factor term-a
36. term-a → * factor term-a | **ε**
37. factor → **(** expression **)** | var | call | **NUM**
38. call → **ID (** args **)**
39. args → arg-list | **ε**
40. arg-list → expression arg-list-a 
41. arg-list-a → **,** expression arg-list-a | **ε**



| Left-factor rule           | Alternative non-left-factor rule  |
|:-------------| :-----|
| declaration → var-declaration \| fun-declaration <br> var-declaration → type-specifier **ID** var-declaration-a <br> fun-declaration → type-specifier **ID (** params **)** compound-stmt | declaration → type-specifier **ID** declaration-a <br> declaration-a → var-declaration \| fun-declaration <br> var-declaration → var-declaration-a <br> fun-declaration → **(** params **)** compound-stmt|
| params → param-list \| **void** <br> param-list → param param-list-a <br> param → type-specifier **ID** param-a <br> type-specifier → **int** \| **void** | |
| expression → var **=** expression \| simple-expression <br> var → **ID** var-a <br> simple-expression → additive-expression simple-expression-a <br> additive-expression → term additive-expression-a <br> term → factor term-a <br> factor → **(** expression **)** \| var \| call \| **NUM** <br> call → **ID (** args **)** | 
| factor → **(** expression **)** \| var \| call \| **NUM** <br> call → **ID (** args **)** <br> var → **ID** var-a  | factor → **(** expression **)** \| **ID** factor-a \| **NUM** <br> factor-a → var-a \| call <br> call → **(** args **)** | 


