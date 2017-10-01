import math
import operator
import os
import sys
import turtle

import environment
import lexer
import utils


class SchemeObject:
    def __init__(self, value):
        # list, atom, string, number, quote, dotted_list, char, bool, lambda, nil
        self.type = None
        self.input_value = value
        self.value = value
        self.env = None

    def create_lambda_obj(self, env):
        self.type = "lambda"
        self.env = env
        return self

    def create_build_in_obj(self):
        self.type = "build_in"
        return self

    def create_obj(self):
        self.parse_value()
        return self

    def parse_value(self):
        if self.input_value is None or len(self.input_value) == 0:
            return
        if self.input_value[0] == "(":
            self.type = "list"
            self.value = []
            self.input_value.remove(self.input_value[0])

            while self.input_value[0] != ")":
                self.value.append(SchemeObject(self.input_value).create_obj())

            self.input_value.remove(self.input_value[0])

        elif utils.is_number(self.input_value[0]):
            self.type = "number"
            if utils.is_int(self.input_value[0]):
                self.value = int(self.input_value.pop(0))
            elif utils.is_float(self.input_value[0]):
                self.value = float(self.input_value.pop(0))

        elif self.input_value[0][0] == "\"":
            self.type = "string"
            self.value = self.input_value.pop(0)

        elif self.input_value[0] == "'":
            self.type = "quote"
            self.input_value.remove(self.input_value[0])
            self.value = SchemeObject(self.input_value).create_obj()

        elif self.input_value[0].find("#\\") == 0:
            self.type = "char"
            self.value = self.input_value.pop(0)[3]

        elif self.input_value[0].find("#t") == 0:
            self.type = "bool"
            self.value = True
            self.input_value.remove(self.input_value[0])

        elif self.input_value[0].find("#f") == 0:
            self.type = "bool"
            self.value = False
            self.input_value.remove(self.input_value[0])

        elif self.input_value[0] == "nil":
            self.type = "nil"
            self.value = None
            self.input_value.remove(self.input_value[0])

        else:
            self.type = "atom"
            self.value = self.input_value.pop(0)
            if self.value == ":exit":
                sys.exit(0)

                # TODO: dotted_list

    def get_value_as_string(self):
        if self.type == "list":
            return "(%s)" % " ".join([value.get_value_as_string() for value in self.value])

        elif self.type == "quote":
            return "'%s" % self.value.get_value_as_string()

        else:
            return str(self.value)

    def print_value(self):
        print(self.get_value_as_string())

    def eval(self, env):
        if self.type == "atom":
            ret_val = env.get_from_env(self.value)
            if ret_val is None:
                print("Atom \"%s\" is not defined!" % self.value)
            return ret_val

        if self.type == "list":
            if self.value[0].type == "atom":
                func_obj = self.value[0].eval(env)
                if func_obj is not None and func_obj.type == "build_in":
                    return func_obj.value(self.value[1:], env)

                if func_obj is not None and func_obj.type == "lambda":
                    lambda_env = environment.Environment(func_obj.env)
                    if len(func_obj.value[0].value) != len(self.value[1:]):
                        print(
                            "not enough arguments: expected %i, got %i"
                            % (len(func_obj.value[0]), len(self.value[1:]))
                        )
                    for idx, key in enumerate(func_obj.value[0].value):
                        lambda_env.add_to_env(key.value, self.value[idx + 1].eval(env))
                    ret_val = None
                    for body_vals in func_obj.value[1:]:
                        ret_val = body_vals.eval(lambda_env)
                    return ret_val

        if self.type == "quote":
            return self.value

        return self


def eval_define(value, env):
    if len(value) != 2:
        print("define requires 2 arguments, %i given" % len(value))
    else:
        env.add_to_env(value[0].value, value[1].eval(env))
        return value[0]


def eval_plus(value, env):
    return SchemeObject([math.fsum([val.eval(env).value for val in value])]).create_obj()


def eval_multiply(value, env):
    return SchemeObject([reduce(operator.mul, [val.eval(env).value for val in value], 1)]).create_obj()


def eval_divide(value, env):
    try:
        return SchemeObject([reduce(operator.truediv, [val.eval(env).value for val in value])]).create_obj()
    except ZeroDivisionError:
        print("division by zero")
        return None


