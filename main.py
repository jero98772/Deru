
#from deruuk import tokenize,atom,read_from_tokens

import functools
import sys, traceback

import copy, time
from itertools import chain

import re
import os, sys, readline as pyreadline

import reader,printer
import mal_types as types

from mal_types import MalException, List, Vector

# Environment

class Env():
    def __init__(self, outer=None, binds=None, exprs=None):
        self.data = {}
        self.outer = outer or None
        if binds:
            for i in range(len(binds)):
                if binds[i] == "&":
                    self.data[binds[i+1]] = exprs[i:]
                    break
                else:
                    self.data[binds[i]] = exprs[i]

    def find(self, key):
        if key in self.data: return self
        elif self.outer:     return self.outer.find(key)
        else:                return None

    def set(self, key, value):
        self.data[key] = value
        return value

    def get(self, key):
        env = self.find(key)
        if not env: raise Exception("'" + key + "' not found")
        return env.data[key]
history_loaded = False
histfile = os.path.expanduser("~/.mal-history")
if sys.version_info[0] >= 3:
    rl = input
else:
    rl = raw_input

def mal_readline(prompt="user> "):
    global history_loaded
    if not history_loaded:
        history_loaded = True
        try:
            with open(histfile, "r") as hf:
                for line in hf.readlines():
                    pyreadline.add_history(line.rstrip("\r\n"))
                    pass
        except IOError:
            #print("Could not open %s" % histfile)
            pass

    try:
        line = rl(prompt)
        pyreadline.add_history(line)
        with open(histfile, "a") as hf:
            hf.write(line + "\n")
    except IOError:
        pass
    except EOFError:
        return None
    return line



# Errors/Exceptions
def throw(obj): raise MalException(obj)


# String functions
def pr_str(*args):
    return " ".join(map(lambda exp: printer._pr_str(exp, True), args))

def do_str(*args):
    return "".join(map(lambda exp: printer._pr_str(exp, False), args))

def prn(*args):
    print(" ".join(map(lambda exp: printer._pr_str(exp, True), args)))
    return None

def println(*args):
    print(" ".join(map(lambda exp: printer._pr_str(exp, False), args)))
    return None


# Hash map functions
def assoc(src_hm, *key_vals):
    hm = copy.copy(src_hm)
    for i in range(0,len(key_vals),2): hm[key_vals[i]] = key_vals[i+1]
    return hm

def dissoc(src_hm, *keys):
    hm = copy.copy(src_hm)
    for key in keys:
        hm.pop(key, None)
    return hm

def get(hm, key):
    if hm is not None:
        return hm.get(key)
    else:
        return None

def contains_Q(hm, key): return key in hm

def keys(hm): return types._list(*hm.keys())

def vals(hm): return types._list(*hm.values())


# Sequence functions
def coll_Q(coll): return sequential_Q(coll) or hash_map_Q(coll)

def cons(x, seq): return List([x]) + List(seq)

def concat(*lsts): return List(chain(*lsts))

def nth(lst, idx):
    if idx < len(lst): return lst[idx]
    else: throw("nth: index out of range")

def first(lst):
    if types._nil_Q(lst): return None
    else: return lst[0]

def rest(lst):
    if types._nil_Q(lst): return List([])
    else: return List(lst[1:])

def empty_Q(lst): return len(lst) == 0

def count(lst):
    if types._nil_Q(lst): return 0
    else: return len(lst)

def apply(f, *args): return f(*(list(args[0:-1])+args[-1]))

def mapf(f, lst): return List(map(f, lst))

# retains metadata
def conj(lst, *args):
    if types._list_Q(lst): 
        new_lst = List(list(reversed(list(args))) + lst)
    else:
        new_lst = Vector(lst + list(args))
    if hasattr(lst, "__meta__"):
        new_lst.__meta__ = lst.__meta__
    return new_lst

def seq(obj):
    if types._list_Q(obj):
        return obj if len(obj) > 0 else None
    elif types._vector_Q(obj):
        return List(obj) if len(obj) > 0 else None
    elif types._string_Q(obj):
        return List([c for c in obj]) if len(obj) > 0 else None
    elif obj == None:
        return None
    else: throw ("seq: called on non-sequence")

# Metadata functions
def with_meta(obj, meta):
    new_obj = types._clone(obj)
    new_obj.__meta__ = meta
    return new_obj

def meta(obj):
    return getattr(obj, "__meta__", None)


# Atoms functions
def deref(atm):    return atm.val
def reset_BANG(atm,val):
    atm.val = val
    return atm.val
def swap_BANG(atm,f,*args):
    atm.val = f(atm.val,*args)
    return atm.val


