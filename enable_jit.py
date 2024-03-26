# nythepegasus 2024
# enable_jit.py for lldb
# Usage: enable_jit <gdb-remote_address> <process_id>

import lldb
import sys

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f enable_jit.enable_jit enable_jit')

def enable_jit(debugger, command, result, internal_dict):
    args = command.split()
    if len(args) != 2:
        print("Usage: enable_jit <gdb-remote_address> <process_id>")
        return

    gdb_remote_address = args[0]
    process_id = args[1]

    res = lldb.SBCommandReturnObject()
    ci = debugger.GetCommandInterpreter()
    ci.HandleCommand(f'platform select remote-ios', res)

    old_debug = debugger.GetAsync()
    debugger.SetAsync(True)
    print(f"Connecting to {gdb_remote_address}..")
    ci.HandleCommand(f'gdb-remote {gdb_remote_address}', res)

    ci.HandleCommand('settings set target.memory-module-load-level minimal', res)

    print(f"Attaching to process {process_id}..")
    ci.HandleCommand(f'attach -p {process_id}', res)
    ci.HandleCommand("process continue", res)
    debugger.SetAsync(old_debug)
    ci.HandleCommand("process detach", res)
    print("\nProcess continued and detached!")

    print(f"JIT enabled for process {process_id} at {gdb_remote_address}!")

