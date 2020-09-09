from cdata.c6Data import get_data

def setup_module(module):
    global d
    d = get_data()

def test_model_setters():
    d.extMod = 'model1, model2, model3, modelN'
    assert d._extMod == ['model1', 'model2', 'model3', 'modelN']

def test_exp_setters():
    d.extExp = 'exp1, exp2, exp3, expN'
    assert d._extExp == ['exp1', 'exp2', 'exp3', 'expN']

def test_var_setters():
    d.extVar = 'var1, var2, var3, varN'
    assert d._extVar == ['var1', 'var2', 'var3', 'varN']