ns = { 
        #'=': types._equal_Q,
        '<':  lambda a,b: a<b,
        '<=': lambda a,b: a<=b,
        '>':  lambda a,b: a>b,
        '>=': lambda a,b: a>=b,
        '+':  lambda a,b: a+b,
        '-':  lambda a,b: a-b,
        '*':  lambda a,b: a*b,
        '/':  lambda a,b: int(a/b),
        'nil?': types._nil_Q, #this answer if is nil , it mean none

        'throw': throw, #raises an exception of make a lisp (mal)
        'true?': types._true_Q,
        'false?': types._false_Q,
        'number?': types._number_Q,
        'string?': types._string_Q,
        'symbol': types._symbol,
        'symbol?': types._symbol_Q,
        'keyword': types._keyword,
        'keyword?': types._keyword_Q,
        'fn?': lambda x: (types._function_Q(x) and not hasattr(x, '_ismacro_')),
        'macro?': lambda x: (types._function_Q(x) and
                             hasattr(x, '_ismacro_') and
                             x._ismacro_),

        'pr-str': pr_str,
        'str': do_str,
        'prn': prn,
        'println': println,
        'input': input,
        'readline': lambda prompt: mal_readline.readline(prompt),
        'read-string': reader.read_str,
        'slurp': lambda file: open(file).read(),# this function takes a file name (string) and returns the contents of the file as a string.
        'time-ms': lambda : int(time.time() * 1000),

        'list': types._list,
        'list?': types._list_Q,
        'vector': types._vector,
        'vector?': types._vector_Q,
        'hash-map': types._hash_map,
        'map?': types._hash_map_Q,
        'assoc': assoc,
        'dissoc': dissoc,
        'get': get,
        'contains?': contains_Q,
        'keys': keys,
        'vals': vals,

        'sequential?': types._sequential_Q,
        'cons': cons,
        'concat': concat,
        'vec': Vector,
        'nth': nth,
        'first': first,
        'rest': rest,
        'empty?': empty_Q,
        'count': count,
        'apply': apply,
        'map': mapf,

        'conj': conj,
        'seq': seq,

        'with-meta': with_meta,
        'meta': meta,
        'atom': types._atom,
        'atom?': types._atom_Q,
        'deref': deref,
        'reset!': reset_BANG,
        'swap!': swap_BANG,


#russian
        'бросок': throw,
        'истина?': types._true_Q,
        'ложь?': types._false_Q,
        'число?': types._number_Q,
        'строка?': types._string_Q,
        'символ': types._symbol,
        'символ?': types._symbol_Q,
        'ключевое_слово': types._keyword,
        'ключевое_слово?': types._keyword_Q,
        'функция?': lambda x: (types._function_Q(x) and not hasattr(x, '_ismacro_')),
        'макрос?': lambda x: (types._function_Q(x) and
                             hasattr(x, '_ismacro_') and
                             x._ismacro_),
        'строка-отображение': pr_str,
        'строка': do_str,
        'печать': prn,
        'печать-строки': println,
        'читать-строку': lambda prompt: mal_readline.readline(prompt),
        'прочитать-текст': reader.read_str,
        'считать-файл': lambda file: open(file).read(),
        'время-мс': lambda: int(time.time() * 1000),

        'список': types._list,
        'список?': types._list_Q,
        'вектор': types._vector,
        'вектор?': types._vector_Q,
        'хэш-таблица': types._hash_map,
        'карта?': types._hash_map_Q,
        'связать': assoc,
        'развязать': dissoc,
        'получить': get,
        'содержит?': contains_Q,
        'ключи': keys,
        'значения': vals,

        'последовательный?': types._sequential_Q,
        'добавить': cons,
        'объединить': concat,
        'век': Vector,
        'энный': nth,
        'первый': first,
        'остальные': rest,
        'пустой?': empty_Q,
        'считать': count,
        'применить': apply,
        'отобразить': mapf,

        'сопрягать': conj,
        'последовательность': seq,

        'с-метаданными': with_meta,
        'метаданные': meta,
        'атом': types._atom,
        'атом?': types._atom_Q,
        'разыменовать': deref,
        'сбросить!': reset_BANG,
        'заменить!': swap_BANG,
#german
        'werfen': throw,
        'wahr?':  types._true_Q,
        'falsch?': types._false_Q,
        'zahl?': types._number_Q,
        'zeichenkette?': types._string_Q,
        'symbol': types._symbol,
        'symbol?': types._symbol_Q,
        'schlüsselwort': types._keyword,
        'schlüsselwort?': types._keyword_Q,
        'funktion?': lambda x: (types._function_Q(x) and not hasattr(x, '_ismacro_')),
        'makro?': lambda x: (types._function_Q(x) and
                             hasattr(x, '_ismacro_') and
                             x._ismacro_),
        'pr-str': pr_str,
        'str': do_str,
        'drucken': prn,
        'println': println,
        'lese-zeile': lambda prompt: mal_readline.readline(prompt),
        'lese-string': reader.read_str,
        'lesen': lambda file: open(file).read(),
        'zeit-ms': lambda: int(time.time() * 1000),

        'liste': types._list,
        'liste?': types._list_Q,
        'vektor': types._vector,
        'vektor?': types._vector_Q,
        'hash-map': types._hash_map,
        'karte?': types._hash_map_Q,
        'assoziieren': assoc,
        'dissoc': dissoc,
        'holen': get,
        'enthalten?': contains_Q,
        'schlüssel': keys,
        'werte': vals,

        'sequenziell?': types._sequential_Q,
        'hinzufügen': cons,
        'verkettet': concat,
        'vektor': Vector,
        'n-te': nth,
        'erste': first,
        'rest': rest,
        'leer?': empty_Q,
        'zählen': count,
        'anwenden': apply,
        'abbilden': mapf,

        'konj': conj,
        'folge': seq,

        'mit-meta': with_meta,
        'meta': meta,
        'atom': types._atom,
        'atom?': types._atom_Q,
        'dereferenzieren': deref,
        'zurücksetzen!': reset_BANG,
        'wechseln!': swap_BANG,
#ukraine
        'кидок': throw,
        'істина?': types._true_Q,
        'брехня?': types._false_Q,
        'рядок?': types._string_Q,
        'функція?': lambda x: (types._function_Q(x) and not hasattr(x, '_ismacro_')),

        'рядок-відображення': pr_str,
        'рядок': do_str,
        'друк': prn,
        'друк-рядка': println,
        'читати-рядок': lambda prompt: mal_readline.readline(prompt),
        'читати-рядок': reader.read_str,
        'читати-файл': lambda file: open(file).read(),
        'час-мс': lambda: int(time.time() * 1000),

        'список': types._list,
        'список?': types._list_Q,
        'хеш-мапа': types._hash_map,
        'мапа?': types._hash_map_Q,
        'асоціювати': assoc,
        'деасоціювати': dissoc,
        'отримати': get,
        'містить?': contains_Q,
        'ключі': keys,
        'значення': vals,

        'послідовний?': types._sequential_Q,
        'додати': cons,
        'обєднати': concat,
        'енний': nth,
        'перший': first,
        'залишок': rest,
        'порожній?': empty_Q,
        'лічити': count,
        'застосувати': apply,
        'відобразити': mapf,

        'приєднати': conj,
        'послідовність': seq,

        'з-метаданими': with_meta,
        'метадані': meta,
        'атом': types._atom,
        'атом?': types._atom_Q,
        'розіменувати': deref,
        'скинути!': reset_BANG,
        'замінити!': swap_BANG,

        }
