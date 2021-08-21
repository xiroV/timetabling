from enum import Enum

class Fzn:
    def __init__(self, include_names=False):
        self.introduced_vars = set()
        self.variables = []
        self.constraints = []
        self.defined_vars = set()
        self.include_names = include_names

    def write(self, fd):
        self.write_variables(fd)
        self.write_constraints(fd)

    def bool_var(self, name, output=False):
        if name not in self.introduced_vars:
            self.introduced_vars.add(name)
            self.variables.append(BoolVar(name, output))
        return name

    def int_var(self, name, domain='int', output=False):
        if domain == 'int':
            print("WARNING: IntVar {} has unbound domain".format(name))
        if name not in self.introduced_vars:
            self.introduced_vars.add(name)
            self.variables.append(IntVar(name, domain, output))
        return name

    def int_array(self, name, arr, domain='int'):
        if domain == 'int':
            print("WARNING: IntArray {} has unbound domain".format(name))
        if name not in self.introduced_vars:
            self.introduced_vars.add(name)
            self.variables.append(IntArray(name, arr, domain))
        return name

    def bool_array(self, name, arr):
        if name not in self.introduced_vars:
            self.introduced_vars.add(name)
            self.variables.append(BoolArray(name, arr))
        return name

    def set_in_reif(self, var, arr, r, defines=None, name=None):
        if defines is None:
            self.constraints.append(SetInReif(var, arr, r, defines, name))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(SetInReif(var, arr, r, defines, name))
        return r

    def bool2int(self, x, y, defines=None, name=None):
        if defines is None:
            self.constraints.append(Bool2Int(x, y, defines, name))
        elif defines not in self.defined_vars:
            self.defined_vars.add(y)
            self.constraints.append(Bool2Int(x, y, defines, name))
        return y

    def int_eq(self, x, y, name=None):
        self.constraints.append(IntEq(x, y, name))

    def int_minus(self, x, y, r, defines=None, name=None):
        if defines is None:
            self.constraints.append(IntMinus(x, y, r, defines, name))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(IntMinus(x, y, r, defines, name))

    def int_plus(self, x, y, r, defines=None):
        if defines is None:
            self.constraints.append(IntPlus(x, y, r, defines))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(IntPlus(x, y, r, defines))

    def int_times(self, x, y, r, defines=None):
        if defines is None:
            self.constraints.append(IntTimes(x, y, r, defines))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(IntTimes(x, y, r, defines))
        return defines

    def int_ne(self, x, y):
        self.constraints.append(IntNe(x, y))

    def int_eq_reif(self, x, y, r, defines=None, name=None):
        if defines is None:
            self.constraints.append(IntEqReif(x, y, r, defines, name))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(IntEqReif(x, y, r, defines, name))
        return defines

    def array_int_element(self, b, a, c, defines=None):
        if defines is None:
            self.constraints.append(ArrayIntElement(b, a, c, defines))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(ArrayIntElement(b, a, c, defines))
        return defines

    def array_bool_element(self, b, a, c, defines=None):
        if defines is None:
            self.constraints.append(ArrayBoolElement(b, a, c, defines))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(ArrayBoolElement(b, a, c, defines))
        return defines

    def int_le_reif(self, x, y, r, defines=None):
        if defines is None:
            self.constraints.append(IntLeReif(x, y, r, defines))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(IntLeReif(x, y, r, defines))
        return defines

    def int_ne_reif(self, x, y, r, defines=None, name=None):
        if defines is None:
            self.constraints.append(IntNeReif(x, y, r, defines, name))
        elif defines not in self.defined_vars:
            self.defined_vars.add(r)
            self.constraints.append(IntNeReif(x, y, r, defines, name))
        return defines

    def bool_and(self, x, y, r, defines=None, name=None):
        if defines is None:
            self.constraints.append(BoolAnd(x, y, r, defines, name))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(BoolAnd(x, y, r, defines, name))
        return defines

    def bool_eq(self, x, y):
        self.constraints.append(BoolEq(x, y))

    def bool_xor(self, x, y, r=None, defines=None, name=None):
        if defines is None:
            self.constraints.append(BoolXor(x, y, r, defines, name))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(BoolXor(x, y, r, defines, name))
        return defines

    def bool_not(self, x, y, defines=None):
        if defines is None:
            self.constraints.append(BoolNot(x, y, defines))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(BoolNot(x, y, defines))
        return defines

    def int_max(self, x, y, r, defines=None):
        if defines is None:
            self.constraints.append(IntMax(x, y, r, defines))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(IntMax(x, y, r, defines))
        return defines

    def int_div(self, x, y, r, defines=None):
        if defines is None:
            self.constraints.append(IntDiv(x, y, r, defines))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(IntDiv(x, y, r, defines))
        return defines

    def array_bool_and(self, arr, r, defines=None, name=None):
        if defines is None:
            self.constraints.append(ArrayBoolAnd(arr, r, defines, name))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(ArrayBoolAnd(arr, r, defines, name))
        return defines

    def array_bool_or(self, arr, r, defines=None, name=None):
        if defines is None:
            self.constraints.append(ArrayBoolOr(arr, r, defines, name))
        elif defines not in self.defined_vars:
            self.defined_vars.add(defines)
            self.constraints.append(ArrayBoolOr(arr, r, defines, name))
        return defines

    def int_lin_eq(self, a, b, c, defines=None, name=None):
        if len(a) > 0 and len(b) > 0:
            if defines is None:
                self.constraints.append(IntLinEq(a, b, c, defines, name))
            elif defines not in self.defined_vars:
                self.defined_vars.add(defines)
                self.constraints.append(IntLinEq(a, b, c, defines, name))
        return defines

    def int_lin_le(self, a, b, c, defines=None, name=None):
        if len(a) > 0 and len(b) > 0:
            if defines is None:
                self.constraints.append(IntLinLe(a, b, c, defines, name))
            elif defines not in self.defined_vars:
                self.defined_vars.add(defines)
                self.constraints.append(IntLinLe(a, b, c, defines, name))
        return defines

    def write_variables(self, f):
        for v in self.variables:
            v.write(f)

    def write_constraints(self, f):
        for c in self.constraints:
            c.write(f, self.include_names)


