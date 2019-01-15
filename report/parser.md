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
| declaration-list → declaration-list declaration \| **ε** | declaration-list → declaration declaration-list \| **ε** |
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
2. declaration-list → declaration declaration-list | **ε** 
3. declaration → var-declaration | fun-declaration
4. var-declaration → type-specifier **ID ;** | type-specifier **ID [ NUM ] ;**
5. type-specifier → **int** | **void**
6. fun-declaration → type-specifier **ID (** params **)** compound-stmt
7. params → param-list | **void**
8. param-list → param param-list-a 
9. param-list-a → **,** param param-list-a | **ε** 
10. param → type-specifier **ID** | type-specifier **ID [ ]**
11. compound-stmt → **{** declaration-list statement-list **}**
12. statement-list → statement statement-list | **ε** 
13. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | switch-stmt
14. expression-stmt → expression **;** | **continue ;** | **break ;** | **;**
15. selection-stmt → **if (** expression **)** statement **else** statement
16. iteration-stmt → **while (** expression **)** statement
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
2. A2 → A3 A2 | **ε** 
3. A3 → A4 | A5
4. A4 → A21 **ID ;** | A21 **ID [ NUM ] ;**
5. A21 → **int** | **void**
6. A5 → A21 **ID (** A6 **)** A23
7. A6 → A7 | **void**
8. A7 → A8 A22 
9. A22 → **,** A8 A22 | **ε** 
10. A8 → A21 **ID** | A21 **ID [ ]**
11. A23 → **{** A2 A9 **}**
12. A9 → A10 A9 | **ε** 
13. A10 → A11 | A23 | A24 | A25 | A26 | A27
14. A11 → A20 **;** | **continue ;** | **break ;** | **;**
15. A24 → **if (** A20 **)** A10 **else** A10
16. A25 → **while (** A20 **)** A10
17. A26 → **return ;** | **return** A20 **;**
18. A27 → **switch (** A20 **) {** A12 A29 **}**
19. A12 → A28 A12 | **ε**
20. A28 → **case NUM :** A9
21. A29 → **default :** A9 | **ε**
22. A20 → A30 **=** A20 | A14
23. A30 → **ID** | **ID [** A20 **]**
24. A14 → A15 A31 A15 | A15
25. A31 → **<** | **==**
26. A15 → A17 A16 
27. A16 → A32 A17 A16 | **ε** 
28. A32 → **+** | **-**
29. A17 → A33 A18
30. A18 → * A33 A18 | **ε**
31. A33 → **(** A20 **)** | A30 | A34 | **NUM**
32. A34 → **ID (** A13 **)**
33. A13 → A19 | **ε**
34. A19 → A20 A35 
35. A35 → **,** A20 A35 | **ε**

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
2. declaration-list → declaration declaration-list | **ε** 
3. declaration → var-declaration | fun-declaration
4. var-declaration → type-specifier **ID** var-declaration-a 
5. var-declaration-a → **;** | **[ NUM ] ;** 
6. type-specifier → **int** | **void**
7. fun-declaration → type-specifier **ID (** params **)** compound-stmt
8. params → param-list | **void**
9. param-list → param param-list-a 
10. param-list-a → **,** param param-list-a | **ε** 
11. param → type-specifier **ID** param-a
12. param-a → **ε** \| **[ ]**
13. compound-stmt → **{** declaration-list statement-list **}**
14. statement-list → statement statement-list | **ε** 
15. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | switch-stmt
16. expression-stmt → expression **;** | **continue ;** | **break ;** | **;**
17. selection-stmt → **if (** expression **)** statement **else** statement
18. iteration-stmt → **while (** expression **)** statement
19. return-stmt → **return** return-stmt-a 
20. return-stmt-a → **;** \| expression **;**
21. switch-stmt → **switch (** expression **) {** case-stmts default-stmt **}**
22. case-stmts → case-stmt case-stmts | **ε**
23. case-stmt → **case NUM :** statement-list
24. default-stmt → **default :** statement-list | **ε**
25. expression → var **=** expression | simple-expression
26. var → **ID** var-a 
27. var-a → **ε** | **[** expression **]**
28. simple-expression → additive-expression simple-expression-a
29. simple-expression-a → relop additive-expression \| **ε**
30. relop → **<** | **==**
31. additive-expression → term additive-expression-a 
32. additive-expression-a → addop term additive-expression-a | **ε** 
33. addop → **+** | **-**
34. term → factor term-a
35. term-a → * factor term-a | **ε**
36. factor → **(** expression **)** | var | call | **NUM**
37. call → **ID (** args **)**
38. args → arg-list | **ε**
39. arg-list → expression arg-list-a 
40. arg-list-a → **,** expression arg-list-a | **ε**