def eval_minus(value, env):
    if len(value) == 0:
        print("at least one argument required, zero give!")
    elif len(value) == 1:
        return SchemeObject([0 - value[0].eval(env).value]).create_obj()
    else:
        return SchemeObject([reduce(operator.sub, [val.eval(env).value for val in value])]).create_obj()


def eval_if(value, env):
    ret_val = value[0].eval(env)
    if ret_val.type != "bool":
        print("condition \"%s\" doesn't evaluate to boolean" % value[0].get_value_as_string())
        return None
    elif ret_val.value:
        return value[1].eval(env)
    else:
        return value[2].eval(env)


def eval_cond(value, env):
    for clause in value:
        if clause.type != "list":
            print("\"%s\" not a valid clause" % clause.get_value_as_string())
            return None
        else:
            if clause.value[0].type == "atom" and clause.value[0].value == "else":
                ret_val = None
                for expr in clause.value[1:]:
                    ret_val = expr.eval(env)
                return ret_val
            evaluated_val = clause.value[0].eval(env)
            if evaluated_val.type != "bool":
                print("condition \"%s\" doesn't evaluate to boolean" % clause.value[0].get_value_as_string())
                return None
            elif evaluated_val.value:
                ret_val = None
                for expr in clause.value[1:]:
                    ret_val = expr.eval(env)
                return ret_val


def eval_print(value, env):
    for entry in value:
        entry.print_value()


def eval_lambda_def(value, env):
    if len(value) < 2:
        print("not a lambda expression: \"(lambda %s)\"" % " ".join([val.get_value_as_string() for val in value]))
        return None
    else:
        return SchemeObject(value).create_lambda_obj(env)


def eval_car(value, env):
    if len(value) != 1:
        print("Only 1 argument allowed. Must be of type quote")
    elif value[0].type != "quote" or value[0].value.type != "list":
        print("argument must be of type \"quoted list\"")
    elif len(value[0].value.value) < 1:
        print("empty quoted list not allowed")
    else:
        return value[0].value.value[0]
    return None


def eval_cdr(value, env):
    if len(value) != 1:
        print("Only 1 argument allowed. Must be of type quote")
    elif value[0].type != "quote" or value[0].value.type != "list":
        print("argument must be of type \"quoted list\"")
    elif len(value[0].value.value) < 1:
        print("empty quoted list not allowed")
    else:
        new_obj = value[0].value
        new_obj.value = new_obj.value[1:]
        return new_obj
    return None


def eval_cons(value, env):
    if len(value) != 2:
        print("Exactly 2 arguments needed!")
    elif value[0].type == "list" or value[1].type == "list":
        print("Only quoted lists allowed!")
    else:
        new_val0 = value[0].eval(env)
        new_val1 = value[1].eval(env)
        if new_val1.type == "list":
            new_val1.value.insert(0, new_val0)
            return new_val1
        else:
            new_obj = SchemeObject([new_val0, new_val1])
            new_obj.type = "list"
            new_obj.env = env
            return new_obj
    return None


def eval_load(value, env):
    if len(value) != 1:
        print("Only one filename allowed!")
    else:
        evaluated_value = value[0].eval(env)
        if evaluated_value.type != "string":
            print("filename must be of type string")
        else:
            file_name = evaluated_value.value[1:-1]
            if not os.path.isfile(file_name):
                print("file \"%s\" doesn't exist" % file_name)
            else:
                with open(file_name) as f:
                    content = f.readlines()
                for line in content:
                    SchemeObject(lexer.lex_input(line.strip())).create_obj().eval(env)
    return None


def eval_less_then(value, env):
    if len(value) != 2:
        print("two arguments expected, %s given" % len(value))
    elif value[0].eval(env).value < value[1].eval(env).value:
        return SchemeObject(["#t"]).create_obj()
    else:
        return SchemeObject(["#f"]).create_obj()
    return None


def eval_greater_then(value, env):
    if len(value) != 2:
        print("two arguments expected, %s given" % len(value))
    elif value[0].eval(env).value > value[1].eval(env).value:
        return SchemeObject(["#t"]).create_obj()
    else:
        return SchemeObject(["#f"]).create_obj()
    return None


