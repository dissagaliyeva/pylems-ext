### PyLEMS extension for code traversal 

This package is created for code traversal and model's equations and parameters storage. The idea behind it is to 
automatically traverse Python code and find the models and its parameters. Then, depending on the found model, 
alter its default values with the newly-found parameters. Next, create a PyLEMS model supplementing the new values. 
Finally, create the XML file(s) in the specified folder.


### Walk-through

Here is an example taken from `examples/50healthy_code.py`:
```
oscilator = models.ReducedSetHindmarshRose(r=[0.006], a=[1.0], b=[3.0], c=[1.0], d=[5.0], s=[4.0], xo=[-1.6], K11=[0.5],
                                           K12=[0.1], K21=[0.15], sigma=[0.3], mu=[2.2],
                                           variables_of_interest=["xi", "alpha"])
```


