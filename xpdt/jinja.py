from jinja2 import Environment, PackageLoader, StrictUndefined
import builtins

__all__ = (
    'ctemplate',
    'pytemplate',
)


def _prefix(s: str, pfx: str) -> str:
    return pfx + s


def _suffix(s: str, sfx: str) -> str:
    return s + sfx


def _wrap(s: str, pfx: str, sfx: str) -> str:
    return pfx + s + sfx


def _macro(s: str) -> str:
    return s.replace('\n', ' \\\n')


def _hex32(s: str) -> str:
    return '%.8x' % int(s)


def _setup(env: Environment) -> None:
    env.undefined = StrictUndefined
    env.filters.update({f: getattr(builtins, f) for f in (
        'len',
        'range',
        'zip',
        'hex',
        'enumerate',
        'sorted',
    )})
    env.filters.update({
        'prefix': _prefix,
        'suffix': _suffix,
        'wrap': _wrap,
        'macro': _macro,
        'hex32': _hex32,
    })


ctemplate = Environment(
    loader=PackageLoader('xpdt', 'templates'),
    line_statement_prefix='//',
    variable_start_string='/*{',
    variable_end_string='}*/',
    block_start_string='/*#',
    block_end_string='#*/',
    keep_trailing_newline=False,
    trim_blocks=True,
    lstrip_blocks=True,
    auto_reload=False,
    autoescape=False,
)
_setup(ctemplate)


pytemplate = Environment(
    loader=PackageLoader('xpdt', 'templates'),
    block_start_string='#%',
    block_end_string='%#',
    line_statement_prefix='##',
    variable_start_string='$$',
    variable_end_string='$$',
    keep_trailing_newline=False,
    trim_blocks=True,
    lstrip_blocks=True,
    auto_reload=False,
    autoescape=False,
)
_setup(pytemplate)
