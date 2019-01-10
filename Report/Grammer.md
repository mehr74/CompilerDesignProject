1. program → declaration-list **EOF**
2. declaration-list → declaration-list declaration | declaration
3. declaration → var-declaration | fun-declaration
4. var-declaration → type-specifier **ID ;** | type-specifier **ID [ NUM ] ;**
5. type-specifier → **int** | **void**
6. fun-declaration → type-specifier **ID (** params **)** compound-stmts
7. params → param-list | **void**
8. param-list → param-list **,** param | param
9. param → type-specifier **ID** | type-specifier **ID []**
10. compound-stms → **{** declaration-list statement-list **}**
11. statement-list → statement-list statement | **ε**
12. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | switch-stmt
13. expression-stmt → expression **;** | **continue ;** | **break ;** | **;**
14. selection-stmt → **if (** expression **)** statement **else** statement
15. iteration-stmt → **return ;** | **return** expression **;**
16. return-stmt → **return ;** | **return** expression **;**
17. switch-stmt → **switch (** expression **) {** case-stmts default-stmt **}**
18. case-stmts → case-stmts case-stmt | **ε**
19. case-stmt → **case NUM :** statement-list
20. default-stmt → **default :** statement-list | **ε**
21. expression → var **=** expression | simple-expression
22. var → **ID** | **ID [** expression **]**
23. simple-expression → additive-expression relop additive-expression | additive-expression
24. relop → **<** | **==**
25. additive-expression → additive-expression addop term | term
26. addop → **+** | **-**
27. term → term * factor | factor
28. factor → **(** expression **)** | var | call | **NUM**
29. call → **ID (** args **)**
30. args → arg-list | **ε**
31. arg-list → arg-list **,** expression | expression
