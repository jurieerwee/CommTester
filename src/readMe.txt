
test_state_6
Tests the PRIME state sequence, termimating with IDLE Cmd.
**Set pressure**
**Simualte reverse flow**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence

Dependent on test3 and test4 passing
******************************************
test_state_8
Tests the PUMPING state enters .
**Set pressure**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence

Dependent on test3 passing

******************************************
test_state_17
Tests the PRIME state sequence, attempting termimating with IDLE Cmd, while tank Empty
**Set pressure**
**Simualte reverse flow**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence

Dependent on test3 and test4 passing

************************************************
test_io_pressurised
Tests the pressured flag.
**Set pressure**
Assumed threashhold pressure is 1.5
Test that the pressurised flags gets set and unset.

**********************************************
test_state_18

Tests filling state enters.
**Set pressure**
**Simualte reverse flow**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence
************************
test_state_19
Tests filling state stops with full tank.
**Set pressure**
**Simualte reverse flow**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence

Requires test_state_18
*****************************
test_state_20
Tests filling state stops with IDLECMD.
**Set pressure**
**Simualte reverse flow**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence

Requires test_state_18
*******************************
test_state_21
Tests filling state ERROR on forward flow
**Set pressure**
**Simualte forward flow**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence

Requires test_state_18
*********************************
test_state_23
Tests OVERRIDE state enters from IDLE

Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence
******************************
test_state_24
Tests OVERRIDE state enters from IDLE_PRES

Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence
**********************************
test_state_25
Tests force_fill state enters from IDLE_PRES
**Set pressure**
**Simualte reverse flow**
Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence
**********************************
test_state_26
Tests force_fill state enters from IDLE
**Set pressure**

Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence
**********************************
test_state_27
Tests force_fill state exits on idleCMD
**Set pressure**

Assumed threashhold pressure is 1.5
Test that update returns 
*correct state sequence

Requires 26 to pass