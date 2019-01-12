1. program → declaration-list **EOF**
2. declaration-list → declaration declaration-list-a 
3. declaration-list-a → declaration declaration-list-a | **ε** 
4. declaration → type-specifier **ID** declaration-a
5. declaration-a → var-declaration | fun-declaration 
6. var-declaration → **;** | **[ NUM ] ;** 
7. type-specifier → **int** | **void**
8. fun-declaration → **(** params **)** compound-stmt 
9. params → **void** params-a | **int ID** param-a param-list
10. params-a → **ID** param-a param-list | **ε**
11. param-list → **,** param param-list | **ε** 
12. param → type-specifier **ID** param-a
13. param-a → **ε** \| **[ ]**
14. compound-stmt → **{** declaration-list statement-list **}**
15. statement-list → statement statement-list | **ε** 
16. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt | switch-stmt
17. expression-stmt → expression **;** | **continue ;** | **break ;** | **;**
18. selection-stmt → **if (** expression **)** <span style="color:red;">**#save**</span> statement <span style="color:red;">**#jpf-save**</span> **else** statement <span style="color:red;">**#jp**</span>
19. iteration-stmt → **while (** expression **)** statement
20. return-stmt → **return** return-stmt-a 
21. return-stmt-a → **;** | expression **;**
22. switch-stmt → **switch (** expression **) {** case-stmts default-stmt **}**
23. case-stmts → case-stmt case-stmts | **ε**
24. case-stmt → **case NUM :** statement-list
25. default-stmt → **default :** statement-list | **ε**
26. expression → **ID** expression-a | **(** expression **)** term-a additive-expression-a simple-expression | **NUM** term-a additive-expression-a simple-expression
27. expression-a → var expression-b | call term-a additive-expression-a simple-expression
28. expression-b → term-a additive-expression-a simple-expression | **ε** 
29. var → **ε** | **[** expression **]**
30. simple-expression → relop additive-expression | **ε**
31. relop → **<** | **==**
32. additive-expression → term additive-expression-a 
33. additive-expression-a → addop term additive-expression-a | **ε** 
34. addop → **+** | **-**
35. term → factor term-a
36. term-a → * factor term-a | **ε**
37. factor → **(** expression **)** | **ID** factor-a | **NUM**
38. factor-a → var | call
39. call → **(** args **)**
40. args → arg-list | **ε**
41. arg-list → expression arg-list-a 
42. arg-list-a → **,** expression arg-list-a | **ε**


* <span style="color:red;">**#save**</span>
```python
case "#save":
	push(i)
	i = i + 1
	break
```

* <span style="color:red;">**#jpf-save**</span>
```python
case "#jpf-save":
	PB[ss(top)] = "(jpf, ss(top-1), i+1)"
	pop(2)
	push(i)
	i = i+1
	break
```