# read
def READ(str):
    return reader.read_str(str)

# eval
def qq_loop(acc, elt):
    if types._list_Q(elt) and len(elt) == 2 and elt[0] == u'splice-unquote':
        return types._list(types._symbol(u'concat'), elt[1], acc)
    else:
        return types._list(types._symbol(u'cons'), quasiquote(elt), acc)

def qq_foldr(seq):
    return functools.reduce(qq_loop, reversed(seq), types._list())

def quasiquote(ast):
    if types._list_Q(ast):
        if len(ast) == 2 and ast[0] == u'unquote':
            return ast[1]
        else:
            return qq_foldr(ast)
    elif types._hash_map_Q(ast) or types._symbol_Q(ast):
        return types._list(types._symbol(u'quote'), ast)
    elif types._vector_Q (ast):
        return types._list(types._symbol(u'vec'), qq_foldr(ast))
    else:
        return ast

def is_macro_call(ast, env):
    return (types._list_Q(ast) and
            types._symbol_Q(ast[0]) and
            env.find(ast[0]) and
            hasattr(env.get(ast[0]), '_ismacro_'))

def macroexpand(ast, env):
    while is_macro_call(ast, env):
        mac = env.get(ast[0])
        ast = mac(*ast[1:])
    return ast

def eval_ast(ast, env):
    if types._symbol_Q(ast):
        return env.get(ast)
    elif types._list_Q(ast):
        return types._list(*map(lambda a: EVAL(a, env), ast))
    elif types._vector_Q(ast):
        return types._vector(*map(lambda a: EVAL(a, env), ast))
    elif types._hash_map_Q(ast):
        return types.Hash_Map((k, EVAL(v, env)) for k, v in ast.items())
    else:
        return ast  # primitive value, return unchanged