class IntMax:
    def __init__(self, x, y, r, defines=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines

    def write(self, f):
        if self.r == True:
            f.write("constraint int_max({0},{1},true);\n".format(
                self.x, self.y))
        elif self.r == False:
            f.write("constraint int_max({0},{1},false);\n".format(
                self.x, self.y))
        else:
            if self.defines is not None:
                f.write(
                    "constraint int_max({0},{1},{2}) :: defines_var({3});\n".
                    format(self.x, self.y, self.r, self.defines))
            else:
                f.write("constraint int_max({0},{1},{2});\n".format(
                    self.x, self.y, self.r))


class IntDiv:
    def __init__(self, x, y, r, defines=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines

    def write(self, f):
        if self.r == True:
            f.write("constraint int_div({0},{1},true);\n".format(
                self.x, self.y))
        elif self.r == False:
            f.write("constraint int_div({0},{1},false);\n".format(
                self.x, self.y))
        else:
            if self.defines is not None:
                f.write(
                    "constraint int_div({0},{1},{2}) :: defines_var({3});\n".
                    format(self.x, self.y, self.r, self.defines))
            else:
                f.write("constraint int_div({0},{1},{2});\n".format(
                    self.x, self.y, self.r))


class BoolVar:
    def __init__(self, name, output=False):
        self.name = name
        self.output = output

    def write(self, f):
        if self.output:
            f.write(
                "var bool: {} :: var_is_introduced :: output_var :: is_defined_var;\n"
                .format(self.name))
        else:
            f.write("var bool: {} :: var_is_introduced :: is_defined_var;\n".
                    format(self.name))


class IntVar:
    def __init__(self, name, domain=None, output=False):
        self.name = name
        self.domain = domain
        self.output = output

    def write(self, f):
        if self.output:
            f.write(
                "var {}: {} :: var_is_introduced :: output_var :: is_defined_var;\n"
                .format(self.domain, self.name))
        else:
            f.write(
                "var {}: {} :: var_is_introduced :: is_defined_var;\n".format(
                    self.domain, self.name))


class IntArray:
    def __init__(self, name, arr, domain=None):
        self.name = name
        self.arr = arr
        self.domain = domain

    def write(self, f):
        f.write("array [1..{}] of int: {} = {};\n".format(
            len(self.arr), self.name, self.arr))


class BoolArray:
    def __init__(self, name, arr):
        self.name = name
        self.arr = arr

    def write(self, f):
        f.write("array [1..{}] of bool: {} = [{}];\n".format(
            len(self.arr), self.name,
            ','.join([str(a).lower() for a in self.arr])))


class IntEq:
    def __init__(self, x, y, name=None):
        self.x = x
        self.y = y
        self.name = name

    def write(self, f, include_name):
        if self.name is not None and include_name:
            f.write("constraint int_eq({0},{1}) :: mzn_constraint_name(\"{2}\");\n".format(self.x, self.y, self.name))
        else:
            f.write("constraint int_eq({0},{1});\n".format(self.x, self.y))


class IntMinus:
    def __init__(self, x, y, r, defines=None, name=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        name_str = ""
        if self.name is not None and include_name:
            name_str = " :: mzn_constraint_name(\"{}\")".format(self.name)

        if self.defines is not None:
            f.write("constraint int_plus({0},{1},{2}){3} :: defines_var({4});\n".
                    format(self.x, self.y * -1, self.r, name_str, self.defines))
        else:
            f.write("constraint int_plus({0},{1},{2}){3};\n".format(
                self.x, self.y * -1, self.r, name_str))


class IntPlus:
    def __init__(self, x, y, r, defines=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines

    def write(self, f):
        if self.defines is not None:
            f.write("constraint int_plus({0},{1},{2}) :: defines_var({3});\n".
                    format(self.x, self.y, self.r, self.defines))
        else:
            f.write("constraint int_plus({0},{1},{2});\n".format(
                self.x, self.y, self.r))


class IntTimes:
    def __init__(self, x, y, r, defines=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines

    def write(self, f):
        if self.defines is not None:
            f.write("constraint int_times({0},{1},{2});\n".format(
                self.x, self.y, self.r))
        else:
            f.write(
                "constraint int_times({0},{1},{2}) :: defines_var();\n".format(
                    self.x, self.y, self.r, self.defines))


class ArrayIntElement:
    def __init__(self, b, a, c, defines=None):
        self.a = a
        self.b = b
        self.c = c
        self.defines = defines

    def write(self, f):
        if self.defines is not None:
            f.write(
                "constraint array_int_element({0},{1},{2}) :: defines_var({3});\n"
                .format(self.b, self.a, self.c, self.defines))
        else:
            f.write("constraint array_int_element({0},{1},{2});\n".format(
                self.b, self.a, self.c))


class ArrayBoolElement:
    def __init__(self, b, a, c, defines=None):
        self.a = a
        self.b = b
        self.c = c
        self.defines = defines

    def write(self, f):
        if type(self.c) == bool:
            c = str(self.c).lower()
        else:
            c = self.c

        if self.defines is not None:
            f.write(
                "constraint array_bool_element({0},{1},{2}) :: defines_var({3});\n"
                .format(self.b, self.a, c, self.defines))
        else:
            f.write("constraint array_bool_element({0},{1},{2});\n".format(
                self.b, self.a, c))


class IntNe:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def write(self, f):
        f.write("constraint int_ne({0},{1});\n".format(self.x, self.y))


class IntEqReif:
    def __init__(self, x, y, r, defines=None, name=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        r_str = ""
        defines_str = ""
        name_str = ""

        if type(self.r) == bool:
            if self.r:
                r_str = "true"
            else:
                r_str = "false"
        else:
            r_str = self.r

        if self.defines is not None:
            defines_str = " :: defines_var({})".format(self.defines)

        if self.name is not None and include_name:
            name_str = " :: mzn_constraint_name(\"{}\")".format(self.name)

        f.write(
            "constraint int_eq_reif({},{},{}){}{};\n"
            .format(self.x, self.y, r_str, name_str, defines_str))


class IntLeReif:
    def __init__(self, x, y, r, defines=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines

    def write(self, f):
        if self.r == True:
            f.write("constraint int_le_reif({0},{1},true);\n".format(
                self.x, self.y))
        elif self.r == False:
            f.write("constraint int_le_reif({0},{1},false);\n".format(
                self.x, self.y))
        else:
            if self.defines is not None:
                f.write(
                    "constraint int_le_reif({0},{1},{2}) :: defines_var({3});\n"
                    .format(self.x, self.y, self.r, self.defines))
            else:
                f.write("constraint int_le_reif({0},{1},{2});\n".format(
                    self.x, self.y, self.r))


class IntNeReif:
    def __init__(self, x, y, r, defines=None, name=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        if self.name is not None and include_name:
            if self.r == True:
                f.write("constraint int_ne_reif({0},{1},true) :: mzn_constraint_name(\"{2}\");\n".format(
                    self.x, self.y, self.name))
            elif self.r == False:
                f.write("constraint int_ne_reif({0},{1},false) :: mzn_constraint_name(\"{2}\");\n".format(
                    self.x, self.y, self.name))
            else:
                if self.defines is not None:
                    f.write(
                        "constraint int_ne_reif({0},{1},{2}) :: mzn_constraint_name(\"{3}\") :: defines_var({4});\n"
                        .format(self.x, self.y, self.r, self.name, self.defines))
                else:
                    f.write("constraint int_ne_reif({0},{1},{2}) :: mzn_constraint_name(\"{3}\");\n".format(
                        self.x, self.y, self.r, self.name))
        else:
            if self.r == True:
                f.write("constraint int_ne_reif({0},{1},true);\n".format(
                    self.x, self.y))
            elif self.r == False:
                f.write("constraint int_ne_reif({0},{1},false);\n".format(
                    self.x, self.y))
            else:
                if self.defines is not None:
                    f.write(
                        "constraint int_ne_reif({0},{1},{2}) :: defines_var({3});\n"
                        .format(self.x, self.y, self.r, self.defines))
                else:
                    f.write("constraint int_ne_reif({0},{1},{2});\n".format(
                        self.x, self.y, self.r))



class Bool2Int:
    def __init__(self, x, y, defines=None, name=None):
        self.x = x
        self.y = y
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        defines_str = ""
        name_str = ""

        if self.defines is not None:
            defines_str = " :: defines_var({})".format(self.defines)

        if self.name is not None and include_name:
            name_str = " :: mzn_constraint_name(\"{}\")".format(self.name)


        f.write(
            "constraint bool2int({},{}){}{};\n".format(
                self.x, self.y, name_str, defines_str))


class IntLinEq:
    def __init__(self, a, b, c, defines=None, name=None):
        self.a = a
        self.b = b
        self.c = c
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        if self.name is not None and include_name:
            if self.defines is not None:
                f.write(
                        "constraint int_lin_eq([{0}],[{1}],{2}) :: mzn_constraint_name(\"{3}\") :: defines_var({4});\n"
                    .format(','.join([str(e) for e in self.a]),
                            ','.join([str(e) for e in self.b]), self.c,
                            self.name,
                            self.defines))
            else:
                f.write("constraint int_lin_eq([{0}],[{1}],{2}) :: mzn_constraint_name(\"{3}\");\n".format(
                    ','.join([str(e) for e in self.a]),
                    ','.join([str(e) for e in self.b]), self.c, self.name))

        else:
            if self.defines is not None:
                f.write(
                    "constraint int_lin_eq([{0}],[{1}],{2}) :: defines_var({3});\n"
                    .format(','.join([str(e) for e in self.a]),
                            ','.join([str(e) for e in self.b]), self.c,
                            self.defines))
            else:
                f.write("constraint int_lin_eq([{0}],[{1}],{2});\n".format(
                    ','.join([str(e) for e in self.a]),
                    ','.join([str(e) for e in self.b]), self.c))


class IntLinLe:
    def __init__(self, a, b, c, defines=None, name=None):
        self.a = a
        self.b = b
        self.c = c
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        defines_str = ""
        name_str = ""

        if self.defines is not None:
            defines_str = " :: defines_var({})".format(self.defines)

        if self.name is not None and include_name:
            name_str = " :: mzn_constraint_name(\"{}\")".format(self.name)

            f.write("constraint int_lin_le([{0}],[{1}],{2}){3}{4};\n".format(
                ','.join([str(e) for e in self.a]),
                ','.join([str(e) for e in self.b]), self.c, name_str, defines_str))


class BoolEq:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def write(self, f):
        f.write("constraint bool_eq({0},{1});\n".format(self.x, self.y))


class BoolAnd:
    def __init__(self, x, y, r, defines=None, name=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        if type(self.r) == bool:
            r = str(self.r).lower()
        else:
            r = self.r

        if type(self.x) == bool:
            x = str(self.x).lower()
        else:
            x = self.x

        if type(self.y) == bool:
            y = str(self.y).lower()
        else:
            y = self.y

        name_str = ""

        if self.name is not None and include_name:
            name_str = " :: mzn_constraint_name(\"{}\")".format(self.name)

        if self.defines is not None:
            f.write("constraint bool_and({0},{1},{2}){3} :: defines_var({4});\n".
                    format(x, y, r, name_str, self.defines))
        else:
            f.write("constraint bool_and({0},{1},{2}){3};\n".format(
                x, y, r, name_str))


class BoolXor:
    def __init__(self, x, y, r=None, defines=None, name=None):
        self.x = x
        self.y = y
        self.r = r
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        name_str = ""
        defines_str = ""

        if self.name is not None and include_name:
            name_str = " :: mzn_constraint_name(\"{}\")".format(self.name)

        if self.defines is not None:
            defines_str = " :: defines_var({})".format(self.defines)

        if type(self.r) == bool:
            r = str(self.r).lower()
        else:
            r = self.r

        if type(self.x) == bool:
            x = str(self.x).lower()
        else:
            x = self.x

        if type(self.y) == bool:
            y = str(self.y).lower()
        else:
            y = self.y

        if r is None:
            f.write("constraint bool_xor({0},{1}){2}{3};\n".format(x, y, name_str, defines_str))
        else:
            f.write("constraint bool_xor({0},{1},{2}){3}{4};\n".format(x, y, r, name_str, defines_str))


class BoolNot:
    def __init__(self, x, y, defines=None):
        self.x = x
        self.y = y
        self.defines = defines

    def write(self, f):
        if type(self.x) == bool:
            x = str(self.x).lower()
        else:
            x = self.x

        if type(self.y) == bool:
            y = str(self.y).lower()
        else:
            y = self.y

        if self.defines is not None:
            f.write(
                "constraint bool_not({0},{1}) :: defines_var({2});\n".format(
                    x, y, self.defines))
        else:
            f.write("constraint bool_not({0},{1});\n".format(x, y))


class ArrayBoolAnd:
    def __init__(self, a, r, defines=None, name=None):
        self.a = a
        self.r = r
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        defines_str = ""
        name_str = ""
        r_str = ""

        if self.defines is not None:
            defines_str = " :: defines_var({})".format(self.defines)

        if self.name is not None and include_name:
            name_str = " :: mzn_constraint_name(\"{}\")".format(self.name)

        if self.r == True:
            r_str = "true"
        elif self.r == False:
            r_str = "false"
        else:
            r_str = self.r

        f.write("constraint array_bool_and([{}],{}){}{};\n"
            .format(','.join(self.a), r_str, name_str, defines_str))



class ArrayBoolOr:
    def __init__(self, a, r, defines=None, name=None):
        self.a = a
        self.r = r
        self.defines = defines
        self.name = name

    def write(self, f, include_name):
        r_str = ""
        name_str = ""
        defines_str = ""
        if type(self.r) == bool:
            if self.r:
                r_str = 'true'
            else:
                r_str = 'false'
        else:
            r_str = self.r 

        if self.name is not None and include_name:
            name_str = " :: mzn_constraint_name(\"{}\")".format(self.name)

        if self.defines is not None:
            defines_str = " :: defines_var({})".format(self.defines)


        f.write(
            "constraint array_bool_or([{0}],{1}){2}{3};\n"
            .format(','.join(self.a), r_str, name_str, defines_str))



class SetInReif:
    def __init__(self, x, s, r, defines=None, name=None):
        self.x = x
        self.s = s
        self.r = r
        self.defines = defines
        self.name = name

        if len(s) < 1:
            if type(s) == list:
                s.append(0)
            elif type(s) == set:
                s.add(0)

    def write(self, f, include_name):
        name_str = ""
        defines_str = ""

        if self.name is not None and include_name:
            name_str = " :: mzn_constraint_name(\"{}\")".format(self.name)

        if self.defines is not None: 
            defines_str = " :: defines_var({})".format(self.defines)

            f.write(
                    "constraint set_in_reif({}, {{{}}}, {}){}{};\n".
                format(self.x, ','.join([str(e) for e in self.s]), self.r,
                    name_str, defines_str))

