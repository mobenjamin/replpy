import math

import schemeobj


class Environment:
    def __init__(self, parent_env=None):
        self.parent_env = parent_env
        self.environment = {}
        return

    def add_to_env(self, key, value):
        self.environment[key] = value

    def get_from_env(self, key):
        if key not in self.environment and self.parent_env is not None:
            return self.parent_env.get_from_env(key)

        else:
            return self.get_from_this_env(key)

    def get_from_this_env(self, key):
        if key not in self.environment:
            return None
        else:
            return self.environment[key]

    def remove_from_env(self, key):
        if key in self.environment:
            del self.environment[key]

    @staticmethod
    def get_default_env():
        env = Environment()
        env.add_to_env("define", schemeobj.SchemeObject(schemeobj.eval_define).create_build_in_obj())
        env.add_to_env("+", schemeobj.SchemeObject(schemeobj.eval_plus).create_build_in_obj())
        env.add_to_env("-", schemeobj.SchemeObject(schemeobj.eval_minus).create_build_in_obj())
        env.add_to_env("*", schemeobj.SchemeObject(schemeobj.eval_multiply).create_build_in_obj())
        env.add_to_env("/", schemeobj.SchemeObject(schemeobj.eval_divide).create_build_in_obj())
        env.add_to_env("<", schemeobj.SchemeObject(schemeobj.eval_less_then).create_build_in_obj())
        env.add_to_env(">", schemeobj.SchemeObject(schemeobj.eval_greater_then).create_build_in_obj())
        env.add_to_env("=", schemeobj.SchemeObject(schemeobj.eval_equals).create_build_in_obj())
        env.add_to_env("dsin", schemeobj.SchemeObject(schemeobj.eval_dsin).create_build_in_obj())
        env.add_to_env("rsin", schemeobj.SchemeObject(schemeobj.eval_rsin).create_build_in_obj())
        env.add_to_env("pi", schemeobj.SchemeObject([math.pi]).create_obj())
        env.add_to_env("e", schemeobj.SchemeObject([math.e]).create_obj())
        env.add_to_env("if", schemeobj.SchemeObject(schemeobj.eval_if).create_build_in_obj())
        env.add_to_env("cond", schemeobj.SchemeObject(schemeobj.eval_cond).create_build_in_obj())
        env.add_to_env("print", schemeobj.SchemeObject(schemeobj.eval_print).create_build_in_obj())
        env.add_to_env("lambda", schemeobj.SchemeObject(schemeobj.eval_lambda_def).create_build_in_obj())
        env.add_to_env("car", schemeobj.SchemeObject(schemeobj.eval_car).create_build_in_obj())
        env.add_to_env("cdr", schemeobj.SchemeObject(schemeobj.eval_cdr).create_build_in_obj())
        env.add_to_env("cons", schemeobj.SchemeObject(schemeobj.eval_cons).create_build_in_obj())
        env.add_to_env("load", schemeobj.SchemeObject(schemeobj.eval_load).create_build_in_obj())

        # Turtle Graphics
        env.add_to_env("tinit", schemeobj.SchemeObject(schemeobj.eval_tinit).create_build_in_obj())
        env.add_to_env("texit", schemeobj.SchemeObject(schemeobj.eval_texit).create_build_in_obj())
        env.add_to_env("tforward", schemeobj.SchemeObject(schemeobj.eval_tforward).create_build_in_obj())
        env.add_to_env("tback", schemeobj.SchemeObject(schemeobj.eval_tback).create_build_in_obj())
        env.add_to_env("tleft", schemeobj.SchemeObject(schemeobj.eval_tleft).create_build_in_obj())
        env.add_to_env("tright", schemeobj.SchemeObject(schemeobj.eval_tright).create_build_in_obj())
        env.add_to_env("tcircle", schemeobj.SchemeObject(schemeobj.eval_tcircle).create_build_in_obj())
        env.add_to_env("tsize", schemeobj.SchemeObject(schemeobj.eval_tsize).create_build_in_obj())
        env.add_to_env("tspiral", schemeobj.SchemeObject(schemeobj.eval_tspiral).create_build_in_obj())
        env.add_to_env("tspeed", schemeobj.SchemeObject(schemeobj.eval_tspeed).create_build_in_obj())
        return env