def EVAL(ast, env):
    while True:
        #print("EVAL %s" % printer._pr_str(ast))
        if not types._list_Q(ast):
            return eval_ast(ast, env)

        # apply list
        ast = macroexpand(ast, env)
        if not types._list_Q(ast):
            return eval_ast(ast, env)
        if len(ast) == 0: return ast
        a0 = ast[0]

        if "let" == a0 or "леть" == a0 :
            #let, let for create variables
            a1, a2 = ast[1], ast[2]
            res = EVAL(a2, env)
            return env.set(a1, res)
        elif "def" == a0 or "деф" == a0:
            a1, a2 = ast[1], ast[2]
            let_env = Env(env)
            for i in range(0, len(a1), 2):
                let_env.set(a1[i], EVAL(a1[i+1], let_env))
            ast = a2
            env = let_env
            # Continue loop (TCO)
        elif "quote" == a0 or "Zitat" == a0 or "цитата" == a0 :
            return ast[1]
        elif "quasiquoteexpand" == a0 or "розширенняквазицитати" == a0 :
            return quasiquote(ast[1]);
        elif "quasiquote" == a0 or "квазицитата" == a0:
            ast = quasiquote(ast[1]);
            # Continue loop (TCO)
        elif 'defmacro' == a0 or 'дефмакро' == a0:
            func = types._clone(EVAL(ast[2], env))
            func._ismacro_ = True
            return env.set(ast[1], func)
        elif 'macroexpand' == a0 or 'Makroexpandierung' == a0 or 'макрорасширение' == a0 or 'макророзширення' == a0:
            return macroexpand(ast[1], env)
        elif "py!" == a0 or "пй!" == a0:
            exec(compile(ast[1], '', 'single'), globals())
            return None
        elif "py*" == a0 or "пй*" == a0:
            return types.py_to_mal(eval(ast[1]))
        elif "." == a0:
            el = eval_ast(ast[2:], env)
            f = eval(ast[1])
            return f(*el)
        elif "try" == a0 or "versuch" == a0 or "проба" == a0 or "спроба" == a0:
            if len(ast) < 3:
                return EVAL(ast[1], env)
            a1, a2 = ast[1], ast[2]
            if a2[0] == "catch" or a2[0] == "fangen" or a2[0] == "поймать" or a2[0] == "зловити":
                err = None
                try:
                    return EVAL(a1, env)
                except types.MalException as exc:
                    err = exc.object
                except Exception as exc:
                    err = exc.args[0]
                catch_env = Env(env, [a2[1]], [err])
                return EVAL(a2[2], catch_env)
            else:
                return EVAL(a1, env);
        elif "do" == a0 or "tun" == a0 or "делать" == a0 or "робити" == a0:
            eval_ast(ast[1:-1], env)
            ast = ast[-1]
            # Continue loop (TCO)
        elif "if" == a0 or "wenn" == a0 or "если"  == a0 or "якщо" == a0:
            a1, a2 = ast[1], ast[2]
            cond = EVAL(a1, env)
            if cond is None or cond is False:
                if len(ast) > 3: ast = ast[3]
                else:            ast = None
            else:
                ast = a2
            # Continue loop (TCO)
        elif "fn" == a0 or "фн" == a0:
            a1, a2 = ast[1], ast[2]
            return types._function(EVAL, Env, a2, env, a1)
        else:
            el = eval_ast(ast, env)
            f = el[0]
            if hasattr(f, '__ast__'):
                ast = f.__ast__
                env = f.__gen_env__(el[1:])
            else:
                return f(*el[1:])

# print
def PRINT(exp):
    return printer._pr_str(exp)

# repl
repl_env = Env()
def REP(str):
    return PRINT(EVAL(READ(str), repl_env))

# core.py: defined using python
for k, v in ns.items(): repl_env.set(types._symbol(k), v)
repl_env.set(types._symbol('eval'), lambda ast: EVAL(ast, repl_env))
repl_env.set(types._symbol('*ARGV*'), types._list(*sys.argv[2:]))

# core.mal: defined using the language itself
REP("(let *host-language* \"python\")")
REP("(let not (fn (a) (if a false true)))")
REP("(let load-file (fn (f) (eval (read-string (str \"(do \" (slurp f) \"\nnil)\")))))")
REP("(defmacro cond (fn (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))")

if len(sys.argv) >= 2:
    REP('(load-file "' + sys.argv[1] + '")')
    sys.exit(0)

# repl loop
REP("(println (str \"Mal [\" *host-language* \"]\"))")
while True:
    try:
        line = mal_readline("user> ")
        if line == None: break
        if line == "": continue
        print(REP(line))
    except reader.Blank: continue
    except types.MalException as e:
        print("Error:", printer._pr_str(e.object))
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))
