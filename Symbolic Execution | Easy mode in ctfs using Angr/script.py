import angr

P = angr.Project('./a.out')

state = P.factory.entry_state()

manager = P.factory.simgr(state)

manager.explore(find = 0x401246, avoid = 0x401229)
