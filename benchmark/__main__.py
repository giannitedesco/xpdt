from timeit import default_timer as timer
from pathlib import Path

from xpdt import NameSpace, StructDef, MemberDef, BaseType


def main():
    cls = NameSpace(
        structs=(
            StructDef(
                name='SomeStruct',
                members=(
                    MemberDef('a', BaseType.u64),
                    MemberDef('b', BaseType.u64),
                    MemberDef('c', BaseType.u64),
                    MemberDef('d', BaseType.u64),
                    MemberDef('e', BaseType.u64),
                    MemberDef('f', BaseType.u64),
                    MemberDef('g', BaseType.u64),
                    MemberDef('h', BaseType.u64),
                    MemberDef('i', BaseType.u64),
                    MemberDef('j', BaseType.u64),
                    MemberDef('k', BaseType.u64),
                    MemberDef('l', BaseType.u64),
                    MemberDef('m', BaseType.u64),
                    MemberDef('n', BaseType.u64),
                    MemberDef('o', BaseType.u64),
                    MemberDef('p', BaseType.u64),
                ),
            ),
        ),
    ).gen_dynamic_python().SomeStruct

    sz = cls._bin_size

    with Path('/dev/zero').open('rb') as f:
        iters = 1000000
        start = timer()
        for i in range(iters):
            buf = f.read(sz)
            obj = cls._frombytes(buf)
        end = timer()
        elapsed = end - start
        per_iter = elapsed / iters
        print(f'{elapsed:.2f} sec elapsed')
        print(f'{per_iter*1e9:.0f} nsec per record')


if __name__ == '__main__':
    main()