def eval_equals(value, env):
    if len(value) != 2:
        print("two arguments expected, %s given" % len(value))
    elif value[0].eval(env).value == value[1].eval(env).value:
        return SchemeObject(["#t"]).create_obj()
    else:
        return SchemeObject(["#f"]).create_obj()
    return None


def eval_dsin(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    else:
        return SchemeObject([math.sin(math.radians(value[0].eval(env).value))]).create_obj()
    return None


def eval_rsin(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    else:
        return SchemeObject([math.sin(math.degrees(value[0].eval(env).value))]).create_obj()
    return None


# Turtle Graphics
def eval_tinit(value, env):
    if len(value) != 2:
        print("two arguments needed (width, height)!")
    elif value[0].type != "number" or value[1].type != "number":
        print("arguments must be of type number!")
    elif (utils.is_int(value[0].value) and not utils.is_int(value[1].value)) or (
        not utils.is_int(value[0].value) and utils.is_int(value[1].value)):
        print("arguments must be of same type (either float or int)!")
    else:
        screen = turtle.Screen()
        screen.setup(value[0].value, value[1].value)
        env.add_to_env("in_build_screen", screen)
        if env.get_from_env("in_build_turtle") is None:
            try:
                env.add_to_env("in_build_turtle", turtle.Turtle())
            except turtle.Terminator:  # This is stupid, but oh well ...
                env.add_to_env("in_build_turtle", turtle.Turtle())
                return None
    return None


def eval_texit(value, env):
    if len(value) > 0:
        print("no argument needed")
    elif env.get_from_env("in_build_screen") is not None:
        env.get_from_env("in_build_screen").bye()
        env.remove_from_env("in_build_turtle")
    return None


def eval_tforward(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    else:
        tess = env.get_from_env("in_build_turtle")
        if tess is None:
            print("no turtle to move!")
        elif value[0].eval(env).type != "number":
            print("argument must be of type \"number\"")
        else:
            tess.forward(value[0].eval(env).value)
    return None


def eval_tback(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    else:
        tess = env.get_from_env("in_build_turtle")
        if tess is None:
            print("no turtle to move!")
        elif value[0].eval(env).type != "number":
            print("argument must be of type \"number\"")
        else:
            tess.back(value[0].eval(env).value)
    return None


def eval_tleft(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    else:
        tess = env.get_from_env("in_build_turtle")
        if tess is None:
            print("no turtle to move!")
        elif value[0].eval(env).type != "number":
            print("argument must be of type \"number\"")
        else:
            tess.left(value[0].eval(env).value)
    return None


def eval_tright(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    else:
        tess = env.get_from_env("in_build_turtle")
        if tess is None:
            print("no turtle to move!")
        elif value[0].eval(env).type != "number":
            print("argument must be of type \"number\"")
        else:
            tess.right(value[0].eval(env).value)
    return None


def eval_tcircle(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    else:
        tess = env.get_from_env("in_build_turtle")
        if tess is None:
            print("no turtle to move!")
        elif value[0].eval(env).type != "number":
            print("argument must be of type \"number\"")
        else:
            tess.circle(value[0].eval(env).value)
    return None


def eval_tsize(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    else:
        tess = env.get_from_env("in_build_turtle")
        if tess is None:
            print("no turtle to set size!")
        elif value[0].eval(env).type != "number":
            print("argument must be of type \"number\"")
        else:
            tess.pensize(value[0].eval(env).value)
    return None


def eval_tspiral(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    elif value[0].eval(env).type != "number":
        print("argument must be of type \"number\"")
    else:
        tess = env.get_from_env("in_build_turtle")
        if tess is None:
            print("no turtle to move!")
        else:
            tess.speed(0)
            colors = ['red', 'purple', 'blue', 'green', 'yellow', 'orange']
            for x in range(value[0].eval(env).value):
                tess.pencolor(colors[x % 6])
                tess.pensize(x / 100 + 1)
                tess.forward(x)
                tess.left(59)
    return None


def eval_tspeed(value, env):
    if len(value) != 1:
        print("exactly one argument needed")
    elif value[0].eval(env).type != "number":
        print("argument must be of type \"number\"")
    else:
        tess = env.get_from_env("in_build_turtle")
        if tess is None:
            print("no turtle to speed up")
        else:
            tess.speed(value[0].eval(env).value)
    return None
