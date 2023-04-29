# Sensitivity Analysis 1 - SALib - 2023-04-28

## tldr;

`SALib` is a library and command line tool for sensitivity analysis. Sensitivity
analysis is used for:

1. Finding the most important factors in a model (factor prioritization)
2. Determining which factors can be ignored (factor fixing)
3. Determining which factors are most influential over a specific output space
   (factor mapping)

SALib implements several methods commonly used for sensitivity analysis and is
aimed at usage with engineering and optimization models.

## Sobol Example

Sobol seems to be the gold standard in sensitivity analysis. It is a global
analysis, meaning the entire set of input parameters is explored at the same
time. This is more robust than commonly used one at a time (OAT) methods, which
are sometimes useful because they are faster, but are less robust.

A sensitivity analysis commonly has 3 phases:

1. Generating sample inputs for the model

Define the variables and their upper and lower bounds for each in a file

```bash
cat << EOF > problem.txt
x1 -3.14159265359 3.14159265359
x2 -3.14159265359 3.14159265359
x3 -3.14159265359 3.14159265359
EOF
```

Use a sampling method to generate sample parameter sets

```bash
# The saltelli method is named after Andrea Saltelli, a prominent researcher in the field...
python3 -m SALib.sample.saltelli \
    -n 1024 \ # this is arbitrary, but there are methods for determining the best sample size
    -p problem.txt \
    -o params.txt
```

2. Running the model to capture the simulated outputs

The model can be in any language. If you're already in Python, you might just
prefer libary usage, but it's handy to know the CLI

```bash
python3 model.py params.txt outputs.txt
```

3. Sensitivity analysis

The sensitivity is cleverly computed using techniques based on ANOVA, so instead
of supplying the inputs alongside the outputs, we provide the problem definition
and outputs only.

```bash
python3 -m SALib.analyze.sobol -p problem.txt -Y outputs.txt
```

## Links

- [SALib](https://github.com/SALib/SALib)
- [Will Usher - PyData 2015 Talk](https://www.youtube.com/watch?v=gkR_lz5OptU)
- [Determining the Appropriate Number of Samples](https://waterprogramming.wordpress.com/2020/03/23/determining-the-appropriate-number-of-samples-for-a-sensitivity-analysis/)
- [@Risk Change in Output Statistic help](https://kb.palisade.com/index.php?pg=kb.page&id=248)

## Further review needed

- Add Morris method to demonstration. Morris is commonly used as a screening
  tool for filtering out less useful factors because it is fast and although it
  is less robust that Sobol, it's output can provide clues into interdependence
  of params by providing the stdev in the ouput.
- Compare the `Change in Output Statistic` method used by @Risk (especially the
  Morris method). Perhaps implement if useful
- Examine whether the sample -> data -> analysis model is required or whether it
  is useful to just take a pre-existing dataset and perform the analysis for the
  purposes of screening out interesting factors.
- How does this type of sensitivity analysis stack up against linear regression?
  The reading suggests that these methods are more robust because some (e.g.
  Sobol) are global whereas regression will "hold all else equal". How useful is
  linear regression when many models are in fact non-linear.
