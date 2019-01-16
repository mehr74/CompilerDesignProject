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
17. selection-stmt → **if (** expression **)** *#save* statement *#jpf-save* **else** statement *#jp*
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


*#save*
```python
case "#save":
	push(i)
	i = i + 1
	break
```

*#jpf-save*
```python
case "#jpf-save":
	PB[ss(top)] = "(jpf, ss(top-1), i+1)"
	pop(2)
	push(i)
	i = i+1
	break
```

*#jp*
```python
case "#jp":
	PB[ss(top)] = "(jp, i, , )"
	pop(1)
	break
```


