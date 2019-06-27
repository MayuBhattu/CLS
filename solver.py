import numpy as np
import frames as fs
from constants_1U import v_w_IO_o

def updateStateTimeRK4(sat,f,h): #This is Runge Kutta-4 solver for ordinary differential equation.
	'''
		Input:
				satellite object
				f: The function returning the derivative of the state given satellite object as its input 
				integration step size
		It sets the value of state at next time (after a time step of h) (x(t+h)) using f and 
		value of state at current time (x(t)) and also updates the value of time.
	'''
	v_state_error_0 = np.hstack((sat.getQ_BI(),sat.getW_BI_b()))	#state at t = t0	
	t = sat.getTime() 

	#checking whether the f is a proper function or not
	if (np.shape(f(sat)) != (7,)):
		print ("Error: derivative of state is not proper")
		return
	#rk-4 routine (updating satellite class state with obtained state at every step of rk4 routine)
	sat.setState( v_state_error_0)
	#first step of rk4 routine
	k1 = h*f(sat)

	#seccdond step of rk4 routine
	v_state_error_1 = v_state_error_0+0.5*k1
	sat.setTime(t+0.5*h)
	sat.setState(v_state_error_1)

	k2 = h*f(sat)
	#third step of rk4 routine	
	v_state_error_2 = v_state_error_0+0.5*k2
	sat.setTime(t+0.5*h)
	sat.setState(v_state_error_2)

	k3 = h*f(sat)
	v_state_error_3 = v_state_error_0+k3
	sat.setTime(t+h)
	sat.setState(v_state_error_3)

	#forth step of rk4 routine
	k4 = h*f(sat)
	v_state_error_new = v_state_error_0 + (1./6.)*(k1 + 2.*k2 + 2.*k3 + k4)

	#Normalize to obtain unit quaternion (different from regular rk4 solver)	
	v_state_error_new[0:4] = v_state_error_new[0:4].copy()/np.linalg.norm(v_state_error_new[0:4].copy()) #error state at t0+h
	
	if v_state_error_new[3] < 0. :
		v_state_error_new[0:4] = -v_state_error_new[0:4].copy()
	
	v_pos_i = sat.getPos()
	v_vel_i = sat.getVel()
	v_q_BO = fs.qBI2qBO(v_state_error_new[0:4],v_pos_i,v_vel_i)
	v_w_BI_b = v_state_error_new[4:7]
	
	wBOb = fs.wBIb2wBOb(v_w_BI_b,v_q_BO,v_w_IO_o)
	v_state_error_new = np.hstack ((v_q_BO, wBOb))
	sat.setState(v_state_error_new.copy())
	#print("statek+1" ,v_state_error_new)
	#print('\n')
	return 
