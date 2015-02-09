#include <stdlib.h>
#include "pin.H"

ADDRINT	shadow_stack[4096];
int		shadow_sp = -1;

VOID push_retaddr(ADDRINT esp, ADDRINT eip)
{
	if(shadow_sp >= (int)sizeof(shadow_stack) - 1){
		// cannot push retaddr to shadow stack
		exit(-1);
	}
	PIN_SafeCopy(&shadow_stack[++shadow_sp], (VOID*)esp, sizeof(ADDRINT));
}

VOID pop_retaddr(ADDRINT esp, ADDRINT eip)
{
	ADDRINT		retaddr;

	PIN_SafeCopy(&retaddr, (VOID*)esp, sizeof(ADDRINT));

	while(shadow_sp >= 0 && shadow_stack[shadow_sp--] != retaddr);
	if(shadow_sp < 0){
		exit(-1);
	}
}

VOID check_syscall(ADDRINT eax)
{
	switch(eax){
	// syscalls for exploit
	case 3:		// sys_read
	case 4:		// sys_write
	case 5:		// sys_open
	case 6:		// sys_close

	// syscalls executed until entry point
	case 45:	// sys_brk
	case 122:	// sys_newuname
	case 192:	// sys_mmap2
	case 197:	// sys_fstatfs64
	case 243:	// sys_set_thread_area
		break;

	// invalid syscalls
	default:
		exit(-1);
	}
}

VOID insert_hooks(INS ins, VOID *val)
{
	if(INS_IsCall(ins)){
		// push retaddr to shadow stack
		if(XED_ICLASS_CALL_FAR == INS_Opcode(ins)){
			exit(-1);
		}
		INS_InsertCall(ins, IPOINT_TAKEN_BRANCH,(AFUNPTR)push_retaddr,
			IARG_REG_VALUE, REG_ESP, IARG_INST_PTR, IARG_END);
	}else if(INS_IsRet(ins)){
		// pop retaddr from shadow stack, and then check it
		if(XED_ICLASS_RET_FAR == INS_Opcode(ins)){
			exit(-1);
		}else{
			INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)pop_retaddr,
				IARG_REG_VALUE, REG_ESP, IARG_INST_PTR, IARG_END);
		}
	}else if(INS_IsSyscall(ins)){
		// check syscall
		INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)check_syscall,
			IARG_REG_VALUE, REG_EAX, IARG_END);
	}
}

int main(int argc, char *argv[])
{
	PIN_Init(argc, argv);
	INS_AddInstrumentFunction(insert_hooks, NULL);
    PIN_StartProgram();
    
    return 0;
}