| Left-factor rule           | Alternative non-left-factor rule  |
|:-------------| :-----|
| declaration → var-declaration \| fun-declaration <br> var-declaration → type-specifier **ID** var-declaration-a <br> fun-declaration → type-specifier **ID (** params **)** compound-stmt | declaration → type-specifier **ID** declaration-a <br> declaration-a → var-declaration-a \| fun-declaration <br> fun-declaration → **(** params **)** compound-stmt |
| params → param-list \| **void** <br> param-list → param param-list-a <br> param → type-specifier **ID** param-a <br> type-specifier → **int** \| **void** | params → **void** params-a \| **int ID** param-a param-list-a <br> params-a → **ID** param-a param-list-a \| **ε** <br> param → type-specifier ID param-a <br> type-specifier → **int** \| **void** |
| factor → **(** expression **)** \| var \| call \| **NUM** <br> call → **ID (** args **)** <br> var → **ID** var-a  | factor → **(** expression **)** \| **ID** factor-a \| **NUM** <br> factor-a → var-a \| call <br> call → **(** args **)** | 
| expression → var **=** expression \| simple-expression <br> var → **ID** var-a <br> simple-expression → additive-expression simple-expression-a <br> additive-expression → term additive-expression-a <br> term → factor term-a <br> factor → **(** expression **)** \| **ID** factor-a \| **NUM** | expression → <br> **ID** expression-a \| <br> **(** expression **)** term-a additive-expression-a simple-expression-a \| <br> **NUM** term-a additive-expression-a simple-expression-a <br> expression-a → var-a expression-b \| call term-a additive-expression-a simple-expression-a<br> expression-b → term-a additive-expression-a simple-expression-a \| **ε** <br>


<br>

1. program → declaration-list **EOF**
2. declaration-list → declaration declaration-list | **ε** 
3. declaration → type-specifier **ID** declaration-a
4. declaration-a → var-declaration | fun-declaration 
5. var-declaration → **;** | **[ NUM ] ;** 
6. type-specifier → **int** | **void**
7. fun-declaration → **(** params **)** compound-stmt 
8. params → **void** params-a | **int ID** param-a param-list
9. params-a → **ID** param-a param-list | **ε**
10. param-list → **,** param param-list | **ε** 
11. param → type-specifier **ID** param-a
12. param-a → **ε** \| **[ ]**
13. compound-stmt → **{** declaration-list statement-list **}**
14. statement-list → statement statement-list | **ε** 
15. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | switch-stmt
16. expression-stmt → expression **;** | **continue ;** | **break ;** | **;**
17. selection-stmt → **if (** expression **)** statement **else** statement
18. iteration-stmt → **while (** expression **)** statement
19. return-stmt → **return** return-stmt-a 
20. return-stmt-a → **;** | expression **;**
21. switch-stmt → **switch (** expression **) {** case-stmts default-stmt **}**
22. case-stmts → case-stmt case-stmts | **ε**
23. case-stmt → **case NUM :** statement-list
24. default-stmt → **default :** statement-list | **ε**
25. expression → **ID** expression-a | **(** expression **)** term-a additive-expression-a simple-expression | **NUM** term-a additive-expression-a simple-expression
26. expression-a → var expression-b | call term-a additive-expression-a simple-expression
27. expression-b → term-a additive-expression-a simple-expression | **=** expression
28. var → **ε** | **[** expression **]**
29. simple-expression → relop additive-expression | **ε**
30. relop → **<** | **==**
31. additive-expression → term additive-expression-a 
32. additive-expression-a → addop term additive-expression-a | **ε** 
33. addop → **+** | **-**
34. term → factor term-a
35. term-a → * factor term-a | **ε**
36. factor → **(** expression **)** | **ID** factor-a | **NUM**
37. factor-a → var | call
38. call → **(** args **)**
39. args → arg-list | **ε**
40. arg-list → expression arg-list-a 
41. arg-list-a → **,** expression arg-list-a | **ε**



