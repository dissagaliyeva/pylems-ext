### PyLEMS extension for code traversal 

This package is created for code traversal and model's equations and parameters storage. The idea behind it is to 
automatically traverse Python code and find the models and its parameters. Then, depending on the found model, 
alter its default values with the newly-found parameters. Next, create a PyLEMS model supplementing the new values. 
Finally, create the XML file(s) in the specified folder.

#### Currently supported models

- HindmarshRose


---


### Getting started

Simply fork the project or run the following command:

```
pip install pylems-py2xml
```

After that, the steps are pretty straightforward. Run the following:

```
import pylems_py2xml

pylems_py2xml.main.XML(input_path='examples/50healthy_code.py', output_path='examples')
```

A couple of arguments to be aware of:

- *input_path*: path to Python code that includes models (e.g., HindmarshRose, WongWang)
- *output_path*: path to the folder where to store results. By default, everything gets stored in the `examples` folder. 
- *units*: 
- *uid*:
- *app*:
- *store_numeric*:
- *suffix*:

You can follow the instructions [in this Jupyter notebook](https://github.com/dissagaliyeva/pylems-ext/blob/master/notebooks/example.ipynb)


### Walk-through

Here is an example taken from `examples/50healthy_code.py`:
```
oscilator = models.ReducedSetHindmarshRose(r=[0.006], a=[1.0], b=[3.0], c=[1.0], d=[5.0], s=[4.0], xo=[-1.6], K11=[0.5],
                                           K12=[0.1], K21=[0.15], sigma=[0.3], mu=[2.2],
                                           variables_of_interest=["xi", "alpha"])
```


