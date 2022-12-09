(module
  (type (;0;) (func))
  (type (;1;) (func (result i32)))
  (type (;2;) (func (param i32 i32)))
  (import "env" "getNumArguments" (func (;0;) (type 1)))
  (import "env" "signalError" (func (;1;) (type 2)))
  (import "env" "checkNoPayment" (func (;2;) (type 0)))
  (func (;3;) (type 0)
    call 2
    call 0
    if  ;; label = @1
      i32.const 1048576
      i32.const 25
      call 1
      unreachable
    end)
  (func (;4;) (type 0)
    nop)
  (memory (;0;) 17)
  (global (;0;) i32 (i32.const 1048601))
  (global (;1;) i32 (i32.const 1048608))
  (export "memory" (memory 0))
  (export "init" (func 3))
  (export "callBack" (func 4))
  (export "__data_end" (global 0))
  (export "__heap_base" (global 1))
  (data (;0;) (i32.const 1048576) "wrong number of arguments"))
