import angr

binNames = ["entropy", "matrix"]

for name in binNames:
  P = angr.Project(name)
  entry = P.factory.entry_state()
  manager = P.factory.simgr()

  manager.run()

  if manager.deadended:
    for state in manager.deadended:
      tmp = state.posix.dumps(0)
      if b"glug{" in tmp.lower():
        print(f"Solution found for {name}: {tmp}")