<br>


1. program → declaration-list **EOF**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/01.png)
2. 2. declaration-list → declaration declaration-list | **ε** 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/03.png)
3. declaration → type-specifier **ID** declaration-a
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/04.png)
4. declaration-a → var-declaration | fun-declaration 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/05.png)
5. var-declaration → **;** | **[ NUM ] ;** 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/06.png)
6. type-specifier → **int** | **void**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/07.png)
7. fun-declaration → **(** params **)** compound-stmt 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/08.png)
8. params → **void** params-a | **int ID** param-a param-list
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/09.png)
9. params-a → **ID** param-a param-list | **ε**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/10.png)
10. param-list → **,** param param-list | **ε** 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/11.png)
11. param → type-specifier **ID** param-a
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/12.png)
12. param-a → **ε** \| **[ ]**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/13.png)
13. compound-stmt → **{** declaration-list statement-list **}**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/14.png)
14. statement-list → statement statement-list | **ε** 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/15.png)
15. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | switch-stmt
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/16.png)
16. expression-stmt → expression **;** | **continue ;** | **break ;** | **;**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/17.png)
17. selection-stmt → **if (** expression **)** statement **else** statement
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/18.png)
18. iteration-stmt → **while (** expression **)** statement
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/19.png)
19. return-stmt → **return** return-stmt-a 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/20.png)
20. return-stmt-a → **;** | expression **;**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/21.png)
21. switch-stmt → **switch (** expression **) {** case-stmts default-stmt **}**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/22.png)
22. case-stmts → case-stmt case-stmts | **ε**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/23.png)
23. case-stmt → **case NUM :** statement-list
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/24.png)
24. default-stmt → **default :** statement-list | **ε**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/25.png)
25. expression → **ID** expression-a | **(** expression **)** term-a additive-expression-a simple-expression | **NUM** term-a additive-expression-a simple-expression
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/26.png)
26. expression-a → var expression-b | call term-a additive-expression-a simple-expression
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/27.png)
27. expression-b → term-a additive-expression-a simple-expression | **ε** 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/28.png)
28. var → **ε** | **[** expression **]**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/29.png)
29. simple-expression → relop additive-expression | **ε**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/30.png)
30. relop → **<** | **==**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/31.png)
31. additive-expression → term additive-expression-a 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/32.png)
32. additive-expression-a → addop term additive-expression-a | **ε** 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/33.png)
33. addop → **+** | **-**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/34.png)
34. term → factor term-a
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/35.png)
35. term-a → * factor term-a | **ε**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/36.png)
36. factor → **(** expression **)** | **ID** factor-a | **NUM**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/37.png)
37. factor-a → var | call
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/38.png)
38. call → **(** args **)**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/39.png)
39. args → arg-list | **ε**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/40.png)
40. arg-list → expression arg-list-a 
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/41.png)
41. arg-list-a → **,** expression arg-list-a | **ε**
<br>![alt text](https://github.com/mehr74/CompilerDesignProject/blob/master/report/images/42.png)



