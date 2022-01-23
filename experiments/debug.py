import inspect


class _DebugBlock:
    def __enter__(self):
        outer_frame = inspect.getouterframes(inspect.currentframe())[1].frame
        self.start_locals = outer_frame.f_locals.copy()

    def __exit__(self, exn_typ, exn_val, traceback):
        outer_frame = inspect.getouterframes(inspect.currentframe())[1].frame
        end_locals = outer_frame.f_locals.copy()
        print(self.start_locals)
        print(end_locals)
        print('---- Debug Block ----')
        for name in end_locals:
            val = end_locals[name]
            if name not in self.start_locals or val != self.start_locals[name]:
                print(f'{name} = {val}')
        print('---------------------')


DebugBlock = _DebugBlock()
